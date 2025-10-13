"""
创建默认管理员账户
"""
from app.database import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_admin():
    db = SessionLocal()
    
    try:
        # 检查管理员是否已存在
        existing_admin = db.query(User).filter(User.email == "admin@tcm.com").first()
        
        if existing_admin:
            print("管理员账户已存在")
            return
        
        # 创建管理员账户
        admin_user = User(
            email="admin@tcm.com",
            username="admin",
            hashed_password=pwd_context.hash("admin123"),
            is_admin=True,
            is_super_admin=True,
            is_active=True
        )
        
        db.add(admin_user)
        db.commit()
        
        print("管理员账户创建成功:")
        print(f"邮箱: {admin_user.email}")
        print(f"密码: admin123")
        print(f"管理员权限: {admin_user.is_admin}")
        
    except Exception as e:
        print(f"创建管理员账户失败: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()