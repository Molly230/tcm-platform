#!/bin/bash
# 中医健康平台 - 总控制脚本

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

show_banner() {
    clear
    echo -e "${GREEN}"
    echo "╔══════════════════════════════════════════════════════╗"
    echo "║              中医健康服务平台                          ║"
    echo "║             管理控制面板                              ║"
    echo "╚══════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

show_menu() {
    echo -e "${BLUE}请选择要执行的操作：${NC}"
    echo ""
    echo "🚀 基础操作："
    echo "  1) 初始化平台 (第一次使用)"
    echo "  2) 启动平台"
    echo "  3) 停止平台"
    echo "  4) 重启平台"
    echo "  5) 快速测试"
    echo ""
    echo "📊 监控和维护："
    echo "  6) 查看运行状态"
    echo "  7) 查看日志"
    echo "  8) 备份数据"
    echo "  9) 清理日志"
    echo ""
    echo "🌐 部署相关："
    echo "  10) Docker部署"
    echo "  11) 生成SSL证书"
    echo "  12) 查看部署指南"
    echo ""
    echo "🛠️ 开发工具："
    echo "  13) 更新依赖"
    echo "  14) 重建数据库"
    echo "  15) 创建测试数据"
    echo ""
    echo "  0) 退出"
    echo ""
    echo -e "${YELLOW}请输入选项编号:${NC}"
}

init_platform() {
    echo -e "${GREEN}初始化平台...${NC}"
    ./setup.sh
}

start_platform() {
    echo -e "${GREEN}启动平台...${NC}"
    if [ -f "start.sh" ]; then
        ./start.sh
    else
        echo -e "${RED}未找到启动脚本，请先初始化平台${NC}"
        echo "选择选项1进行初始化"
    fi
}

stop_platform() {
    echo -e "${YELLOW}停止平台...${NC}"
    if [ -f "stop.sh" ]; then
        ./stop.sh
    else
        echo -e "${YELLOW}未找到停止脚本，尝试手动停止...${NC}"
        pkill -f "uvicorn app.main:app" 2>/dev/null || true
        pkill -f "npm run dev" 2>/dev/null || true
        echo "已尝试停止所有相关进程"
    fi
}

restart_platform() {
    echo -e "${YELLOW}重启平台...${NC}"
    stop_platform
    sleep 3
    start_platform
}

quick_test() {
    echo -e "${BLUE}执行快速测试...${NC}"
    python3 quick_test.py
    echo ""
    read -p "按回车键继续..." 
}

check_status() {
    echo -e "${BLUE}检查服务状态...${NC}"
    echo ""
    
    # 检查进程
    if [ -f "backend.pid" ]; then
        echo -e "${GREEN}✓ 后端服务运行中 (PID: $(cat backend.pid))${NC}"
    else
        echo -e "${RED}✗ 后端服务未运行${NC}"
    fi
    
    if [ -f "frontend.pid" ]; then
        echo -e "${GREEN}✓ 前端服务运行中 (PID: $(cat frontend.pid))${NC}"
    else
        echo -e "${RED}✗ 前端服务未运行${NC}"
    fi
    
    # 检查端口占用
    if lsof -i:8000 &>/dev/null; then
        echo -e "${GREEN}✓ 后端端口8000已占用${NC}"
    else
        echo -e "${RED}✗ 后端端口8000未使用${NC}"
    fi
    
    if lsof -i:5173 &>/dev/null; then
        echo -e "${GREEN}✓ 前端端口5173已占用${NC}"
    else
        echo -e "${RED}✗ 前端端口5173未使用${NC}"
    fi
    
    echo ""
    read -p "按回车键继续..."
}

view_logs() {
    echo -e "${BLUE}选择要查看的日志：${NC}"
    echo "1) 后端日志"
    echo "2) 前端日志" 
    echo "3) 所有日志"
    echo "4) 错误日志"
    read -p "请选择: " log_choice
    
    case $log_choice in
        1)
            if [ -f "logs/backend.log" ]; then
                tail -f logs/backend.log
            else
                echo "后端日志文件不存在"
            fi
            ;;
        2)
            if [ -f "logs/frontend.log" ]; then
                tail -f logs/frontend.log
            else
                echo "前端日志文件不存在"
            fi
            ;;
        3)
            if [ -f "logs/backend.log" ] && [ -f "logs/frontend.log" ]; then
                tail -f logs/backend.log logs/frontend.log
            else
                echo "日志文件不完整"
            fi
            ;;
        4)
            if [ -f "logs/error.log" ]; then
                tail -f logs/error.log
            else
                echo "错误日志文件不存在"
            fi
            ;;
        *)
            echo "无效选项"
            ;;
    esac
}

backup_data() {
    echo -e "${GREEN}备份数据...${NC}"
    if [ -f "scripts/backup.sh" ]; then
        ./scripts/backup.sh
    else
        # 简单备份
        backup_dir="backups/$(date +%Y%m%d_%H%M%S)"
        mkdir -p "$backup_dir"
        
        if [ -f "backend/tcm_backend.db" ]; then
            cp backend/tcm_backend.db "$backup_dir/"
            echo "✓ 数据库已备份"
        fi
        
        if [ -d "uploads" ]; then
            cp -r uploads "$backup_dir/"
            echo "✓ 上传文件已备份"
        fi
        
        echo "备份完成: $backup_dir"
    fi
    read -p "按回车键继续..."
}

clean_logs() {
    echo -e "${YELLOW}清理日志文件...${NC}"
    echo "将删除7天前的日志文件"
    read -p "确定要继续吗？(y/N): " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        find logs -name "*.log*" -mtime +7 -delete 2>/dev/null || true
        echo -e "${GREEN}日志清理完成${NC}"
    else
        echo "已取消"
    fi
    read -p "按回车键继续..."
}

docker_deploy() {
    echo -e "${GREEN}Docker部署...${NC}"
    if command -v docker &> /dev/null; then
        ./deploy.sh
    else
        echo -e "${RED}Docker未安装${NC}"
        echo "请先安装Docker: https://docs.docker.com/get-docker/"
    fi
    read -p "按回车键继续..."
}

generate_ssl() {
    echo -e "${GREEN}生成SSL证书...${NC}"
    if [ -f "scripts/generate_ssl.sh" ]; then
        ./scripts/generate_ssl.sh
    else
        echo "SSL生成脚本不存在"
    fi
    read -p "按回车键继续..."
}

show_deployment_guide() {
    if [ -f "小白操作指南.md" ]; then
        echo -e "${BLUE}显示部署指南...${NC}"
        cat "小白操作指南.md"
    else
        echo "部署指南文件不存在"
    fi
    echo ""
    read -p "按回车键继续..."
}

update_dependencies() {
    echo -e "${GREEN}更新依赖...${NC}"
    
    # 更新后端依赖
    echo "更新Python依赖..."
    cd backend
    if [ -d "venv" ]; then
        source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
        pip install --upgrade pip
        pip install -r requirements.txt --upgrade
    fi
    cd ..
    
    # 更新前端依赖
    echo "更新Node.js依赖..."
    cd frontend
    if [ -d "node_modules" ]; then
        npm update
    fi
    cd ..
    
    echo -e "${GREEN}依赖更新完成${NC}"
    read -p "按回车键继续..."
}

rebuild_database() {
    echo -e "${YELLOW}重建数据库...${NC}"
    echo -e "${RED}警告: 这将删除所有现有数据！${NC}"
    read -p "确定要继续吗？(y/N): " confirm
    
    if [[ $confirm =~ ^[Yy]$ ]]; then
        stop_platform
        
        if [ -f "backend/tcm_backend.db" ]; then
            mv backend/tcm_backend.db backend/tcm_backend.db.backup
        fi
        
        cd backend
        if [ -d "venv" ]; then
            source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
            alembic upgrade head
            python create_admin.py
        fi
        cd ..
        
        echo -e "${GREEN}数据库重建完成${NC}"
    else
        echo "已取消"
    fi
    read -p "按回车键继续..."
}

create_test_data() {
    echo -e "${GREEN}创建测试数据...${NC}"
    cd backend
    if [ -d "venv" ]; then
        source venv/bin/activate 2>/dev/null || source venv/Scripts/activate
        python seed_data.py
    fi
    cd ..
    echo -e "${GREEN}测试数据创建完成${NC}"
    read -p "按回车键继续..."
}

# 主循环
main() {
    while true; do
        show_banner
        show_menu
        read -r choice
        
        case $choice in
            1) init_platform ;;
            2) start_platform ;;
            3) stop_platform ;;
            4) restart_platform ;;
            5) quick_test ;;
            6) check_status ;;
            7) view_logs ;;
            8) backup_data ;;
            9) clean_logs ;;
            10) docker_deploy ;;
            11) generate_ssl ;;
            12) show_deployment_guide ;;
            13) update_dependencies ;;
            14) rebuild_database ;;
            15) create_test_data ;;
            0) 
                echo -e "${GREEN}谢谢使用！${NC}"
                exit 0
                ;;
            *)
                echo -e "${RED}无效选项，请重新选择${NC}"
                sleep 2
                ;;
        esac
    done
}

# 运行主程序
main