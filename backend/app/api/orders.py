"""
订单相关API路由
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from app import models
from app.schemas.product import OrderCreate, Order, PaymentData
from app.database import get_db
from app.core.exceptions import (
    NotFoundException, 
    BusinessException, 
    ValidationException, 
    FileTooLargeException, 
    UnsupportedFileTypeException, 
    DatabaseException, 
    CommonErrors
)
from app.core.enums_v2 import ProductStatus, OrderStatus

router = APIRouter(tags=["orders"])

# 管理员获取所有订单 - 使用明确的路径避免与 /{order_id} 冲突
@router.get("/admin/all", response_model=List[Order])
def get_all_orders(
    skip: int = 0,
    limit: int = 100,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取所有订单列表（管理员用）"""
    query = db.query(models.Order)

    if status_filter:
        query = query.filter(models.Order.status == status_filter)

    orders = query.order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders

@router.get("/user/{user_id}", response_model=List[Order])
def get_user_orders(
    user_id: int = 1,
    skip: int = 0,
    limit: int = 20,
    status_filter: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """获取用户订单列表"""
    query = db.query(models.Order).filter(models.Order.user_id == user_id)

    if status_filter:
        query = query.filter(models.Order.status == status_filter)

    orders = query.order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()
    return orders

@router.post("/")
def create_order(
    order_data: OrderCreate,
    user_id: int = 1,  # 临时固定用户ID，实际应该从认证中获取
    db: Session = Depends(get_db)
):
    """创建订单"""
    
    # 生成订单号
    order_number = f"TCM{datetime.now().strftime('%Y%m%d%H%M%S')}{str(uuid.uuid4())[:8].upper()}"
    
    # 验证商品库存
    total_amount = 0
    order_items = []
    
    for item_data in order_data.items:
        product = db.query(models.Product).filter(
            models.Product.id == item_data.product_id,
            models.Product.status == ProductStatus.ACTIVE
        ).first()

        if not product:
            raise CommonErrors.PRODUCT_NOT_FOUND

        if product.stock_quantity < item_data.quantity:
            raise CommonErrors.INSUFFICIENT_STOCK

        # 始终使用产品表中的价格，忽略前端传的价格（防止篡改）
        unit_price = float(product.price)
        item_total = unit_price * item_data.quantity
        total_amount += item_total
        
        order_items.append({
            "product_id": item_data.product_id,
            "product_name": product.name,
            "product_price": unit_price,  # OrderItem使用product_price字段
            "quantity": item_data.quantity
        })
    
    # 创建订单 - 使用前端传入的customer_info
    from decimal import Decimal
    # 构建收货地址JSON（包含所有客户信息）
    shipping_info = {
        "name": order_data.customer_info.name,
        "phone": order_data.customer_info.phone,
        "address": order_data.customer_info.address
    }

    db_order = models.Order(
        order_number=order_number,
        user_id=user_id,
        total_amount=Decimal(str(total_amount)),  # 使用后端计算的金额
        shipping_fee=Decimal(str(order_data.shipping_fee or 0)),
        discount_amount=Decimal(str(order_data.discount_amount or 0)),
        shipping_address=str(shipping_info),  # 存储为字符串
        notes=order_data.remark,
        status=OrderStatus.PENDING
    )
    
    db.add(db_order)
    db.flush()  # 获取订单ID
    
    # 创建订单项
    for item_data in order_items:
        order_item = models.OrderItem(
            order_id=db_order.id,
            **item_data
        )
        db.add(order_item)
    
    # 更新商品库存
    for item_data in order_data.items:
        product = db.query(models.Product).filter(
            models.Product.id == item_data.product_id
        ).first()
        product.stock_quantity -= item_data.quantity
    
    db.commit()
    db.refresh(db_order)
    
    # 临时返回简单的成功消息，避免响应模型验证问题
    return {
        "success": True,
        "message": "订单创建成功",
        "order_id": db_order.id,
        "order_number": db_order.order_number,
        "status": db_order.status.value,
        "total_amount": float(db_order.total_amount)
    }

@router.get("/{order_id}", response_model=Order)
def get_order(order_id: int, db: Session = Depends(get_db)):
    """获取订单详情"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    if not order:
        raise CommonErrors.ORDER_NOT_FOUND

    return order

@router.put("/{order_id}/status")
def update_order_status(
    order_id: int,
    status_update: str,
    db: Session = Depends(get_db)
):
    """更新订单状态"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        raise CommonErrors.ORDER_NOT_FOUND
    
    # 验证状态转换的有效性
    valid_statuses = [s.value for s in OrderStatus]
    if status_update not in valid_statuses:
        raise ValidationException(f"无效状态。有效状态：{valid_statuses}")

    order.status = status_update

    # 如果是支付成功，更新支付时间
    if status_update == OrderStatus.PAID:
        order.paid_at = datetime.utcnow()
    
    db.commit()
    return {"message": "Order status updated successfully", "status": status_update}

@router.post("/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    """取消订单"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        raise CommonErrors.ORDER_NOT_FOUND
    
    # 只有待支付的订单才能取消
    if order.status != OrderStatus.PENDING:
        raise CommonErrors.ORDER_CANNOT_CANCEL

    # 恢复商品库存
    for item in order.items:
        product = db.query(models.Product).filter(
            models.Product.id == item.product_id
        ).first()
        if product:
            product.stock_quantity += item.quantity

    order.status = OrderStatus.CANCELLED
    order.cancelled_at = datetime.utcnow()
    
    db.commit()
    return {"message": "Order cancelled successfully"}

# 旧的支付端点已废弃，请使用 /api/payment/create

