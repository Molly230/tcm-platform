"""
用户模型
"""
from sqlalchemy import Column, Integer, String, DateTime, Boolean, Text, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    USER = "USER"           # 普通用户
    VIP = "VIP"            # VIP用户
    DOCTOR = "DOCTOR"      # 医生
    ADMIN = "ADMIN"        # 管理员
    SUPER_ADMIN = "SUPER_ADMIN"  # 超级管理员

class UserStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"      # 活跃
    INACTIVE = "INACTIVE"  # 未激活
    SUSPENDED = "SUSPENDED"  # 暂停
    BANNED = "BANNED"      # 封禁

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    
    # 基础信息
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    phone = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    
    # 个人信息
    full_name = Column(String)
    avatar = Column(String)  # 头像URL
    gender = Column(String)  # male, female, other
    birthday = Column(DateTime)
    bio = Column(Text)  # 个人简介
    
    # 账户状态
    role = Column(Enum(UserRole), default=UserRole.USER, nullable=False)
    status = Column(Enum(UserStatus), default=UserStatus.INACTIVE, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)  # 邮箱验证
    is_phone_verified = Column(Boolean, default=False, nullable=False)  # 手机验证
    
    # 时间字段
    last_login = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # 关系
    consultations = relationship("Consultation", back_populates="user")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', username='{self.username}')>"
    
    # 权限检查方法
    def is_admin_user(self) -> bool:
        """检查是否为管理员"""
        return self.role in [UserRole.ADMIN, UserRole.SUPER_ADMIN]
    
    def is_doctor_user(self) -> bool:
        """检查是否为医生"""
        return self.role == UserRole.DOCTOR or self.is_admin_user()
    
    def is_vip_user(self) -> bool:
        """检查是否为VIP用户"""
        return self.role in [UserRole.VIP, UserRole.DOCTOR, UserRole.ADMIN, UserRole.SUPER_ADMIN]
    
    def can_access_admin(self) -> bool:
        """检查是否可以访问管理后台"""
        return self.is_admin_user() and self.status == UserStatus.ACTIVE and self.is_active