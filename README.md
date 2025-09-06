# 中医健康服务平台

一个完整的中医健康服务平台，包含用户管理、课程教育、专家咨询、商品销售、支付系统等功能。

## 🚀 快速开始（5分钟搞定）

### 对于小白用户

1. **安装必需软件**（只需要安装一次）
   - [下载Python 3.8+](https://www.python.org/downloads/)
   - [下载Node.js 18+](https://nodejs.org/)

2. **一键启动**
   ```bash
   ./setup.sh
   ```
   这个命令会自动完成所有设置，包括安装依赖、创建数据库、启动服务等。

3. **访问平台**
   - 前端页面: http://localhost:5173
   - 管理后台: http://localhost:5173/admin
   - API文档: http://localhost:8000/docs

4. **测试账户**
   - 管理员: admin@tcm.com / admin123
   - 普通用户: user@tcm.com / user123

### 图形化管理界面

如果你不喜欢命令行，可以使用图形化管理界面：
```bash
./manage.sh
```

## 📁 项目结构

```
中医健康平台/
├── frontend/          # Vue.js 前端
├── backend/           # FastAPI 后端
├── mobile/            # UniApp 移动端
├── nginx/             # Nginx 配置
├── scripts/           # 各种脚本
├── logs/              # 日志文件
├── uploads/           # 上传文件
├── backups/           # 数据备份
├── ssl/               # SSL证书
├── setup.sh           # 一键初始化
├── manage.sh          # 图形化管理
├── start.sh           # 启动平台
├── stop.sh            # 停止平台
└── deploy.sh          # 部署到服务器
```

## 🎯 核心功能

### 用户系统
- ✅ 用户注册/登录
- ✅ 权限管理
- ✅ 个人资料管理

### 教育系统
- ✅ 课程管理
- ✅ 视频播放
- ✅ 学习进度跟踪

### 咨询系统
- ✅ 专家列表
- ✅ 在线咨询
- ✅ 视频通话（腾讯云TRTC）

### 电商系统
- ✅ 商品管理
- ✅ 购物车
- ✅ 订单系统
- ✅ 支付集成（支付宝/微信支付）

### 管理系统
- ✅ 后台管理界面
- ✅ 数据统计
- ✅ 内容审核
- ✅ 系统监控

## 🛠️ 常用命令

### 基础操作
```bash
# 初始化平台（第一次使用）
./setup.sh

# 启动平台
./start.sh

# 停止平台
./stop.sh

# 图形化管理
./manage.sh

# 快速测试
python3 quick_test.py
```

### 数据管理
```bash
# 备份数据
./scripts/backup.sh

# 恢复数据
./scripts/restore.sh 20241201_120000

# 重置数据库
cd backend && python create_admin.py
```

### 日志查看
```bash
# 查看实时日志
tail -f logs/backend.log logs/frontend.log

# 查看错误日志
tail -f logs/error.log
```

## 🌐 部署到服务器

### 方案1: 传统部署（适合小白）
1. 购买云服务器
2. 将项目文件夹上传到服务器
3. 运行 `./setup.sh`
4. 配置域名解析

### 方案2: Docker部署（推荐）
1. 服务器安装Docker
2. 运行 `./deploy.sh`
3. 配置域名和SSL证书

### 方案3: Git自动部署
1. 代码上传到GitHub
2. 修改 `deploy_git.sh` 配置
3. 运行 `./deploy_git.sh`

详细部署说明请查看 [DEPLOYMENT.md](DEPLOYMENT.md)

## ⚙️ 配置说明

### 环境变量
复制 `.env.example` 为 `.env` 并修改以下配置：

```bash
# 数据库
DB_PASSWORD=your_secure_password

# JWT密钥
SECRET_KEY=your-super-secret-key

# 支付配置
ALIPAY_APP_ID=your_app_id
WECHAT_APP_ID=your_wechat_app_id

# 服务器地址
SERVER_HOST=https://your-domain.com
```

### 支付配置
1. 申请支付宝商户账号
2. 申请微信支付商户号
3. 配置回调地址
4. 在 `.env` 文件中填入相关参数

## 📊 监控和维护

### 系统监控
```bash
# 实时监控
python3 scripts/monitor.py --daemon

# 查看监控报告
python3 scripts/monitor.py
```

### 日志管理
- 应用日志: `logs/app.log`
- 错误日志: `logs/error.log`
- 支付日志: `logs/payment.log`
- 访问日志: `logs/nginx/access.log`

### 数据备份
```bash
# 手动备份
./scripts/backup.sh

# 定时备份（每天凌晨2点）
./scripts/setup_cron.sh
```

## 🔧 开发指南

### 本地开发
```bash
# 后端开发
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# 前端开发
cd frontend
npm run dev

# 移动端开发
cd mobile
npm run dev:h5
```

### 添加新功能
1. 后端：在 `backend/app/api/` 添加路由
2. 前端：在 `frontend/src/views/` 添加页面
3. 数据库：使用 `alembic revision --autogenerate`

### 代码规范
- 后端遵循 FastAPI 最佳实践
- 前端使用 Vue 3 Composition API
- 统一使用 TypeScript

## ❓ 常见问题

### Q: 启动失败怎么办？
A: 运行 `python3 quick_test.py` 检查问题，通常是端口占用或依赖未安装。

### Q: 如何重置系统？
A: 停止服务，删除 `backend/tcm_backend.db`，重新运行 `./setup.sh`。

### Q: 支付功能如何测试？
A: 使用支付宝/微信支付的沙箱环境进行测试。

### Q: 如何更新代码？
A: 运行 `git pull` 然后 `./deploy.sh update`。

### Q: 数据丢失了怎么办？
A: 使用 `./scripts/restore.sh` 恢复最近的备份。

## 📞 技术支持

遇到问题时：
1. 查看 [小白操作指南.md](小白操作指南.md)
2. 运行 `python3 quick_test.py` 诊断问题
3. 检查日志文件：`tail -f logs/*.log`
4. 重启服务：`./stop.sh && ./start.sh`

## 📄 许可证

本项目仅用于学习和个人使用。商业使用请联系作者。

## 🎉 开始使用

现在就运行以下命令开始使用你的中医健康服务平台：

```bash
./setup.sh
```

等待几分钟后，访问 http://localhost:5173 即可看到你的平台！

---

**记住最重要的几个命令：**
- 🚀 启动: `./start.sh`
- ⏹️ 停止: `./stop.sh`
- 🔧 管理: `./manage.sh`
- 📋 测试: `python3 quick_test.py`