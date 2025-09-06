"""
用户相关API路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta

from app import models
from app.schemas.user import *
from app.database import get_db
from app.core.security import (
    get_password_hash, 
    verify_password, 
    create_access_token,
    create_refresh_token,
    verify_token,
    create_email_verification_token,
    create_password_reset_token,
    verify_password_reset_token,
    verify_email_verification_token
)
from app.core.permissions import (
    get_current_user, 
    get_current_active_user, 
    require_admin_role,
    require_super_admin_role,
    check_resource_ownership
)

router = APIRouter(tags=["users"])

# 用户注册
@router.post("/register", response_model=User)
def register_user(user_data: UserRegister, db: Session = Depends(get_db)):
    """用户注册"""
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
    db_user = models.User(
        email=user_data.email,
        username=user_data.username,
        phone=user_data.phone,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=models.UserRole.USER,
        status=models.UserStatus.ACTIVE  # 直接激活，实际项目中可能需要邮箱验证
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# 用户登录
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
    if not user.is_active or user.status == models.UserStatus.BANNED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已被禁用"
        )
    
    if user.status == models.UserStatus.SUSPENDED:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="账户已被暂停"
        )
    
    # 更新最后登录时间
    user.last_login = datetime.utcnow()
    db.commit()
    
    # 创建访问令牌
    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "expires_in": 24 * 60 * 60,  # 24小时，单位秒
        "user": user
    }

# OAuth2 登录（兼容性）
@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """OAuth2 登录获取令牌"""
    login_data = UserLogin(
        email_or_username=form_data.username,
        password=form_data.password
    )
    return login_user(login_data, db)

@router.post("/", response_model=User)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    """创建新用户（管理员用）"""
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
    db_user = models.User(
        email=user_data.email,
        username=user_data.username,
        phone=user_data.phone,
        full_name=user_data.full_name,
        hashed_password=hashed_password,
        role=user_data.role,
        status=user_data.status
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@router.get("/", response_model=List[UserListItem])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """获取用户列表"""
    users = db.query(models.User).offset(skip).limit(limit).all()
    return users

@router.get("/me", response_model=UserDetail)
def read_current_user(current_user: models.User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

@router.get("/{user_id}", response_model=User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """获取特定用户"""
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    return db_user

@router.put("/me", response_model=User)
def update_current_user(user_update: UserUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """更新当前用户信息"""
    # 检查用户名是否被其他用户使用
    if user_update.username and user_update.username != current_user.username:
        existing_user = db.query(models.User).filter(
            models.User.username == user_update.username,
            models.User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="用户名已被使用"
            )
    
    # 检查手机号是否被其他用户使用
    if user_update.phone and user_update.phone != current_user.phone:
        existing_user = db.query(models.User).filter(
            models.User.phone == user_update.phone,
            models.User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="手机号已被使用"
            )
    
    # 更新用户信息
    for field, value in user_update.dict(exclude_unset=True).items():
        if hasattr(current_user, field):
            setattr(current_user, field, value)
    
    current_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/me/password")
def change_password(password_data: UserPasswordUpdate, current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    """更改当前用户密码"""
    # 验证旧密码
    if not verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="原密码错误"
        )
    
    # 更新密码
    current_user.hashed_password = get_password_hash(password_data.new_password)
    current_user.updated_at = datetime.utcnow()
    db.commit()
    
    return {"message": "密码更新成功"}

@router.put("/{user_id}", response_model=User)
def update_user(user_id: int, user_update: UserAdminUpdate, current_user: models.User = Depends(require_admin_role), db: Session = Depends(get_db)):
    """管理员更新用户信息"""
    
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 检查邮箱是否被其他用户使用
    if user_update.email and user_update.email != db_user.email:
        existing_user = db.query(models.User).filter(
            models.User.email == user_update.email,
            models.User.id != user_id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="邮箱已被其他用户使用"
            )
    
    # 更新用户信息
    for field, value in user_update.dict(exclude_unset=True).items():
        if hasattr(db_user, field):
            setattr(db_user, field, value)
    
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user

@router.delete("/{user_id}", response_model=User)
def delete_user(user_id: int, current_user: models.User = Depends(require_admin_role), db: Session = Depends(get_db)):
    """删除用户（软删除）"""
    
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    
    # 软删除：设置为非活跃状态
    db_user.is_active = False
    db_user.status = models.UserStatus.BANNED
    db_user.updated_at = datetime.utcnow()
    db.commit()
    
    return db_user