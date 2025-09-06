"""
Application configuration
"""
import os
from typing import List
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 项目基本信息
    PROJECT_NAME: str = "中医健康服务平台"
    PROJECT_VERSION: str = "1.0.0"
    PROJECT_DESCRIPTION: str = "中医健康服务平台后端API"
    
    # 数据库配置
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "sqlite:///./tcm_backend.db"  # 开发环境默认使用SQLite
    )
    
    # JWT配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # 腾讯云配置
    TENCENT_SECRET_ID: str = os.getenv("TENCENT_SECRET_ID", "")
    TENCENT_SECRET_KEY: str = os.getenv("TENCENT_SECRET_KEY", "")
    TRTC_SDK_APP_ID: str = os.getenv("TRTC_SDK_APP_ID", "")
    TRTC_KEY: str = os.getenv("TRTC_KEY", "")
    
    # 腾讯云点播配置
    VOD_SUB_APP_ID: str = os.getenv("VOD_SUB_APP_ID", "")
    VOD_DOMAIN: str = os.getenv("VOD_DOMAIN", "")
    
    # 视频安全配置
    VIDEO_SECRET_KEY: str = os.getenv("VIDEO_SECRET_KEY", "default-video-secret-key")
    VIDEO_DOMAIN: str = os.getenv("VIDEO_DOMAIN", "your-video-domain.com")
    VIDEO_TOKEN_EXPIRE: int = 3600  # 视频token过期时间（秒）
    
    # 支付配置
    ALIPAY_APP_ID: str = os.getenv("ALIPAY_APP_ID", "")
    ALIPAY_PRIVATE_KEY: str = os.getenv("ALIPAY_PRIVATE_KEY", "")
    ALIPAY_PUBLIC_KEY: str = os.getenv("ALIPAY_PUBLIC_KEY", "")
    
    WECHAT_APP_ID: str = os.getenv("WECHAT_APP_ID", "")
    WECHAT_MCH_ID: str = os.getenv("WECHAT_MCH_ID", "")
    WECHAT_API_KEY: str = os.getenv("WECHAT_API_KEY", "")
    
    # 服务器配置
    SERVER_HOST: str = os.getenv("SERVER_HOST", "http://localhost:8000")
    
    # 调试模式
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS配置
    CORS_ORIGINS: str = os.getenv(
        "CORS_ORIGINS", 
        "http://localhost:3000,http://localhost:8080,http://localhost:5173"
    )
    
    @property
    def BACKEND_CORS_ORIGINS(self) -> List[str]:
        """动态获取CORS origins"""
        if self.DEBUG:
            # 开发环境
            return [
                "http://localhost:3000",
                "http://localhost:8080", 
                "http://localhost:5173",
            ]
        else:
            # 生产环境，从环境变量读取
            return [origin.strip() for origin in self.CORS_ORIGINS.split(",") if origin.strip()]
    
    class Config:
        env_file = ".env"

settings = Settings()