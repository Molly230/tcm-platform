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

nohup uvicorn app.main:app --reload --port 8001 > ../logs/backend.log 2>&1 &
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
echo "📱 前端访问: http://localhost:3000"
echo "🔧 后端API: http://localhost:8001"
echo "📚 API文档: http://localhost:8001/docs"
echo ""
echo "👤 管理员账户: admin@tcm.com"
echo "🔑 默认密码: admin123"
echo ""
echo "📋 查看日志: tail -f logs/backend.log logs/frontend.log"
echo "⏹️ 停止服务: ./stop.sh"
