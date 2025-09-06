#!/bin/bash
# 本地开发测试启动脚本

echo "中医健康平台 - 本地测试启动"

# 检查是否已安装依赖
echo "1. 检查环境..."

# 后端依赖检查
if [ ! -d "backend/venv" ]; then
    echo "创建Python虚拟环境..."
    cd backend
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# 前端依赖检查
if [ ! -d "frontend/node_modules" ]; then
    echo "安装前端依赖..."
    cd frontend
    npm install
    cd ..
fi

# 创建SQLite数据库（开发用）
if [ ! -f "backend/tcm_backend.db" ]; then
    echo "初始化数据库..."
    cd backend
    source venv/bin/activate
    alembic upgrade head
    python create_admin.py
    cd ..
fi

echo "2. 启动服务..."

# 启动后端
echo "启动后端 API 服务..."
cd backend
source venv/bin/activate
nohup uvicorn app.main:app --reload --port 8000 > ../logs/backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 5

# 启动前端
echo "启动前端开发服务器..."
cd frontend
nohup npm run dev > ../logs/frontend.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo "✅ 启动完成!"
echo ""
echo "前端地址: http://localhost:5173"
echo "后端API: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo ""
echo "管理员账户: admin@tcm.com / admin123"
echo ""
echo "停止服务: kill $BACKEND_PID $FRONTEND_PID"
echo "查看日志: tail -f logs/backend.log logs/frontend.log"

# 保存进程ID
echo $BACKEND_PID > backend.pid
echo $FRONTEND_PID > frontend.pid