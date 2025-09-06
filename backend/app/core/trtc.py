"""
腾讯云TRTC服务
"""
import time
import hmac
import hashlib
import base64
import json
from typing import Dict, Any
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.trtc.v20190722 import trtc_client, models
from app.core.config import settings


class TRTCService:
    """腾讯云TRTC服务类"""
    
    def __init__(self):
        self.secret_id = settings.TENCENT_SECRET_ID
        self.secret_key = settings.TENCENT_SECRET_KEY
        self.sdk_app_id = settings.TRTC_SDK_APP_ID
        self.key = settings.TRTC_KEY
        
        # 初始化腾讯云客户端
        cred = credential.Credential(self.secret_id, self.secret_key)
        http_profile = HttpProfile()
        http_profile.endpoint = "trtc.tencentcloudapi.com"
        client_profile = ClientProfile()
        client_profile.httpProfile = http_profile
        self.client = trtc_client.TrtcClient(cred, "ap-beijing", client_profile)
    
    def generate_user_sig(self, user_id: str, expire: int = 86400 * 7) -> str:
        """
        生成UserSig签名
        
        Args:
            user_id: 用户ID
            expire: 签名有效期，默认7天
            
        Returns:
            UserSig签名字符串
        """
        current_time = int(time.time())
        signature_expired = current_time + expire
        
        # 构造签名内容
        content = {
            "TLS.ver": "2.0",
            "TLS.identifier": user_id,
            "TLS.sdkappid": int(self.sdk_app_id),
            "TLS.expire": expire,
            "TLS.time": current_time,
            "TLS.sig": ""
        }
        
        # 生成签名
        def hmac_sha256(key: bytes, msg: str) -> bytes:
            return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()
        
        # 第一步：生成字符串
        content_str = f"TLS.identifier:{user_id}\n"
        content_str += f"TLS.sdkappid:{self.sdk_app_id}\n"
        content_str += f"TLS.time:{current_time}\n"
        content_str += f"TLS.expire:{expire}\n"
        
        # 第二步：使用HMAC-SHA256算法签名
        signature = hmac_sha256(self.key.encode('utf-8'), content_str)
        
        # 第三步：签名结果进行Base64编码
        content["TLS.sig"] = base64.b64encode(signature).decode('utf-8')
        
        # 第四步：整个JSON进行Base64编码
        json_str = json.dumps(content, separators=(',', ':'))
        user_sig = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        
        return user_sig
    
    def create_room(self, room_id: str, user_id: str) -> Dict[str, Any]:
        """
        创建TRTC房间
        
        Args:
            room_id: 房间ID
            user_id: 用户ID
            
        Returns:
            房间信息
        """
        try:
            req = models.CreateTroubleInfoRequest()
            params = {
                "SdkAppId": self.sdk_app_id,
                "RoomId": room_id,
                "UserId": user_id
            }
            req.from_json_string(json.dumps(params))
            
            resp = self.client.CreateTroubleInfo(req)
            
            return {
                "room_id": room_id,
                "user_id": user_id,
                "user_sig": self.generate_user_sig(user_id),
                "sdk_app_id": self.sdk_app_id,
                "created_at": int(time.time())
            }
        except Exception as e:
            print(f"创建TRTC房间失败: {e}")
            return {
                "room_id": room_id,
                "user_id": user_id,
                "user_sig": self.generate_user_sig(user_id),
                "sdk_app_id": self.sdk_app_id,
                "created_at": int(time.time())
            }
    
    def dismiss_room(self, room_id: str) -> bool:
        """
        解散TRTC房间
        
        Args:
            room_id: 房间ID
            
        Returns:
            是否成功
        """
        try:
            req = models.DismissRoomRequest()
            params = {
                "SdkAppId": self.sdk_app_id,
                "RoomId": int(room_id) if room_id.isdigit() else hash(room_id) % (2**31)
            }
            req.from_json_string(json.dumps(params))
            
            resp = self.client.DismissRoom(req)
            return True
        except Exception as e:
            print(f"解散TRTC房间失败: {e}")
            return False
    
    def get_room_users(self, room_id: str) -> list:
        """
        获取房间内用户列表
        
        Args:
            room_id: 房间ID
            
        Returns:
            用户列表
        """
        try:
            req = models.DescribeRoomInfoRequest()
            params = {
                "SdkAppId": self.sdk_app_id,
                "RoomId": int(room_id) if room_id.isdigit() else hash(room_id) % (2**31),
                "StartTime": int(time.time()) - 3600,  # 最近1小时
                "EndTime": int(time.time())
            }
            req.from_json_string(json.dumps(params))
            
            resp = self.client.DescribeRoomInfo(req)
            return []
        except Exception as e:
            print(f"获取房间用户失败: {e}")
            return []


# 全局TRTC服务实例
trtc_service = TRTCService()