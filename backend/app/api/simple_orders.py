"""
简单订单API - 用于测试支付流程
"""
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import uuid
from datetime import datetime

router = APIRouter(tags=["simple-orders"])

# 临时存储（用于测试）
temp_orders = {}

class SimpleOrderItem(BaseModel):
    product_id: int
    quantity: int

class SimpleOrderCreate(BaseModel):
    items: List[SimpleOrderItem]
    shipping_address: Optional[str] = None
    notes: Optional[str] = None

class SimpleOrder(BaseModel):
    id: int
    order_number: str
    total_amount: float
    status: str
    created_at: str

@router.post("/simple-orders", response_model=dict)
def create_simple_order(order_data: SimpleOrderCreate):
    """创建简单订单（测试用）"""

    # 生成订单ID和订单号
    order_id = len(temp_orders) + 1
    order_number = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{order_id:03d}"

    # 计算总金额（简化版）
    total_amount = 0
    for item in order_data.items:
        # 模拟价格（实际应该从数据库获取）
        price = 168.80  # 简化为固定价格
        total_amount += price * item.quantity

    # 创建订单
    order = {
        "id": order_id,
        "order_number": order_number,
        "items": [item.dict() for item in order_data.items],
        "shipping_address": order_data.shipping_address,
        "notes": order_data.notes,
        "total_amount": total_amount,
        "status": "PENDING_PAYMENT",
        "created_at": datetime.now().isoformat()
    }

    # 保存到临时存储
    temp_orders[order_id] = order

    return {
        "success": True,
        "data": order,
        "message": "订单创建成功"
    }

@router.get("/simple-orders/{order_id}")
def get_simple_order(order_id: int):
    """获取订单详情"""

    if order_id not in temp_orders:
        return {"success": False, "message": "订单不存在"}

    return {
        "success": True,
        "data": temp_orders[order_id]
    }

@router.get("/simple-orders")
def list_simple_orders():
    """获取所有订单"""

    return {
        "success": True,
        "data": list(temp_orders.values())
    }