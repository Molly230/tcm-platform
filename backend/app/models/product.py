"""
商品和订单模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, Enum, JSON, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.core.enums_v2 import ProductCategory, ProductStatus, AuditStatus, OrderStatus


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    # 基本信息
    name = Column(String, nullable=False, index=True)
    description = Column(Text)
    category = Column(Enum(ProductCategory), nullable=False)
    price = Column(Numeric(8, 2))
    stock_quantity = Column(Integer, default=0)
    images = Column(JSON, default=list)  # 图片URL列表
    usage_instructions = Column(Text)  # 使用说明

    # 标志
    is_featured = Column(Boolean, default=False)  # 是否精选
    is_common = Column(Boolean, default=False)    # 是否常用

    # 状态
    status = Column(Enum(ProductStatus), default=ProductStatus.DRAFT)
    audit_status = Column(Enum(AuditStatus), default=AuditStatus.DRAFT)

    # 审计字段
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(Integer)  # 外键到用户表
    is_deleted = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', category='{self.category}')>"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String, unique=True, index=True)  # 订单号

    # 用户信息
    user_id = Column(Integer, ForeignKey("users.id"))

    # 订单金额
    total_amount = Column(Numeric(10, 2), nullable=False)
    shipping_fee = Column(Numeric(8, 2), default=0)
    discount_amount = Column(Numeric(8, 2), default=0)

    # 收货信息
    shipping_address = Column(Text)
    notes = Column(Text)

    # 状态
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)

    # 审计字段
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    is_deleted = Column(Boolean, default=False)

    # 关系
    items = relationship("OrderItem", back_populates="order")
    shipping = relationship("Shipping", back_populates="order", uselist=False)  # 一对一关系

    def __repr__(self):
        return f"<Order(id={self.id}, order_number='{self.order_number}', status='{self.status}')>"


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)

    # 关联
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))

    # 商品信息（快照）
    product_name = Column(String)  # 下单时的商品名称
    product_price = Column(Numeric(8, 2))  # 下单时的商品价格
    quantity = Column(Integer, nullable=False)

    # 审计字段
    created_at = Column(DateTime, default=func.now())
    is_deleted = Column(Boolean, default=False)

    # 关系
    order = relationship("Order", back_populates="items")
    product = relationship("Product")

    def __repr__(self):
        return f"<OrderItem(id={self.id}, product_id={self.product_id}, quantity={self.quantity})>"