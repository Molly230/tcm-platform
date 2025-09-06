"""
数据库模型初始化文件
"""
from app.database import Base
from .user import User
from .consultation import Consultation, ConsultationMessage, ConsultationStatus, PaymentStatus
from .course import Course, Lesson, Enrollment, WatchRecord, VideoStatus
from .expert import Expert, ExpertSchedule, ExpertReview
from .product import Product, CartItem, Order, OrderItem, Payment, OrderStatus, PaymentMethod

__all__ = [
    "Base", "User", 
    "Consultation", "ConsultationMessage", "ConsultationStatus", "PaymentStatus",
    "Course", "Lesson", "Enrollment", "WatchRecord", "VideoStatus",
    "Expert", "ExpertSchedule", "ExpertReview",
    "Product", "CartItem", "Order", "OrderItem", "Payment", "OrderStatus", "PaymentMethod"
]