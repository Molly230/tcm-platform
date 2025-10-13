# Nginx + SSL证书配置指南

## 🚀 快速部署流程

### 1. 安装Nginx

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install nginx -y

# CentOS/RHEL
sudo yum install nginx -y

# 启动Nginx
sudo systemctl start nginx
sudo systemctl enable nginx
```

---

## 🔐 获取免费SSL证书（Let's Encrypt）

### 方法一：使用Certbot（推荐）

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx -y

# 自动配置Nginx + 获取证书
sudo certbot --nginx -d tcmlife.top -d www.tcmlife.top

# 自动续期（证书90天有效期）
sudo certbot renew --dry-run
```

### 方法二：手动获取证书

```bash
# 仅获取证书
sudo certbot certonly --nginx -d tcmlife.top

# 证书路径：
# /etc/letsencrypt/live/tcmlife.top/fullchain.pem
# /etc/letsencrypt/live/tcmlife.top/privkey.pem
```

---

## 📝 Nginx配置文件

创建 `/etc/nginx/sites-available/tcmlife`:

```nginx
# HTTP -> HTTPS 重定向
server {
    listen 80;
    listen [::]:80;
    server_name tcmlife.top www.tcmlife.top;

    # Let's Encrypt验证
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    # 其他请求重定向到HTTPS
    location / {
        return 301 https://$server_name$request_uri;
    }
}

# HTTPS主配置
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name tcmlife.top www.tcmlife.top;

    # SSL证书
    ssl_certificate /etc/letsencrypt/live/tcmlife.top/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/tcmlife.top/privkey.pem;

    # SSL配置（Mozilla推荐）
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # 安全头
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # 日志
    access_log /var/log/nginx/tcmlife_access.log;
    error_log /var/log/nginx/tcmlife_error.log;

    # 前端静态文件
    location / {
        root /var/www/tcmlife/frontend/dist;
        try_files $uri $uri/ /index.html;

        # 缓存配置
        location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2|ttf|eot)$ {
            expires 1y;
            add_header Cache-Control "public, immutable";
        }
    }

    # 后端API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;

        # 超时设置
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }

    # 上传文件代理
    location /uploads/ {
        proxy_pass http://127.0.0.1:8001/uploads/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;

        # 大文件上传
        client_max_body_size 100M;
    }

    # WebSocket支持（如果需要）
    location /ws/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    # 健康检查
    location /health {
        proxy_pass http://127.0.0.1:8001/health;
        access_log off;
    }
}
```

---

## 🔧 启用配置

```bash
# 创建软链接
sudo ln -s /etc/nginx/sites-available/tcmlife /etc/nginx/sites-enabled/

# 测试配置
sudo nginx -t

# 重载Nginx
sudo systemctl reload nginx
```

---

## 🛡️ 防火墙配置

```bash
# UFW (Ubuntu)
sudo ufw allow 'Nginx Full'
sudo ufw allow 22/tcp  # SSH
sudo ufw enable

# firewalld (CentOS)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

---

## 📊 性能优化

编辑 `/etc/nginx/nginx.conf`:

```nginx
user www-data;
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 4096;
    use epoll;
}

http {
    # 基础配置
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    server_tokens off;

    # Gzip压缩
    gzip on;
    gzip_vary on;
    gzip_proxied any;
    gzip_comp_level 6;
    gzip_types text/plain text/css text/xml text/javascript
               application/json application/javascript application/xml+rss
               application/rss+xml font/truetype font/opentype
               application/vnd.ms-fontobject image/svg+xml;

    # 文件上传大小
    client_max_body_size 100M;
    client_body_buffer_size 128k;

    # 缓存
    proxy_cache_path /var/cache/nginx levels=1:2 keys_zone=my_cache:10m max_size=1g inactive=60m;
    proxy_cache_key "$scheme$request_method$host$request_uri";
}
```

---

## ✅ 验证SSL配置

### 在线检测工具

1. **SSL Labs**: https://www.ssllabs.com/ssltest/
2. **Security Headers**: https://securityheaders.com/

### 命令行测试

```bash
# 检查证书
openssl s_client -connect tcmlife.top:443 -servername tcmlife.top

# 测试HTTP2
curl -I --http2 https://tcmlife.top
```

---

## 🔄 自动续期SSL证书

Certbot会自动添加cron任务，手动测试：

```bash
# 测试续期
sudo certbot renew --dry-run

# 查看自动任务
sudo systemctl status certbot.timer

# 手动续期
sudo certbot renew
sudo systemctl reload nginx
```

---

## 🆘 常见问题

### 1. 证书获取失败

检查DNS解析:
```bash
dig tcmlife.top
nslookup tcmlife.top
```

### 2. Nginx启动失败

检查配置语法:
```bash
sudo nginx -t
```

查看错误日志:
```bash
sudo tail -f /var/log/nginx/error.log
```

### 3. 502 Bad Gateway

检查后端服务:
```bash
# 后端是否运行
curl http://localhost:8001/health

# 查看后端日志
cd backend
tail -f app.log
```

---

## 🚀 部署清单

- [ ] 安装Nginx
- [ ] 获取SSL证书
- [ ] 配置Nginx文件
- [ ] 测试配置
- [ ] 启用站点
- [ ] 配置防火墙
- [ ] 验证SSL安全性
- [ ] 测试完整流程
- [ ] 配置自动续期

**完成！** 你的网站现在是HTTPS安全连接 🔐
