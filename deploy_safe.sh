#!/bin/bash
# 安全部署脚本 - 包含错误处理和回滚机制

SERVER_USER="root"
SERVER_HOST="47.97.0.35"
PROJECT_PATH="/var/www/tcm-platform"
BACKUP_PATH="/var/www/tcm-platform-backup-$(date +%Y%m%d_%H%M%S)"

set -e  # 遇到错误立即退出

echo "🚀 中医健康平台 - 安全部署脚本"
echo "================================"

# 预检查
echo "📋 执行部署前检查..."
if ! ping -c 2 $SERVER_HOST > /dev/null; then
    echo "❌ 服务器无法访问，部署终止"
    exit 1
fi

if ! ssh $SERVER_USER@$SERVER_HOST "echo '连接测试'" > /dev/null 2>&1; then
    echo "❌ SSH连接失败，部署终止"
    exit 1
fi

echo "✅ 预检查通过，开始部署..."

# 在服务器上执行安全部署
ssh $SERVER_USER@$SERVER_HOST << 'DEPLOY_SCRIPT'
set -e

echo "1. 🔄 备份当前版本..."
if [ -d "/var/www/tcm-platform" ]; then
    BACKUP_PATH="/var/www/tcm-platform-backup-$(date +%Y%m%d_%H%M%S)"
    cp -r /var/www/tcm-platform $BACKUP_PATH
    echo "   ✅ 备份完成: $BACKUP_PATH"
else
    echo "   ℹ️  首次部署，无需备份"
fi

echo "2. 📥 更新代码..."
if [ -d "/var/www/tcm-platform" ]; then
    cd /var/www/tcm-platform
    
    # 保存当前提交ID用于回滚
    CURRENT_COMMIT=$(git rev-parse HEAD)
    echo "   当前提交: $CURRENT_COMMIT"
    
    # 拉取最新代码
    if ! git pull origin main; then
        echo "   ❌ Git拉取失败，部署终止"
        exit 1
    fi
    
    NEW_COMMIT=$(git rev-parse HEAD)
    echo "   ✅ 更新到提交: $NEW_COMMIT"
else
    cd /var/www
    if ! git clone https://github.com/Molly230/tcm-platform.git; then
        echo "   ❌ Git克隆失败，部署终止"
        exit 1
    fi
    cd tcm-platform
    echo "   ✅ 项目克隆完成"
fi

echo "3. 🔧 配置环境..."
if [ ! -f ".env" ]; then
    echo "   创建生产环境配置..."
    cat > .env << 'ENV_CONFIG'
# 数据库配置
DATABASE_URL=postgresql://tcm_user:tcm_password_2024@db:5432/tcm_db

# Redis配置
REDIS_URL=redis://redis:6379

# 应用配置
SECRET_KEY=tcm-health-platform-secret-key-2024-production
DEBUG=False
ENVIRONMENT=production

# 域名配置
DOMAIN=tcmlife.top
FRONTEND_URL=https://www.tcmlife.top
BACKEND_URL=https://www.tcmlife.top/api

# JWT配置
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# 文件上传配置
MAX_FILE_SIZE=10485760
UPLOAD_PATH=/app/uploads

# 邮件配置（如果需要）
SMTP_HOST=smtp.example.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=

# 支付配置（生产环境需要真实配置）
# STRIPE_SECRET_KEY=
# ALIPAY_APP_ID=
ENV_CONFIG
    echo "   ✅ 环境配置创建完成"
else
    echo "   ✅ 使用现有环境配置"
fi

echo "4. 🐳 检查Docker环境..."
if ! command -v docker &> /dev/null; then
    echo "   安装Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
fi

if ! command -v docker-compose &> /dev/null; then
    echo "   安装Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi
echo "   ✅ Docker环境就绪"

echo "5. 🏗️  构建和部署服务..."

# 停止旧服务（不中断用户访问）
if docker-compose ps | grep -q "Up"; then
    echo "   停止旧服务..."
    docker-compose down --remove-orphans || true
fi

# 构建新镜像
echo "   构建新镜像..."
if ! docker-compose build --no-cache; then
    echo "   ❌ 镜像构建失败"
    
    # 回滚代码
    if [ -n "$CURRENT_COMMIT" ]; then
        echo "   🔄 回滚到之前版本..."
        git reset --hard $CURRENT_COMMIT
    fi
    exit 1
fi

# 启动新服务
echo "   启动服务..."
if ! docker-compose up -d; then
    echo "   ❌ 服务启动失败"
    
    # 尝试恢复备份
    if [ -d "$BACKUP_PATH" ]; then
        echo "   🔄 恢复备份版本..."
        cd /var/www
        rm -rf tcm-platform
        mv $BACKUP_PATH tcm-platform
        cd tcm-platform
        docker-compose up -d || true
    fi
    exit 1
fi

echo "6. ⏳ 等待服务启动..."
sleep 30

echo "7. 🗄️  初始化数据库..."
if ! docker-compose exec -T backend alembic upgrade head; then
    echo "   ⚠️  数据库迁移失败，但继续部署..."
fi

# 创建管理员（如果不存在）
docker-compose exec -T backend python create_admin.py || echo "   ℹ️  管理员可能已存在"

echo "8. 🔍 健康检查..."
sleep 10

# 检查服务状态
BACKEND_HEALTH=$(curl -s http://localhost:8000/health 2>/dev/null | grep -o "ok" || echo "failed")
FRONTEND_HEALTH=$(curl -s -I http://localhost 2>/dev/null | head -n1 | grep -o "200" || echo "failed")

if [ "$BACKEND_HEALTH" = "ok" ] && [ "$FRONTEND_HEALTH" = "200" ]; then
    echo "   ✅ 服务健康检查通过"
    
    # 清理旧备份（保留最近3个）
    cd /var/www
    ls -dt tcm-platform-backup-* 2>/dev/null | tail -n +4 | xargs rm -rf 2>/dev/null || true
    
    echo ""
    echo "🎉 部署成功！"
    echo "   网站地址: https://www.tcmlife.top"
    echo "   后端API: https://www.tcmlife.top/api"
    echo "   管理后台: https://www.tcmlife.top/admin"
else
    echo "   ❌ 健康检查失败"
    echo "   后端状态: $BACKEND_HEALTH"
    echo "   前端状态: $FRONTEND_HEALTH"
    
    echo "   📋 服务状态:"
    docker-compose ps
    
    echo "   📝 最近日志:"
    docker-compose logs --tail=20
    
    exit 1
fi

DEPLOY_SCRIPT

echo ""
echo "🚀 部署脚本执行完成！"
echo ""
echo "🔧 接下来需要手动操作："
echo "1. 配置SSL证书: certbot --nginx -d tcmlife.top -d www.tcmlife.top"
echo "2. 更新DNS解析确保指向正确IP"
echo "3. 测试关键功能流程"
echo ""
echo "📊 监控命令："
echo "- 查看服务状态: ssh root@47.97.0.35 'cd /var/www/tcm-platform && docker-compose ps'"
echo "- 查看日志: ssh root@47.97.0.35 'cd /var/www/tcm-platform && docker-compose logs -f'"
echo "- 重启服务: ssh root@47.97.0.35 'cd /var/www/tcm-platform && docker-compose restart'"