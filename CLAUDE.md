# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述
这是一个中医健康服务平台，包含教育、健康咨询和轻问诊功能。采用前后端分离架构，支持多端访问。

## 架构组成
- **frontend/**: Vue 3 + TypeScript + Element Plus 前端应用
- **backend/**: FastAPI + Python 后端 API 服务  
- **mobile/**: UniApp 移动端（支持微信小程序、H5、APP）

## 常用开发命令

### 前端开发 (frontend/)
```bash
cd frontend
npm install
npm run dev      # 开发服务器
npm run build    # 生产构建
npm run preview  # 预览构建结果
npm run lint     # ESLint 代码检查
npm run type-check  # TypeScript 类型检查
```

### 后端开发 (backend/)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload  # 开发服务器，API文档: http://localhost:8000/docs

# 数据库迁移
alembic revision --autogenerate -m "描述"  # 生成迁移文件
alembic upgrade head                      # 执行迁移

# 数据管理
python create_admin.py           # 创建管理员
python seed_data.py              # 初始化数据
python create_test_data.py       # 创建测试数据
python clean_and_recreate_data.py  # 清理并重新创建数据
```

### 移动端开发 (mobile/)
```bash
cd mobile
npm install
npm run dev:h5           # H5开发
npm run build:h5         # H5构建
npm run dev:mp-weixin    # 微信小程序开发
npm run build:mp-weixin  # 微信小程序构建
```

## 核心技术栈

### 前端
- Vue 3 + Composition API
- TypeScript
- Element Plus UI框架
- Pinia 状态管理
- Vite 构建工具

### 后端
- FastAPI + Pydantic
- SQLAlchemy ORM + PostgreSQL
- JWT认证 (python-jose)
- Alembic数据库迁移
- Websockets支持
- 腾讯云SDK集成

### 移动端
- UniApp框架
- Vue 3语法
- 多平台编译

## 项目结构要点

### 后端核心模块
- `app/api/` - API路由和端点
- `app/models/` - SQLAlchemy数据模型 
- `app/schemas/` - Pydantic验证模式
- `app/core/` - 配置和安全设置
- `app/database.py` - 数据库连接

### 前端核心结构
- `src/components/` - 公共组件
- `src/views/` - 页面视图
- `src/router/` - Vue路由配置
- `src/store/` - Pinia状态管理

### 移动端页面结构
- `src/pages/` - 各平台页面
- `src/components/` - 公共组件
- `pages.json` - 页面配置

## 业务域模型
- **用户管理**: 注册、登录、权限
- **专家系统**: 专家信息、资质管理
- **课程教育**: 课程内容、学习进度
- **健康咨询**: AI问诊、专家咨询
- **预约系统**: 咨询预约、时间管理

## 开发注意事项
- 后端使用FastAPI自动生成API文档，开发时访问 `/docs`
- 前端采用TypeScript，注意类型定义
- 移动端使用UniApp语法，注意平台兼容性
- 数据库迁移使用Alembic管理
- 医疗相关功能需注意合规性要求

## 文件上传与静态资源
- 文件上传目录：`backend/uploads/`
- 视频文件存储：`uploads/videos/`
- 图片文件存储：`uploads/images/`
- 静态文件访问：`http://localhost:8000/uploads/`

## 安全配置
- JWT Token认证
- CORS配置支持跨域
- 密码使用bcrypt加密
- 权限管理基于角色

## 第三方服务集成
- 腾讯云服务：视频通话、云存储
- WebSocket：实时通讯

## 快速启动命令

### 一键初始化（首次使用）
```bash
./setup.sh                    # 自动安装依赖、初始化数据库、启动服务
python quick_test.py          # 快速检测系统状态
```

### 项目管理
```bash
./start.sh                    # 启动所有服务（如果存在）
./stop.sh                     # 停止所有服务（如果存在）
./manage.sh                   # 图形化管理界面（如果存在）
```

### 测试与诊断
```bash
python quick_test.py          # 系统健康检查
./scripts/backup.sh           # 数据备份（如果存在）
./scripts/restore.sh [备份ID] # 数据恢复（如果存在）
```

## 数据库相关操作

### 数据库管理脚本
```bash
cd backend
python create_admin.py              # 创建管理员用户
python seed_data.py                 # 初始化基础数据
python create_test_data.py          # 创建测试数据
python clean_and_recreate_data.py   # 重置数据库
python recreate_db.py               # 完全重建数据库（如果存在）
```

### 测试账户（开发用）
- 管理员: admin@tcm.com / admin123  
- 普通用户: user@tcm.com / user123

## 服务端口配置
- 前端: http://localhost:5173
- 后端API: http://localhost:8000  
- API文档: http://localhost:8000/docs
- 管理后台: http://localhost:5173/admin

## 重要架构说明

### FastAPI应用结构
- 主应用入口: `backend/app/main.py`
- API路由集合: `backend/app/api/api.py` 
- 数据库连接: `backend/app/database.py`
- 配置管理: `backend/app/core/config.py`

### 支付系统集成
项目集成了多种支付方式：
- 支付宝支付 (alipay-sdk-python)
- 微信支付 (wechatpy)  
- Ping++支付聚合 (pingpp)

### 数据库说明
- 使用SQLite作为默认数据库 (`backend/tcm_backend.db`)
- 支持PostgreSQL生产环境
- Alembic管理数据库迁移版本

### 部署脚本
项目包含多种部署方案：
- `deploy.sh` - Docker部署
- `deploy_git.sh` - Git自动部署  
- `deploy_traditional.sh` - 传统部署