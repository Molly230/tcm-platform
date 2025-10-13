# 阿里云部署完整指南

## 🎯 推荐架构

```
用户浏览器
    ↓
阿里云CDN (可选)
    ↓
轻量应用服务器 (2核4G)
├── Nginx (前端 + 反向代理)
├── Backend (FastAPI + Gunicorn)
├── PostgreSQL (或使用RDS)
└── 文件存储 (OSS对象存储)
```

---

## 📦 第一步: 购买阿里云资源

### 1.1 轻量应用服务器

**推荐配置**:
- 地域: 选择离你用户最近的(如华东2-上海)
- 镜像: Ubuntu 22.04 LTS
- 套餐: 2核4G 80GB SSD (¥80/月) - 适合测试和小流量
- 套餐: 4核8G 180GB SSD (¥180/月) - 适合正式运营

**购买地址**:
https://www.aliyun.com/product/swas

**操作步骤**:
```bash
1. 登录阿里云控制台
2. 产品与服务 → 轻量应用服务器
3. 选择配置和地域
4. 设置服务器密码(记住!)
5. 购买并等待创建完成
```

### 1.2 数据库选择(二选一)

**方案A: RDS PostgreSQL(推荐生产环境)**
- 配置: 2核4G 100GB (¥240/月)
- 优点: 自动备份、高可用、免运维
- 购买地址: https://www.aliyun.com/product/rds/postgresql

**方案B: ECS自建PostgreSQL(推荐省钱)**
- 成本: 免费(使用ECS资源)
- 优点: 省钱
- 缺点: 需要手动备份和维护

### 1.3 OSS对象存储(存储图片/视频)

**配置**:
- 地域: 与ECS同一地域
- 存储类型: 标准存储
- 按量付费: 约¥0.12/GB/月

**购买地址**:
https://www.aliyun.com/product/oss

---

## 🔧 第二步: 服务器初始化

### 2.1 连接服务器

**Windows用户**:
```bash
# 下载XShell或使用阿里云自带的Web终端
ssh root@你的服务器IP
```

**Mac/Linux用户**:
```bash
ssh root@你的服务器IP
```

### 2.2 基础环境配置

```bash
# 更新系统
apt update && apt upgrade -y

# 安装基础工具
apt install -y git curl wget vim nginx certbot python3-certbot-nginx

# 安装Python 3.11
apt install -y python3.11 python3.11-venv python3-pip

# 安装Node.js 18
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# 安装PostgreSQL (如果不用RDS)
apt install -y postgresql postgresql-contrib

# 验证安装
python3.11 --version
node --version
npm --version
psql --version
```

### 2.3 创建部署用户(安全考虑)

```bash
# 创建www用户
useradd -m -s /bin/bash www
passwd www  # 设置密码

# 添加到sudo组
usermod -aG sudo www

# 切换到www用户
su - www
```

---

## 📂 第三步: 部署代码

### 3.1 上传代码到服务器

**方法1: Git(推荐)**
```bash
cd /home/www
git clone https://github.com/your-repo/999.git tcm-project
cd tcm-project
```

**方法2: 使用SCP/FTP上传**
```bash
# 在本地电脑执行
scp -r F:\360MoveData\Users\administered\Desktop\999 root@服务器IP:/home/www/tcm-project
```

### 3.2 配置后端

```bash
cd /home/www/tcm-project/backend

# 创建虚拟环境
python3.11 -m venv venv
source venv/bin/activate

# 安装依赖
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn  # 生产环境WSGI服务器

# 创建.env配置文件
cat > .env << 'EOF'
# 【必改】生成强随机密钥
SECRET_KEY=$(openssl rand -hex 32)

# 【必改】数据库配置
# 如果使用RDS:
DATABASE_URL=postgresql://用户名:密码@RDS内网地址:5432/tcm_production
# 如果自建PostgreSQL:
DATABASE_URL=postgresql://tcm_user:强密码@localhost:5432/tcm_production

# 【必改】微信支付配置
WECHAT_PAY_MOCK_MODE=false
WECHAT_APPID=你的AppID
WECHAT_MCHID=你的商户号
WECHAT_API_V3_KEY=你的32位APIv3密钥
WECHAT_APIV3_CERT_SERIAL_NUMBER=你的证书序列号
WECHAT_APIV3_PRIVATE_KEY_PATH=/home/www/tcm-project/backend/cert/apiclient_key.pem

# 【必改】回调地址 - 必须是HTTPS
WECHAT_NOTIFY_URL=https://你的域名.com/api/wechat-pay/notify

# 【必改】允许的域名
ALLOWED_ORIGINS=https://你的域名.com,https://www.你的域名.com

# 其他配置
CORS_ORIGINS=https://你的域名.com
DEBUG=false
EOF

# 生成真实的SECRET_KEY
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_hex(32))" >> .env.tmp
grep SECRET_KEY .env.tmp  # 复制这个值替换.env中的SECRET_KEY
rm .env.tmp
```

### 3.3 配置数据库

**如果使用RDS PostgreSQL**:
```bash
# 在阿里云控制台创建数据库
# 数据库名: tcm_production
# 字符集: UTF8
# 然后在ECS上执行:

cd /home/www/tcm-project/backend
source venv/bin/activate
alembic upgrade head  # 执行数据库迁移
python scripts/seed_data.py  # 初始化数据
python scripts/create_admin.py  # 创建管理员
```

**如果自建PostgreSQL**:
```bash
# 切换到postgres用户
sudo -u postgres psql

# 在PostgreSQL命令行执行:
CREATE DATABASE tcm_production;
CREATE USER tcm_user WITH PASSWORD '强密码';
GRANT ALL PRIVILEGES ON DATABASE tcm_production TO tcm_user;
\q

# 返回www用户执行迁移
cd /home/www/tcm-project/backend
source venv/bin/activate
alembic upgrade head
python scripts/seed_data.py
python scripts/create_admin.py
```

### 3.4 配置前端

```bash
cd /home/www/tcm-project/frontend

# 安装依赖
npm install

# 创建生产环境配置
cat > .env.production << 'EOF'
VITE_API_BASE_URL=https://你的域名.com
EOF

# 生产构建
npm run build

# 构建完成后,dist目录就是前端静态文件
```

---

## 🌐 第四步: 配置域名和SSL

### 4.1 域名解析

在阿里云域名控制台添加A记录:
```
主机记录: @
记录类型: A
记录值: 你的服务器公网IP
TTL: 10分钟

主机记录: www
记录类型: A
记录值: 你的服务器公网IP
TTL: 10分钟
```

### 4.2 申请免费SSL证书

```bash
# 使用Let's Encrypt申请免费证书
sudo certbot --nginx -d 你的域名.com -d www.你的域名.com

# 按提示输入邮箱和同意协议
# 证书会自动配置到Nginx

# 设置自动续期
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

---

## ⚙️ 第五步: 配置Nginx

### 5.1 创建Nginx配置

```bash
sudo vim /etc/nginx/sites-available/tcm
```

粘贴以下配置:

```nginx
# HTTP自动跳转HTTPS
server {
    listen 80;
    server_name 你的域名.com www.你的域名.com;
    return 301 https://$server_name$request_uri;
}

# HTTPS主配置
server {
    listen 443 ssl http2;
    server_name 你的域名.com www.你的域名.com;

    # SSL证书(Let's Encrypt会自动配置)
    ssl_certificate /etc/letsencrypt/live/你的域名.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/你的域名.com/privkey.pem;

    # SSL优化配置
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    # 前端静态文件
    root /home/www/tcm-project/frontend/dist;
    index index.html;

    # 前端路由(Vue Router history模式)
    location / {
        try_files $uri $uri/ /index.html;
    }

    # 后端API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket支持
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";

        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 上传文件静态访问
    location /uploads/ {
        alias /home/www/tcm-project/backend/uploads/;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }

    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_min_length 1024;
    gzip_types text/plain text/css text/xml text/javascript application/javascript application/json application/xml+rss;

    # 安全头
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # 限制上传大小
    client_max_body_size 100M;
}
```

### 5.2 启用配置

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/tcm /etc/nginx/sites-enabled/

# 删除默认配置
sudo rm /etc/nginx/sites-enabled/default

# 测试配置
sudo nginx -t

# 重启Nginx
sudo systemctl restart nginx
sudo systemctl enable nginx
```

---

## 🚀 第六步: 配置后端服务(Systemd)

### 6.1 创建Systemd服务文件

```bash
sudo vim /etc/systemd/system/tcm-backend.service
```

粘贴以下内容:

```ini
[Unit]
Description=TCM Backend Service
After=network.target postgresql.service

[Service]
Type=notify
User=www
Group=www
WorkingDirectory=/home/www/tcm-project/backend
Environment="PATH=/home/www/tcm-project/backend/venv/bin"

# Gunicorn启动命令
ExecStart=/home/www/tcm-project/backend/venv/bin/gunicorn \
    app.main:app \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8001 \
    --access-logfile /var/log/tcm/access.log \
    --error-logfile /var/log/tcm/error.log \
    --log-level info

# 重启策略
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 6.2 创建日志目录

```bash
sudo mkdir -p /var/log/tcm
sudo chown www:www /var/log/tcm
```

### 6.3 启动服务

```bash
# 重载systemd配置
sudo systemctl daemon-reload

# 启动服务
sudo systemctl start tcm-backend

# 设置开机自启
sudo systemctl enable tcm-backend

# 查看状态
sudo systemctl status tcm-backend

# 查看日志
sudo journalctl -u tcm-backend -f
```

---

## 🗄️ 第七步: 配置OSS对象存储(可选)

### 7.1 创建OSS Bucket

```bash
1. 登录阿里云OSS控制台
2. 创建Bucket
   - 名称: tcm-uploads
   - 地域: 与ECS同一地域
   - 读写权限: 私有
3. 获取AccessKey
   - 阿里云控制台 → AccessKey管理
   - 创建AccessKey并保存
```

### 7.2 配置后端使用OSS

```bash
cd /home/www/tcm-project/backend

# 安装OSS SDK
source venv/bin/activate
pip install oss2

# 在.env添加OSS配置
cat >> .env << 'EOF'

# OSS配置
OSS_ENABLE=true
OSS_ACCESS_KEY_ID=你的AccessKeyId
OSS_ACCESS_KEY_SECRET=你的AccessKeySecret
OSS_BUCKET_NAME=tcm-uploads
OSS_ENDPOINT=oss-cn-shanghai.aliyuncs.com
OSS_BASE_URL=https://tcm-uploads.oss-cn-shanghai.aliyuncs.com
EOF

# 重启后端服务
sudo systemctl restart tcm-backend
```

---

## 🔍 第八步: 验证部署

### 8.1 检查各项服务

```bash
# 检查Nginx
sudo systemctl status nginx
curl -I https://你的域名.com

# 检查后端
sudo systemctl status tcm-backend
curl https://你的域名.com/api/health/detailed

# 检查数据库连接
cd /home/www/tcm-project/backend
source venv/bin/activate
python -c "from app.database import engine; print('DB OK:', engine.url)"

# 查看日志
sudo tail -f /var/log/tcm/error.log
sudo tail -f /var/log/nginx/error.log
```

### 8.2 功能测试

```bash
# 测试登录
curl -X POST https://你的域名.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@tcm.com","password":"admin123"}'

# 测试商品列表
curl https://你的域名.com/api/products-simple/

# 测试微信支付配置
curl https://你的域名.com/api/wechat-pay/config
```

### 8.3 浏览器测试

1. 访问 https://你的域名.com
2. 注册/登录账号
3. 添加商品到购物车
4. 测试下单和支付流程
5. 检查微信支付二维码是否正常显示

---

## 📊 第九步: 监控和维护

### 9.1 配置日志轮转

```bash
sudo vim /etc/logrotate.d/tcm
```

```
/var/log/tcm/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    missingok
    create 0640 www www
}
```

### 9.2 数据库备份

```bash
# 创建备份脚本
cat > /home/www/backup.sh << 'EOF'
#!/bin/bash
BACKUP_DIR=/home/www/backups
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 备份数据库
pg_dump tcm_production > $BACKUP_DIR/db_$DATE.sql

# 备份上传文件
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz /home/www/tcm-project/backend/uploads

# 删除30天前的备份
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $DATE"
EOF

chmod +x /home/www/backup.sh

# 添加到定时任务(每天凌晨2点)
crontab -e
# 添加这行:
0 2 * * * /home/www/backup.sh >> /var/log/backup.log 2>&1
```

### 9.3 监控脚本

```bash
# 创建健康检查脚本
cat > /home/www/health_check.sh << 'EOF'
#!/bin/bash

# 检查后端服务
if ! systemctl is-active --quiet tcm-backend; then
    echo "Backend is down! Restarting..."
    systemctl restart tcm-backend
fi

# 检查Nginx
if ! systemctl is-active --quiet nginx; then
    echo "Nginx is down! Restarting..."
    systemctl restart nginx
fi

# 检查磁盘空间
DISK_USAGE=$(df -h / | awk 'NR==2 {print $5}' | sed 's/%//')
if [ $DISK_USAGE -gt 80 ]; then
    echo "Warning: Disk usage is ${DISK_USAGE}%"
fi
EOF

chmod +x /home/www/health_check.sh

# 每5分钟检查一次
crontab -e
# 添加:
*/5 * * * * /home/www/health_check.sh >> /var/log/health_check.log 2>&1
```

---

## 🎯 优化建议

### 性能优化

1. **启用CDN加速**
   - 阿里云CDN控制台配置
   - 加速域名绑定
   - 缓存静态资源

2. **数据库优化**
   ```sql
   -- 为常用字段添加索引
   CREATE INDEX idx_orders_user_id ON orders(user_id);
   CREATE INDEX idx_orders_status ON orders(status);
   CREATE INDEX idx_products_status ON products(status);
   ```

3. **Redis缓存**
   ```bash
   # 安装Redis
   apt install redis-server

   # Python安装redis包
   pip install redis

   # 在.env添加
   REDIS_URL=redis://localhost:6379/0
   ```

### 安全加固

1. **防火墙配置**
   ```bash
   # 启用UFW防火墙
   sudo ufw allow 22/tcp    # SSH
   sudo ufw allow 80/tcp    # HTTP
   sudo ufw allow 443/tcp   # HTTPS
   sudo ufw enable
   ```

2. **Fail2Ban防暴力破解**
   ```bash
   sudo apt install fail2ban
   sudo systemctl enable fail2ban
   ```

3. **定期更新**
   ```bash
   # 每周自动更新安全补丁
   sudo apt install unattended-upgrades
   sudo dpkg-reconfigure -plow unattended-upgrades
   ```

---

## 💰 成本估算

### 方案1: 入门配置 (约¥90/月)
- 轻量服务器 2核4G: ¥80/月
- 自建PostgreSQL: ¥0 (使用ECS资源)
- OSS按量付费: ¥10/月

### 方案2: 标准配置 (约¥270/月)
- 轻量服务器 2核4G: ¥80/月
- RDS PostgreSQL 2核4G: ¥180/月
- OSS按量付费: ¥10/月

### 方案3: 高性能配置 (约¥450/月)
- 轻量服务器 4核8G: ¥180/月
- RDS PostgreSQL 2核4G: ¥240/月
- OSS按量付费: ¥20/月
- CDN: ¥10/月

---

## 🆘 常见问题

### 1. 无法连接服务器
```bash
# 检查阿里云安全组
- 入站规则添加: 22, 80, 443端口

# 检查防火墙
sudo ufw status
```

### 2. SSL证书申请失败
```bash
# 确保域名已解析
ping 你的域名.com

# 确保80端口可访问
sudo netstat -tlnp | grep :80

# 停止Nginx重新申请
sudo systemctl stop nginx
sudo certbot certonly --standalone -d 你的域名.com
```

### 3. 后端无法启动
```bash
# 查看详细错误
sudo journalctl -u tcm-backend -n 50

# 检查配置文件
cd /home/www/tcm-project/backend
source venv/bin/activate
python -c "from app.main import app; print('OK')"
```

### 4. 微信支付回调失败
```bash
# 确认回调URL配置正确
grep WECHAT_NOTIFY_URL /home/www/tcm-project/backend/.env

# 必须是HTTPS
# 必须是公网可访问

# 查看回调日志
sudo tail -f /var/log/tcm/error.log | grep wechat
```

---

## 📞 技术支持

- 阿里云工单: https://workorder.console.aliyun.com/
- FastAPI文档: https://fastapi.tiangolo.com/
- Nginx文档: https://nginx.org/en/docs/
- PostgreSQL文档: https://www.postgresql.org/docs/

---

**部署完成后记得测试完整的购物和支付流程!** 🎉
