# 🚀 生产环境上线检查清单

## ✅ 已完成项（可以上线）

### 🔐 安全配置
- [x] **强SECRET_KEY已生成** (64字节)
  - 路径: `backend/.env`
  - 验证: `SECRET_KEY=dhuwFmKjMF3n...`

- [x] **SECRET_KEY强制校验**
  - 未配置将抛出异常，防止使用默认密钥

- [x] **Git历史清理**
  - 移除57个Python缓存文件
  - 更新.gitignore防止未来泄露

- [x] **.env文件安全**
  - 已在.gitignore中
  - Git历史无泄露记录

### 💳 支付系统
- [x] **微信支付已配置**
  - AppID: `wx8ef971d8efa87ffb`
  - 商户号: `1727330435`
  - API密钥: 已配置
  - Mock模式: `false` (真实支付)

- [x] **无用支付代码已清理**
  - Ping++、支付宝代码已删除
  - 仅保留微信支付

### 📚 文档准备
- [x] **PostgreSQL配置文档** - `POSTGRESQL_SETUP.md`
- [x] **Nginx+SSL配置文档** - `NGINX_SSL_SETUP.md`
- [x] **Git清理指南** - `GIT_CLEANUP.md`
- [x] **微信支付文档** - `WECHAT_PAY_CONFIG.md`

---

## ⚠️ 必须完成（上线前）

### 🗄️ 数据库切换
- [ ] **配置PostgreSQL**
  ```bash
  # 参考：POSTGRESQL_SETUP.md
  # 1. 创建数据库和用户
  # 2. 更新.env中的DATABASE_URL
  # 3. 运行数据库迁移
  ```

- [ ] **数据迁移验证**
  ```bash
  cd backend
  alembic upgrade head
  python ../scripts/create_admin.py
  ```

### 🌐 Web服务器配置
- [ ] **安装Nginx**
  ```bash
  sudo apt install nginx
  ```

- [ ] **获取SSL证书**
  ```bash
  sudo certbot --nginx -d tcmlife.top
  ```

- [ ] **配置Nginx**
  - 参考: `NGINX_SSL_SETUP.md`
  - 配置文件: `/etc/nginx/sites-available/tcmlife`

### 🔥 防火墙配置
- [ ] **开放端口**
  ```bash
  sudo ufw allow 80/tcp   # HTTP
  sudo ufw allow 443/tcp  # HTTPS
  sudo ufw allow 22/tcp   # SSH
  sudo ufw enable
  ```

### 🚀 部署代码
- [ ] **上传代码到服务器**
  ```bash
  # 方式1：Git克隆
  git clone <你的仓库地址>

  # 方式2：rsync上传
  rsync -avz --exclude='.git' . user@server:/var/www/tcmlife/
  ```

- [ ] **安装依赖**
  ```bash
  # 后端
  cd backend
  pip install -r requirements.txt

  # 前端
  cd ../frontend
  npm install
  npm run build
  ```

- [ ] **配置环境变量**
  ```bash
  cp backend/.env.example backend/.env
  # 编辑.env，填入生产环境配置
  ```

### 🔄 启动服务
- [ ] **后端服务（使用systemd）**

  创建 `/etc/systemd/system/tcmlife-backend.service`:
  ```ini
  [Unit]
  Description=TCM Platform Backend
  After=network.target

  [Service]
  User=www-data
  WorkingDirectory=/var/www/tcmlife/backend
  Environment="PATH=/usr/local/bin"
  ExecStart=/usr/local/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```

  启动:
  ```bash
  sudo systemctl enable tcmlife-backend
  sudo systemctl start tcmlife-backend
  sudo systemctl status tcmlife-backend
  ```

---

## ✔️ 测试验证

### 1. 本地测试
- [ ] **后端启动正常**
  ```bash
  cd backend
  uvicorn app.main:app --reload --port 8001
  ```
  访问: http://localhost:8001/docs

- [ ] **前端构建成功**
  ```bash
  cd frontend
  npm run build
  # 检查dist/目录
  ```

### 2. 生产环境测试
- [ ] **HTTPS访问正常**
  - 访问: https://tcmlife.top
  - 检查SSL证书有效

- [ ] **API接口测试**
  ```bash
  curl https://tcmlife.top/api/health
  ```

- [ ] **微信支付测试**
  - 创建测试订单
  - 验证支付流程
  - 检查回调通知

- [ ] **用户注册/登录**
  - 注册新用户
  - 登录验证
  - JWT token正常

- [ ] **管理后台访问**
  - https://tcmlife.top/admin
  - 管理员登录正常

---

## 🔍 监控和日志

### 设置日志
- [ ] **Nginx日志**
  ```bash
  tail -f /var/log/nginx/tcmlife_access.log
  tail -f /var/log/nginx/tcmlife_error.log
  ```

- [ ] **应用日志**
  ```bash
  tail -f /var/www/tcmlife/backend/app.log
  ```

### 配置监控（可选）
- [ ] 安装Prometheus + Grafana
- [ ] 配置Sentry错误追踪
- [ ] 设置告警通知

---

## 📋 上线前最终检查

### 安全检查
- [x] SECRET_KEY是强密钥（非默认值）
- [ ] DEBUG=False（生产环境）
- [x] WECHAT_MOCK_MODE=false（真实支付）
- [ ] PostgreSQL密码足够强
- [ ] 服务器已更新系统补丁
- [ ] SSH密钥登录（禁用密码）

### 性能检查
- [ ] 数据库索引已优化
- [ ] 前端已压缩（gzip）
- [ ] 静态文件CDN配置（可选）
- [ ] 数据库连接池配置

### 备份策略
- [ ] 数据库自动备份
- [ ] 代码版本管理（Git）
- [ ] 配置文件备份

---

## 🎯 上线步骤（按顺序执行）

1. **服务器准备** (30分钟)
   - [ ] 购买/准备服务器
   - [ ] 配置SSH访问
   - [ ] 安装基础软件

2. **数据库配置** (30分钟)
   - [ ] 安装PostgreSQL
   - [ ] 创建数据库和用户
   - [ ] 运行数据迁移

3. **Web服务器** (1小时)
   - [ ] 安装Nginx
   - [ ] 获取SSL证书
   - [ ] 配置Nginx

4. **部署应用** (30分钟)
   - [ ] 上传代码
   - [ ] 安装依赖
   - [ ] 配置环境变量
   - [ ] 启动服务

5. **测试验证** (30分钟)
   - [ ] 功能测试
   - [ ] 性能测试
   - [ ] 安全测试

6. **上线** ✅
   - [ ] DNS解析到服务器
   - [ ] 监控启动
   - [ ] 通知团队

---

## 🆘 回滚计划

如果出现严重问题:

```bash
# 1. 停止新服务
sudo systemctl stop tcmlife-backend

# 2. 恢复数据库备份（如果需要）
psql -U tcm_user tcm_platform < backup.sql

# 3. 切换到旧版本
git checkout <上一个稳定版本>

# 4. 重启服务
sudo systemctl start tcmlife-backend
```

---

## 📞 联系方式

- **技术支持**: [你的邮箱]
- **紧急联系**: [你的电话]
- **文档**: https://github.com/[你的仓库]

---

**预计总时长**: 3-4小时（首次部署）

**当前状态**: 🟡 代码就绪，等待服务器部署

**下一步**: 按照 `POSTGRESQL_SETUP.md` 配置数据库
