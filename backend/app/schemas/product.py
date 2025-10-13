"""
商品相关的Pydantic模型
"""
from pydantic import BaseModel, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal
from app.core.enums_v2 import ProductCategory, ProductStatus, AuditStatus


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: ProductCategory
    price: Optional[Decimal] = None
    stock_quantity: Optional[int] = 0
    images: Optional[List[str]] = []
    usage_instructions: Optional[str] = None
    is_featured: bool = False
    is_common: bool = False


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ProductCategory] = None
    price: Optional[Decimal] = None
    stock_quantity: Optional[int] = None
    images: Optional[List[str]] = None
    usage_instructions: Optional[str] = None
    is_featured: Optional[bool] = None
    is_common: Optional[bool] = None
    status: Optional[ProductStatus] = None
    audit_status: Optional[AuditStatus] = None


class Product(ProductBase):
    id: int
    status: ProductStatus
    audit_status: AuditStatus
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    is_deleted: bool = False

    class Config:
        from_attributes = True


class ProductResponse(Product):
    pass


class ProductSubmitRequest(BaseModel):
    product_id: int


class ProductAuditRequest(BaseModel):
    product_id: int
    action: str  # "approve" or "reject"
    reason: Optional[str] = None


class CartItem(BaseModel):
    id: int
    user_id: int
    product_id: int
    quantity: int
    created_at: datetime

    class Config:
        from_attributes = True


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = 1
    price: Optional[float] = None  # 可选价格


class OrderItem(BaseModel):
    id: int
    order_id: int
    product_id: int
    quantity: int
    price: Decimal
    created_at: datetime

    class Config:
        from_attributes = True


class OrderItemCreateData(BaseModel):
    product_id: int
    quantity: int


class CustomerInfo(BaseModel):
    """客户信息"""
    name: str
    phone: str
    address: str


class OrderCreate(BaseModel):
    items: List[OrderItemCreate]
    customer_info: CustomerInfo  # 客户信息对象
    remark: Optional[str] = None  # 备注
    total_amount: float  # 总金额
    subtotal: Optional[float] = None  # 小计
    shipping_fee: Optional[float] = 0  # 运费
    discount_amount: Optional[float] = 0  # 折扣


class Order(BaseModel):
    id: int
    user_id: int
    total_amount: Decimal
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentData(BaseModel):
    order_id: int
    payment_method: str
    amount: Decimal