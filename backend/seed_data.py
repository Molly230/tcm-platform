#!/usr/bin/env python3
"""
创建测试数据
"""
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import get_db, engine
from app import models
from app.core.security import get_password_hash
import json
from datetime import datetime, timedelta
import uuid

def create_test_data():
    """创建测试数据"""
    db = next(get_db())
    
    try:
        print("Creating test data...")
        
        # 1. 创建管理员用户
        admin = models.User(
            email="admin@tcm.com",
            username="admin",
            hashed_password=get_password_hash("admin123"),
            full_name="系统管理员",
            role=models.UserRole.ADMIN,
            status=models.UserStatus.ACTIVE,
            is_active=True,
            is_verified=True,
            is_admin=True
        )
        db.add(admin)
        
        # 2. 创建普通用户
        user1 = models.User(
            email="user1@example.com",
            username="user1",
            hashed_password=get_password_hash("123456"),
            full_name="张三",
            role=models.UserRole.USER,
            status=models.UserStatus.ACTIVE,
            is_active=True
        )
        db.add(user1)
        
        # 3. 创建专家用户
        expert_user = models.User(
            email="doctor@tcm.com", 
            username="doctor",
            hashed_password=get_password_hash("doctor123"),
            full_name="李医师",
            role=models.UserRole.DOCTOR,
            status=models.UserStatus.ACTIVE,
            is_active=True,
            is_verified=True
        )
        db.add(expert_user)
        
        db.flush()  # 获取用户ID
        
        # 4. 创建专家信息
        expert1 = models.Expert(
            name="张中医",
            title="主任医师",
            level=models.ExpertLevel.CHIEF,
            category=models.ExpertCategory.INTERNAL,
            description="从事中医内科临床工作25年，擅长治疗消化系统疾病、呼吸系统疾病及慢性疲劳综合征。",
            specialties=json.dumps(["消化系统疾病", "呼吸系统疾病", "慢性疲劳"]),
            qualifications=json.dumps(["执业医师证", "主任医师证", "中医师承证书"]),
            education="北京中医药大学 中医学博士",
            experience_years=25,
            hospital_affiliation="北京中医医院",
            department="内科",
            services_offered=json.dumps(["text", "voice", "video"]),
            working_hours=json.dumps({
                "monday": ["09:00-12:00", "14:00-17:00"],
                "tuesday": ["09:00-12:00", "14:00-17:00"],
                "wednesday": ["09:00-12:00"],
                "thursday": ["09:00-12:00", "14:00-17:00"],
                "friday": ["09:00-12:00", "14:00-17:00"]
            }),
            text_price=80.0,
            voice_price=150.0,
            video_price=300.0,
            rating=4.8,
            consultation_count=1250,
            total_rating_count=856,
            response_time=15,
            status=models.ExpertStatus.ACTIVE,
            is_active=True,
            is_verified=True,
            is_featured=True,
            phone="13800138001",
            email="zhangdoctor@hospital.com",
            personal_statement="以患者为中心，用心治疗每一位病人",
            treatment_philosophy="中西医结合，标本兼治"
        )
        db.add(expert1)
        
        expert2 = models.Expert(
            name="李妇科",
            title="副主任医师", 
            level=models.ExpertLevel.SENIOR,
            category=models.ExpertCategory.GYNECOLOGY,
            description="专注妇科疾病治疗18年，对月经不调、不孕不育、妇科炎症有丰富临床经验。",
            specialties=json.dumps(["月经不调", "不孕不育", "妇科炎症", "更年期综合征"]),
            qualifications=json.dumps(["执业医师证", "副主任医师证"]),
            education="上海中医药大学 中医妇科学硕士",
            experience_years=18,
            hospital_affiliation="上海妇幼保健院",
            department="中医妇科",
            services_offered=json.dumps(["text", "voice", "video"]),
            text_price=100.0,
            voice_price=200.0,
            video_price=400.0,
            rating=4.9,
            consultation_count=980,
            total_rating_count=654,
            response_time=20,
            status=models.ExpertStatus.ACTIVE,
            is_active=True,
            is_verified=True,
            is_featured=True
        )
        db.add(expert2)
        
        # 5. 创建商品
        products_data = [
            {
                "name": "野生黑枸杞",
                "description": "来自青海的野生黑枸杞，富含花青素，具有抗氧化功效。",
                "category": models.ProductCategory.HERBAL_MEDICINE,
                "price": 158.0,
                "original_price": 198.0,
                "discount": 0.8,
                "stock_quantity": 100,
                "images": json.dumps(["/images/products/black-goji.jpg"]),
                "specifications": json.dumps({"weight": "500g", "origin": "青海"}),
                "features": json.dumps(["抗氧化", "明目", "补肾"]),
                "is_featured": True,
                "sales_count": 156,
                "rating": 4.8,
                "review_count": 89
            },
            {
                "name": "陈皮普洱茶", 
                "description": "精选新会陈皮配云南普洱，理气健脾，降脂消食。",
                "category": models.ProductCategory.HEALTH_PRODUCTS,
                "price": 88.0,
                "stock_quantity": 200,
                "images": json.dumps(["/images/products/chenpi-tea.jpg"]),
                "specifications": json.dumps({"weight": "250g", "origin": "广东新会"}),
                "features": json.dumps(["理气健脾", "降脂", "消食"]),
                "sales_count": 234,
                "rating": 4.7,
                "review_count": 123
            },
            {
                "name": "艾灸盒套装",
                "description": "纯铜艾灸盒，配优质艾条，适合家庭养生使用。",
                "category": models.ProductCategory.MEDICAL_EQUIPMENT,
                "price": 129.0,
                "original_price": 168.0,
                "discount": 0.77,
                "stock_quantity": 50,
                "images": json.dumps(["/images/products/moxibustion-box.jpg"]),
                "specifications": json.dumps({"material": "纯铜", "size": "大号"}),
                "features": json.dumps(["温经散寒", "扶阳固脱", "家用便携"]),
                "sales_count": 67,
                "rating": 4.6,
                "review_count": 45
            }
        ]
        
        for product_data in products_data:
            product = models.Product(**product_data)
            db.add(product)
        
        # 6. 创建课程
        course1 = models.Course(
            title="中医基础理论精讲",
            description="系统学习中医基础理论，包括阴阳五行、脏腑经络、气血津液等核心概念。",
            category="basic",
            duration="20课时",
            price=199.0,
            instructor="王教授",
            is_published=True,
            total_lessons=20,
            total_duration=1200  # 20小时
        )
        db.add(course1)
        
        course2 = models.Course(
            title="四季养生实用指南",
            description="根据四季变化特点，学习不同季节的养生方法和注意事项。",
            category="seasonal", 
            duration="12课时",
            price=99.0,
            instructor="李医师",
            is_published=True,
            total_lessons=12,
            total_duration=720  # 12小时
        )
        db.add(course2)
        
        db.flush()  # 获取对象ID
        
        # 7. 创建咨询记录
        consultation = models.Consultation(
            consultation_number=f"C{datetime.now().strftime('%Y%m%d')}{uuid.uuid4().hex[:8].upper()}",
            user_id=user1.id,
            expert_id=expert1.id,
            type=models.ConsultationType.TEXT,
            status=models.ConsultationStatus.COMPLETED,
            title="消化不良咨询",
            symptoms="最近总是消化不良，胃胀气，食欲不振",
            duration="3天",
            medical_history="有轻微胃炎史",
            expert_diagnosis="脾胃虚弱，消化功能减退",
            expert_recommendations="建议调理脾胃，注意饮食规律，可配合中药调理",
            price=80.0,
            payment_status=models.PaymentStatus.PAID,
            user_rating=4.8,
            user_feedback="医生很专业，建议很有效",
            started_at=datetime.now() - timedelta(days=2),
            completed_at=datetime.now() - timedelta(days=1),
            consultation_duration=45
        )
        db.add(consultation)
        
        db.commit()
        print("✅ Test data created successfully!")
        
        # 显示创建的数据统计
        print(f"Users: {db.query(models.User).count()}")
        print(f"Experts: {db.query(models.Expert).count()}")
        print(f"Products: {db.query(models.Product).count()}")
        print(f"Courses: {db.query(models.Course).count()}")
        print(f"Consultations: {db.query(models.Consultation).count()}")
        
    except Exception as e:
        print(f"❌ Error creating test data: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_test_data()