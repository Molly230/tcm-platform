#!/usr/bin/env python3
"""
创建商品测试数据
"""
import sys
import os
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine, SessionLocal, Base
from app.models.product import Product, ProductCategory, ProductStatus

def create_products_data():
    """创建商品测试数据"""
    db = SessionLocal()
    
    try:
        # 确保数据库表存在
        Base.metadata.create_all(bind=engine)
        
        # 中药材商品
        herbal_products = [
            {
                "name": "人参（长白山野山参）",
                "description": "长白山野生人参，具有大补元气、复脉固脱、补脾益肺、生津养血、安神益智等功效。",
                "category": ProductCategory.HERBAL_MEDICINE,
                "price": 388.0,
                "original_price": 450.0,
                "discount": 0.86,
                "stock_quantity": 50,
                "images": [
                    "https://via.placeholder.com/400x300/8FBC8F/FFFFFF?text=人参",
                    "https://via.placeholder.com/400x300/9ACD32/FFFFFF?text=人参细节"
                ],
                "specifications": {"weight": "50g", "origin": "长白山", "grade": "特级"},
                "features": ["大补元气", "生津养血", "安神益智"],
                "usage_instructions": "每次3-5克，煎汤或研末服用",
                "is_featured": True,
                "sales_count": 156,
                "rating": 4.8,
                "review_count": 89
            },
            {
                "name": "当归片（甘肃岷县）",
                "description": "甘肃岷县正宗当归，补血活血，调经止痛，润肠通便。女性养血佳品。",
                "category": ProductCategory.HERBAL_MEDICINE,
                "price": 45.8,
                "stock_quantity": 200,
                "images": ["https://via.placeholder.com/400x300/DEB887/FFFFFF?text=当归"],
                "specifications": {"weight": "250g", "origin": "甘肃岷县"},
                "features": ["补血活血", "调经止痛", "润肠通便"],
                "usage_instructions": "每次6-12克，煎汤服用",
                "sales_count": 324,
                "rating": 4.7,
                "review_count": 178
            },
            {
                "name": "枸杞子（宁夏中宁）",
                "description": "宁夏中宁枸杞，滋补肝肾，益精明目。颗粒饱满，色泽红润。",
                "category": ProductCategory.HERBAL_MEDICINE,
                "price": 29.9,
                "original_price": 35.0,
                "discount": 0.85,
                "stock_quantity": 500,
                "images": ["https://via.placeholder.com/400x300/CD5C5C/FFFFFF?text=枸杞"],
                "specifications": {"weight": "500g", "origin": "宁夏中宁", "grade": "特级"},
                "features": ["滋补肝肾", "益精明目", "提高免疫"],
                "usage_instructions": "每日10-15克，泡茶或煮粥",
                "is_featured": True,
                "sales_count": 876,
                "rating": 4.9,
                "review_count": 432
            }
        ]
        
        # 养生产品
        health_products = [
            {
                "name": "阿胶固元膏",
                "description": "纯正东阿阿胶制作，添加核桃、黑芝麻、红枣等，补血养颜，滋阴润燥。",
                "category": ProductCategory.HEALTH_PRODUCTS,
                "price": 168.0,
                "stock_quantity": 80,
                "images": ["https://via.placeholder.com/400x300/8B4513/FFFFFF?text=阿胶膏"],
                "specifications": {"weight": "500g", "保质期": "12个月"},
                "features": ["补血养颜", "滋阴润燥", "增强体质"],
                "usage_instructions": "每日早晚各一勺，开水冲服",
                "sales_count": 245,
                "rating": 4.6,
                "review_count": 134
            },
            {
                "name": "蜂蜜柠檬膏",
                "description": "优质土蜂蜜配柠檬精制而成，润肺止咳，美容养颜，口感酸甜。",
                "category": ProductCategory.HEALTH_PRODUCTS,
                "price": 78.0,
                "stock_quantity": 120,
                "images": ["https://via.placeholder.com/400x300/FFD700/FFFFFF?text=蜂蜜柠檬膏"],
                "specifications": {"重量": "350g"},
                "features": ["润肺止咳", "美容养颜", "提神醒脑"],
                "usage_instructions": "每次1-2勺，温水冲调饮用",
                "sales_count": 189,
                "rating": 4.5,
                "review_count": 95
            }
        ]
        
        # 保健食品
        health_foods = [
            {
                "name": "灵芝孢子粉胶囊",
                "description": "破壁灵芝孢子粉，提高免疫力，抗疲劳，延缓衰老。每粒含纯孢子粉500mg。",
                "category": ProductCategory.HEALTH_FOOD,
                "price": 299.0,
                "original_price": 350.0,
                "discount": 0.85,
                "stock_quantity": 60,
                "images": ["https://via.placeholder.com/400x300/9370DB/FFFFFF?text=灵芝孢子粉"],
                "specifications": {"规格": "60粒/瓶", "含量": "500mg/粒"},
                "features": ["提高免疫", "抗疲劳", "延缓衰老"],
                "usage_instructions": "每日2次，每次2粒，饭前温水送服",
                "is_featured": True,
                "sales_count": 432,
                "rating": 4.8,
                "review_count": 256
            }
        ]
        
        # 医疗器械
        medical_equipment = [
            {
                "name": "电子针灸仪",
                "description": "家用电子针灸治疗仪，模拟传统针灸，安全便捷，适用于多种穴位治疗。",
                "category": ProductCategory.MEDICAL_EQUIPMENT,
                "price": 199.0,
                "stock_quantity": 30,
                "images": ["https://via.placeholder.com/400x300/4682B4/FFFFFF?text=针灸仪"],
                "specifications": {"功率": "5W", "电源": "锂电池", "保修": "1年"},
                "features": ["模拟针灸", "安全便捷", "多档调节"],
                "usage_instructions": "选择相应穴位，调节合适强度使用",
                "sales_count": 87,
                "rating": 4.3,
                "review_count": 45
            },
            {
                "name": "拔罐器套装",
                "description": "12罐真空拔罐器套装，硅胶材质，操作简单，适合家庭保健使用。",
                "category": ProductCategory.MEDICAL_EQUIPMENT,
                "price": 89.0,
                "stock_quantity": 100,
                "images": ["https://via.placeholder.com/400x300/DC143C/FFFFFF?text=拔罐器"],
                "specifications": {"材质": "硅胶", "规格": "12罐装"},
                "features": ["真空拔罐", "操作简单", "家庭保健"],
                "usage_instructions": "清洁皮肤后，按压排气使用",
                "sales_count": 156,
                "rating": 4.4,
                "review_count": 78
            }
        ]
        
        # 中医书籍
        books = [
            {
                "name": "《黄帝内经》白话全译",
                "description": "中医四大经典之首，白话文全译本，配有详细注解，是学习中医的必备经典。",
                "category": ProductCategory.TCM_BOOKS,
                "price": 58.0,
                "stock_quantity": 200,
                "images": ["https://via.placeholder.com/400x300/228B22/FFFFFF?text=黄帝内经"],
                "specifications": {"页数": "680页", "出版社": "中医古籍出版社"},
                "features": ["经典著作", "白话译文", "详细注解"],
                "usage_instructions": "建议配合专业指导学习",
                "sales_count": 267,
                "rating": 4.7,
                "review_count": 145
            }
        ]
        
        # 配套用品
        accessories = [
            {
                "name": "药材储存密封罐套装",
                "description": "玻璃材质密封罐，专为中药材储存设计，防潮防虫，保持药材新鲜。",
                "category": ProductCategory.ACCESSORIES,
                "price": 45.0,
                "stock_quantity": 150,
                "images": ["https://via.placeholder.com/400x300/2E8B57/FFFFFF?text=储存罐"],
                "specifications": {"材质": "玻璃", "规格": "5个装"},
                "features": ["密封防潮", "防虫保鲜", "透明可视"],
                "usage_instructions": "清洁干燥后放入药材密封保存",
                "sales_count": 123,
                "rating": 4.2,
                "review_count": 67
            }
        ]
        
        # 合并所有商品
        all_products = (herbal_products + health_products + health_foods + 
                        medical_equipment + books + accessories)
        
        # 添加到数据库
        for product_data in all_products:
            product = Product(**product_data)
            db.add(product)
        
        db.commit()
        print(f"成功创建 {len(all_products)} 个商品数据")
        
    except Exception as e:
        print(f"创建商品数据失败: {e}")
        db.rollback()
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_products_data()