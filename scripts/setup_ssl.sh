#!/bin/bash
# SSL证书配置脚本

DOMAIN="tcmlife.top"
SSL_DIR="/var/www/tcm-platform/ssl"
EMAIL="admin@tcmlife.top"

echo "=== 中医健康平台 SSL证书配置 ==="

# 创建SSL目录
mkdir -p $SSL_DIR

# 检查是否为生产环境
if [ "$1" = "production" ]; then
    echo "生产环境 - 申请Let's Encrypt证书"
    
    # 安装certbot
    if ! command -v certbot &> /dev/null; then
        echo "安装Certbot..."
        apt-get update
        apt-get install -y certbot
    fi
    
    # 停止nginx避免端口冲突
    docker-compose stop nginx || true
    
    # 申请证书
    echo "为域名 $DOMAIN 申请SSL证书..."
    certbot certonly --standalone \
        -d $DOMAIN \
        -d www.$DOMAIN \
        --email $EMAIL \
        --agree-tos \
        --non-interactive
    
    # 复制证书到项目目录
    cp /etc/letsencrypt/live/$DOMAIN/fullchain.pem $SSL_DIR/cert.pem
    cp /etc/letsencrypt/live/$DOMAIN/privkey.pem $SSL_DIR/key.pem
    
    # 设置权限
    chown -R www-data:www-data $SSL_DIR
    chmod 600 $SSL_DIR/key.pem
    chmod 644 $SSL_DIR/cert.pem
    
    # 设置自动续期
    echo "设置证书自动续期..."
    (crontab -l 2>/dev/null; echo "0 2 * * 0 certbot renew --quiet --post-hook 'docker-compose restart nginx'") | crontab -
    
    echo "✅ 生产SSL证书配置完成"
    
else
    echo "开发环境 - 生成自签名证书"
    
    # 生成自签名证书
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout $SSL_DIR/key.pem \
        -out $SSL_DIR/cert.pem \
        -subj "/C=CN/ST=Beijing/L=Beijing/O=TCM Platform/CN=localhost"
    
    # 设置权限
    chmod 600 $SSL_DIR/key.pem
    chmod 644 $SSL_DIR/cert.pem
    
    echo "✅ 开发SSL证书生成完成"
fi

echo "SSL证书文件位置："
echo "  证书文件: $SSL_DIR/cert.pem"
echo "  私钥文件: $SSL_DIR/key.pem"

# 验证证书
if openssl x509 -in $SSL_DIR/cert.pem -text -noout > /dev/null 2>&1; then
    echo "✅ 证书验证通过"
    
    # 显示证书信息
    echo "证书信息："
    openssl x509 -in $SSL_DIR/cert.pem -noout -subject -dates
else
    echo "❌ 证书验证失败"
    exit 1
fi