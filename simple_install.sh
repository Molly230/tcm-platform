#!/bin/bash
# 简化版一键安装脚本
set -e

echo "开始安装环境..."

# 更新系统
echo "[1/10] 更新系统..."
apt update -y && apt upgrade -y

# 安装基础工具
echo "[2/10] 安装基础工具..."
apt install -y git curl wget vim unzip build-essential software-properties-common

# 安装Python 3.11
echo "[3/10] 安装Python 3.11..."
add-apt-repository -y ppa:deadsnakes/ppa
apt update -y
apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1

# 安装Node.js
echo "[4/10] 安装Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs

# 安装PostgreSQL
echo "[5/10] 安装PostgreSQL..."
apt install -y postgresql postgresql-contrib
systemctl start postgresql
systemctl enable postgresql

# 安装Nginx
echo "[6/10] 安装Nginx..."
apt install -y nginx
systemctl start nginx
systemctl enable nginx

# 安装Certbot
echo "[7/10] 安装SSL工具..."
apt install -y certbot python3-certbot-nginx

# 配置防火墙
echo "[8/10] 配置防火墙..."
apt install -y ufw
ufw --force enable
ufw allow 22/tcp
ufw allow 80/tcp
ufw allow 443/tcp

# 创建用户
echo "[9/10] 创建用户..."
if ! id "www" &>/dev/null; then
    useradd -m -s /bin/bash www
    usermod -aG sudo www
fi

# 创建目录
echo "[10/10] 创建目录..."
mkdir -p /home/www/tcm-project
mkdir -p /var/log/tcm
chown -R www:www /home/www/tcm-project
chown -R www:www /var/log/tcm

echo "✅ 安装完成！"
python3 --version
node --version
