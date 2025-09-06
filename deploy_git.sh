#!/bin/bash
# Git自动部署脚本

# 服务器配置
SERVER_USER="root"
SERVER_HOST="your-server-ip"
PROJECT_PATH="/var/www/tcm-platform"
REPO_URL="https://github.com/yourusername/tcm-platform.git"

echo "中医健康平台 - Git自动部署"

# 在服务器上执行部署
ssh ${SERVER_USER}@${SERVER_HOST} << 'ENDSSH'

echo "1. 检查Docker环境..."
if ! command -v docker &> /dev/null; then
    echo "安装Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
fi

if ! command -v docker-compose &> /dev/null; then
    echo "安装Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

echo "2. 拉取最新代码..."
if [ -d "/var/www/tcm-platform" ]; then
    cd /var/www/tcm-platform
    git pull origin main
else
    cd /var/www
    git clone https://github.com/yourusername/tcm-platform.git
    cd tcm-platform
fi

echo "3. 检查环境变量..."
if [ ! -f ".env" ]; then
    echo "复制环境变量模板..."
    cp .env.example .env
    echo "警告: 请编辑 .env 文件配置生产参数！"
fi

echo "4. 启动服务..."
docker-compose down || true
docker-compose up -d --build

echo "5. 等待服务启动..."
sleep 30

echo "6. 初始化数据..."
docker-compose exec -T backend alembic upgrade head
docker-compose exec -T backend python create_admin.py || true

echo "Git自动部署完成!"
echo "访问地址: http://your-server-ip"
echo "请配置域名和SSL证书"

ENDSSH

echo "部署完成！记得："
echo "1. 替换脚本中的服务器IP和仓库地址"
echo "2. 在服务器上配置.env文件"
echo "3. 配置域名DNS解析"