"""
用户相关的Pydantic模型
"""
from pydantic import BaseModel, EmailStr, validator
from typing import Optional, List
from datetime import datetime
from app.core.enums_v2 import UserRole, UserStatus

# 用户注册
class UserRegister(BaseModel):
    email: EmailStr
    username: str
    password: str
    confirm_password: str
    phone: Optional[str] = None
    full_name: Optional[str] = None
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('用户名至少需要3个字符')
        if len(v) > 20:
            raise ValueError('用户名不能超过20个字符')
        return v
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('密码至少需要6个字符')
        return v
    
    @validator('confirm_password')
    def validate_confirm_password(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('两次输入的密码不一致')
        return v

# 用户登录
class UserLogin(BaseModel):
    email_or_username: str
    password: str

# 为了向后兼容
LoginRequest = UserLogin

# 用户基础信息
class UserBase(BaseModel):
    email: EmailStr
    username: str
    phone: Optional[str] = None
    full_name: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[datetime] = None
    bio: Optional[str] = None

# 用户创建（管理员用）
class UserCreate(UserBase):
    password: str
    role: UserRole = UserRole.USER
    status: UserStatus = UserStatus.ACTIVE

# 用户更新
class UserUpdate(BaseModel):
    username: Optional[str] = None
    phone: Optional[str] = None
    full_name: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    birthday: Optional[datetime] = None
    bio: Optional[str] = None

# 用户密码更新
class UserPasswordUpdate(BaseModel):
    old_password: str
    new_password: str
    confirm_password: str
    
    @validator('new_password')
    def validate_new_password(cls, v):
        if len(v) < 6:
            raise ValueError('密码至少需要6个字符')
        return v
    
    @validator('confirm_password')
    def validate_confirm_password(cls, v, values):
        if 'new_password' in values and v != values['new_password']:
            raise ValueError('两次输入的密码不一致')
        return v

# 管理员用户更新
class UserAdminUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[UserRole] = None
    status: Optional[UserStatus] = None
    is_active: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_phone_verified: Optional[bool] = None

# 用户响应
class User(UserBase):
    id: int
    role: UserRole
    status: UserStatus
    is_active: bool
    is_verified: bool
    is_phone_verified: Optional[bool] = None
    is_admin: bool = False
    is_super_admin: bool = False
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        use_enum_values = True  # 使用枚举的值而不是名称
        from_attributes = True  # 从SQLAlchemy模型读取

    @validator('is_admin', always=True)
    def compute_is_admin(cls, v, values):
        role = values.get('role')
        return role in [UserRole.ADMIN, UserRole.SUPER_ADMIN] if role else False
    
    @validator('is_super_admin', always=True)
    def compute_is_super_admin(cls, v, values):
        role = values.get('role')
        return role == UserRole.SUPER_ADMIN if role else False

    class Config:
        from_attributes = True

# 用户详细信息（包含敏感信息）
class UserDetail(User):
    is_superuser: bool = False
    
    @validator('is_superuser', always=True)
    def compute_is_superuser(cls, v, values):
        # is_superuser 与 is_super_admin 相同
        role = values.get('role')
        return role == UserRole.SUPER_ADMIN if role else False

# 用户列表项
class UserListItem(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str] = None
    role: UserRole
    status: UserStatus
    is_active: bool
    last_login: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

# 令牌
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    user: User

class TokenData(BaseModel):
    email: Optional[str] = None
    user_id: Optional[int] = None

# 用户统计
class UserStats(BaseModel):
    total_users: int
    active_users: int
    new_users_today: int
    verified_users: int