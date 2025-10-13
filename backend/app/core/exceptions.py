"""
统一异常处理
"""
from typing import Any, Dict, Optional
from fastapi import HTTPException, status


class TCMException(HTTPException):
    """中医平台基础异常类"""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        headers: Optional[Dict[str, Any]] = None,
        error_code: Optional[str] = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code


# ===== 业务异常 =====

class BusinessException(TCMException):
    """业务逻辑异常"""
    
    def __init__(self, detail: str, error_code: str = "BUSINESS_ERROR"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code
        )


class ValidationException(TCMException):
    """数据验证异常"""
    
    def __init__(self, detail: str, error_code: str = "VALIDATION_ERROR"):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code=error_code
        )


# ===== 权限异常 =====

class AuthenticationException(TCMException):
    """认证异常"""
    
    def __init__(self, detail: str = "认证失败", error_code: str = "AUTH_FAILED"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code=error_code,
            headers={"WWW-Authenticate": "Bearer"}
        )


class PermissionDeniedException(TCMException):
    """权限拒绝异常"""
    
    def __init__(self, detail: str = "权限不足", error_code: str = "PERMISSION_DENIED"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code=error_code
        )


# ===== 资源异常 =====

class NotFoundException(TCMException):
    """资源不存在异常"""
    
    def __init__(self, resource: str = "资源", error_code: str = "NOT_FOUND"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource}不存在",
            error_code=error_code
        )


class ConflictException(TCMException):
    """资源冲突异常"""
    
    def __init__(self, detail: str, error_code: str = "CONFLICT"):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            error_code=error_code
        )


# ===== 文件异常 =====

class FileUploadException(TCMException):
    """文件上传异常"""
    
    def __init__(self, detail: str, error_code: str = "FILE_UPLOAD_ERROR"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code
        )


class FileTooLargeException(TCMException):
    """文件过大异常"""
    
    def __init__(self, max_size: str = "5MB", error_code: str = "FILE_TOO_LARGE"):
        super().__init__(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"文件大小超过限制 ({max_size})",
            error_code=error_code
        )


class UnsupportedFileTypeException(TCMException):
    """不支持的文件类型异常"""
    
    def __init__(self, allowed_types: str = "支持的格式", error_code: str = "UNSUPPORTED_FILE_TYPE"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"不支持的文件类型，{allowed_types}",
            error_code=error_code
        )


# ===== 支付异常 =====

class PaymentException(TCMException):
    """支付异常"""
    
    def __init__(self, detail: str, error_code: str = "PAYMENT_ERROR"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code=error_code
        )


class PaymentFailedException(TCMException):
    """支付失败异常"""
    
    def __init__(self, detail: str = "支付失败", error_code: str = "PAYMENT_FAILED"):
        super().__init__(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail=detail,
            error_code=error_code
        )


# ===== 外部服务异常 =====

class ExternalServiceException(TCMException):
    """外部服务异常"""
    
    def __init__(self, service: str, detail: str = "", error_code: str = "EXTERNAL_SERVICE_ERROR"):
        message = f"{service}服务异常"
        if detail:
            message += f": {detail}"
        
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=message,
            error_code=error_code
        )


class ThirdPartyAPIException(TCMException):
    """第三方API异常"""
    
    def __init__(self, api_name: str, detail: str = "", error_code: str = "THIRD_PARTY_API_ERROR"):
        message = f"{api_name} API调用失败"
        if detail:
            message += f": {detail}"
            
        super().__init__(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=message,
            error_code=error_code
        )


# ===== 数据库异常 =====

class DatabaseException(TCMException):
    """数据库异常"""
    
    def __init__(self, detail: str = "数据库操作失败", error_code: str = "DATABASE_ERROR"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
            error_code=error_code
        )


# ===== 异常处理工具函数 =====

def handle_database_error(error: Exception) -> TCMException:
    """处理数据库错误，转换为统一的异常格式"""
    error_str = str(error).lower()
    
    if "unique" in error_str or "duplicate" in error_str:
        return ConflictException("数据已存在，请检查输入")
    elif "foreign key" in error_str:
        return BusinessException("关联数据不存在")
    elif "not null" in error_str:
        return ValidationException("必填字段不能为空")
    else:
        return DatabaseException(f"数据库操作失败: {str(error)}")


def handle_validation_error(errors: list) -> ValidationException:
    """处理Pydantic验证错误"""
    error_messages = []
    for error in errors:
        loc = " -> ".join(str(l) for l in error.get("loc", []))
        msg = error.get("msg", "验证失败")
        error_messages.append(f"{loc}: {msg}")
    
    return ValidationException("; ".join(error_messages))


# ===== 常用错误响应 =====

class CommonErrors:
    """常用错误响应"""
    
    # 认证相关
    INVALID_CREDENTIALS = AuthenticationException("邮箱/用户名或密码错误")
    TOKEN_EXPIRED = AuthenticationException("登录已过期，请重新登录", "TOKEN_EXPIRED")
    TOKEN_INVALID = AuthenticationException("无效的访问令牌", "TOKEN_INVALID")
    
    # 权限相关
    ADMIN_REQUIRED = PermissionDeniedException("仅限管理员访问", "ADMIN_REQUIRED")
    DOCTOR_REQUIRED = PermissionDeniedException("仅限医生访问", "DOCTOR_REQUIRED")
    OWNER_REQUIRED = PermissionDeniedException("只能操作自己的数据", "OWNER_REQUIRED")
    
    # 资源相关
    USER_NOT_FOUND = NotFoundException("用户", "USER_NOT_FOUND")
    EXPERT_NOT_FOUND = NotFoundException("专家", "EXPERT_NOT_FOUND")
    PRODUCT_NOT_FOUND = NotFoundException("商品", "PRODUCT_NOT_FOUND")
    ORDER_NOT_FOUND = NotFoundException("订单", "ORDER_NOT_FOUND")
    COURSE_NOT_FOUND = NotFoundException("课程", "COURSE_NOT_FOUND")
    
    # 业务逻辑
    EMAIL_ALREADY_EXISTS = ConflictException("邮箱已被注册", "EMAIL_EXISTS")
    USERNAME_ALREADY_EXISTS = ConflictException("用户名已被占用", "USERNAME_EXISTS")
    PHONE_ALREADY_EXISTS = ConflictException("手机号已被注册", "PHONE_EXISTS")
    
    # 订单相关
    ORDER_CANNOT_CANCEL = BusinessException("订单状态不允许取消", "ORDER_CANNOT_CANCEL")
    ORDER_ALREADY_PAID = BusinessException("订单已支付", "ORDER_ALREADY_PAID")
    INSUFFICIENT_STOCK = BusinessException("库存不足", "INSUFFICIENT_STOCK")
    
    # 咨询相关
    CONSULTATION_NOT_AVAILABLE = BusinessException("专家暂不接受咨询", "CONSULTATION_NOT_AVAILABLE")
    CONSULTATION_TIME_CONFLICT = BusinessException("咨询时间冲突", "TIME_CONFLICT")