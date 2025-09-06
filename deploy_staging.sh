#!/bin/bash
# 预发布环境部署脚本

set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}部署到预发布环境${NC}"
echo -e "${BLUE}========================================${NC}"

# 预发布环境配置
STAGING_DIR="/var/www/tcm-platform-staging"
STAGING_PORT="8001"
STAGING_FRONTEND_PORT="3001"

deploy_staging() {
    echo -e "${YELLOW}准备预发布环境...${NC}"
    
    # 创建预发布目录
    mkdir -p "$STAGING_DIR"
    
    # 复制代码
    rsync -av --exclude='.git' --exclude='node_modules' --exclude='__pycache__' . "$STAGING_DIR/"
    
    cd "$STAGING_DIR"
    
    # 创建预发布环境配置
    cat > .env << EOF
# 预发布环境配置
DEBUG=True
SECRET_KEY=staging-secret-key-for-testing-only
DATABASE_URL=sqlite:///./tcm_staging.db
CORS_ORIGINS=http://localhost:3001,http://staging.your-domain.com
SERVER_HOST=http://localhost:8001

# 使用测试环境的第三方服务配置
TENCENT_SECRET_ID=test_secret_id
TENCENT_SECRET_KEY=test_secret_key
ALIPAY_APP_ID=test_app_id
EOF
    
    echo -e "${YELLOW}启动预发布服务...${NC}"
    
    # 启动后端（不同端口）
    cd backend
    pip install -r requirements.txt
    nohup uvicorn app.main:app --host 0.0.0.0 --port $STAGING_PORT > ../logs/staging-backend.log 2>&1 &
    echo $! > ../staging-backend.pid
    
    # 启动前端（不同端口）
    cd ../frontend
    npm install
    npm run build
    nohup npm run preview -- --port $STAGING_FRONTEND_PORT > ../logs/staging-frontend.log 2>&1 &
    echo $! > ../staging-frontend.pid
    
    echo -e "${GREEN}预发布环境启动完成${NC}"
    echo "前端访问: http://localhost:$STAGING_FRONTEND_PORT"
    echo "后端API: http://localhost:$STAGING_PORT"
    echo "API文档: http://localhost:$STAGING_PORT/docs"
}

stop_staging() {
    echo -e "${YELLOW}停止预发布环境...${NC}"
    
    if [[ -f "$STAGING_DIR/staging-backend.pid" ]]; then
        kill $(cat "$STAGING_DIR/staging-backend.pid") || true
        rm "$STAGING_DIR/staging-backend.pid"
    fi
    
    if [[ -f "$STAGING_DIR/staging-frontend.pid" ]]; then
        kill $(cat "$STAGING_DIR/staging-frontend.pid") || true
        rm "$STAGING_DIR/staging-frontend.pid"
    fi
    
    echo -e "${GREEN}预发布环境已停止${NC}"
}

case "${1:-deploy}" in
    "deploy")
        deploy_staging
        ;;
    "stop")
        stop_staging
        ;;
    "restart")
        stop_staging
        sleep 2
        deploy_staging
        ;;
    "logs")
        tail -f "$STAGING_DIR/logs/staging-backend.log" "$STAGING_DIR/logs/staging-frontend.log"
        ;;
    *)
        echo "用法: $0 [deploy|stop|restart|logs]"
        exit 1
        ;;
esac