"""
配送/物流模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Enum, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.core.enums_v2 import ShippingStatus, CourierCompany


class Shipping(Base):
    """配送/物流信息"""
    __tablename__ = "shippings"

    id = Column(Integer, primary_key=True, index=True)

    # 关联订单
    order_id = Column(Integer, ForeignKey("orders.id"), unique=True, nullable=False, index=True)

    # 物流公司信息
    courier_company = Column(Enum(CourierCompany), nullable=False)  # 物流公司
    courier_company_name = Column(String)  # 物流公司名称（冗余，方便显示）
    tracking_number = Column(String, nullable=False, index=True)  # 物流单号

    # 配送状态
    status = Column(Enum(ShippingStatus), default=ShippingStatus.PENDING)

    # 配送员信息
    courier_name = Column(String)  # 配送员姓名
    courier_phone = Column(String)  # 配送员电话

    # 时间节点
    shipped_at = Column(DateTime)  # 发货时间
    estimated_delivery_at = Column(DateTime)  # 预计送达时间
    delivered_at = Column(DateTime)  # 实际送达时间

    # 物流轨迹（JSON格式）
    # 格式: [{"time": "2025-10-25 10:00", "status": "已揽收", "location": "北京市"}]
    tracking_history = Column(JSON, default=list)

    # 备注
    notes = Column(Text)  # 备注信息

    # 审计字段
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    created_by = Column(Integer)  # 创建人ID（管理员）

    # 关系
    order = relationship("Order", back_populates="shipping")

    def __repr__(self):
        return f"<Shipping(id={self.id}, order_id={self.order_id}, tracking_number='{self.tracking_number}', status='{self.status}')>"
