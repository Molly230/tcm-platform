#!/bin/bash
# 传统部署方式（不使用Docker）

echo "中医健康平台 - 传统部署方式"

# 检查Node.js
if ! command -v node &> /dev/null; then
    echo "请先安装 Node.js 18+"
    exit 1
fi

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "请先安装 Python 3.8+"
    exit 1
fi

# 检查PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "请先安装 PostgreSQL"
    exit 1
fi

echo "1. 安装后端依赖..."
cd backend
pip3 install -r requirements.txt

echo "2. 配置数据库..."
# 需要手动创建数据库
createdb tcm_platform
alembic upgrade head
python create_admin.py

echo "3. 安装前端依赖..."
cd ../frontend
npm install
npm run build

echo "4. 启动后端..."
cd ../backend
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 &

echo "5. 配置Nginx..."
# 需要手动配置Nginx指向前端构建文件

echo "传统部署完成，但你需要手动配置很多东西..."