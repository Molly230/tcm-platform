"""
Pydantic schemas for API validation
"""
from .user import (
    User, UserCreate, UserUpdate, UserBase, Token, TokenData, 
    UserLogin, UserRegister, UserPasswordUpdate, UserAdminUpdate,
    UserListItem, UserDetail, UserStats, LoginRequest
)
from .course import (
    Course, CourseCreate, CourseUpdate, CourseBase,
    Lesson, LessonCreate, LessonUpdate, LessonBase,
    Enrollment, EnrollmentCreate, WatchRecord, WatchRecordCreate, WatchRecordUpdate
)
from .expert import Expert, ExpertCreate, ExpertUpdate, ExpertBase
from .consultation import Consultation, ConsultationCreate, ConsultationUpdate, ConsultationBase
from .product import (
    Product, ProductCreate, ProductUpdate, ProductBase, ProductSubmitRequest, ProductAuditRequest,
    CartItem, CartItemCreate, Order, OrderCreate, OrderItem, OrderItemCreate,
    OrderItemCreateData, PaymentData
)

__all__ = [
    "User", "UserCreate", "UserUpdate", "UserBase", "Token", "TokenData", "LoginRequest",
    "Course", "CourseCreate", "CourseUpdate", "CourseBase",
    "Lesson", "LessonCreate", "LessonUpdate", "LessonBase",
    "Enrollment", "EnrollmentCreate", "WatchRecord", "WatchRecordCreate", "WatchRecordUpdate",
    "Expert", "ExpertCreate", "ExpertUpdate", "ExpertBase", 
    "Consultation", "ConsultationCreate", "ConsultationUpdate", "ConsultationBase",
    "Product", "ProductCreate", "ProductUpdate", "ProductBase", "ProductSubmitRequest", "ProductAuditRequest",
    "CartItem", "CartItemCreate", "Order", "OrderCreate", "OrderItem", "OrderItemCreate",
    "OrderItemCreateData", "PaymentData"
]