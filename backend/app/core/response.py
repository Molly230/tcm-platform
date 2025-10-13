"""
统一API响应格式
简单、直接、易用
"""
from typing import Any, Optional


class ApiResponse:
    """统一API响应格式"""
    
    @staticmethod
    def success(data: Any = None, message: str = "操作成功"):
        """成功响应"""
        return {
            "success": True,
            "data": data,
            "message": message
        }
    
    @staticmethod
    def error(message: str, code: int = 400, data: Any = None):
        """错误响应"""
        return {
            "success": False,
            "data": data,
            "message": message,
            "code": code
        }
    
    @staticmethod
    def paginate(items: list, total: int, page: int = 1, size: int = 20, message: str = "获取成功"):
        """分页响应"""
        return {
            "success": True,
            "data": {
                "items": items,
                "pagination": {
                    "total": total,
                    "page": page,
                    "size": size,
                    "pages": (total + size - 1) // size
                }
            },
            "message": message
        }


def to_dict(obj, exclude_fields: Optional[list] = None) -> dict:
    """
    将SQLAlchemy模型转为dict，避免复杂的schema
    """
    exclude_fields = exclude_fields or []
    result = {}
    
    for column in obj.__table__.columns:
        field_name = column.name
        if field_name in exclude_fields:
            continue
            
        value = getattr(obj, field_name)
        
        # 处理枚举类型，直接返回值
        if hasattr(value, 'value'):
            result[field_name] = value.value
        else:
            result[field_name] = value
    
    return result


# 便利函数
def success_response(data: Any = None, message: str = "操作成功"):
    """快速创建成功响应"""
    return ApiResponse.success(data, message)

def error_response(message: str, code: int = 400, data: Any = None):
    """快速创建错误响应"""
    return ApiResponse.error(message, code, data)

def user_to_dict(user) -> dict:
    """用户对象转dict，添加便利字段"""
    result = to_dict(user, exclude_fields=['hashed_password'])
    
    # 添加便利字段
    result['is_admin'] = user.role.value in ['ADMIN', 'SUPER_ADMIN']
    result['is_super_admin'] = user.role.value == 'SUPER_ADMIN'
    
    # 处理可能为NULL的bool字段
    if result.get('is_phone_verified') is None:
        result['is_phone_verified'] = False
        
    return result