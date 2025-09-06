"""
商品相关模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, Enum, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class ProductCategory(str, enum.Enum):
    HERB = "中药材"              # 中药材
    WELLNESS = "养生产品"         # 养生产品
    MEDICAL_DEVICE = "医疗器械"    # 医疗器械
    HEALTH_FOOD = "保健食品"      # 保健食品
    BOOKS = "中医书籍"           # 中医书籍
    ACCESSORIES = "配套用品"      # 配套用品

class ProductStatus(str, enum.Enum):
    ACTIVE = "active"         # 在售
    INACTIVE = "inactive"     # 下架
    OUT_OF_STOCK = "out_of_stock"  # 缺货

class AuditStatus(str, enum.Enum):
    PENDING = "pending"       # 待审核
    APPROVED = "approved"     # 审核通过
    REJECTED = "rejected"     # 审核拒绝
    REVISION = "revision"     # 需要修改

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    category = Column(Enum(ProductCategory), nullable=False)
    
    # 价格信息
    price = Column(Float, nullable=False)  # 现价
    original_price = Column(Float)  # 原价
    discount = Column(Float, default=1.0)  # 折扣 (0.8 = 8折)
    
    # 库存信息
    stock_quantity = Column(Integer, default=0)  # 库存数量
    min_stock_alert = Column(Integer, default=10)  # 最低库存预警
    
    # 商品信息
    images = Column(JSON)  # 商品图片数组 ['url1', 'url2']
    specifications = Column(JSON)  # 规格信息 {'weight': '100g', 'origin': '安徽'}
    features = Column(JSON)  # 功效特点 ['补气', '养血']
    usage_instructions = Column(Text)  # 使用方法
    
    # 状态和标签
    status = Column(Enum(ProductStatus), default=ProductStatus.ACTIVE)
    is_featured = Column(Boolean, default=False)  # 是否推荐
    is_common = Column(Boolean, default=False)   # 是否为常用产品
    is_prescription_required = Column(Boolean, default=False)  # 是否需要处方
    
    # 审核相关字段
    audit_status = Column(Enum(AuditStatus), default=AuditStatus.PENDING)  # 审核状态
    submitted_by = Column(String)  # 提交人
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())  # 提交时间
    reviewed_by = Column(String)  # 审核人
    reviewed_at = Column(DateTime(timezone=True))  # 审核时间
    audit_notes = Column(Text)  # 审核备注
    
    # SEO信息
    seo_title = Column(String)
    seo_keywords = Column(String)
    seo_description = Column(Text)
    
    # 销售统计
    sales_count = Column(Integer, default=0)  # 销量
    rating = Column(Float, default=5.0)  # 评分
    review_count = Column(Integer, default=0)  # 评价数量
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', category='{self.category}')>"

class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    selected = Column(Boolean, default=True)  # 是否选中待结算
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    product = relationship("Product", back_populates="cart_items")

class OrderStatus(str, enum.Enum):
    PENDING_PAYMENT = "pending_payment"    # 待支付
    PAID = "paid"                         # 已支付
    PROCESSING = "processing"             # 处理中
    SHIPPED = "shipped"                   # 已发货
    DELIVERED = "delivered"               # 已送达
    CANCELLED = "cancelled"               # 已取消
    REFUNDED = "refunded"                 # 已退款

class PaymentMethod(str, enum.Enum):
    WECHAT_PAY = "wechat_pay"       # 微信支付
    ALIPAY = "alipay"               # 支付宝
    UNION_PAY = "union_pay"         # 银联支付
    DIGITAL_CURRENCY = "digital_currency"  # 数字人民币

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, nullable=False, index=True)  # 订单号
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 金额信息
    subtotal = Column(Float, nullable=False)  # 商品总额
    shipping_fee = Column(Float, default=0.0)  # 运费
    discount_amount = Column(Float, default=0.0)  # 优惠金额
    total_amount = Column(Float, nullable=False)  # 实付金额
    
    # 订单状态
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING_PAYMENT)
    payment_method = Column(Enum(PaymentMethod))
    payment_id = Column(String)  # 第三方支付订单号
    
    # 收货信息
    shipping_address = Column(JSON)  # 收货地址信息
    shipping_name = Column(String)  # 收货人姓名
    shipping_phone = Column(String)  # 收货人电话
    
    # 物流信息
    tracking_number = Column(String)  # 快递单号
    courier_company = Column(String)  # 快递公司
    
    # 备注
    user_note = Column(Text)  # 用户备注
    admin_note = Column(Text)  # 管理员备注
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    paid_at = Column(DateTime(timezone=True))
    shipped_at = Column(DateTime(timezone=True))
    delivered_at = Column(DateTime(timezone=True))
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    order_items = relationship("OrderItem", back_populates="order")
    items = relationship("OrderItem", back_populates="order", overlaps="order_items")  # 别名，用于API返回

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    
    # 商品快照信息（防止商品信息变更影响历史订单）
    product_name = Column(String, nullable=False)
    product_image = Column(String)
    product_specifications = Column(JSON)
    
    # 数量和价格
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Float, nullable=False)  # 单价
    total_price = Column(Float, nullable=False)  # 小计

    # 关系
    order = relationship("Order", back_populates="order_items")
    product = relationship("Product")

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    payment_method = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, default="pending")  # pending, success, failed
    transaction_id = Column(String)  # 第三方支付交易号
    
    # 时间字段
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    order = relationship("Order")