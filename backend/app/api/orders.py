"""
订单相关API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import uuid
from datetime import datetime

from app import models
from app.schemas.product import OrderCreate, Order, PaymentData
from app.database import get_db

router = APIRouter(tags=["orders"])

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
            models.Product.status == "active"
        ).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product {item_data.product_id} not found"
            )
        
        if product.stock_quantity < item_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.name}"
            )
        
        # 计算商品价格
        item_total = item_data.price * item_data.quantity
        total_amount += item_total
        
        order_items.append({
            "product_id": item_data.product_id,
            "product_name": product.name,
            "product_image": product.images[0] if product.images else None,
            "product_specifications": product.specifications,
            "quantity": item_data.quantity,
            "unit_price": item_data.price,
            "total_price": item_total
        })
    
    # 创建订单
    db_order = models.Order(
        order_number=order_number,
        user_id=user_id,
        total_amount=order_data.total_amount or total_amount,
        subtotal=order_data.subtotal or total_amount,
        shipping_fee=order_data.shipping_fee or 0,
        discount_amount=order_data.discount_amount or 0,
        shipping_address={"address": order_data.shipping_address},  # 转换为字典格式
        shipping_name="默认收货人",  # 临时设置默认值
        shipping_phone="13800138000",  # 临时设置默认值
        user_note=order_data.remark,
        status=models.OrderStatus.PENDING_PAYMENT
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    return order

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

@router.put("/{order_id}/status")
def update_order_status(
    order_id: int,
    status_update: str,
    db: Session = Depends(get_db)
):
    """更新订单状态"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # 验证状态转换的有效性
    valid_statuses = [s.value for s in models.OrderStatus]
    if status_update not in valid_statuses:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status. Valid statuses: {valid_statuses}"
        )
    
    order.status = status_update
    
    # 如果是支付成功，更新支付时间
    if status_update == models.OrderStatus.PAID:
        order.paid_at = datetime.utcnow()
    
    db.commit()
    return {"message": "Order status updated successfully", "status": status_update}

@router.post("/{order_id}/cancel")
def cancel_order(order_id: int, db: Session = Depends(get_db)):
    """取消订单"""
    order = db.query(models.Order).filter(models.Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # 只有待支付的订单才能取消
    if order.status != models.OrderStatus.PENDING_PAYMENT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only pending orders can be cancelled"
        )
    
    # 恢复商品库存
    for item in order.items:
        product = db.query(models.Product).filter(
            models.Product.id == item.product_id
        ).first()
        if product:
            product.stock_quantity += item.quantity
    
    order.status = models.OrderStatus.CANCELLED
    order.cancelled_at = datetime.utcnow()
    
    db.commit()
    return {"message": "Order cancelled successfully"}

# 旧的支付端点已废弃，请使用 /api/payment/create