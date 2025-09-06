#!/bin/bash
# 生产环境一键配置脚本

set -e  # 遇到错误立即退出

PROJECT_DIR="/var/www/tcm-platform"
BACKUP_DIR="/var/backups/tcm-platform"

echo "=== 中医健康平台生产环境配置 ==="

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    echo "请使用root权限运行此脚本"
    exit 1
fi

# 1. 更新系统
echo "1. 更新系统包..."
apt-get update && apt-get upgrade -y

# 2. 安装必要软件
echo "2. 安装必要软件..."
apt-get install -y curl git nginx certbot python3-certbot-nginx ufw fail2ban

# 3. 安装Docker
if ! command -v docker &> /dev/null; then
    echo "3. 安装Docker..."
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker
    systemctl enable docker
    rm get-docker.sh
else
    echo "3. Docker已安装，跳过"
fi

# 4. 安装Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "4. 安装Docker Compose..."
    curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo "4. Docker Compose已安装，跳过"
fi

# 5. 配置防火墙
echo "5. 配置防火墙..."
ufw --force reset
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 80/tcp
ufw allow 443/tcp
ufw --force enable

# 6. 配置Fail2Ban
echo "6. 配置Fail2Ban..."
cat > /etc/fail2ban/jail.local << 'EOF'
[DEFAULT]
bantime = 3600
findtime = 600
maxretry = 3

[sshd]
enabled = true
port = ssh
logpath = /var/log/auth.log

[nginx-http-auth]
enabled = true
filter = nginx-http-auth
logpath = /var/log/nginx/error.log

[nginx-limit-req]
enabled = true
filter = nginx-limit-req
logpath = /var/log/nginx/error.log
EOF

systemctl restart fail2ban
systemctl enable fail2ban

# 7. 创建项目目录
echo "7. 创建项目目录..."
mkdir -p $PROJECT_DIR
mkdir -p $BACKUP_DIR
mkdir -p /var/log/tcm-platform

# 8. 设置目录权限
echo "8. 设置目录权限..."
chown -R www-data:www-data $PROJECT_DIR
chmod -R 755 $PROJECT_DIR

# 9. 生成强密码
echo "9. 生成配置密钥..."
SECRET_KEY=$(openssl rand -base64 32)
DB_PASSWORD=$(openssl rand -base64 16)
REDIS_PASSWORD=$(openssl rand -base64 16)

# 10. 创建生产环境配置
echo "10. 创建生产环境配置..."
cat > $PROJECT_DIR/.env << EOF
# 生产环境配置 - 自动生成于 $(date)

# 基础配置
DEBUG=false
PROJECT_NAME=中医健康服务平台
PROJECT_VERSION=1.0.0
ENVIRONMENT=production

# 安全配置
SECRET_KEY=$SECRET_KEY
VIDEO_SECRET_KEY=$(openssl rand -base64 32)

# 数据库配置
DATABASE_URL=postgresql://tcm_user:$DB_PASSWORD@db:5432/tcm_platform
DB_PASSWORD=$DB_PASSWORD

# Redis配置
REDIS_URL=redis://:$REDIS_PASSWORD@redis:6379/0
REDIS_PASSWORD=$REDIS_PASSWORD

# 服务器配置
SERVER_HOST=https://tcmlife.top
FRONTEND_URL=https://tcmlife.top
CORS_ORIGINS=https://tcmlife.top,https://www.tcmlife.top

# 文件上传配置
UPLOAD_PATH=/app/uploads
MAX_UPLOAD_SIZE=10485760

# 日志配置
LOG_LEVEL=INFO
LOG_FILE=/app/logs/app.log

# 安全配置
MIN_PASSWORD_LENGTH=8
REQUIRE_SPECIAL_CHARS=true
SESSION_TIMEOUT=3600
MAX_LOGIN_ATTEMPTS=5

# API限流配置
RATE_LIMIT_PER_MINUTE=100
RATE_LIMIT_PER_HOUR=1000

# 监控告警
ALERT_EMAIL=admin@tcmlife.top

# 备份配置
BACKUP_SCHEDULE=0 2 * * *
BACKUP_RETENTION_DAYS=30
BACKUP_STORAGE_PATH=$BACKUP_DIR

# SSL配置
SSL_CERT_PATH=/etc/nginx/ssl/cert.pem
SSL_KEY_PATH=/etc/nginx/ssl/key.pem

# TODO: 请手动配置以下参数
# 腾讯云配置
# TENCENT_SECRET_ID=
# TENCENT_SECRET_KEY=
# TRTC_SDK_APP_ID=
# TRTC_KEY=

# 支付配置
# ALIPAY_APP_ID=
# ALIPAY_PRIVATE_KEY=
# ALIPAY_PUBLIC_KEY=
# WECHAT_APP_ID=
# WECHAT_MCH_ID=
# WECHAT_API_KEY=

# 邮件配置
# SMTP_HOST=
# SMTP_PORT=587
# SMTP_USER=
# SMTP_PASSWORD=
# EMAIL_FROM=noreply@tcmlife.top
EOF

# 11. 设置配置文件权限
chmod 600 $PROJECT_DIR/.env

# 12. 创建备份脚本
echo "12. 创建备份脚本..."
cat > /usr/local/bin/tcm-backup << 'EOF'
#!/bin/bash
BACKUP_DIR="/var/backups/tcm-platform"
DATE=$(date +%Y%m%d_%H%M%S)
PROJECT_DIR="/var/www/tcm-platform"

mkdir -p $BACKUP_DIR

# 备份数据库
docker-compose -f $PROJECT_DIR/docker-compose.yml exec -T db pg_dump -U tcm_user tcm_platform | gzip > $BACKUP_DIR/db_$DATE.sql.gz

# 备份上传文件
tar -czf $BACKUP_DIR/uploads_$DATE.tar.gz -C $PROJECT_DIR backend/uploads/

# 备份配置文件
cp $PROJECT_DIR/.env $BACKUP_DIR/env_$DATE

# 清理30天前的备份
find $BACKUP_DIR -name "*.gz" -mtime +30 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
find $BACKUP_DIR -name "env_*" -mtime +30 -delete

echo "备份完成: $DATE"
EOF

chmod +x /usr/local/bin/tcm-backup

# 13. 设置定时任务
echo "13. 设置定时任务..."
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/tcm-backup") | crontab -

echo ""
echo "🎉 生产环境配置完成！"
echo ""
echo "⚠️  重要提醒："
echo "1. 请编辑 $PROJECT_DIR/.env 文件，配置支付、邮件等参数"
echo "2. 请运行 'cd $PROJECT_DIR && chmod +x scripts/setup_ssl.sh && ./scripts/setup_ssl.sh production' 配置SSL证书"
echo "3. 数据库密码: $DB_PASSWORD"
echo "4. Redis密码: $REDIS_PASSWORD"
echo "5. JWT密钥: $SECRET_KEY"
echo ""
echo "下一步："
echo "1. git clone 你的代码到 $PROJECT_DIR"
echo "2. cd $PROJECT_DIR && docker-compose up -d"
echo "3. ./scripts/setup_ssl.sh production"
echo ""
echo "📝 配置文件位置: $PROJECT_DIR/.env"
echo "📦 备份目录: $BACKUP_DIR"
echo "🔧 备份命令: tcm-backup"