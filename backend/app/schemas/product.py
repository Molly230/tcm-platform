"""
商品相关的Pydantic模型
"""
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
from enum import Enum

class ProductCategory(str, Enum):
    HERB = "中药材"              # 中药材
    WELLNESS = "养生产品"         # 养生产品
    MEDICAL_DEVICE = "医疗器械"    # 医疗器械
    HEALTH_FOOD = "保健食品"      # 保健食品
    BOOKS = "中医书籍"           # 中医书籍
    ACCESSORIES = "配套用品"      # 配套用品

class ProductStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    OUT_OF_STOCK = "out_of_stock"

class AuditStatus(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISION = "revision"

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    category: ProductCategory
    price: float
    original_price: Optional[float] = None
    discount: float = 1.0
    stock_quantity: int = 0
    min_stock_alert: int = 10
    images: Optional[List[str]] = []
    specifications: Optional[Dict[str, Any]] = {}
    features: Optional[List[str]] = []
    usage_instructions: Optional[str] = None
    status: ProductStatus = ProductStatus.ACTIVE
    is_featured: bool = False
    is_common: bool = False
    is_prescription_required: bool = False
    audit_status: AuditStatus = AuditStatus.PENDING
    submitted_by: Optional[str] = None
    audit_notes: Optional[str] = None
    seo_title: Optional[str] = None
    seo_keywords: Optional[str] = None
    seo_description: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    category: Optional[ProductCategory] = None
    price: Optional[float] = None
    original_price: Optional[float] = None
    discount: Optional[float] = None
    stock_quantity: Optional[int] = None
    images: Optional[List[str]] = None
    specifications: Optional[Dict[str, Any]] = None
    features: Optional[List[str]] = None
    usage_instructions: Optional[str] = None
    status: Optional[ProductStatus] = None
    is_featured: Optional[bool] = None
    is_common: Optional[bool] = None

class Product(ProductBase):
    id: int
    sales_count: int
    rating: float
    review_count: int
    submitted_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None
    reviewed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# 审核操作schemas
class ProductAuditRequest(BaseModel):
    action: str  # "approve", "reject", "revision"
    notes: Optional[str] = None

class ProductSubmitRequest(ProductBase):
    pass

class CartItemBase(BaseModel):
    user_id: int
    product_id: int
    quantity: int = 1
    selected: bool = True

class CartItemCreate(CartItemBase):
    pass

class CartItem(CartItemBase):
    id: int
    product: Product
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class OrderStatus(str, Enum):
    PENDING_PAYMENT = "pending_payment"
    PAID = "paid"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"

class PaymentMethod(str, Enum):
    WECHAT_PAY = "wechat_pay"
    ALIPAY = "alipay"
    UNION_PAY = "union_pay"
    DIGITAL_CURRENCY = "digital_currency"

class OrderItemBase(BaseModel):
    product_id: int
    product_name: str
    product_image: Optional[str] = None
    product_specifications: Optional[Dict[str, Any]] = {}
    quantity: int
    unit_price: float
    total_price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    user_id: int
    subtotal: float
    shipping_fee: float = 0.0
    discount_amount: float = 0.0
    total_amount: float
    payment_method: Optional[PaymentMethod] = None
    shipping_address: Optional[Dict[str, Any]] = {}
    shipping_name: Optional[str] = None
    shipping_phone: Optional[str] = None
    user_note: Optional[str] = None

class OrderItemCreateData(BaseModel):
    product_id: int
    quantity: int
    price: float

class OrderCreate(BaseModel):
    items: List[OrderItemCreateData] = []
    subtotal: Optional[float] = None
    shipping_fee: float = 0.0
    discount_amount: float = 0.0
    total_amount: float
    shipping_address: str
    remark: Optional[str] = None

class PaymentData(BaseModel):
    payment_method: str
    amount: Optional[float] = None  # 保持兼容性，但实际不使用

class PaymentCreate(BaseModel):
    order_number: str
    payment_method: str  # "alipay", "wechat"
    openid: Optional[str] = None  # 微信支付时需要

class PaymentResponse(BaseModel):
    success: bool
    payment_method: str
    payment_url: Optional[str] = None  # 支付宝支付链接
    qr_code_url: Optional[str] = None  # 微信扫码支付二维码
    jsapi_params: Optional[Dict[str, Any]] = None  # 微信JSAPI支付参数
    error: Optional[str] = None

class Order(OrderBase):
    id: int
    order_number: str
    status: OrderStatus
    payment_id: Optional[str] = None
    tracking_number: Optional[str] = None
    courier_company: Optional[str] = None
    admin_note: Optional[str] = None
    created_at: datetime
    paid_at: Optional[datetime] = None
    shipped_at: Optional[datetime] = None
    delivered_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    order_items: List[OrderItem] = []

    class Config:
        from_attributes = True