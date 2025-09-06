"""
数据库初始化脚本
"""
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import engine, Base, get_db
from app.core.security import get_password_hash

def init_db():
    """初始化数据库"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    
    # 获取数据库会话
    db = next(get_db())
    
    # 创建默认管理员用户
    create_initial_data(db)

def create_initial_data(db: Session):
    """创建初始数据"""
    # 检查是否已存在管理员用户
    user = db.query(models.User).filter(models.User.email == "admin@example.com").first()
    if not user:
        # 创建管理员用户
        admin_user = models.User(
            email="admin@example.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            is_superuser=True
        )
        db.add(admin_user)
        
        # 创建示例专家
        expert1 = models.Expert(
            name="张医师",
            title="主任医师",
            category="internal",
            description="从事中医内科临床工作20年，擅长治疗消化系统疾病和呼吸系统疾病。",
            rating=98.0,
            consultation_count=1200,
            text_price=50.0,
            voice_price=100.0,
            video_price=200.0
        )
        db.add(expert1)
        
        expert2 = models.Expert(
            name="李医师",
            title="副主任医师",
            category="gynecology",
            description="专注于妇科疾病治疗15年，对月经不调、不孕不育等有丰富经验。",
            rating=96.0,
            consultation_count=800,
            text_price=60.0,
            voice_price=120.0,
            video_price=250.0
        )
        db.add(expert2)
        
        # 创建示例课程
        course1 = models.Course(
            title="中医基础理论",
            description="学习中医的基本概念和理论体系",
            category="basic",
            duration="10课时",
            price=99.0,
            is_published=True
        )
        db.add(course1)
        
        course2 = models.Course(
            title="四季养生法",
            description="根据四季变化调整养生方法",
            category="seasonal",
            duration="8课时",
            price=79.0,
            is_published=True
        )
        db.add(course2)
        
        course3 = models.Course(
            title="中医养生入门",
            description="中医养生的基本概念和方法",
            category="basic",
            duration="5课时",
            price=0.0,
            is_free=True,
            is_published=True
        )
        db.add(course3)
        
        db.commit()
        print("初始数据创建成功")
    else:
        print("初始数据已存在")

if __name__ == "__main__":
    init_db()