#!/bin/bash
# 中医健康服务平台 - 一键部署脚本

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}中医健康服务平台 - 一键部署脚本${NC}"
echo -e "${GREEN}========================================${NC}"

# 检查系统
check_system() {
    echo -e "${YELLOW}检查系统环境...${NC}"
    
    # 检查Docker
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}错误: Docker未安装${NC}"
        echo "请先安装Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    # 检查Docker Compose
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}错误: Docker Compose未安装${NC}"
        echo "请先安装Docker Compose"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Docker环境检查通过${NC}"
}

# 环境配置
setup_environment() {
    echo -e "${YELLOW}配置部署环境...${NC}"
    
    # 创建必需目录
    mkdir -p logs/nginx logs/backend backups ssl
    
    # 检查.env文件
    if [ ! -f ".env" ]; then
        if [ -f ".env.example" ]; then
            echo -e "${YELLOW}未找到.env文件，从模板创建...${NC}"
            cp .env.example .env
            echo -e "${RED}警告: 请编辑.env文件，配置所有必需参数${NC}"
            echo "特别是数据库密码、JWT密钥、支付配置等"
            read -p "是否现在编辑.env文件? (y/n): " -n 1 -r
            echo
            if [[ $REPLY =~ ^[Yy]$ ]]; then
                ${EDITOR:-nano} .env
            fi
        else
            echo -e "${RED}错误: 未找到.env或.env.example文件${NC}"
            exit 1
        fi
    fi
    
    echo -e "${GREEN}✓ 环境配置完成${NC}"
}

# 生成SSL证书
setup_ssl() {
    echo -e "${YELLOW}配置SSL证书...${NC}"
    
    if [ ! -f "ssl/cert.pem" ] || [ ! -f "ssl/key.pem" ]; then
        echo "生成自签名SSL证书（仅用于开发环境）..."
        ./scripts/generate_ssl.sh
        echo -e "${YELLOW}注意: 生产环境请使用真实的SSL证书${NC}"
    else
        echo -e "${GREEN}✓ SSL证书已存在${NC}"
    fi
}

# 构建和启动服务
deploy_services() {
    echo -e "${YELLOW}构建和启动服务...${NC}"
    
    # 停止现有服务
    echo "停止现有服务..."
    docker-compose down || true
    
    # 构建服务
    echo "构建Docker镜像..."
    docker-compose build
    
    # 启动服务
    echo "启动服务..."
    docker-compose up -d
    
    # 等待服务启动
    echo "等待服务启动..."
    sleep 30
    
    # 检查服务状态
    echo "检查服务状态..."
    docker-compose ps
}

# 初始化数据库
init_database() {
    echo -e "${YELLOW}初始化数据库...${NC}"
    
    # 等待数据库就绪
    echo "等待数据库就绪..."
    max_attempts=30
    attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if docker-compose exec -T db pg_isready -U tcm_user -d tcm_platform &>/dev/null; then
            echo -e "${GREEN}✓ 数据库连接成功${NC}"
            break
        fi
        
        echo "等待数据库启动... ($attempt/$max_attempts)"
        sleep 2
        ((attempt++))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        echo -e "${RED}错误: 数据库连接超时${NC}"
        exit 1
    fi
    
    # 运行数据库迁移
    echo "运行数据库迁移..."
    docker-compose exec -T backend alembic upgrade head
    
    # 创建管理员账户
    echo "创建管理员账户..."
    docker-compose exec -T backend python create_admin.py || echo "管理员账户可能已存在"
    
    # 初始化数据
    echo "初始化基础数据..."
    docker-compose exec -T backend python seed_data.py || echo "基础数据可能已存在"
}

# 设置定时任务
setup_monitoring() {
    echo -e "${YELLOW}设置监控和定时任务...${NC}"
    
    # 在后端容器中设置cron任务
    docker-compose exec -T backend /app/scripts/setup_cron.sh || echo "定时任务设置可能失败，请手动检查"
    
    echo -e "${GREEN}✓ 监控配置完成${NC}"
}

# 健康检查
health_check() {
    echo -e "${YELLOW}执行健康检查...${NC}"
    
    # 检查后端API
    if curl -f -s http://localhost:8000/api/health > /dev/null; then
        echo -e "${GREEN}✓ 后端API健康${NC}"
    else
        echo -e "${RED}✗ 后端API不可用${NC}"
    fi
    
    # 检查前端
    if curl -f -s http://localhost > /dev/null; then
        echo -e "${GREEN}✓ 前端服务健康${NC}"
    else
        echo -e "${RED}✗ 前端服务不可用${NC}"
    fi
    
    # 检查HTTPS
    if curl -f -s -k https://localhost > /dev/null; then
        echo -e "${GREEN}✓ HTTPS服务健康${NC}"
    else
        echo -e "${RED}✗ HTTPS服务不可用${NC}"
    fi
}

# 显示部署信息
show_deployment_info() {
    echo -e "\n${GREEN}========================================${NC}"
    echo -e "${GREEN}部署完成!${NC}"
    echo -e "${GREEN}========================================${NC}"
    echo ""
    echo -e "前端访问地址: ${GREEN}http://localhost${NC}"
    echo -e "HTTPS访问地址: ${GREEN}https://localhost${NC}"
    echo -e "后端API地址: ${GREEN}http://localhost:8000${NC}"
    echo -e "API文档地址: ${GREEN}http://localhost:8000/docs${NC}"
    echo ""
    echo -e "${YELLOW}重要提醒:${NC}"
    echo "1. 默认管理员账户: admin@tcm.com / admin123"
    echo "2. 生产环境请立即修改默认密码"
    echo "3. 配置真实的SSL证书"
    echo "4. 设置防火墙规则"
    echo "5. 定期备份数据"
    echo ""
    echo -e "日志查看: ${GREEN}docker-compose logs -f${NC}"
    echo -e "服务管理: ${GREEN}docker-compose [start|stop|restart]${NC}"
    echo -e "数据备份: ${GREEN}./scripts/backup.sh${NC}"
    echo ""
}

# 主执行流程
main() {
    case "${1:-deploy}" in
        "deploy")
            check_system
            setup_environment
            setup_ssl
            deploy_services
            init_database
            setup_monitoring
            health_check
            show_deployment_info
            ;;
        "update")
            echo -e "${YELLOW}更新部署...${NC}"
            docker-compose down
            docker-compose build
            docker-compose up -d
            health_check
            echo -e "${GREEN}更新完成${NC}"
            ;;
        "start")
            echo -e "${YELLOW}启动服务...${NC}"
            docker-compose start
            health_check
            ;;
        "stop")
            echo -e "${YELLOW}停止服务...${NC}"
            docker-compose stop
            ;;
        "restart")
            echo -e "${YELLOW}重启服务...${NC}"
            docker-compose restart
            health_check
            ;;
        "logs")
            docker-compose logs -f
            ;;
        "status")
            docker-compose ps
            health_check
            ;;
        *)
            echo "用法: $0 [deploy|update|start|stop|restart|logs|status]"
            echo ""
            echo "deploy  - 完整部署（默认）"
            echo "update  - 更新部署"
            echo "start   - 启动服务"
            echo "stop    - 停止服务"
            echo "restart - 重启服务"
            echo "logs    - 查看日志"
            echo "status  - 查看状态"
            exit 1
            ;;
    esac
}

# 执行主函数
main "$@"