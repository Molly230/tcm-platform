# 🚀 部署指南（小白版）

> 这是一个零基础也能看懂的部署教程，预计 3-4 小时完成

---

## 📋 部署前准备

### 你需要：
1. ✅ 一台服务器（阿里云/腾讯云）
2. ✅ 一个域名（如 tcmlife.top）
3. ✅ 基础的SSH连接知识
4. ✅ 本项目代码（已就绪）

---

## 🎯 部署流程（6大步骤）

### 第一步：购买服务器 (10分钟)

**推荐配置：**
- CPU: 2核
- 内存: 4GB
- 系统: Ubuntu 22.04 LTS
- 带宽: 5Mbps
- 服务商: 阿里云/腾讯云

**完成后你会得到：**
- 服务器IP地址（如：123.456.789.0）
- SSH登录密码

---

### 第二步：连接服务器 (5分钟)

**Windows用户：**
```bash
# 下载并安装 XShell 或使用 Windows Terminal
ssh root@你的服务器IP

# 输入密码登录
```

**Mac/Linux用户：**
```bash
ssh root@你的服务器IP
```

---

### 第三步：安装基础软件 (30分钟)

登录服务器后，依次执行：

#### 3.1 更新系统
```bash
sudo apt update && sudo apt upgrade -y
```

#### 3.2 安装Python 3.11+
```bash
sudo apt install python3.11 python3.11-venv python3-pip -y
```

#### 3.3 安装Node.js 18+
```bash
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs -y
node -v  # 验证安装
```

#### 3.4 安装PostgreSQL
```bash
sudo apt install postgresql postgresql-contrib -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

#### 3.5 安装Nginx
```bash
sudo apt install nginx -y
sudo systemctl start nginx
sudo systemctl enable nginx
```

#### 3.6 安装SSL证书工具
```bash
sudo apt install certbot python3-certbot-nginx -y
```

---

### 第四步：配置数据库 (20分钟)

#### 4.1 创建数据库和用户
```bash
# 切换到postgres用户
sudo -u postgres psql

# 在PostgreSQL命令行中执行：
CREATE DATABASE tcm_platform;
CREATE USER tcm_user WITH PASSWORD '你的强密码_改这里';
GRANT ALL PRIVILEGES ON DATABASE tcm_platform TO tcm_user;
\q  # 退出
```

**⚠️ 重要：记下你设置的密码！**

---

### 第五步：上传代码并配置 (30分钟)

#### 5.1 创建项目目录
```bash
sudo mkdir -p /var/www/tcmlife
sudo chown -R $USER:$USER /var/www/tcmlife
cd /var/www/tcmlife
```

#### 5.2 上传代码

**方式A：使用Git（推荐）**
```bash
# 如果你的代码在GitHub/Gitee
git clone https://github.com/你的用户名/你的仓库.git .

# 如果代码是私有仓库，需要配置SSH密钥或使用token
```

**方式B：使用SFTP工具上传**
```
使用 FileZilla 或 WinSCP：
1. 连接到服务器
2. 上传整个项目文件夹到 /var/www/tcmlife/
```

#### 5.3 配置后端环境变量
```bash
cd /var/www/tcmlife/backend

# 复制环境变量模板
cp .env.example .env

# 编辑环境变量
nano .env
```

**修改以下内容：**
```ini
# 数据库配置（修改密码为你在步骤4设置的密码）
DATABASE_URL=postgresql://tcm_user:你的数据库密码@localhost:5432/tcm_platform

# JWT密钥（已经配置好，无需修改）
SECRET_KEY=dhuwFmKjMF3nupfx8YpPYgwetG7nmxqG07n2K_KN-NPK15YV-0rmQvtDbN4QizC-z_1I1Ot48PSpaujSu1qV7w

# 微信支付配置（已经配置好，无需修改）
WECHAT_APP_ID=wx8ef971d8efa87ffb
WECHAT_MCH_ID=1727330435
WECHAT_API_KEY=50f96b28cbce26aaaf1e9fd1f5aebbe2
WECHAT_MOCK_MODE=false

# 域名配置（修改为你的域名）
WECHAT_NOTIFY_URL=https://tcmlife.top/api/wechat-pay/notify
WECHAT_H5_DOMAIN=tcmlife.top
```

按 `Ctrl+O` 保存，`Ctrl+X` 退出

#### 5.4 安装后端依赖
```bash
cd /var/www/tcmlife/backend

# 创建虚拟环境
python3.11 -m venv venv
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 运行数据库迁移
alembic upgrade head

# 创建管理员账户
python ../scripts/create_admin.py
```

#### 5.5 构建前端
```bash
cd /var/www/tcmlife/frontend

# 安装依赖
npm install

# 构建生产版本
npm run build
```

---

### 第六步：配置Web服务器 (40分钟)

#### 6.1 域名解析
在你的域名服务商（如阿里云）添加DNS记录：
```
类型: A
主机记录: @
记录值: 你的服务器IP
TTL: 10分钟
```

等待5-10分钟让DNS生效，可以用这个命令检查：
```bash
ping tcmlife.top
```

#### 6.2 获取SSL证书
```bash
# 自动配置SSL证书（会自动配置Nginx）
sudo certbot --nginx -d tcmlife.top -d www.tcmlife.top

# 按提示操作：
# 1. 输入邮箱
# 2. 同意服务条款 (Y)
# 3. 选择是否重定向HTTP到HTTPS (2 - 推荐)
```

#### 6.3 配置Nginx
```bash
# 创建Nginx配置文件
sudo nano /etc/nginx/sites-available/tcmlife
```

**粘贴以下配置：**
```nginx
server {
    listen 80;
    listen [::]:80;
    server_name tcmlife.top www.tcmlife.top;

    # 重定向到HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name tcmlife.top www.tcmlife.top;

    # SSL证书（Certbot自动配置）
    ssl_certificate /etc/letsencrypt/live/tcmlife.top/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tcmlife.top/privkey.pem;

    # 日志
    access_log /var/log/nginx/tcmlife_access.log;
    error_log /var/log/nginx/tcmlife_error.log;

    # 前端静态文件
    location / {
        root /var/www/tcmlife/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # 上传文件
    location /uploads/ {
        proxy_pass http://127.0.0.1:8001/uploads/;
        client_max_body_size 100M;
    }
}
```

保存并退出（`Ctrl+O`, `Ctrl+X`）

**启用配置：**
```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/tcmlife /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重载Nginx
sudo systemctl reload nginx
```

#### 6.4 配置后端服务（systemd）
```bash
# 创建服务文件
sudo nano /etc/systemd/system/tcmlife-backend.service
```

**粘贴以下内容：**
```ini
[Unit]
Description=TCM Platform Backend
After=network.target

[Service]
User=www-data
WorkingDirectory=/var/www/tcmlife/backend
Environment="PATH=/var/www/tcmlife/backend/venv/bin"
ExecStart=/var/www/tcmlife/backend/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8001
Restart=always

[Install]
WantedBy=multi-user.target
```

保存并退出

**启动服务：**
```bash
# 修改目录权限
sudo chown -R www-data:www-data /var/www/tcmlife

# 重载systemd
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start tcmlife-backend

# 设置开机自启
sudo systemctl enable tcmlife-backend

# 查看状态
sudo systemctl status tcmlife-backend
```

#### 6.5 配置防火墙
```bash
# 允许HTTP和HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp  # SSH

# 启用防火墙
sudo ufw enable
```

---

## ✅ 测试验证

### 1. 检查后端服务
```bash
# 查看服务状态
sudo systemctl status tcmlife-backend

# 查看日志
sudo journalctl -u tcmlife-backend -f
```

### 2. 测试网站访问
打开浏览器访问：
- https://tcmlife.top - 前端页面
- https://tcmlife.top/api/health - 后端健康检查
- https://tcmlife.top/docs - API文档

### 3. 测试管理后台
访问：https://tcmlife.top/admin
使用创建的管理员账户登录

---

## 🆘 常见问题

### 问题1：502 Bad Gateway
```bash
# 检查后端服务是否运行
sudo systemctl status tcmlife-backend

# 查看错误日志
sudo journalctl -u tcmlife-backend -n 50

# 重启后端
sudo systemctl restart tcmlife-backend
```

### 问题2：页面无法访问
```bash
# 检查Nginx状态
sudo systemctl status nginx

# 查看Nginx错误日志
sudo tail -f /var/log/nginx/tcmlife_error.log

# 测试Nginx配置
sudo nginx -t
```

### 问题3：SSL证书获取失败
```bash
# 确认域名已解析
ping tcmlife.top

# 重新获取证书
sudo certbot --nginx -d tcmlife.top
```

### 问题4：数据库连接失败
```bash
# 检查PostgreSQL状态
sudo systemctl status postgresql

# 测试数据库连接
sudo -u postgres psql -c "\l"

# 查看后端日志
sudo journalctl -u tcmlife-backend -n 50
```

---

## 🔄 更新代码

当你需要更新代码时：
```bash
cd /var/www/tcmlife

# 拉取最新代码
git pull

# 更新后端
cd backend
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head

# 更新前端
cd ../frontend
npm install
npm run build

# 重启后端服务
sudo systemctl restart tcmlife-backend
```

---

## 📊 监控和维护

### 查看日志
```bash
# 后端日志
sudo journalctl -u tcmlife-backend -f

# Nginx访问日志
sudo tail -f /var/log/nginx/tcmlife_access.log

# Nginx错误日志
sudo tail -f /var/log/nginx/tcmlife_error.log
```

### 数据库备份
```bash
# 手动备份
sudo -u postgres pg_dump tcm_platform > backup_$(date +%Y%m%d).sql

# 设置自动备份（每天凌晨2点）
sudo crontab -e
# 添加：0 2 * * * /usr/bin/pg_dump -U postgres tcm_platform > /var/backups/tcm_$(date +\%Y\%m\%d).sql
```

---

## 🎉 完成！

恭喜！你的中医健康平台已经成功部署到生产环境！

**访问地址：**
- 🌐 网站首页: https://tcmlife.top
- 👨‍💼 管理后台: https://tcmlife.top/admin
- 📚 API文档: https://tcmlife.top/docs

**记得：**
- ✅ 定期备份数据库
- ✅ 关注服务器日志
- ✅ 及时更新系统补丁

需要帮助？查看详细文档：
- `DEPLOY_CHECKLIST.md` - 完整检查清单
- `POSTGRESQL_SETUP.md` - 数据库详细配置
- `NGINX_SSL_SETUP.md` - Web服务器详细配置
