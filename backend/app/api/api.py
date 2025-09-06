"""
主API路由文件
"""
from fastapi import APIRouter

from app.api import users, auth, consultations, courses, experts, video, admin, products, orders, reliable_payment, diagnosis, upload

api_router = APIRouter()

# 添加API根路径
@api_router.get("/")
def api_root():
    """API根路径"""
    return {"message": "中医健康服务平台API", "version": "1.0.0"}

# 包含各模块路由
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(consultations.router, prefix="/consultations", tags=["consultations"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(experts.router, prefix="/experts", tags=["experts"])
api_router.include_router(video.router, prefix="/video", tags=["video"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(reliable_payment.router, tags=["可靠支付"])
api_router.include_router(diagnosis.router, tags=["诊断系统"])
api_router.include_router(upload.router, prefix="", tags=["upload"])

# 测试路由
@api_router.get("/health")
def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "API is running"}