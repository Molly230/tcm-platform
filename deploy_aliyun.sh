#!/bin/bash
# 阿里云服务器一键部署脚本

set -e  # 遇到错误立即退出

echo "🚀 开始部署中医健康平台..."

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 配置变量
PROJECT_DIR="/var/www/tcm-platform"
BACKEND_PORT=8001
DOMAIN="tcmlife.top"  # 修改为你的域名

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo -e "${RED}请使用root用户运行此脚本${NC}"
    echo "使用: sudo bash deploy_aliyun.sh"
    exit 1
fi

# 1. 安装必要软件
echo -e "${GREEN}[1/8] 安装必要软件...${NC}"
if [ -f /etc/debian_version ]; then
    # Ubuntu/Debian
    apt update
    apt install -y git nginx python3.9 python3-pip python3-venv nodejs npm
elif [ -f /etc/redhat-release ]; then
    # CentOS/RHEL
    yum update -y
    yum install -y git nginx python39 python39-pip nodejs npm
fi

# 安装PM2
npm install -g pm2

# 2. 克隆或更新代码
echo -e "${GREEN}[2/8] 获取代码...${NC}"
if [ -d "$PROJECT_DIR" ]; then
    echo "项目目录已存在，拉取最新代码..."
    cd $PROJECT_DIR
    git pull origin main
else
    echo "克隆项目..."
    mkdir -p /var/www
    cd /var/www
    git clone https://github.com/Molly230/tcm-platform.git
    cd tcm-platform
fi

# 3. 配置后端
echo -e "${GREEN}[3/8] 配置后端...${NC}"
cd $PROJECT_DIR/backend

# 创建虚拟环境
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 激活虚拟环境并安装依赖
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

# 配置环境变量
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}创建.env配置文件...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}⚠️  请稍后手动编辑 $PROJECT_DIR/backend/.env 文件配置生产环境密钥${NC}"
fi

# 初始化数据库
echo "初始化数据库..."
alembic upgrade head || echo "数据库迁移可能已完成"

# 4. 构建前端
echo -e "${GREEN}[4/8] 构建前端...${NC}"
cd $PROJECT_DIR/frontend
npm install
npm run build

# 5. 配置Nginx
echo -e "${GREEN}[5/8] 配置Nginx...${NC}"
cat > /etc/nginx/conf.d/tcmlife.conf <<EOF
# 后端API负载均衡
upstream backend_api {
    server 127.0.0.1:$BACKEND_PORT;
    keepalive 32;
}

server {
    listen 80;
    server_name $DOMAIN www.$DOMAIN;

    # 客户端上传限制
    client_max_body_size 100M;

    # 前端静态文件
    location / {
        root $PROJECT_DIR/frontend/dist;
        try_files \$uri \$uri/ /index.html;

        # 静态资源缓存
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # API代理
    location /api/ {
        proxy_pass http://backend_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_cache_bypass \$http_upgrade;

        # 超时设置
        proxy_connect_timeout 30s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 文档接口
    location /docs {
        proxy_pass http://backend_api;
        proxy_set_header Host \$host;
    }

    location /redoc {
        proxy_pass http://backend_api;
        proxy_set_header Host \$host;
    }

    location /openapi.json {
        proxy_pass http://backend_api;
        proxy_set_header Host \$host;
    }

    # 上传文件
    location /uploads/ {
        proxy_pass http://backend_api;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;

        # 缓存设置
        expires 1y;
        add_header Cache-Control "public";
    }

    # WebSocket支持
    location /ws/ {
        proxy_pass http://backend_api;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    # 健康检查
    location /health {
        proxy_pass http://backend_api;
        access_log off;
    }
}
EOF

# 测试Nginx配置
nginx -t

# 6. 配置后端服务
echo -e "${GREEN}[6/8] 配置后端服务...${NC}"

# 停止旧的PM2进程（如果存在）
pm2 delete tcm-backend 2>/dev/null || true

# 启动后端
cd $PROJECT_DIR/backend
pm2 start "venv/bin/uvicorn app.main:app --host 0.0.0.0 --port $BACKEND_PORT" \
    --name tcm-backend \
    --log $PROJECT_DIR/logs/backend.log \
    --error $PROJECT_DIR/logs/backend-error.log

# 保存PM2配置
pm2 save

# 设置PM2开机自启
pm2 startup systemd -u root --hp /root

# 7. 重启Nginx
echo -e "${GREEN}[7/8] 重启Nginx...${NC}"
systemctl restart nginx
systemctl enable nginx

# 8. 验证部署
echo -e "${GREEN}[8/8] 验证部署...${NC}"
sleep 3

# 检查后端服务
if curl -s http://localhost:$BACKEND_PORT/health > /dev/null; then
    echo -e "${GREEN}✅ 后端服务运行正常${NC}"
else
    echo -e "${RED}❌ 后端服务异常，请检查日志${NC}"
    echo "查看日志: pm2 logs tcm-backend"
fi

# 检查Nginx
if systemctl is-active --quiet nginx; then
    echo -e "${GREEN}✅ Nginx运行正常${NC}"
else
    echo -e "${RED}❌ Nginx异常${NC}"
fi

# 显示服务状态
echo ""
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}🎉 部署完成！${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "📊 服务状态:"
pm2 status
echo ""
echo "🌐 访问地址:"
echo "   前端: http://$DOMAIN"
echo "   API文档: http://$DOMAIN/docs"
echo ""
echo "📝 常用命令:"
echo "   查看后端日志: pm2 logs tcm-backend"
echo "   重启后端: pm2 restart tcm-backend"
echo "   查看Nginx状态: systemctl status nginx"
echo "   重启Nginx: systemctl restart nginx"
echo ""
echo -e "${YELLOW}⚠️  重要提醒:${NC}"
echo "   1. 请编辑 $PROJECT_DIR/backend/.env 配置生产环境密钥"
echo "   2. 建议配置SSL证书: certbot --nginx -d $DOMAIN -d www.$DOMAIN"
echo "   3. 检查阿里云安全组是否开放了80和443端口"
echo ""
