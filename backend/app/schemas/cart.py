"""
购物车Schema定义
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class CartItemCreate(BaseModel):
    """创建购物车项"""
    product_id: int
    quantity: int = Field(default=1, ge=1)


class CartItemUpdate(BaseModel):
    """更新购物车项"""
    quantity: int = Field(ge=0)  # 0表示删除


class CartItemResponse(BaseModel):
    """购物车项响应"""
    id: int
    cart_id: int
    product_id: int
    quantity: int
    price_snapshot: Optional[Decimal] = None
    created_at: datetime
    updated_at: datetime

    # 关联的商品信息
    product: Optional[dict] = None

    model_config = {
        'from_attributes': True,
        'arbitrary_types_allowed': True  # 允许任意类型，避免严格验证
    }


class CartResponse(BaseModel):
    """购物车响应"""
    id: int
    user_id: int
    items: List[CartItemResponse] = []
    created_at: datetime
    updated_at: datetime

    # 计算字段
    total_items: int = 0
    total_price: Decimal = Decimal('0.00')

    class Config:
        from_attributes = True
