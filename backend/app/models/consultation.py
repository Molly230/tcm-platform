"""
健康咨询模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, Enum, Boolean, JSON, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
from app.core.enums_v2 import ConsultationType, ConsultationStatus, PaymentStatus

class Consultation(Base):
    __tablename__ = "consultations"

    id = Column(Integer, primary_key=True, index=True)
    consultation_number = Column(String, unique=True, nullable=False, index=True)  # 咨询单号
    
    # 基础信息
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    expert_id = Column(Integer, ForeignKey("experts.id"), nullable=True)
    type = Column(Enum(ConsultationType), nullable=False)
    status = Column(Enum(ConsultationStatus), default=ConsultationStatus.PENDING)
    
    # 咨询内容
    title = Column(String, nullable=False)  # 咨询标题
    symptoms = Column(Text)  # 主要症状
    duration = Column(String)  # 持续时间
    medical_history = Column(Text)  # 既往病史
    current_medications = Column(Text)  # 正在服用的药物
    additional_info = Column(Text)  # 补充信息
    
    # AI相关
    ai_response = Column(Text)  # AI回复
    ai_confidence = Column(Float)  # AI置信度
    ai_suggestions = Column(JSON)  # AI建议 ['建议1', '建议2']
    
    # 专家相关
    expert_notes = Column(Text)  # 专家笔记
    expert_diagnosis = Column(Text)  # 专家诊断
    expert_recommendations = Column(Text)  # 专家建议
    prescription = Column(JSON)  # 处方信息
    follow_up_required = Column(Boolean, default=False)  # 是否需要复诊
    follow_up_date = Column(DateTime(timezone=True))  # 复诊时间
    
    # 多媒体内容
    attachments = Column(JSON)  # 附件 [{'type': 'image', 'url': '...'}]
    voice_messages = Column(JSON)  # 语音消息
    video_call_id = Column(String)  # 视频通话ID
    
    # 支付信息
    price = Column(Numeric(8, 2))  # 咨询费用
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    payment_id = Column(String)  # 支付订单号
    paid_at = Column(DateTime(timezone=True))  # 支付时间
    
    # 评价信息
    user_rating = Column(Float)  # 用户评分
    user_feedback = Column(Text)  # 用户反馈
    expert_rating = Column(Float)  # 专家对用户评分
    
    # 管理信息
    priority = Column(Integer, default=0)  # 优先级 0-普通 1-紧急
    tags = Column(JSON)  # 标签 ['慢性病', '复诊']
    admin_notes = Column(Text)  # 管理员备注
    quality_score = Column(Float)  # 质量评分
    
    # 统计信息
    response_time = Column(Integer)  # 专家响应时间（分钟）
    consultation_duration = Column(Integer)  # 咨询持续时间（分钟）
    message_count = Column(Integer, default=0)  # 消息数量
    
    # 时间字段
    started_at = Column(DateTime(timezone=True))  # 咨询开始时间
    completed_at = Column(DateTime(timezone=True))  # 咨询完成时间
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    user = relationship("User", back_populates="consultations")
    expert = relationship("Expert", back_populates="consultations")
    messages = relationship("ConsultationMessage", back_populates="consultation")

    def __repr__(self):
        return f"<Consultation(id={self.id}, type='{self.type}', status='{self.status}')>"


class ConsultationMessage(Base):
    """咨询消息记录"""
    __tablename__ = "consultation_messages"
    
    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id"), nullable=False)
    
    # 消息信息
    sender_type = Column(String, nullable=False)  # user, expert, ai, system
    sender_id = Column(Integer)  # 发送者ID
    message_type = Column(String, default='text')  # text, image, audio, video
    content = Column(Text)  # 消息内容
    attachments = Column(JSON)  # 附件信息
    
    # 状态
    is_read = Column(Boolean, default=False)  # 是否已读
    is_deleted = Column(Boolean, default=False)  # 是否删除
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    consultation = relationship("Consultation", back_populates="messages")