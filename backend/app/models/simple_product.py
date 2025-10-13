"""
简洁的商品模型
"""
from sqlalchemy import Column, Integer, String, Text, Numeric, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class SimpleProduct(Base):
    """简洁的商品模型"""
    __tablename__ = "simple_products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False, comment="商品名称")
    description = Column(Text, comment="商品描述")
    price = Column(Numeric(10, 2), nullable=False, comment="商品价格")
    original_price = Column(Numeric(10, 2), comment="原价")
    category = Column(String(100), comment="商品分类")
    images = Column(JSON, comment="商品图片列表")
    stock = Column(Integer, default=0, comment="库存数量")
    is_active = Column(Boolean, default=True, comment="是否上架")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class SimpleCart(Base):
    """简洁的购物车模型"""
    __tablename__ = "simple_cart"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False, comment="用户ID")
    product_id = Column(Integer, nullable=False, comment="商品ID")
    quantity = Column(Integer, default=1, comment="数量")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class SimpleOrder(Base):
    """简洁的订单模型"""
    __tablename__ = "simple_orders"

    id = Column(Integer, primary_key=True, index=True)
    order_number = Column(String(50), unique=True, nullable=False, comment="订单号")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    total_amount = Column(Numeric(10, 2), nullable=False, comment="订单总额")
    status = Column(String(20), default="pending", comment="订单状态")
    shipping_name = Column(String(100), comment="收货人")
    shipping_phone = Column(String(20), comment="收货电话")
    shipping_address = Column(Text, comment="收货地址")
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    paid_at = Column(DateTime(timezone=True), comment="支付时间")

class SimpleOrderItem(Base):
    """简洁的订单项模型"""
    __tablename__ = "simple_order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, nullable=False, comment="订单ID")
    product_id = Column(Integer, nullable=False, comment="商品ID")
    product_name = Column(String(200), comment="商品名称")
    product_price = Column(Numeric(10, 2), comment="商品价格")
    quantity = Column(Integer, comment="数量")
    subtotal = Column(Numeric(10, 2), comment="小计")
