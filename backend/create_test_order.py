"""创建测试订单数据"""

import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

from app.database import SessionLocal, engine
from app import models
from app.models.product import ProductCategory, ProductStatus
import time

def create_test_order():
    """创建测试订单"""
    db = SessionLocal()
    
    try:
        # 检查是否已经存在用户，如果没有创建一个
        user = db.query(models.User).filter(models.User.email == "test@example.com").first()
        if not user:
            user = models.User(
                username="test_user",
                email="test@example.com", 
                phone="13800138000",
                hashed_password="test_password",
                is_active=True
            )
            db.add(user)
            db.commit()
            db.refresh(user)
        
        # 创建测试商品（如果不存在）
        product = db.query(models.Product).filter(models.Product.name == "测试商品").first()
        if not product:
            product = models.Product(
                name="测试商品",
                description="这是一个测试商品，用于测试支付功能",
                price=299.80,
                stock_quantity=100,
                category=ProductCategory.PRODUCT,
                status=ProductStatus.ACTIVE,
                is_common=True
            )
            db.add(product)
            db.commit()
            db.refresh(product)
        
        # 创建测试订单
        order_number = f"TCM{int(time.time())}"
        
        # 检查订单是否已存在
        existing_order = db.query(models.Order).filter(models.Order.order_number == order_number).first()
        if existing_order:
            print(f"订单已存在: {order_number}")
            return order_number
            
        order = models.Order(
            order_number=order_number,
            user_id=user.id,
            subtotal=299.80,
            shipping_fee=0.0,
            discount_amount=0.0,
            total_amount=299.80,
            status=models.OrderStatus.PENDING_PAYMENT,
            shipping_address={
                "province": "北京市",
                "city": "朝阳区", 
                "district": "建国门外大街",
                "address": "1号国际大厦"
            },
            shipping_name="测试用户",
            shipping_phone="13800138000",
            user_note="测试订单"
        )
        db.add(order)
        db.commit()
        db.refresh(order)
        
        # 创建订单商品
        order_item = models.OrderItem(
            order_id=order.id,
            product_id=product.id,
            product_name=product.name,
            quantity=1,
            unit_price=product.price,
            total_price=product.price
        )
        db.add(order_item)
        db.commit()
        
        print("测试订单创建成功！")
        print(f"订单号: {order_number}")
        print(f"用户ID: {user.id}")
        print(f"商品: {product.name}")
        print(f"金额: ¥{order.total_amount}")
        print()
        print("可以访问以下URL测试支付:")
        print(f"支付页面1: http://localhost:3000/payment/{order_number}")
        print(f"支付页面2: http://localhost:3000/simple-pay/{order_number}")
        print()
        print("API测试命令:")
        print(f'curl -X POST "http://127.0.0.1:8000/api/reliable-pay/create" -H "Content-Type: application/json" -d \'{{"order_id": "{order_number}", "payment_method": "alipay_qr"}}\'')
        
        return order_number
        
    except Exception as e:
        db.rollback()
        print(f"创建测试订单失败: {e}")
        return None
    finally:
        db.close()

if __name__ == "__main__":
    # 确保数据库表存在
    models.Base.metadata.create_all(bind=engine)
    create_test_order()