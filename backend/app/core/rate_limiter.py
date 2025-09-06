"""
API速率限制中间件
"""
import time
from collections import defaultdict
from typing import Dict, Optional
from fastapi import Request, HTTPException, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware


class RateLimiter:
    def __init__(self, max_requests: int = 100, window_seconds: int = 60):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests: Dict[str, list] = defaultdict(list)
    
    def is_allowed(self, client_ip: str) -> tuple[bool, Optional[int]]:
        """
        检查IP是否在速率限制内
        返回: (是否允许, 重置时间戳)
        """
        now = time.time()
        window_start = now - self.window_seconds
        
        # 清理过期请求
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] 
            if req_time > window_start
        ]
        
        # 检查当前窗口内的请求数
        if len(self.requests[client_ip]) >= self.max_requests:
            # 计算重置时间
            reset_time = int(self.requests[client_ip][0] + self.window_seconds)
            return False, reset_time
        
        # 记录当前请求
        self.requests[client_ip].append(now)
        return True, None
    
    def get_remaining(self, client_ip: str) -> int:
        """获取剩余请求次数"""
        return max(0, self.max_requests - len(self.requests[client_ip]))


class RateLimitMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, calls_per_minute: int = 100):
        super().__init__(app)
        self.limiter = RateLimiter(max_requests=calls_per_minute, window_seconds=60)
    
    async def dispatch(self, request: Request, call_next):
        # 获取客户端IP
        client_ip = self.get_client_ip(request)
        
        # 检查速率限制
        allowed, reset_time = self.limiter.is_allowed(client_ip)
        
        if not allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "detail": "请求过于频繁，请稍后重试",
                    "retry_after": reset_time - int(time.time()) if reset_time else 60
                },
                headers={
                    "X-RateLimit-Limit": str(self.limiter.max_requests),
                    "X-RateLimit-Remaining": "0",
                    "X-RateLimit-Reset": str(reset_time) if reset_time else "",
                    "Retry-After": str(60)
                }
            )
        
        # 执行请求
        response = await call_next(request)
        
        # 添加速率限制头
        remaining = self.limiter.get_remaining(client_ip)
        response.headers["X-RateLimit-Limit"] = str(self.limiter.max_requests)
        response.headers["X-RateLimit-Remaining"] = str(remaining)
        
        return response
    
    def get_client_ip(self, request: Request) -> str:
        """获取客户端真实IP"""
        # 优先使用代理头
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            return forwarded_for.split(",")[0].strip()
        
        real_ip = request.headers.get("X-Real-IP")
        if real_ip:
            return real_ip
        
        # 最后使用连接IP
        return request.client.host if request.client else "unknown"


# 不同API的速率限制策略
class APIRateLimits:
    # 认证相关API - 更严格的限制
    AUTH_LIMITER = RateLimiter(max_requests=10, window_seconds=60)
    
    # 支付相关API - 非常严格的限制  
    PAYMENT_LIMITER = RateLimiter(max_requests=5, window_seconds=60)
    
    # 文件上传API - 限制上传频率
    UPLOAD_LIMITER = RateLimiter(max_requests=20, window_seconds=60)
    
    # 普通API
    GENERAL_LIMITER = RateLimiter(max_requests=100, window_seconds=60)


def get_rate_limiter(endpoint: str) -> RateLimiter:
    """根据API端点返回对应的速率限制器"""
    if "/auth/" in endpoint:
        return APIRateLimits.AUTH_LIMITER
    elif "/payment/" in endpoint or "/orders/" in endpoint:
        return APIRateLimits.PAYMENT_LIMITER
    elif "/upload/" in endpoint:
        return APIRateLimits.UPLOAD_LIMITER
    else:
        return APIRateLimits.GENERAL_LIMITER