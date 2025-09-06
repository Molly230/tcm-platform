# 中医健康服务平台 - 部署指南

## 快速部署

### 一键部署
```bash
# 克隆项目并进入目录
cd tcm-platform

# 执行一键部署
./deploy.sh
```

## 详细部署流程

### 1. 环境要求

**系统要求:**
- Linux/macOS/Windows (推荐 Ubuntu 20.04+)
- 至少 4GB RAM
- 至少 20GB 磁盘空间

**软件要求:**
- Docker 20.10+
- Docker Compose 2.0+
- Git

### 2. 获取代码
```bash
git clone <repository-url>
cd tcm-platform
```

### 3. 配置环境变量
```bash
# 复制环境变量模板
cp .env.example .env

# 编辑配置文件
nano .env
```

**必须配置的参数:**
```bash
# 数据库密码
DB_PASSWORD=your_secure_db_password

# JWT密钥（生成强密码）
SECRET_KEY=your-super-secret-key-change-in-production

# 支付配置
ALIPAY_APP_ID=your_alipay_app_id
ALIPAY_PRIVATE_KEY=your_alipay_private_key
ALIPAY_PUBLIC_KEY=your_alipay_public_key

WECHAT_APP_ID=your_wechat_app_id  
WECHAT_MCH_ID=your_wechat_mch_id
WECHAT_API_KEY=your_wechat_api_key

# 服务器地址
SERVER_HOST=https://your-domain.com
```

### 4. 生成SSL证书

**开发环境（自签名证书）:**
```bash
./scripts/generate_ssl.sh
```

**生产环境（Let's Encrypt）:**
```bash
# 安装 certbot
sudo apt-get install certbot

# 获取证书
sudo certbot certonly --standalone -d your-domain.com

# 复制证书到项目目录
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ssl/key.pem
```

### 5. 启动服务
```bash
# 完整部署
./deploy.sh deploy

# 或者使用 Docker Compose
docker-compose up -d
```

### 6. 初始化数据
```bash
# 运行生产环境初始化脚本
python scripts/init_production.py
```

## 服务管理

### 基本命令
```bash
# 启动服务
./deploy.sh start

# 停止服务
./deploy.sh stop

# 重启服务
./deploy.sh restart

# 查看日志
./deploy.sh logs

# 查看状态
./deploy.sh status

# 更新部署
./deploy.sh update
```

### Docker Compose 命令
```bash
# 查看服务状态
docker-compose ps

# 查看实时日志
docker-compose logs -f

# 单独重启服务
docker-compose restart backend
docker-compose restart frontend
docker-compose restart nginx

# 进入容器
docker-compose exec backend bash
docker-compose exec db psql -U tcm_user -d tcm_platform
```

## 数据管理

### 备份数据
```bash
# 手动备份
./scripts/backup.sh

# 查看备份文件
ls -la backups/

# 备份日志
tail -f logs/backup.log
```

### 恢复数据
```bash
# 查看可用备份
./scripts/restore.sh

# 恢复指定备份
./scripts/restore.sh 20241201_120000
```

### 定时备份
```bash
# 设置定时任务
./scripts/setup_cron.sh

# 查看定时任务
crontab -l
```

## 监控和日志

### 系统监控
```bash
# 单次监控检查
python scripts/monitor.py

# 守护进程监控
python scripts/monitor.py --daemon
```

### 日志文件位置
```
logs/
├── app.log              # 应用日志
├── error.log            # 错误日志  
├── database.log         # 数据库日志
├── payment.log          # 支付日志
├── security.log         # 安全日志
├── nginx/               # Nginx日志
│   ├── access.log
│   └── error.log
└── monitor.log          # 监控日志
```

## 性能优化

### 1. 数据库优化
```sql
-- 创建索引
CREATE INDEX idx_orders_user_id ON orders(user_id);
CREATE INDEX idx_products_category ON products(category);
CREATE INDEX idx_consultations_status ON consultations(status);
```

### 2. 缓存配置
```bash
# Redis 缓存已在 docker-compose.yml 中配置
# 可以通过环境变量调整缓存策略
```

### 3. 文件服务优化
```bash
# 配置 CDN 加速静态文件
# 在 nginx 配置中添加缓存头
```

## 安全配置

### 1. 防火墙设置
```bash
# 只开放必要端口
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable
```

### 2. SSL/TLS 配置
- 使用强加密套件
- 启用 HSTS
- 定期更新证书

### 3. 应用安全
- 定期更新依赖
- 使用强密码
- 限制 API 请求频率
- 监控异常访问

## 域名配置

### 1. DNS 设置
```
A    @            your-server-ip
A    www          your-server-ip
```

### 2. Nginx 配置
修改 `nginx/conf.d/default.conf` 中的 `server_name`:
```nginx
server_name your-domain.com www.your-domain.com;
```

## 故障排除

### 常见问题

**1. 服务无法启动**
```bash
# 检查端口占用
sudo netstat -tlnp | grep :80
sudo netstat -tlnp | grep :443

# 检查 Docker 状态
docker-compose ps
docker-compose logs backend
```

**2. 数据库连接失败**
```bash
# 检查数据库状态
docker-compose exec db pg_isready -U tcm_user

# 查看数据库日志
docker-compose logs db
```

**3. SSL 证书问题**
```bash
# 检查证书文件
ls -la ssl/
openssl x509 -in ssl/cert.pem -text -noout
```

**4. 支付功能异常**
- 检查支付配置参数
- 查看支付日志
- 验证回调地址

### 调试模式
```bash
# 开启调试模式
echo "DEBUG=true" >> .env
docker-compose restart backend

# 查看详细日志
docker-compose logs -f backend
```

## 升级指南

### 1. 准备升级
```bash
# 备份数据
./scripts/backup.sh

# 备份配置
cp .env .env.backup
cp -r ssl ssl.backup
```

### 2. 执行升级
```bash
# 拉取最新代码
git pull origin main

# 更新部署
./deploy.sh update
```

### 3. 验证升级
```bash
# 检查服务状态
./deploy.sh status

# 执行健康检查
curl http://localhost:8000/api/health
```

## 扩展部署

### 负载均衡
```yaml
# docker-compose.yml 示例
nginx:
  image: nginx:alpine
  depends_on:
    - backend-1
    - backend-2
```

### 高可用数据库
```yaml
# PostgreSQL 主从配置
db-master:
  image: postgres:15
  
db-slave:
  image: postgres:15
  environment:
    POSTGRES_MASTER_SERVICE: db-master
```

## 联系支持

如果遇到部署问题，请：
1. 查看日志文件
2. 检查配置文件
3. 参考故障排除部分
4. 提交 Issue 到项目仓库