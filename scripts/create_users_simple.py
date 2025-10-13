"""
简单版本创建测试用户
"""
import sqlite3
import bcrypt
from datetime import datetime

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def create_test_users():
    conn = sqlite3.connect('tcm_backend.db')
    cursor = conn.cursor()
    
    # 测试用户数据
    test_users = [
        ('user001', 'user001@tcm.com', 'user123', 'USER', '普通用户001'),
        ('vip001', 'vip001@tcm.com', 'vip123', 'VIP', 'VIP用户001'), 
        ('doctor001', 'doctor001@tcm.com', 'doctor123', 'DOCTOR', '医生用户001'),
        ('operator001', 'operator001@tcm.com', 'operator123', 'USER', '运营人员001')
    ]
    
    print("开始创建测试用户...")
    
    for username, email, password, role, full_name in test_users:
        try:
            # 检查是否存在
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                print(f"用户 {username} 已存在")
                continue
            
            # 创建用户
            hashed_pwd = hash_password(password)
            cursor.execute("""
                INSERT INTO users (
                    username, email, hashed_password, full_name, role, 
                    status, is_active, is_verified, created_at
                ) VALUES (?, ?, ?, ?, ?, 'ACTIVE', 1, 1, datetime('now'))
            """, (username, email, hashed_pwd, full_name, role))
            
            print(f"创建用户成功: {username} ({role})")
            
        except Exception as e:
            print(f"创建用户失败 {username}: {e}")
    
    conn.commit()
    
    # 显示所有用户
    print("\n所有用户列表:")
    cursor.execute("SELECT username, email, role FROM users")
    for user in cursor.fetchall():
        print(f"{user[0]} | {user[1]} | {user[2]}")
    
    conn.close()
    print("\n用户创建完成!")

if __name__ == "__main__":
    create_test_users()