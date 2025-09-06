#!/usr/bin/env python3
"""
创建测试产品数据
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models.product import Product, ProductCategory, ProductStatus

def create_test_products():
    """创建测试产品数据"""
    db = SessionLocal()
    try:
        # 清理现有产品数据
        db.query(Product).delete()
        
        # 创建测试产品
        test_products = [
            {
                "name": "人参片",
                "description": "优质人参制成的片剂，补气养血，增强免疫力",
                "category": ProductCategory.PRODUCT,
                "price": 188.00,
                "original_price": 228.00,
                "stock_quantity": 50,
                "images": ["/images/renshen.jpg"],
                "features": ["补气", "养血", "增强免疫"],
                "usage_instructions": "每日2-3片，温水送服",
                "is_featured": True,
                "is_common": True,  # 常用产品
                "sales_count": 156,
                "rating": 4.8,
                "seo_keywords": "人参,补气,养血,免疫力"
            },
            {
                "name": "枸杞子",
                "description": "宁夏优质枸杞，明目养肝，滋阴补肾",
                "category": ProductCategory.PRODUCT,
                "price": 68.00,
                "original_price": 88.00,
                "stock_quantity": 100,
                "images": ["/images/gouqizi.jpg"],
                "features": ["明目", "养肝", "滋阴补肾"],
                "usage_instructions": "泡茶或直接食用，每日10-15粒",
                "is_featured": False,
                "is_common": True,  # 常用产品
                "sales_count": 234,
                "rating": 4.6,
                "seo_keywords": "枸杞,明目,养肝,滋阴"
            },
            {
                "name": "黄芪丸",
                "description": "传统黄芪制丸，补中益气，提升体力",
                "category": ProductCategory.PRODUCT,
                "price": 128.00,
                "stock_quantity": 75,
                "images": ["/images/huangqi.jpg"],
                "features": ["补中益气", "提升体力", "增强抵抗力"],
                "usage_instructions": "每次6-8丸，每日2次",
                "is_featured": True,
                "is_common": True,  # 常用产品
                "sales_count": 89,
                "rating": 4.7,
                "seo_keywords": "黄芪,补气,体力,抵抗力"
            },
            {
                "name": "当归片",
                "description": "精选当归制片，补血调经，美容养颜",
                "category": ProductCategory.PRODUCT,
                "price": 98.00,
                "stock_quantity": 60,
                "images": ["/images/danggui.jpg"],
                "features": ["补血", "调经", "美容养颜"],
                "usage_instructions": "每日2片，饭后服用",
                "is_featured": False,
                "is_common": False,  # 普通产品
                "sales_count": 67,
                "rating": 4.5,
                "seo_keywords": "当归,补血,调经,美容"
            },
            {
                "name": "灵芝孢子粉",
                "description": "破壁灵芝孢子粉，提高免疫，抗疲劳",
                "category": ProductCategory.PRODUCT,
                "price": 298.00,
                "original_price": 358.00,
                "stock_quantity": 30,
                "images": ["/images/lingzhi.jpg"],
                "features": ["提高免疫", "抗疲劳", "改善睡眠"],
                "usage_instructions": "每日1-2克，温水冲服",
                "is_featured": True,
                "is_common": False,  # 普通产品
                "sales_count": 123,
                "rating": 4.9,
                "seo_keywords": "灵芝,免疫,抗疲劳,睡眠"
            },
            {
                "name": "陈皮茶",
                "description": "陈年陈皮制茶，理气健脾，化痰止咳",
                "category": ProductCategory.PRODUCT,
                "price": 58.00,
                "stock_quantity": 120,
                "images": ["/images/chenpi.jpg"],
                "features": ["理气健脾", "化痰", "止咳"],
                "usage_instructions": "开水冲泡，可反复冲泡3-5次",
                "is_featured": False,
                "is_common": True,  # 常用产品
                "sales_count": 178,
                "rating": 4.4,
                "seo_keywords": "陈皮,理气,健脾,化痰"
            }
        ]
        
        # 插入产品数据
        for product_data in test_products:
            product = Product(**product_data)
            db.add(product)
        
        # 提交到数据库
        db.commit()
        print(f"成功创建 {len(test_products)} 个测试产品")
        print("包含常用产品：人参片、枸杞子、黄芪丸、陈皮茶")
        
    except Exception as e:
        db.rollback()
        print(f"创建测试产品失败: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_products()