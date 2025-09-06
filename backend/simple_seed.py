#!/usr/bin/env python3
"""
简单测试数据创建
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import get_db, engine
from app import models
from app.core.security import get_password_hash
from app.models.user import UserRole, UserStatus
from app.models.expert import ExpertCategory, ExpertLevel, ExpertStatus
from app.models.product import ProductCategory, ProductStatus
from app.models.consultation import ConsultationType, ConsultationStatus, PaymentStatus
import json
from datetime import datetime, timedelta

def create_simple_data():
    """创建简单测试数据"""
    db = next(get_db())
    
    try:
        print("Creating simple test data...")
        
        # 创建管理员用户
        admin = models.User(
            email="admin@tcm.com",
            username="admin", 
            hashed_password=get_password_hash("admin123"),
            full_name="管理员",
            role=UserRole.ADMIN,
            status=UserStatus.ACTIVE,
            is_active=True,
            is_verified=True,
            is_admin=True
        )
        db.add(admin)
        
        # 创建专家
        expert = models.Expert(
            name="张医师",
            title="主任医师",
            category=ExpertCategory.INTERNAL,
            description="中医内科专家",
            text_price=50.0,
            voice_price=100.0, 
            video_price=200.0,
            rating=4.8,
            consultation_count=100,
            status=ExpertStatus.ACTIVE,
            is_active=True
        )
        db.add(expert)
        
        # 创建商品
        product = models.Product(
            name="测试商品",
            description="这是一个测试商品",
            category=ProductCategory.HERBAL_MEDICINE,
            price=99.0,
            stock_quantity=100,
            status=ProductStatus.ACTIVE
        )
        db.add(product)
        
        # 创建课程
        course = models.Course(
            title="测试课程",
            description="这是一个测试课程",
            category="basic",
            duration="10课时",
            price=199.0,
            is_published=True
        )
        db.add(course)
        
        db.commit()
        print("Test data created successfully!")
        
        # 显示统计
        print(f"Users: {db.query(models.User).count()}")
        print(f"Experts: {db.query(models.Expert).count()}")
        print(f"Products: {db.query(models.Product).count()}")
        print(f"Courses: {db.query(models.Course).count()}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    create_simple_data()