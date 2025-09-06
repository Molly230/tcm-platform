"""
专家模型
"""
from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Enum, Boolean, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class ExpertCategory(str, enum.Enum):
    INTERNAL = "internal"  # 中医内科
    GYNECOLOGY = "gynecology"  # 中医妇科
    PEDIATRICS = "pediatrics"  # 中医儿科
    ACUPUNCTURE = "acupuncture"  # 针灸推拿
    HEALTH = "health"  # 中医养生
    TRADITIONAL_CHINESE_MEDICINE = "tcm"  # 传统中医
    ORTHOPEDICS = "orthopedics"  # 中医骨科
    DERMATOLOGY = "dermatology"  # 中医皮肤科

class ExpertLevel(str, enum.Enum):
    JUNIOR = "junior"  # 初级医师
    INTERMEDIATE = "intermediate"  # 中级医师
    SENIOR = "senior"  # 高级医师
    CHIEF = "chief"  # 主任医师

class ExpertStatus(str, enum.Enum):
    ACTIVE = "active"  # 在线
    BUSY = "busy"  # 忙碌
    OFFLINE = "offline"  # 离线
    ON_VACATION = "on_vacation"  # 休假

class Expert(Base):
    __tablename__ = "experts"

    id = Column(Integer, primary_key=True, index=True)
    
    # 基本信息
    name = Column(String, nullable=False, index=True)
    title = Column(String)  # 职称: 主任医师、副主任医师等
    level = Column(Enum(ExpertLevel), default=ExpertLevel.JUNIOR)
    category = Column(Enum(ExpertCategory), nullable=False)
    avatar_url = Column(String)
    description = Column(Text)
    
    # 专业信息
    specialties = Column(JSON)  # 专业领域 ['消化系统', '呼吸系统']
    qualifications = Column(JSON)  # 资质认证 ['执业医师证', '主任医师证']
    education = Column(Text)  # 教育背景
    experience_years = Column(Integer, default=0)  # 从业年限
    hospital_affiliation = Column(String)  # 所属医院
    department = Column(String)  # 科室
    
    # 服务信息
    services_offered = Column(JSON)  # 提供的服务类型 ['text', 'voice', 'video']
    text_price = Column(Float)  # 文字咨询价格
    voice_price = Column(Float)  # 语音咨询价格
    video_price = Column(Float)  # 视频咨询价格
    
    # 工作时间
    working_hours = Column(JSON)  # 工作时间 {'monday': ['09:00-12:00', '14:00-17:00']}
    timezone = Column(String, default='Asia/Shanghai')
    
    # 统计信息
    rating = Column(Float, default=0.0)  # 评分
    consultation_count = Column(Integer, default=0)  # 咨询次数
    total_rating_count = Column(Integer, default=0)  # 评价总数
    response_time = Column(Integer, default=30)  # 平均响应时间（分钟）
    
    # 状态
    status = Column(Enum(ExpertStatus), default=ExpertStatus.OFFLINE)
    is_active = Column(Boolean, default=True)  # 是否启用
    is_verified = Column(Boolean, default=False)  # 是否认证
    is_featured = Column(Boolean, default=False)  # 是否推荐专家
    
    # 联系信息
    phone = Column(String)
    email = Column(String)
    wechat = Column(String)
    
    # 个人介绍
    personal_statement = Column(Text)  # 个人陈述
    treatment_philosophy = Column(Text)  # 治疗理念
    successful_cases = Column(Text)  # 成功案例
    
    # 时间字段
    last_online = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    consultations = relationship("Consultation", back_populates="expert")
    schedules = relationship("ExpertSchedule", back_populates="expert")

    def __repr__(self):
        return f"<Expert(id={self.id}, name='{self.name}', category='{self.category}')>"


class ExpertSchedule(Base):
    """专家排班表"""
    __tablename__ = "expert_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    expert_id = Column(Integer, ForeignKey("experts.id"), nullable=False)
    
    # 排班信息
    date = Column(DateTime(timezone=True), nullable=False)  # 排班日期
    start_time = Column(String, nullable=False)  # 开始时间 "09:00"
    end_time = Column(String, nullable=False)  # 结束时间 "17:00"
    max_consultations = Column(Integer, default=10)  # 最大咨询数
    current_consultations = Column(Integer, default=0)  # 当前咨询数
    
    is_available = Column(Boolean, default=True)  # 是否可预约
    notes = Column(Text)  # 备注
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # 关系
    expert = relationship("Expert", back_populates="schedules")


class ExpertReview(Base):
    """专家评价"""
    __tablename__ = "expert_reviews"
    
    id = Column(Integer, primary_key=True, index=True)
    expert_id = Column(Integer, ForeignKey("experts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    consultation_id = Column(Integer, ForeignKey("consultations.id"))
    
    # 评价内容
    rating = Column(Float, nullable=False)  # 1-5分
    comment = Column(Text)  # 评价内容
    service_attitude = Column(Float)  # 服务态度评分
    professional_level = Column(Float)  # 专业水平评分
    response_speed = Column(Float)  # 响应速度评分
    
    # 管理
    is_anonymous = Column(Boolean, default=False)  # 是否匿名
    is_published = Column(Boolean, default=True)  # 是否显示
    admin_reply = Column(Text)  # 管理员回复
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # 关系
    expert = relationship("Expert")
    user = relationship("User")
    consultation = relationship("Consultation")