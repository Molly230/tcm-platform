"""
主API路由文件
"""
from fastapi import APIRouter

from app.api import users, auth, consultations, courses, experts, admin, orders, diagnosis, upload, system, draft_orders, products_simple, simple_orders, cart, wechat_pay

api_router = APIRouter()

# 添加API根路径
@api_router.get("/")
def api_root():
    """API根路径"""
    return {"message": "中医健康服务平台API", "version": "1.0.0"}

# 包含各模块路由 - 核心功能模块
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(consultations.router, prefix="/consultations", tags=["consultations"])
api_router.include_router(courses.router, prefix="/courses", tags=["courses"])
api_router.include_router(experts.router, prefix="/experts", tags=["experts"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
api_router.include_router(products_simple.router, tags=["products-simple"])
api_router.include_router(cart.router, tags=["cart"])
api_router.include_router(orders.router, prefix="/orders", tags=["orders"])
api_router.include_router(wechat_pay.router, tags=["微信支付"])
api_router.include_router(diagnosis.router, tags=["诊断系统"])
api_router.include_router(upload.router, prefix="", tags=["upload"])
api_router.include_router(system.router, prefix="/system", tags=["system"])
api_router.include_router(draft_orders.router, tags=["预订单"])
api_router.include_router(simple_orders.router, tags=["简单订单"])

# 测试路由
@api_router.get("/health")
def health_check():
    """健康检查接口"""
    return {"status": "healthy", "message": "API is running"}