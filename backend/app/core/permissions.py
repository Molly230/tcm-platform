"""
权限验证和用户角色管理
"""
from typing import Optional, List
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
import jwt
from app.core.config import settings
from app.database import get_db
from app.models import User
from app.models.user import UserRole, UserStatus

security = HTTPBearer()

def verify_token(token: str) -> Optional[dict]:
    """验证JWT token"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except jwt.PyJWTError:
        return None

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """获取当前用户"""
    token = credentials.credentials
    payload = verify_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user_email = payload.get("sub")
    if not user_email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    """获取当前活跃用户"""
    if not current_user.is_active or current_user.status == UserStatus.BANNED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已被禁用"
        )
    
    if current_user.status == UserStatus.SUSPENDED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已被暂停"
        )
    
    if current_user.status == UserStatus.INACTIVE:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户未激活"
        )
    
    return current_user

def require_roles(required_roles: List[UserRole]):
    """要求特定角色权限的装饰器工厂"""
    def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role not in required_roles:
            role_names = [role.value for role in required_roles]
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"需要以下角色之一：{', '.join(role_names)}"
            )
        return current_user
    return role_checker

def require_user_role(current_user: User = Depends(get_current_active_user)):
    """要求用户角色"""
    return current_user  # 已通过 get_current_active_user 验证

def require_vip_role(current_user: User = Depends(get_current_active_user)):
    """要求VIP角色"""
    if current_user.role not in [UserRole.VIP, UserRole.DOCTOR, UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要VIP或更高权限"
        )
    return current_user

def require_doctor_role(current_user: User = Depends(get_current_active_user)):
    """要求医生角色"""
    if current_user.role not in [UserRole.DOCTOR, UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要医生或更高权限"
        )
    return current_user

def require_admin_role(current_user: User = Depends(get_current_active_user)):
    """要求管理员角色"""
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要管理员权限"
        )
    return current_user

def require_super_admin_role(current_user: User = Depends(get_current_active_user)):
    """要求超级管理员角色"""
    if current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="需要超级管理员权限"
        )
    return current_user

# 为了向后兼容，保留旧的函数名
def require_admin(current_user: User = Depends(get_current_user)):
    """要求管理员权限（兼容性）"""
    if not current_user.is_admin and current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user

def require_super_admin(current_user: User = Depends(get_current_user)):
    """要求超级管理员权限（兼容性）"""
    if not current_user.is_super_admin and current_user.role != UserRole.SUPER_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Super admin privileges required"
        )
    return current_user

def check_resource_ownership(current_user: User, resource_user_id: int):
    """检查资源所有权"""
    if current_user.role not in [UserRole.ADMIN, UserRole.SUPER_ADMIN] and current_user.id != resource_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权访问此资源"
        )
    return True