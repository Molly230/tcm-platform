"""
视频安全和防盗链服务
"""
import time
import hmac
import hashlib
import base64
import uuid
from typing import Dict, Any, Optional
from app.core.config import settings


class VideoSecurityService:
    """视频安全服务类"""
    
    def __init__(self):
        self.secret_key = settings.VIDEO_SECRET_KEY
        self.domain = settings.VIDEO_DOMAIN
    
    def generate_secure_url(
        self, 
        video_id: str, 
        user_id: str, 
        expire_time: int = 3600,
        watermark: Optional[str] = None
    ) -> str:
        """
        生成带防盗链的安全视频URL
        
        Args:
            video_id: 腾讯云视频ID
            user_id: 用户ID
            expire_time: 过期时间（秒）
            watermark: 水印文字
            
        Returns:
            安全的视频播放URL
        """
        timestamp = int(time.time()) + expire_time
        nonce = str(uuid.uuid4())
        
        # 构造签名字符串
        sign_str = f"{video_id}{user_id}{timestamp}{nonce}{self.secret_key}"
        signature = hashlib.md5(sign_str.encode()).hexdigest()
        
        # 构造播放URL
        base_url = f"https://{self.domain}/video/{video_id}"
        params = {
            'user': user_id,
            'time': timestamp,
            'nonce': nonce,
            'sign': signature
        }
        
        if watermark:
            params['watermark'] = base64.b64encode(watermark.encode()).decode()
        
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        return f"{base_url}?{query_string}"
    
    def verify_video_access(
        self, 
        video_id: str, 
        user_id: str, 
        timestamp: int, 
        nonce: str, 
        signature: str
    ) -> bool:
        """
        验证视频访问权限
        
        Args:
            video_id: 视频ID
            user_id: 用户ID  
            timestamp: 时间戳
            nonce: 随机数
            signature: 签名
            
        Returns:
            是否有访问权限
        """
        # 检查是否过期
        if int(time.time()) > timestamp:
            return False
            
        # 验证签名
        sign_str = f"{video_id}{user_id}{timestamp}{nonce}{self.secret_key}"
        expected_signature = hashlib.md5(sign_str.encode()).hexdigest()
        
        return signature == expected_signature
    
    def generate_token_for_lesson(
        self, 
        lesson_id: int, 
        user_id: str, 
        course_id: int
    ) -> str:
        """
        为特定课程生成访问token
        
        Args:
            lesson_id: 课程ID
            user_id: 用户ID
            course_id: 课程ID
            
        Returns:
            访问token
        """
        timestamp = int(time.time())
        expire_time = timestamp + 7200  # 2小时有效期
        
        token_data = {
            'lesson_id': lesson_id,
            'user_id': user_id,
            'course_id': course_id,
            'timestamp': timestamp,
            'expire': expire_time
        }
        
        # 生成token签名
        token_str = f"{lesson_id}{user_id}{course_id}{timestamp}{expire_time}{self.secret_key}"
        token_hash = hashlib.sha256(token_str.encode()).hexdigest()
        
        # Base64编码
        payload = base64.b64encode(
            f"{lesson_id}:{user_id}:{course_id}:{timestamp}:{expire_time}:{token_hash}".encode()
        ).decode()
        
        return payload
    
    def verify_lesson_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        验证课程访问token
        
        Args:
            token: 访问token
            
        Returns:
            解析后的token数据，验证失败返回None
        """
        try:
            # Base64解码
            decoded = base64.b64decode(token.encode()).decode()
            parts = decoded.split(':')
            
            if len(parts) != 6:
                return None
                
            lesson_id, user_id, course_id, timestamp, expire_time, token_hash = parts
            
            # 检查是否过期
            if int(time.time()) > int(expire_time):
                return None
            
            # 验证签名
            token_str = f"{lesson_id}{user_id}{course_id}{timestamp}{expire_time}{self.secret_key}"
            expected_hash = hashlib.sha256(token_str.encode()).hexdigest()
            
            if token_hash != expected_hash:
                return None
                
            return {
                'lesson_id': int(lesson_id),
                'user_id': user_id,
                'course_id': int(course_id),
                'timestamp': int(timestamp),
                'expire_time': int(expire_time)
            }
            
        except Exception:
            return None


class VideoWatermarkService:
    """视频水印服务"""
    
    @staticmethod
    def generate_user_watermark(user_id: str, username: str) -> str:
        """
        生成用户水印文字
        
        Args:
            user_id: 用户ID
            username: 用户名
            
        Returns:
            水印文字
        """
        timestamp = time.strftime("%Y-%m-%d %H:%M", time.localtime())
        return f"{username} | {user_id} | {timestamp}"
    
    @staticmethod
    def get_watermark_config(user_id: str, username: str) -> Dict[str, Any]:
        """
        获取水印配置
        
        Args:
            user_id: 用户ID
            username: 用户名
            
        Returns:
            水印配置
        """
        watermark_text = VideoWatermarkService.generate_user_watermark(user_id, username)
        
        return {
            "type": "text",
            "content": watermark_text,
            "position": "top-right",
            "opacity": 0.5,
            "font_size": 14,
            "color": "rgba(255,255,255,0.8)",
            "interval": 5  # 每5秒显示一次
        }


# 全局服务实例
video_security_service = VideoSecurityService()
video_watermark_service = VideoWatermarkService()