#!/bin/bash
# 生产环境零停机更新脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# 配置
PROJECT_DIR="/var/www/tcm-platform"
BACKUP_DIR="/backups/deployments"
SERVICE_NAME="tcm-platform"
NGINX_CONFIG="/etc/nginx/sites-available/tcm-platform"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}中医健康服务平台 - 生产环境更新${NC}"
echo -e "${BLUE}========================================${NC}"

# 检查权限
check_permissions() {
    if [[ $EUID -ne 0 ]]; then
        echo -e "${RED}错误: 请使用sudo执行此脚本${NC}"
        exit 1
    fi
}

# 创建备份
create_backup() {
    echo -e "${YELLOW}创建系统备份...${NC}"
    
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    BACKUP_PATH="$BACKUP_DIR/backup_$TIMESTAMP"
    
    mkdir -p "$BACKUP_PATH"
    
    # 备份代码
    echo "备份应用代码..."
    cp -r "$PROJECT_DIR" "$BACKUP_PATH/code"
    
    # 备份数据库
    echo "备份数据库..."
    if [[ "$DATABASE_URL" == postgresql* ]]; then
        pg_dump "$DATABASE_URL" > "$BACKUP_PATH/database.sql"
    elif [[ "$DATABASE_URL" == mysql* ]]; then
        mysqldump --single-transaction --routines --triggers "$DATABASE_URL" > "$BACKUP_PATH/database.sql"
    fi
    
    # 备份uploads目录
    echo "备份上传文件..."
    cp -r "$PROJECT_DIR/uploads" "$BACKUP_PATH/uploads" || true
    
    # 记录当前版本信息
    cd "$PROJECT_DIR"
    git rev-parse HEAD > "$BACKUP_PATH/git_commit.txt"
    docker-compose ps > "$BACKUP_PATH/services_status.txt"
    
    echo -e "${GREEN}✓ 备份完成: $BACKUP_PATH${NC}"
    echo "$BACKUP_PATH" > /tmp/last_backup_path
}

# 拉取最新代码
update_code() {
    echo -e "${YELLOW}更新应用代码...${NC}"
    
    cd "$PROJECT_DIR"
    
    # 确保在正确的分支上
    git checkout main
    
    # 获取最新代码
    git pull origin main
    
    # 显示更新信息
    echo -e "${GREEN}✓ 代码更新完成${NC}"
    git log --oneline -5
}

# 检查数据库迁移
check_database_migration() {
    echo -e "${YELLOW}检查数据库迁移...${NC}"
    
    cd "$PROJECT_DIR/backend"
    
    # 检查是否有新的迁移文件
    NEW_MIGRATIONS=$(alembic heads | wc -l)
    CURRENT_MIGRATION=$(alembic current | wc -l)
    
    if [[ $NEW_MIGRATIONS -gt $CURRENT_MIGRATION ]]; then
        echo -e "${YELLOW}发现新的数据库迁移${NC}"
        
        # 询问是否继续
        read -p "是否执行数据库迁移? (y/n): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo -e "${RED}取消部署${NC}"
            exit 1
        fi
        
        # 执行迁移
        echo "执行数据库迁移..."
        alembic upgrade head
        echo -e "${GREEN}✓ 数据库迁移完成${NC}"
    else
        echo -e "${GREEN}✓ 无需数据库迁移${NC}"
    fi
}

# 构建前端
build_frontend() {
    echo -e "${YELLOW}构建前端...${NC}"
    
    cd "$PROJECT_DIR/frontend"
    
    # 安装依赖
    npm ci --production
    
    # 构建生产版本
    npm run build
    
    echo -e "${GREEN}✓ 前端构建完成${NC}"
}

# 重启后端服务
restart_backend() {
    echo -e "${YELLOW}重启后端服务...${NC}"
    
    cd "$PROJECT_DIR"
    
    # 使用滚动更新策略
    if docker-compose ps | grep -q "backend"; then
        # Docker部署
        echo "使用Docker滚动更新..."
        docker-compose build backend
        docker-compose up -d --no-deps backend
        
        # 等待服务启动
        sleep 10
        
        # 健康检查
        for i in {1..30}; do
            if curl -f -s http://localhost:8000/health > /dev/null; then
                echo -e "${GREEN}✓ 后端服务启动成功${NC}"
                break
            fi
            echo "等待后端服务启动... ($i/30)"
            sleep 2
        done
        
        if [[ $i -eq 30 ]]; then
            echo -e "${RED}✗ 后端服务启动失败${NC}"
            rollback
            exit 1
        fi
    else
        # 传统部署
        echo "重启传统部署服务..."
        systemctl restart "$SERVICE_NAME"
        systemctl status "$SERVICE_NAME"
    fi
}

# 更新前端文件
update_frontend() {
    echo -e "${YELLOW}更新前端文件...${NC}"
    
    # 备份当前前端文件
    if [[ -d /var/www/html ]]; then
        cp -r /var/www/html /var/www/html.backup.$(date +%Y%m%d_%H%M%S)
    fi
    
    # 复制新的前端文件
    cp -r "$PROJECT_DIR/frontend/dist/"* /var/www/html/
    
    # 重新加载Nginx配置
    nginx -t && nginx -s reload
    
    echo -e "${GREEN}✓ 前端更新完成${NC}"
}

# 健康检查
health_check() {
    echo -e "${YELLOW}执行健康检查...${NC}"
    
    # 检查后端API
    if curl -f -s http://localhost:8000/health/detailed | grep -q '"status": "healthy"'; then
        echo -e "${GREEN}✓ 后端API健康${NC}"
    else
        echo -e "${RED}✗ 后端API异常${NC}"
        return 1
    fi
    
    # 检查前端
    if curl -f -s http://localhost > /dev/null; then
        echo -e "${GREEN}✓ 前端服务健康${NC}"
    else
        echo -e "${RED}✗ 前端服务异常${NC}"
        return 1
    fi
    
    # 检查数据库连接
    cd "$PROJECT_DIR/backend"
    if python -c "from app.database import engine; engine.connect()"; then
        echo -e "${GREEN}✓ 数据库连接正常${NC}"
    else
        echo -e "${RED}✗ 数据库连接异常${NC}"
        return 1
    fi
    
    return 0
}

# 回滚功能
rollback() {
    echo -e "${RED}执行回滚操作...${NC}"
    
    if [[ -f /tmp/last_backup_path ]]; then
        BACKUP_PATH=$(cat /tmp/last_backup_path)
        
        if [[ -d "$BACKUP_PATH" ]]; then
            echo "回滚到备份: $BACKUP_PATH"
            
            # 回滚代码
            rm -rf "$PROJECT_DIR"
            cp -r "$BACKUP_PATH/code" "$PROJECT_DIR"
            
            # 回滚数据库
            read -p "是否回滚数据库? (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                if [[ -f "$BACKUP_PATH/database.sql" ]]; then
                    echo "回滚数据库..."
                    # 这里需要根据数据库类型执行回滚
                    echo "请手动执行数据库回滚: $BACKUP_PATH/database.sql"
                fi
            fi
            
            # 回滚上传文件
            if [[ -d "$BACKUP_PATH/uploads" ]]; then
                rm -rf "$PROJECT_DIR/uploads"
                cp -r "$BACKUP_PATH/uploads" "$PROJECT_DIR/uploads"
            fi
            
            # 重启服务
            cd "$PROJECT_DIR"
            docker-compose down && docker-compose up -d
            
            echo -e "${GREEN}回滚完成${NC}"
        else
            echo -e "${RED}备份目录不存在: $BACKUP_PATH${NC}"
        fi
    else
        echo -e "${RED}未找到备份信息${NC}"
    fi
}

# 发送通知
send_notification() {
    local status=$1
    local message=$2
    
    # 可以集成邮件、短信、钉钉等通知方式
    echo "$(date): $status - $message" >> /var/log/deployment.log
    
    # 示例：发送邮件通知
    # echo "$message" | mail -s "TCM Platform Deployment $status" admin@your-domain.com
}

# 主更新流程
main_update() {
    echo -e "${BLUE}开始更新部署...${NC}"
    
    # 创建备份
    create_backup
    
    # 更新代码
    update_code
    
    # 检查数据库迁移
    check_database_migration
    
    # 构建前端
    build_frontend
    
    # 重启后端服务
    restart_backend
    
    # 更新前端文件
    update_frontend
    
    # 健康检查
    if health_check; then
        echo -e "${GREEN}========================================${NC}"
        echo -e "${GREEN}更新部署成功！${NC}"
        echo -e "${GREEN}========================================${NC}"
        send_notification "SUCCESS" "Production deployment completed successfully"
    else
        echo -e "${RED}健康检查失败，开始回滚...${NC}"
        rollback
        send_notification "FAILED" "Production deployment failed, rollback initiated"
        exit 1
    fi
}

# 命令行参数处理
case "${1:-update}" in
    "update")
        check_permissions
        main_update
        ;;
    "rollback")
        check_permissions
        rollback
        ;;
    "health")
        health_check
        ;;
    "backup")
        check_permissions
        create_backup
        ;;
    *)
        echo "用法: $0 [update|rollback|health|backup]"
        echo ""
        echo "update   - 执行完整更新部署（默认）"
        echo "rollback - 回滚到上一个版本"
        echo "health   - 健康检查"
        echo "backup   - 仅创建备份"
        exit 1
        ;;
esac