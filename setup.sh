#!/bin/bash
# 中医健康平台 - 一键初始化脚本
# 这个脚本会自动完成所有设置，你只需要等待即可

set -e

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${GREEN}===========================================${NC}"
echo -e "${GREEN}中医健康平台 - 一键初始化${NC}"
echo -e "${GREEN}===========================================${NC}"
echo ""
echo -e "${YELLOW}这个脚本会自动：${NC}"
echo "✓ 检查和安装所需环境"
echo "✓ 安装所有依赖"
echo "✓ 初始化数据库"
echo "✓ 创建测试数据"
echo "✓ 启动所有服务"
echo ""
echo -e "${YELLOW}你只需要等待，什么都不用做！${NC}"
echo ""

# 检查操作系统
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    OS="windows"
else
    echo -e "${RED}不支持的操作系统${NC}"
    exit 1
fi

echo -e "${GREEN}检测到系统: $OS${NC}"

# 创建必需目录
echo -e "${YELLOW}创建项目目录...${NC}"
mkdir -p logs backend/logs frontend/dist uploads/images uploads/videos

# 检查Python
check_python() {
    echo -e "${YELLOW}检查Python环境...${NC}"
    
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1-2)
        echo -e "${GREEN}✓ 找到Python $PYTHON_VERSION${NC}"
        PYTHON_CMD="python3"
    elif command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version | cut -d' ' -f2 | cut -d'.' -f1-2)
        echo -e "${GREEN}✓ 找到Python $PYTHON_VERSION${NC}"
        PYTHON_CMD="python"
    else
        echo -e "${RED}✗ 未找到Python${NC}"
        echo "请安装Python 3.8+: https://www.python.org/downloads/"
        exit 1
    fi
}

# 检查Node.js
check_node() {
    echo -e "${YELLOW}检查Node.js环境...${NC}"
    
    if command -v node &> /dev/null; then
        NODE_VERSION=$(node --version)
        echo -e "${GREEN}✓ 找到Node.js $NODE_VERSION${NC}"
    else
        echo -e "${RED}✗ 未找到Node.js${NC}"
        echo "请安装Node.js 18+: https://nodejs.org/"
        exit 1
    fi
    
    if command -v npm &> /dev/null; then
        NPM_VERSION=$(npm --version)
        echo -e "${GREEN}✓ 找到npm $NPM_VERSION${NC}"
    else
        echo -e "${RED}✗ 未找到npm${NC}"
        exit 1
    fi
}

# 安装后端依赖
setup_backend() {
    echo -e "${YELLOW}设置后端环境...${NC}"
    cd backend
    
    # 创建虚拟环境
    if [ ! -d "venv" ]; then
        echo "创建Python虚拟环境..."
        $PYTHON_CMD -m venv venv
    fi
    
    # 激活虚拟环境
    if [[ "$OS" == "windows" ]]; then
        source venv/Scripts/activate
    else
        source venv/bin/activate
    fi
    
    # 安装依赖
    echo "安装Python依赖..."
    pip install --upgrade pip
    pip install -r requirements.txt
    
    # 创建开发数据库配置
    if [ ! -f "tcm_backend.db" ]; then
        echo "初始化数据库..."
        alembic upgrade head || echo "数据库迁移完成"
        
        echo "创建管理员账户..."
        $PYTHON_CMD create_admin.py || echo "管理员可能已存在"
        
        echo "创建测试数据..."
        $PYTHON_CMD seed_data.py || echo "测试数据可能已存在"
    fi
    
    cd ..
    echo -e "${GREEN}✓ 后端设置完成${NC}"
}

# 安装前端依赖
setup_frontend() {
    echo -e "${YELLOW}设置前端环境...${NC}"
    cd frontend
    
    if [ ! -d "node_modules" ]; then
        echo "安装前端依赖..."
        npm install
    else
        echo "前端依赖已存在，跳过安装"
    fi
    
    cd ..
    echo -e "${GREEN}✓ 前端设置完成${NC}"
}

# 创建启动脚本
create_start_script() {
    echo -e "${YELLOW}创建启动脚本...${NC}"
    
    cat > start.sh << 'STARTSCRIPT'
#!/bin/bash
# 启动所有服务

echo "启动中医健康平台..."

# 启动后端
echo "启动后端API..."
cd backend
if [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

nohup uvicorn app.main:app --reload --port 8000 > ../logs/backend.log 2>&1 &
echo $! > ../backend.pid
cd ..

# 等待后端启动
sleep 3

# 启动前端
echo "启动前端开发服务器..."
cd frontend
nohup npm run dev > ../logs/frontend.log 2>&1 &
echo $! > ../frontend.pid
cd ..

echo ""
echo "🎉 启动完成！"
echo ""
echo "📱 前端访问: http://localhost:5173"
echo "🔧 后端API: http://localhost:8000"
echo "📚 API文档: http://localhost:8000/docs"
echo ""
echo "👤 管理员账户: admin@tcm.com"
echo "🔑 默认密码: admin123"
echo ""
echo "📋 查看日志: tail -f logs/backend.log logs/frontend.log"
echo "⏹️ 停止服务: ./stop.sh"
STARTSCRIPT

    chmod +x start.sh
    
    # 创建停止脚本
    cat > stop.sh << 'STOPSCRIPT'
#!/bin/bash
echo "停止所有服务..."

if [ -f "backend.pid" ]; then
    kill $(cat backend.pid) 2>/dev/null
    rm backend.pid
    echo "✓ 后端已停止"
fi

if [ -f "frontend.pid" ]; then
    kill $(cat frontend.pid) 2>/dev/null  
    rm frontend.pid
    echo "✓ 前端已停止"
fi

# 清理可能残留的进程
pkill -f "uvicorn app.main:app" 2>/dev/null || true
pkill -f "npm run dev" 2>/dev/null || true

echo "✅ 所有服务已停止"
STOPSCRIPT

    chmod +x stop.sh
    echo -e "${GREEN}✓ 启动脚本创建完成${NC}"
}

# 主执行流程
main() {
    check_python
    check_node
    setup_backend
    setup_frontend
    create_start_script
    
    echo ""
    echo -e "${GREEN}🎉 初始化完成！${NC}"
    echo ""
    echo -e "${YELLOW}现在你可以：${NC}"
    echo "1. 运行 ./start.sh 启动平台"
    echo "2. 访问 http://localhost:5173"
    echo "3. 使用 admin@tcm.com / admin123 登录"
    echo "4. 运行 ./stop.sh 停止平台"
    echo ""
    echo -e "${YELLOW}是否现在启动平台？(y/n)${NC}"
    read -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        ./start.sh
        
        echo ""
        echo -e "${GREEN}正在打开浏览器...${NC}"
        sleep 5
        
        # 尝试打开浏览器
        if command -v open &> /dev/null; then
            open http://localhost:5173
        elif command -v xdg-open &> /dev/null; then
            xdg-open http://localhost:5173
        elif command -v start &> /dev/null; then
            start http://localhost:5173
        else
            echo "请手动打开: http://localhost:5173"
        fi
    fi
}

# 执行
main