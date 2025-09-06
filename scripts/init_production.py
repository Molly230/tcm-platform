#!/usr/bin/env python3
"""
生产环境初始化脚本
"""
import os
import sys
import subprocess
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "backend"))

def run_command(cmd, cwd=None):
    """执行系统命令"""
    print(f"执行: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    
    if result.returncode != 0:
        print(f"错误: {result.stderr}")
        return False
    
    if result.stdout:
        print(result.stdout)
    return True

def init_database():
    """初始化数据库"""
    print("=== 初始化数据库 ===")
    
    backend_dir = project_root / "backend"
    
    # 运行数据库迁移
    if not run_command("alembic upgrade head", cwd=backend_dir):
        return False
    
    # 创建管理员账户
    if not run_command("python create_admin.py", cwd=backend_dir):
        print("警告: 管理员账户创建失败或已存在")
    
    # 初始化基础数据
    if not run_command("python seed_data.py", cwd=backend_dir):
        print("警告: 基础数据初始化失败")
    
    return True

def setup_directories():
    """创建必需的目录"""
    print("=== 创建目录结构 ===")
    
    directories = [
        "backend/uploads/videos",
        "backend/uploads/images", 
        "logs/nginx",
        "logs/backend",
        "backups",
        "ssl"
    ]
    
    for dir_path in directories:
        full_path = project_root / dir_path
        full_path.mkdir(parents=True, exist_ok=True)
        print(f"创建目录: {full_path}")

def generate_env_template():
    """生成环境变量模板"""
    print("=== 生成环境变量模板 ===")
    
    env_template = """# 数据库配置
DATABASE_URL=postgresql://tcm_user:your_password@localhost:5432/tcm_platform

# JWT配置
SECRET_KEY=your-super-secret-key-change-in-production

# Redis配置
REDIS_URL=redis://:your_redis_password@localhost:6379/0

# 服务器配置
SERVER_HOST=https://your-domain.com
DEBUG=false

# 支付配置
ALIPAY_APP_ID=your_alipay_app_id
ALIPAY_PRIVATE_KEY=your_alipay_private_key
ALIPAY_PUBLIC_KEY=your_alipay_public_key

WECHAT_APP_ID=your_wechat_app_id
WECHAT_MCH_ID=your_wechat_mch_id
WECHAT_API_KEY=your_wechat_api_key

# 腾讯云配置
TENCENT_SECRET_ID=your_tencent_secret_id
TENCENT_SECRET_KEY=your_tencent_secret_key
TRTC_SDK_APP_ID=your_trtc_app_id
TRTC_KEY=your_trtc_key

# Docker Compose配置
DB_PASSWORD=your_db_password
REDIS_PASSWORD=your_redis_password
"""
    
    env_file = project_root / ".env.example"
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(env_template)
    
    print(f"环境变量模板已生成: {env_file}")
    print("请复制为 .env 文件并填入真实配置")

def main():
    """主函数"""
    print("中医健康服务平台 - 生产环境初始化")
    print("=" * 50)
    
    # 检查是否在项目根目录
    if not (project_root / "docker-compose.yml").exists():
        print("错误: 请在项目根目录运行此脚本")
        return 1
    
    try:
        # 创建目录结构
        setup_directories()
        
        # 生成环境变量模板
        generate_env_template()
        
        # 检查是否存在.env文件
        env_file = project_root / ".env"
        if not env_file.exists():
            print("警告: .env 文件不存在，请根据 .env.example 创建")
            print("数据库初始化将跳过，请配置完成后手动运行")
            return 0
        
        # 初始化数据库
        if init_database():
            print("✅ 生产环境初始化成功!")
        else:
            print("❌ 数据库初始化失败")
            return 1
            
    except Exception as e:
        print(f"错误: {e}")
        return 1
    
    print("\n后续步骤:")
    print("1. 配置 .env 文件中的所有参数")
    print("2. 运行 docker-compose up -d 启动服务")
    print("3. 配置域名和SSL证书")
    print("4. 设置数据备份计划任务")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())