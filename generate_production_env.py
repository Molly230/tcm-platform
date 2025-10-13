#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成生产环境.env配置文件
"""
import secrets
import string
from pathlib import Path

def generate_secret_key():
    """生成强随机SECRET_KEY"""
    return secrets.token_hex(32)

def generate_postgres_password():
    """生成强随机PostgreSQL密码"""
    # 包含大小写字母、数字、特殊符号
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    # 去掉容易混淆的字符
    chars = chars.replace('l', '').replace('1', '').replace('I', '')
    chars = chars.replace('0', '').replace('O', '').replace('o', '')

    password = ''.join(secrets.choice(chars) for _ in range(24))
    return password

def create_production_env():
    """创建生产环境.env文件"""

    print("=" * 60)
    print("  生产环境配置生成器")
    print("=" * 60)
    print()

    # 生成密钥
    secret_key = generate_secret_key()
    postgres_password = generate_postgres_password()

    print("✅ 已生成强随机SECRET_KEY")
    print("✅ 已生成PostgreSQL密码")
    print()

    # 询问用户信息
    print("请输入以下信息（如果不确定，可以稍后修改.env.production文件）：")
    print()

    domain = input("域名（例如：tcmlife.top）: ").strip() or "tcmlife.top"
    pg_user = input("PostgreSQL用户名（默认：tcm_user）: ").strip() or "tcm_user"
    pg_database = input("PostgreSQL数据库名（默认：tcm_production）: ").strip() or "tcm_production"

    # 微信支付配置（从现有.env读取）
    current_env = Path("backend/.env")
    wechat_app_id = "wx8ef971d8efa87ffb"
    wechat_mch_id = "1727330435"
    wechat_api_key = "50f96b28cbce26aaaf1e9fd1f5aebbe2"

    if current_env.exists():
        with open(current_env, 'r', encoding='utf-8') as f:
            for line in f:
                if line.startswith('WECHAT_APP_ID='):
                    wechat_app_id = line.split('=')[1].strip()
                elif line.startswith('WECHAT_MCH_ID='):
                    wechat_mch_id = line.split('=')[1].strip()
                elif line.startswith('WECHAT_API_KEY='):
                    wechat_api_key = line.split('=')[1].strip()

    print()
    print("=" * 60)

    # 生成后端.env.production
    backend_env = f"""# 生产环境配置 - 阿里云部署
# 生成时间: {Path(__file__).stat().st_mtime}

# ================================
# 安全配置（必改）
# ================================
SECRET_KEY={secret_key}
DEBUG=false

# ================================
# 数据库配置
# ================================
# PostgreSQL连接字符串
DATABASE_URL=postgresql://{pg_user}:{postgres_password}@localhost:5432/{pg_database}

# ================================
# 微信支付配置
# ================================
WECHAT_APP_ID={wechat_app_id}
WECHAT_MCH_ID={wechat_mch_id}
WECHAT_API_KEY={wechat_api_key}
WECHAT_NOTIFY_URL=https://{domain}/api/wechat-pay/notify
WECHAT_H5_DOMAIN={domain}
WECHAT_PAYMENT_TYPE=JSAPI

# 生产环境使用真实支付
WECHAT_MOCK_MODE=false

# ================================
# 支付宝配置（可选）
# ================================
ALIPAY_APP_ID=请填写你的支付宝AppID
ALIPAY_PRIVATE_KEY=请填写你的支付宝私钥
ALIPAY_PUBLIC_KEY=请填写你的支付宝公钥

# ================================
# CORS配置
# ================================
ALLOWED_ORIGINS=https://{domain},https://www.{domain}
CORS_ORIGINS=https://{domain}

# ================================
# 文件上传配置
# ================================
UPLOAD_DIR=/home/www/tcm-project/backend/uploads

# ================================
# 日志配置
# ================================
LOG_LEVEL=INFO
LOG_FILE=/var/log/tcm/backend.log

# ================================
# OSS配置（可选，如使用阿里云OSS）
# ================================
# OSS_ENABLE=true
# OSS_ACCESS_KEY_ID=你的AccessKeyId
# OSS_ACCESS_KEY_SECRET=你的AccessKeySecret
# OSS_BUCKET_NAME=tcm-uploads
# OSS_ENDPOINT=oss-cn-shanghai.aliyuncs.com
"""

    # 生成前端.env.production
    frontend_env = f"""# 前端生产环境配置
VITE_API_BASE_URL=https://{domain}
"""

    # 保存文件
    backend_env_path = Path("backend/.env.production")
    frontend_env_path = Path("frontend/.env.production")

    with open(backend_env_path, 'w', encoding='utf-8') as f:
        f.write(backend_env)

    with open(frontend_env_path, 'w', encoding='utf-8') as f:
        f.write(frontend_env)

    # 生成PostgreSQL创建脚本
    postgres_script = f"""-- PostgreSQL数据库和用户创建脚本
-- 在阿里云服务器上以postgres用户执行

-- 创建用户
CREATE USER {pg_user} WITH PASSWORD '{postgres_password}';

-- 创建数据库
CREATE DATABASE {pg_database} OWNER {pg_user} ENCODING 'UTF8';

-- 授权
GRANT ALL PRIVILEGES ON DATABASE {pg_database} TO {pg_user};

-- 切换到新数据库并授权schema
\\c {pg_database}
GRANT ALL ON SCHEMA public TO {pg_user};

-- 查看用户
\\du

-- 查看数据库
\\l
"""

    postgres_script_path = Path("backend/create_postgres_production.sql")
    with open(postgres_script_path, 'w', encoding='utf-8') as f:
        f.write(postgres_script)

    print()
    print("✅ 生产环境配置文件已生成：")
    print(f"   📄 {backend_env_path}")
    print(f"   📄 {frontend_env_path}")
    print(f"   📄 {postgres_script_path}")
    print()
    print("=" * 60)
    print("📋 重要信息（请妥善保管）：")
    print("=" * 60)
    print()
    print(f"域名: {domain}")
    print(f"PostgreSQL用户: {pg_user}")
    print(f"PostgreSQL数据库: {pg_database}")
    print(f"PostgreSQL密码: {postgres_password}")
    print()
    print("⚠️  密码已保存到 .env.production 文件中")
    print()
    print("=" * 60)
    print("📝 下一步操作：")
    print("=" * 60)
    print()
    print("1. 将 backend/.env.production 上传到服务器并重命名为 .env")
    print("2. 在服务器上执行 create_postgres_production.sql 创建数据库")
    print("3. 执行数据库迁移：alembic upgrade head")
    print("4. 初始化数据：python scripts/seed_data.py")
    print()

    # 保存密码到单独文件
    credentials_path = Path("deployment_credentials.txt")
    with open(credentials_path, 'w', encoding='utf-8') as f:
        f.write(f"""阿里云部署凭证
生成时间: {Path(__file__).stat().st_mtime}

域名: {domain}
PostgreSQL用户: {pg_user}
PostgreSQL数据库: {pg_database}
PostgreSQL密码: {postgres_password}

SECRET_KEY: {secret_key}

⚠️  请妥善保管此文件，不要提交到Git仓库！
""")

    print(f"🔐 凭证信息已保存到: {credentials_path}")
    print()
    print("⚠️  注意：请不要将 .env.production 和 deployment_credentials.txt 提交到Git！")
    print()

if __name__ == "__main__":
    create_production_env()
