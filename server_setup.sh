#!/bin/bash
# ========================================
# 阿里云服务器一键配置脚本 (Ubuntu 22.04)
# ========================================

set -e  # 遇到错误立即停止

echo "========================================"
echo "  阿里云服务器环境配置脚本"
echo "  系统: Ubuntu 22.04 LTS"
echo "========================================"
echo ""

# 颜色定义
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# 打印函数
print_info() {
    echo -e "${GREEN}[信息]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[警告]${NC} $1"
}

print_error() {
    echo -e "${RED}[错误]${NC} $1"
}

# 检查是否为root用户
if [ "$EUID" -ne 0 ]; then
    print_error "请使用root用户执行此脚本"
    exit 1
fi

# ========================================
# 1. 更新系统
# ========================================
print_info "步骤 1/10: 更新系统软件包..."
apt update -y
apt upgrade -y
print_info "✅ 系统更新完成"
echo ""

# ========================================
# 2. 安装基础工具
# ========================================
print_info "步骤 2/10: 安装基础工具..."
apt install -y \
    git \
    curl \
    wget \
    vim \
    unzip \
    build-essential \
    software-properties-common \
    apt-transport-https \
    ca-certificates \
    gnupg \
    lsb-release
print_info "✅ 基础工具安装完成"
echo ""

# ========================================
# 3. 安装Python 3.11
# ========================================
print_info "步骤 3/10: 安装Python 3.11..."
add-apt-repository -y ppa:deadsnakes/ppa
apt update -y
apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
# 设置python3.11为默认python3
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.11 1
print_info "✅ Python 3.11 安装完成"
python3 --version
echo ""

# ========================================
# 4. 安装Node.js 18
# ========================================
print_info "步骤 4/10: 安装Node.js 18..."
curl -fsSL https://deb.nodesource.com/setup_18.x | bash -
apt install -y nodejs
print_info "✅ Node.js 安装完成"
node --version
npm --version
echo ""

# ========================================
# 5. 安装PostgreSQL 14
# ========================================
print_info "步骤 5/10: 安装PostgreSQL 14..."
apt install -y postgresql postgresql-contrib
# 启动PostgreSQL服务
systemctl start postgresql
systemctl enable postgresql
print_info "✅ PostgreSQL 14 安装完成"
sudo -u postgres psql --version
echo ""

# ========================================
# 6. 安装Nginx
# ========================================
print_info "步骤 6/10: 安装Nginx..."
apt install -y nginx
systemctl start nginx
systemctl enable nginx
print_info "✅ Nginx 安装完成"
nginx -v
echo ""

# ========================================
# 7. 安装SSL证书工具 (Certbot)
# ========================================
print_info "步骤 7/10: 安装SSL证书工具..."
apt install -y certbot python3-certbot-nginx
print_info "✅ Certbot 安装完成"
certbot --version
echo ""

# ========================================
# 8. 配置防火墙
# ========================================
print_info "步骤 8/10: 配置防火墙..."
apt install -y ufw
ufw --force enable
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw status
print_info "✅ 防火墙配置完成"
echo ""

# ========================================
# 9. 创建部署用户
# ========================================
print_info "步骤 9/10: 创建部署用户 www..."
if id "www" &>/dev/null; then
    print_warning "用户 www 已存在，跳过创建"
else
    useradd -m -s /bin/bash www
    usermod -aG sudo www
    print_info "✅ 用户 www 创建完成"
fi
echo ""

# ========================================
# 10. 创建项目目录
# ========================================
print_info "步骤 10/10: 创建项目目录..."
mkdir -p /home/www/tcm-project
mkdir -p /var/log/tcm
chown -R www:www /home/www/tcm-project
chown -R www:www /var/log/tcm
print_info "✅ 项目目录创建完成"
echo ""

# ========================================
# 配置完成
# ========================================
echo "========================================"
echo "  ✅ 服务器环境配置完成！"
echo "========================================"
echo ""
echo "📋 已安装的软件版本："
echo "  - Python: $(python3 --version)"
echo "  - Node.js: $(node --version)"
echo "  - npm: $(npm --version)"
echo "  - PostgreSQL: $(sudo -u postgres psql --version | head -1)"
echo "  - Nginx: $(nginx -v 2>&1)"
echo ""
echo "📁 项目目录："
echo "  - /home/www/tcm-project (代码上传到这里)"
echo "  - /var/log/tcm (日志文件)"
echo ""
echo "🔧 下一步操作："
echo "  1. 上传代码到 /home/www/tcm-project"
echo "  2. 创建PostgreSQL数据库"
echo "  3. 配置Nginx"
echo "  4. 申请SSL证书"
echo ""
print_warning "建议重启服务器以确保所有配置生效："
echo "  reboot"
echo ""
