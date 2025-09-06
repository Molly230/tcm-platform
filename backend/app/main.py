"""
FastAPI main application
"""
import os
import logging
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import time

from app.api.api import api_router
from app.core.config import settings
from app.core.logging_config import setup_logging
from app.core.rate_limiter import RateLimitMiddleware

# 初始化日志系统
setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.PROJECT_VERSION
)

# 请求日志中间件 - 临时禁用异常捕获
def sanitize_url_for_logging(url: str) -> str:
    """清理URL中的敏感信息"""
    import re
    from urllib.parse import urlparse, parse_qs
    
    parsed = urlparse(str(url))
    
    # 敏感参数列表
    sensitive_params = {
        'password', 'token', 'key', 'secret', 'auth', 
        'api_key', 'access_token', 'refresh_token'
    }
    
    # 如果查询参数包含敏感信息，替换为[FILTERED]
    query_params = parse_qs(parsed.query)
    filtered_params = {}
    
    for param, values in query_params.items():
        if any(sensitive_word in param.lower() for sensitive_word in sensitive_params):
            filtered_params[param] = '[FILTERED]'
        else:
            filtered_params[param] = values
    
    # 重构URL
    if filtered_params:
        query_string = '&'.join(f"{k}={v[0] if isinstance(v, list) else v}" 
                               for k, v in filtered_params.items())
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}?{query_string}"
    else:
        clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
    
    return clean_url


@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    
    # 清理URL中的敏感信息
    clean_url = sanitize_url_for_logging(str(request.url))
    
    # 记录请求（不包含敏感信息）
    logger.info(f"请求开始: {request.method} {clean_url}")
    
    response = await call_next(request)
    
    # 计算处理时间
    process_time = time.time() - start_time
    
    # 记录响应
    logger.info(
        f"请求完成: {request.method} {clean_url} "
        f"状态码: {response.status_code} 耗时: {process_time:.3f}s"
    )
    
    return response

# 全局异常处理器
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    # 记录详细错误信息到日志（不包含敏感信息）
    logger.error(
        f"全局异常: {request.method} {request.url.path} - {type(exc).__name__}: {str(exc)}", 
        exc_info=True
    )
    
    # 开发环境返回详细错误，生产环境返回通用错误
    if settings.DEBUG:
        return JSONResponse(
            status_code=500,
            content={
                "detail": f"{type(exc).__name__}: {str(exc)}",
                "type": "internal_server_error"
            }
        )
    else:
        return JSONResponse(
            status_code=500,
            content={
                "detail": "服务器内部错误，请稍后重试",
                "type": "internal_server_error"
            }
        )

# 添加速率限制中间件（生产环境）
if not settings.DEBUG:
    app.add_middleware(RateLimitMiddleware, calls_per_minute=100)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 创建上传目录
os.makedirs("uploads/videos", exist_ok=True)
os.makedirs("uploads/images", exist_ok=True)

# 挂载静态文件
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 包含API路由
app.include_router(api_router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "中医健康服务平台API"}

@app.get("/health")
async def health_check():
    """基础健康检查"""
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/health/detailed")
async def detailed_health_check():
    """详细健康检查"""
    from app.database import engine
    from sqlalchemy import text
    
    health_status = {
        "status": "healthy",
        "timestamp": time.time(),
        "checks": {}
    }
    
    # 检查数据库连接
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        health_status["checks"]["database"] = {"status": "healthy"}
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy", 
            "error": str(e)
        }
    
    # 检查上传目录
    try:
        import os
        upload_dirs = ["uploads/images", "uploads/videos", "uploads/documents"]
        for dir_path in upload_dirs:
            if not os.path.exists(dir_path):
                os.makedirs(dir_path, exist_ok=True)
        health_status["checks"]["storage"] = {"status": "healthy"}
    except Exception as e:
        health_status["status"] = "unhealthy" 
        health_status["checks"]["storage"] = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # 检查配置
    critical_configs = ["SECRET_KEY", "DATABASE_URL"]
    config_status = "healthy"
    config_errors = []
    
    for config in critical_configs:
        value = getattr(settings, config, None)
        if not value or value in ["your-secret-key-change-in-production", "default-video-secret-key"]:
            config_status = "unhealthy"
            config_errors.append(f"{config} not properly configured")
    
    health_status["checks"]["configuration"] = {
        "status": config_status,
        "errors": config_errors if config_errors else None
    }
    
    if config_status == "unhealthy":
        health_status["status"] = "unhealthy"
    
    return health_status

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)