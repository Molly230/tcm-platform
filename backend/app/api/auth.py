"""
认证相关API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from app import models
from app.models.user import UserRole, UserStatus
from app.schemas.user import UserRegister, UserLogin, Token, User
from app.database import get_db
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token
)
from app.core.validation import (
    validate_password_strength,
    validate_email,
    validate_phone,
    validate_username,
    validate_full_name,
    sanitize_string
)

router = APIRouter(tags=["auth"])

@router.post("/register", response_model=User)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """用户注册"""
    
    # 输入验证
    # 1. 验证邮箱
    is_valid_email, email_msg = validate_email(user_data.email)
    if not is_valid_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=email_msg
        )
    
    # 2. 验证用户名
    is_valid_username, username_msg = validate_username(user_data.username)
    if not is_valid_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=username_msg
        )
    
    # 3. 验证密码强度
    is_valid_password, password_msg = validate_password_strength(user_data.password)
    if not is_valid_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=password_msg
        )
    
    # 4. 验证手机号
    if user_data.phone:
        is_valid_phone, phone_msg = validate_phone(user_data.phone)
        if not is_valid_phone:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=phone_msg
            )
    
    # 5. 验证真实姓名
    if user_data.full_name:
        is_valid_name, name_msg = validate_full_name(user_data.full_name)
        if not is_valid_name:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=name_msg
            )
    
    # 检查邮箱是否已存在
    if db.query(models.User).filter(models.User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱已被注册"
        )
    
    # 检查用户名是否已存在
    if db.query(models.User).filter(models.User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已被使用"
        )
    
    # 检查手机号是否已存在（如果提供）
    if user_data.phone:
        if db.query(models.User).filter(models.User.phone == user_data.phone).first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="手机号已被注册"
            )
    
    # 创建新用户
    hashed_password = get_password_hash(user_data.password)
    
    # 清理用户输入
    clean_email = sanitize_string(user_data.email.lower(), 254)
    clean_username = sanitize_string(user_data.username, 20)
    clean_phone = sanitize_string(user_data.phone, 20) if user_data.phone else None
    clean_full_name = sanitize_string(user_data.full_name, 50) if user_data.full_name else None
    
    db_user = models.User(
        email=clean_email,
        username=clean_username,
        phone=clean_phone,
        full_name=clean_full_name,
        hashed_password=hashed_password,
        role=UserRole.USER,
        status=UserStatus.ACTIVE
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
def login_user(login_data: UserLogin, db: Session = Depends(get_db)):
    """用户登录"""
    # 查找用户（支持邮箱或用户名登录）
    user = None
    if "@" in login_data.email_or_username:
        user = db.query(models.User).filter(models.User.email == login_data.email_or_username).first()
    else:
        user = db.query(models.User).filter(models.User.username == login_data.email_or_username).first()
    
    # 验证用户和密码
    if not user or not verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱/用户名或密码错误"
        )
    
    # 检查用户状态
    if not user.is_active or user.status == UserStatus.BANNED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已被禁用"
        )
    
    if user.status == UserStatus.SUSPENDED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已被暂停"
        )
    
    # 更新最后登录时间
    user.last_login = datetime.now(timezone.utc)
    db.commit()
    
    # 创建访问令牌
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 24 * 60 * 60,  # 24小时，单位秒
        "user": user
    }