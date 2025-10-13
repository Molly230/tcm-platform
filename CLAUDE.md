# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述
这是一个中医健康服务平台，包含教育、健康咨询和轻问诊功能。采用前后端分离架构，支持多端访问。项目采用了服务层、统一异常处理、枚举管理等企业级架构模式。

## 架构组成
- **frontend/**: Vue 3 + TypeScript + Element Plus 前端应用
- **backend/**: FastAPI + Python 后端 API 服务（包含完整的服务层架构）
- **mobile/**: UniApp 移动端（支持微信小程序、H5、APP）

## ✅ 架构问题已修复
近期已完成的架构优化：
1. **✅ 枚举统一管理**: 已迁移所有代码使用 `enums_v2.py`，旧版 `enums.py` 已备份移除
2. **✅ 服务层架构简化**: 移除过度抽象的服务层，新增简化版API (`products_simple.py`)
3. **✅ 前端组件重构**: `EnumSelect.vue` 已拆分为多个专用组件 (`enum/` 目录)
4. **✅ 启动脚本修复**: 端口配置已更正为 3000/8001
5. **待优化**: 测试体系仍需完善，主要依赖独立测试脚本

## 常用开发命令

### 前端开发 (frontend/)
```bash
cd frontend
npm install
npm run dev      # 开发服务器 (http://localhost:3000)
npm run build    # 生产构建
npm run preview  # 预览构建结果

# TypeScript类型检查 (手动运行，项目未配置自动检查)
npx vue-tsc --noEmit  # 检查TypeScript类型错误
```

### 后端开发 (backend/)
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001  # 开发服务器，API文档: http://localhost:8001/docs

# 数据库迁移
alembic revision --autogenerate -m "描述"  # 生成迁移文件
alembic upgrade head                      # 执行迁移

# 数据管理
python create_admin.py           # 创建管理员
python seed_data.py              # 初始化数据
python create_test_data.py       # 创建测试数据
python clean_and_recreate_data.py  # 清理并重新创建数据
python create_users_simple.py   # 简化版用户创建

# 开发测试脚本（项目采用独立测试脚本模式）
python test_simple_api.py        # 测试基础API功能
python test_admin_endpoint.py    # 测试管理员接口
python test_course_create.py     # 测试课程创建和删除
python test_course_save.py       # 测试课程保存功能
python debug_simple.py          # 枚举和基础功能调试
python debug_users.py           # 用户相关功能调试
python debug_product_create.py  # 产品创建调试
python test_422_error.py        # 422验证错误测试

# 数据库操作
cd backend && python -c "from app.database import engine; print('Database:', engine.url)"

# 枚举相关工具（⚠️ 注意枚举重复问题）
python fix_enum_simple.py       # 修复重复枚举定义
python migrate_enum_values.py   # 迁移枚举值（处理v1到v2的迁移）
python check_course_categories.py # 检查课程分类枚举
```

### 移动端开发 (mobile/)
```bash
cd mobile
npm install
npm run dev:h5           # H5开发 (运行在默认端口)
npm run build:h5         # H5构建  
npm run dev:mp-weixin    # 微信小程序开发
npm run build:mp-weixin  # 微信小程序构建

# 注意：移动端使用 UniApp 框架，命令格式为 uni -p <platform>
# package.json 中的实际命令可能需要根据 UniApp CLI 版本调整
```

### 环境变量配置
```bash
# 复制环境变量模板
cp backend/.env.example backend/.env
# 根据需要修改配置
```

## 核心技术栈

### 前端
- Vue 3 + Composition API
- TypeScript
- Element Plus UI框架
- Pinia 状态管理
- Vite 构建工具

### 后端
- FastAPI 0.116.1 + Pydantic 2.11.7
- SQLAlchemy 2.0.43 ORM + SQLite (默认) / PostgreSQL (生产环境)
- JWT认证 (python-jose 3.5.0 + PyJWT 2.9.0)
- Alembic 1.16.5 数据库迁移
- Websockets 12.0 支持
- 腾讯云SDK集成
- **支付集成**: Ping++ 2.7.2, 支付宝SDK 3.7.779, 微信支付 1.8.18
- **统一枚举管理** (⚠️ 使用 `app/core/enums_v2.py`，避免使用旧版 `enums.py`)
- **服务层架构** (`app/services/`) - 注意避免过度抽象
- **统一异常处理** (`app/core/exceptions.py`)
- **统一响应格式** (`app/core/response.py`)
- **审计日志系统** (`app/models/audit_log.py`)

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
  - `EnumSelect.vue` - 枚举选择组件（⚠️ 组件过于复杂，建议拆分）
  - `StatusTransition.vue` - 状态转换组件
  - `NavigationBar.vue` - 导航栏组件
- `src/views/` - 页面视图
  - `admin/` - 管理后台页面
  - `AboutWuShanShanView.vue` - 关于页面
- `src/router/` - Vue路由配置
- `src/stores/` - Pinia状态管理
- `src/utils/api.ts` - 统一API调用工具
- `src/services/` - 前端服务层

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

### 架构关键点
- **统一枚举管理**: ⚠️ 当前存在重复定义问题
  - 优先使用: `backend/app/core/enums_v2.py` (新版本，支持状态机和元数据)
  - 避免使用: `backend/app/core/enums.py` (旧版本，计划废弃)
  - 迁移工具: `migrate_enum_values.py`, `fix_enum_simple.py`
- **服务层架构**: `backend/app/services/` - 包含业务逻辑、权限检查、审计日志
  - ⚠️ 注意: 当前服务层可能过于复杂，需要权衡抽象度
- **异常处理系统**: 
  - 自定义异常类: `backend/app/core/exceptions.py`
  - 全局异常处理器: `backend/app/main.py`
  - 统一响应格式: `backend/app/core/response.py`
- **端口配置**: 后端默认运行在8001端口，前端通过Vite代理（vite.config.ts）对接
- **权限系统**: 基于JWT + 角色的权限控制，路由守卫在 `frontend/src/router/index.ts`
- **静态文件**: 上传文件通过FastAPI StaticFiles挂载在 `/uploads` 路径
- **审计日志**: 所有重要操作记录在 `audit_log` 表中，包含操作者、对象、变更内容

### 开发规范
- **API文档**: FastAPI自动生成，开发时访问 `http://localhost:8001/docs`
- **前端代码**: TypeScript语法但未配置严格类型检查
- **数据库**: Alembic管理迁移，SQLAlchemy ORM模式，软删除设计（is_deleted字段）
- **文件上传**: 统一存储在 `backend/uploads/` 目录，按类型和日期分类
- **医疗合规**: 医疗相关功能需注意合规性要求
- **测试方式**: ⚠️ 项目采用独立测试脚本模式而非传统测试框架
  - API测试: `backend/test_*.py` 脚本
  - 功能调试: `backend/debug_*.py` 脚本  
  - 业务测试: 各模块专用测试脚本
- **代码检查**: ⚠️ 项目未配置ESLint、Prettier或mypy等代码检查工具
- **枚举使用**: 新功能必须使用 `enums_v2.py`，避免重复定义
- **服务层调用**: 复杂业务逻辑通过服务层处理，但避免过度抽象

### 调试技巧
- 使用 `backend/debug_*.py` 脚本进行快速调试
- 422验证错误会在控制台打印详细信息（main.py异常处理器）
- 健康检查接口: `GET /health/detailed` 检查系统状态
- 请求日志中间件会记录所有API调用和响应时间
- 敏感信息（密码、token等）在日志中自动过滤

## 文件上传与静态资源
- 文件上传目录：`backend/uploads/`
- 视频文件存储：`uploads/videos/`
- 图片文件存储：`uploads/images/`
- 文档文件存储：`uploads/documents/`
- 静态文件访问：`http://localhost:8001/uploads/`（注意端口是8001）
- 前端通过代理访问：`http://localhost:3000/uploads/`

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
python quick_test.py          # 快速检测系统状态（如果存在）
```

⚠️ **注意**: start.sh脚本端口配置有误，建议手动启动或修复脚本

### 系统诊断和测试工具
```bash
# 完整业务流程测试（推荐）
python test_shopping.py       # 测试注册→登录→购物→支付完整流程

# 端口占用检查工具（Windows）
python kill_port_8001.py     # 清理8001端口占用（如需要）
netstat -ano | findstr :8001 # 检查8001端口状态
netstat -ano | findstr :3000 # 检查3000端口状态

# 服务状态检查
curl http://localhost:8001/health/detailed  # 后端健康检查
curl http://localhost:3000                  # 前端访问检查
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
✅ **端口配置已统一修复**
- **前端开发服务器**: http://localhost:3000 (Vite开发服务器)
- **后端API服务**: http://localhost:8001 (FastAPI服务器)
- **API文档**: http://localhost:8001/docs (Swagger文档)
- **管理后台**: http://localhost:3000/admin
- **健康检查**: http://localhost:8001/health/detailed
- **WebSocket**: ws://localhost:8001 (实时通讯)
- **静态文件访问**: http://localhost:8001/uploads/ (通过前端代理: http://localhost:3000/uploads/)
- **移动端H5**: 根据UniApp配置的端口
- **✅ 修复**: start.sh脚本端口配置已更正，与vite.config.ts保持一致

## 数据模型关系
- **用户系统**: User -> UserProfile (1:1)
- **专家系统**: Expert -> User (多对一)
- **课程系统**: Course -> Lesson (一对多), User -> Course (多对多学习关系)
- **订单系统**: Order -> OrderItem (一对多), User -> Order (一对多)
- **咨询系统**: Consultation -> User/Expert (多对一关系)
- **产品系统**: Product -> Category (多对一)

## 项目特殊文件说明

### 关键配置文件
- **PINGPP_CONFIG.md** - Ping++支付聚合服务配置文档
- **nginx-dev.conf** - 开发环境Nginx配置
- **ping_rsa_private_key.pem** - Ping++支付RSA私钥（生产环境）
- **ping_rsa_private_key.pem.example** - RSA私钥示例文件

### 服务层架构文件
- **backend/app/services/product_service.py** - 商品业务服务层（完整的企业级架构示例）
- **backend/app/core/enums_v2.py** - 新版枚举管理系统（支持状态机）
- **backend/app/core/enums.py** - ⚠️ 旧版枚举（计划废弃）
- **backend/app/core/exceptions.py** - 统一异常处理
- **backend/app/core/response.py** - API响应格式标准化

### 前端特殊组件
- **frontend/src/components/EnumSelect.vue** - 枚举选择组件（⚠️ 247行，功能过多，建议拆分）
- **frontend/src/services/** - 前端服务层封装
- **frontend/src/utils/api.ts** - 统一API调用工具

### 测试和调试脚本
项目采用独立测试脚本模式，而非传统pytest框架：
- `test_*.py` - 功能测试脚本
- `debug_*.py` - 调试辅助脚本  
- `migrate_*.py` - 数据迁移脚本
- `create_*.py` - 数据初始化脚本

## 重要架构说明

### FastAPI应用结构
- **主应用入口**: `backend/app/main.py` - 包含全局异常处理、CORS配置、中间件、静态文件挂载
- **API路由集合**: `backend/app/api/api.py` - 统一路由注册
- **数据库连接**: `backend/app/database.py` - SQLAlchemy引擎和会话管理
- **配置管理**: `backend/app/core/config.py` - 环境变量和应用配置
- **核心模块**: `backend/app/core/` - 包含：
  - `enums_v2.py` - 统一枚举定义（推荐版本，支持状态机和元数据）
  - `enums.py` - 旧版枚举定义（⚠️ 计划废弃，避免使用）
  - `exceptions.py` - 自定义异常类（TCMException基类，支持业务错误码）
  - `response.py` - 统一响应格式（ApiResponse工具类）
  - `config.py` - 环境配置和应用设置
  - `reliable_pay.py` - 支付服务封装

### 前端架构特点
- **Vue 3 + Composition API**: 使用最新的Vue3语法和组合式API
- **路由权限控制**: 管理员和用户路由分离，统一权限验证
- **状态管理**: Pinia store用于用户状态和购物车管理
- **组件库**: Element Plus提供UI组件，自定义业务组件在 `src/components/`
- **API代理**: Vite配置代理到后端8001端口（vite.config.ts），支持开发时跨域
- **特殊组件**: ⚠️ 部分组件过于复杂，建议拆分
  - `EnumSelect.vue` - 枚举选择组件（247行，功能过多）
  - `StatusTransition.vue` - 状态转换组件
  - `NavigationBar.vue` - 导航栏组件  
- **API工具**: `src/utils/api.ts` - 统一API调用工具（包含自动token管理和错误处理）
- **服务层**: `src/services/` - 前端业务服务封装

### 支付系统集成
项目集成了多种支付方式：
- 支付宝支付 (alipay-sdk-python)
- 微信支付 (wechatpy)  
- **Ping++支付聚合** (pingpp) - 主要支付方案
  - 支持模拟支付模式（PINGPP_MOCK_MODE=true） - 当前默认设置
  - 配置文件：`PINGPP_CONFIG.md` - 完整配置指南
  - API端点：`/api/reliable-pay/` - 支付服务接口
  - 智能降级：配置错误时自动切换到模拟支付
  - 测试密钥：`[REDACTED_TEST_KEY]` (已配置)
  - App ID：`[REDACTED_APP_ID]` (已配置)
  - **重要**: 因Python 3.13兼容性问题，目前使用模拟+真实配置混合模式

### 支付测试命令
```bash
# 快速支付功能测试（推荐）
python test_shopping.py        # 完整购物+支付流程测试

# 支付API单独测试
curl -X POST http://localhost:8001/api/reliable-pay/create \
  -H "Content-Type: application/json" \
  -d '{"order_id":"TEST001","payment_method":"alipay_qr"}'

# 模拟支付成功
curl -X POST http://localhost:8001/api/reliable-pay/simulate-success/TEST001
```

### 数据库说明
- **开发环境**: SQLite数据库 (`backend/tcm_backend.db`)
- **生产环境**: 支持PostgreSQL (通过DATABASE_URL环境变量配置)
- **迁移管理**: Alembic管理数据库版本和结构变更 (位于 `backend/alembic/`)
- **数据模型**: 统一枚举定义避免重复，models和schemas分离
- **审计字段**: 所有主要表包含 created_at, updated_at, is_deleted 字段
- **软删除**: 使用 is_deleted 标志实现软删除

### 一键部署
- **快速启动**: `./setup.sh` - 全自动环境设置和服务启动
- **日常管理**: `./start.sh` 启动服务，`./stop.sh` 停止服务
- **健康检查**: `python quick_test.py` 检测系统状态

## 关键业务逻辑

### 用户权限系统
- **角色层级**: SUPER_ADMIN > ADMIN > DOCTOR > VIP > USER
- **JWT认证**: 使用 python-jose 实现，token有效期可配置
- **权限检查**: 通过依赖注入在API端点进行权限验证

### 支付流程
1. 用户下单 → 创建Order记录
2. 调用支付接口 → 创建Payment记录
3. 支付回调 → 更新订单状态
4. 发送通知 → 完成交易

### 文件处理
- **上传限制**: 图片10MB，视频100MB，文档5MB
- **文件类型验证**: 后端验证MIME类型和文件扩展名
- **路径结构**: uploads/{type}/{year}/{month}/filename

## 常见问题排查

### 端口冲突（Windows）
```bash
netstat -ano | findstr :8001  # 检查8001端口占用
netstat -ano | findstr :3000  # 检查3000端口占用
taskkill /F /PID <PID>        # 强制结束进程
```

### 数据库问题
```bash
cd backend
rm tcm_backend.db           # 删除数据库重新初始化
alembic upgrade head        # 重新执行迁移
python create_admin.py      # 重新创建管理员
```

### 前端构建问题
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install                 # 重新安装依赖
```

### API调试问题
```bash
# 检查API服务状态
curl http://localhost:8001/health/detailed

# 测试登录接口
python backend/debug_simple.py

# 查看数据库内容
sqlite3 backend/tcm_backend.db ".tables"  # 查看所有表
sqlite3 backend/tcm_backend.db "SELECT * FROM users LIMIT 5;"
```