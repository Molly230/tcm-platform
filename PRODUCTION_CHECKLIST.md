# 生产环境部署检查清单

## ⚠️ 部署前必须修改的配置

### 1. 后端环境变量 (backend/.env)

```bash
# 【必改】安全密钥 - 生成一个随机的长字符串
SECRET_KEY=请生成一个强随机密钥

# 【必改】数据库配置 - 使用PostgreSQL
DATABASE_URL=postgresql://user:password@localhost:5432/tcm_production

# 【必改】微信支付 - 切换到生产模式
WECHAT_PAY_MOCK_MODE=false

# 【必改】微信支付商户配置
WECHAT_MCHID=你的商户号
WECHAT_API_V3_KEY=你的APIv3密钥(32位)
WECHAT_APIV3_CERT_SERIAL_NUMBER=你的证书序列号

# 【必改】微信支付回调URL - 必须是公网可访问的HTTPS地址
WECHAT_NOTIFY_URL=https://your-domain.com/api/wechat-pay/notify

# 【必改】允许的域名
ALLOWED_ORIGINS=https://your-domain.com,https://www.your-domain.com
```

### 2. 前端配置 (frontend/.env.production)

```bash
# API地址 - 指向生产环境后端
VITE_API_BASE_URL=https://api.your-domain.com
```

## 📋 部署步骤

### Step 1: 服务器准备
- [ ] 安装Python 3.10+
- [ ] 安装Node.js 18+
- [ ] 安装PostgreSQL 14+
- [ ] 安装Nginx
- [ ] 配置防火墙(开放80, 443端口)
- [ ] 配置SSL证书(Let's Encrypt推荐)

### Step 2: 数据库准备
```bash
# 创建生产数据库
createdb tcm_production

# 配置数据库用户和权限
psql -c "CREATE USER tcm_user WITH PASSWORD 'strong_password';"
psql -c "GRANT ALL PRIVILEGES ON DATABASE tcm_production TO tcm_user;"
```

### Step 3: 后端部署
```bash
cd backend

# 安装依赖
pip install -r requirements.txt

# 执行数据库迁移
alembic upgrade head

# 初始化数据
python scripts/seed_data.py

# 创建管理员账号
python scripts/create_admin.py

# 使用Gunicorn启动(推荐)
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8001
```

### Step 4: 前端部署
```bash
cd frontend

# 安装依赖
npm install

# 生产构建
npm run build

# 将dist目录部署到Nginx
cp -r dist /var/www/html/tcm-frontend
```

### Step 5: Nginx配置
```nginx
# 前端
server {
    listen 80;
    server_name your-domain.com;
    
    # 自动跳转HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    root /var/www/html/tcm-frontend;
    index index.html;
    
    # 前端路由
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    # API代理
    location /api/ {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # 静态文件
    location /uploads/ {
        alias /path/to/backend/uploads/;
    }
}
```

### Step 6: 进程管理(使用systemd)

创建服务文件: `/etc/systemd/system/tcm-backend.service`

```ini
[Unit]
Description=TCM Backend Service
After=network.target

[Service]
Type=notify
User=www-data
WorkingDirectory=/path/to/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 127.0.0.1:8001
Restart=always

[Install]
WantedBy=multi-user.target
```

启动服务:
```bash
systemctl daemon-reload
systemctl enable tcm-backend
systemctl start tcm-backend
systemctl status tcm-backend
```

## 🔒 安全检查清单

- [ ] 修改了默认的SECRET_KEY
- [ ] 使用了强密码
- [ ] 配置了HTTPS
- [ ] 限制了CORS允许的域名
- [ ] 关闭了DEBUG模式
- [ ] 配置了防火墙
- [ ] 定期备份数据库
- [ ] 设置了日志轮转
- [ ] 微信支付使用生产模式和真实密钥
- [ ] 微信支付回调URL是HTTPS公网地址

## 📊 监控和维护

### 日志位置
- 后端日志: `/var/log/tcm/backend.log`
- Nginx日志: `/var/log/nginx/`

### 数据库备份
```bash
# 每日自动备份
0 2 * * * pg_dump tcm_production > /backup/tcm_$(date +\%Y\%m\%d).sql
```

### 健康检查
```bash
# 检查后端API
curl https://your-domain.com/api/health/detailed

# 检查前端
curl https://your-domain.com

# 检查微信支付配置
curl https://your-domain.com/api/wechat-pay/config
```

## ⚡ 性能优化建议

1. **数据库优化**
   - 为常用字段添加索引
   - 定期VACUUM清理
   - 配置连接池

2. **静态文件**
   - 启用Nginx gzip压缩
   - 配置浏览器缓存
   - 使用CDN加速

3. **应用层**
   - 使用Redis缓存
   - 启用数据库查询缓存
   - 优化API响应时间

## 🆘 故障排查

### 常见问题
1. **支付回调失败**
   - 检查WECHAT_NOTIFY_URL是否正确
   - 确认是HTTPS且公网可访问
   - 查看后端日志

2. **前端无法连接后端**
   - 检查Nginx配置
   - 确认CORS设置
   - 检查防火墙

3. **数据库连接失败**
   - 检查DATABASE_URL配置
   - 确认PostgreSQL运行状态
   - 检查连接数限制

## 📞 技术支持
- 微信支付文档: https://pay.weixin.qq.com/wiki/doc/apiv3/
- FastAPI文档: https://fastapi.tiangolo.com/
- Vue 3文档: https://vuejs.org/
