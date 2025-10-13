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
