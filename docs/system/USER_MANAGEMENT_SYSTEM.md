# 用户管理系统实现文档

## 🎉 项目概述

本文档记录了中医健康服务平台用户管理系统的完整实现过程，涵盖了从后端数据模型设计到前端用户界面的全栈开发。

---

## ✅ 完成功能清单

### 1. 设计用户数据模型（后端）

**实现位置**: `backend/app/models/user.py`

#### 核心特性
- **多角色支持**: USER, VIP, DOCTOR, ADMIN, SUPER_ADMIN
- **用户状态管理**: ACTIVE, INACTIVE, SUSPENDED, BANNED
- **完整个人信息**: 姓名、手机、头像、性别、生日、个人简介
- **时间戳跟踪**: 创建时间、更新时间、最后登录时间

#### 数据库结构
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    email VARCHAR UNIQUE NOT NULL,
    username VARCHAR UNIQUE NOT NULL,
    phone VARCHAR UNIQUE,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    avatar VARCHAR,
    gender VARCHAR,
    birthday DATETIME,
    bio TEXT,
    role ENUM('USER', 'VIP', 'DOCTOR', 'ADMIN', 'SUPER_ADMIN') DEFAULT 'USER',
    status ENUM('ACTIVE', 'INACTIVE', 'SUSPENDED', 'BANNED') DEFAULT 'INACTIVE',
    is_active BOOLEAN DEFAULT TRUE,
    is_verified BOOLEAN DEFAULT FALSE,
    is_phone_verified BOOLEAN DEFAULT FALSE,
    last_login DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME
);
```

#### 关键特性
- 邮箱、用户名、手机号唯一性约束
- 索引优化查询性能
- 软删除支持（通过状态字段）
- 兼容性字段保留（is_admin, is_super_admin等）

---

### 2. 实现JWT令牌管理

**实现位置**: `backend/app/core/security.py`

#### 令牌类型
1. **访问令牌** (Access Token)
   - 有效期: 24小时
   - 用途: API访问认证
   - 包含: 用户邮箱、用户ID、过期时间

2. **刷新令牌** (Refresh Token)
   - 有效期: 30天
   - 用途: 延长会话时间
   - 标记: type="refresh"

3. **邮箱验证令牌** (Email Verification Token)
   - 有效期: 1小时
   - 用途: 邮箱验证确认
   - 标记: type="email_verification"

4. **密码重置令牌** (Password Reset Token)
   - 有效期: 30分钟
   - 用途: 密码重置验证
   - 标记: type="password_reset"

#### 核心功能
```python
# 令牌创建
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str
def create_refresh_token(data: dict) -> str
def create_email_verification_token(email: str) -> str
def create_password_reset_token(email: str) -> str

# 令牌验证
def verify_token(token: str) -> Optional[dict]
def verify_password_reset_token(token: str) -> Optional[str]
def verify_email_verification_token(token: str) -> Optional[str]

# 密码处理
def get_password_hash(password: str) -> str
def verify_password(plain_password: str, hashed_password: str) -> bool
```

---

### 3. 创建用户认证API接口

**实现位置**: 
- `backend/app/api/auth.py` - 认证相关接口
- `backend/app/api/users.py` - 用户管理接口

#### 认证接口 (/api/auth/)
1. **POST /register** - 用户注册
   ```json
   {
     "email": "user@example.com",
     "username": "testuser",
     "password": "123456",
     "confirm_password": "123456",
     "full_name": "测试用户",
     "phone": "13888888888"
   }
   ```

2. **POST /login** - 用户登录
   ```json
   {
     "email_or_username": "user@example.com",
     "password": "123456"
   }
   ```

#### 用户管理接口 (/api/users/)
1. **GET /me** - 获取当前用户信息
2. **PUT /me** - 更新当前用户信息
3. **PUT /me/password** - 修改密码
4. **GET /{user_id}** - 获取特定用户信息
5. **PUT /{user_id}** - 管理员更新用户信息
6. **DELETE /{user_id}** - 软删除用户（管理员权限）

#### 输入验证
- 邮箱格式验证
- 用户名长度限制（3-20字符）
- 密码强度要求（最少6字符）
- 重复数据检查（邮箱、用户名、手机号）

---

### 4. 创建登录注册页面（前端）

**实现位置**: `frontend/src/views/LoginView.vue`

#### 界面特性
- **模式切换**: 登录/注册一体化界面
- **响应式设计**: 适配桌面和移动端
- **表单验证**: 实时验证用户输入
- **错误处理**: 友好的错误提示

#### 表单字段
**登录模式**:
- 邮箱地址
- 密码

**注册模式**:
- 用户名 (必填, 3-20字符)
- 真实姓名 (必填)
- 手机号 (可选)
- 邮箱地址 (必填)
- 密码 (必填, 最少6字符)
- 确认密码 (必填)

#### 核心功能
```javascript
// 登录处理
const handleLogin = async () => {
  const response = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email_or_username: form.email,
      password: form.password,
    }),
  })
  // 保存令牌和用户信息到localStorage
  localStorage.setItem('user_token', data.access_token)
  localStorage.setItem('user_data', JSON.stringify(data.user))
}

// 注册处理
const handleRegister = async () => {
  const response = await fetch('/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(registerData),
  })
}
```

---

### 5. 实现权限控制中间件

**实现位置**: `backend/app/core/permissions.py`

#### 权限层级
1. **用户认证**: `get_current_user()` - 验证JWT令牌
2. **活跃用户**: `get_current_active_user()` - 检查用户状态
3. **角色权限**: 基于用户角色的访问控制

#### 权限函数
```python
# 基础权限
def get_current_user() -> User                    # 验证令牌
def get_current_active_user() -> User             # 验证活跃用户

# 角色权限
def require_user_role() -> User                   # 普通用户
def require_vip_role() -> User                    # VIP用户
def require_doctor_role() -> User                 # 医生角色
def require_admin_role() -> User                  # 管理员
def require_super_admin_role() -> User            # 超级管理员

# 灵活权限
def require_roles(roles: List[UserRole])          # 多角色选择
def check_resource_ownership()                    # 资源所有权验证
```

#### 状态检查
- **BANNED**: 账户被禁用，拒绝访问
- **SUSPENDED**: 账户被暂停，拒绝访问
- **INACTIVE**: 账户未激活，拒绝访问
- **ACTIVE**: 正常访问

#### 使用示例
```python
@router.get("/admin-only")
def admin_function(user: User = Depends(require_admin_role)):
    return {"message": "管理员功能"}

@router.get("/vip-content")  
def vip_content(user: User = Depends(require_vip_role)):
    return {"content": "VIP专享内容"}
```

---

### 6. 添加用户状态管理（前端）

**实现位置**: `frontend/src/components/NavigationBar.vue`

#### 状态管理功能
1. **登录状态检测**: 检查localStorage中的令牌和用户数据
2. **用户信息显示**: 导航栏显示用户名和头像
3. **下拉菜单**: 个人资料、订单、课程、退出登录
4. **跨标签页同步**: 监听localStorage变化事件
5. **自动登出**: 令牌过期或用户数据错误时自动清理

#### 界面状态
**未登录状态**:
```html
<el-button type="primary" @click="$router.push('/login')">
  登录 / 注册
</el-button>
```

**已登录状态**:
```html
<el-dropdown @command="handleUserAction">
  <el-button type="text" class="user-dropdown">
    <el-icon><User /></el-icon>
    {{ userData?.username || userData?.full_name || '用户' }}
    <el-icon class="el-icon--right"><ArrowDown /></el-icon>
  </el-button>
  <template #dropdown>
    <el-dropdown-menu>
      <el-dropdown-item command="profile">个人资料</el-dropdown-item>
      <el-dropdown-item command="orders">我的订单</el-dropdown-item>
      <el-dropdown-item command="courses">我的课程</el-dropdown-item>
      <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
    </el-dropdown-menu>
  </template>
</el-dropdown>
```

#### 核心逻辑
```javascript
const checkLoginStatus = () => {
  const token = localStorage.getItem('user_token')
  const userDataStr = localStorage.getItem('user_data')
  
  if (token && userDataStr) {
    userData.value = JSON.parse(userDataStr)
    isLoggedIn.value = true
  } else {
    isLoggedIn.value = false
    userData.value = null
  }
}

// 监听跨标签页状态变化
window.addEventListener('storage', (e) => {
  if (e.key === 'user_token' || e.key === 'user_data') {
    checkLoginStatus()
  }
})
```

---

### 7. 实现用户个人中心页面

**实现位置**: `frontend/src/views/ProfileView.vue`

#### 页面布局
- **左侧菜单**: 用户头像、导航菜单
- **右侧内容**: 对应菜单的功能页面

#### 功能模块
1. **基本信息管理**
   - 用户名、真实姓名、手机号
   - 性别、生日、个人简介
   - 在线编辑、实时保存

2. **账户安全管理**
   - 修改密码功能
   - 原密码验证
   - 新密码确认

3. **扩展模块** (预留)
   - 我的订单
   - 我的课程

#### 表单验证
```javascript
const profileRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度为3-20个字符', trigger: 'blur' }
  ],
  full_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ]
}

const passwordRules = {
  old_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认新密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
}
```

#### API集成
```javascript
// 更新个人资料
const saveProfile = async () => {
  const response = await fetch('/api/users/me', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(profileData)
  })
}

// 修改密码
const changePassword = async () => {
  const response = await fetch('/api/users/me/password', {
    method: 'PUT',
    headers: {
      'Content-Type': 'application/json',
      'Authorization': `Bearer ${token}`
    },
    body: JSON.stringify(passwordData)
  })
}
```

---

### 8. 集成用户系统到现有功能

**实现位置**: 
- `frontend/src/router/index.ts` - 路由守卫
- 各API接口的权限控制集成

#### 路由守卫
```javascript
router.beforeEach((to, from, next) => {
  // 检查是否需要用户认证
  if (to.meta.requiresAuth) {
    const token = localStorage.getItem('user_token')
    const userData = localStorage.getItem('user_data')
    
    if (!token || !userData) {
      next('/login')  // 未登录跳转到登录页
      return
    }
    
    // 检查用户状态
    const user = JSON.parse(userData)
    if (!user.is_active || user.status === 'banned') {
      localStorage.removeItem('user_token')
      localStorage.removeItem('user_data')
      next('/login')
      return
    }
  }
  
  next()
})
```

#### 受保护路由
```javascript
{
  path: '/profile',
  name: 'profile', 
  component: ProfileView,
  meta: { requiresAuth: true }  // 需要登录
}
```

#### API权限集成示例
```python
# 课程管理 - 需要VIP权限
@router.get("/premium-courses")
def get_premium_courses(user: User = Depends(require_vip_role)):
    return get_vip_courses()

# 专家咨询 - 需要医生权限  
@router.post("/consultation/respond")
def respond_consultation(user: User = Depends(require_doctor_role)):
    return create_consultation_response()

# 用户管理 - 需要管理员权限
@router.get("/admin/users")
def manage_users(user: User = Depends(require_admin_role)):
    return get_all_users()
```

---

## 🛠 技术栈和架构

### 后端技术栈
- **FastAPI**: 现代Python Web框架
- **SQLAlchemy**: ORM数据库操作
- **Alembic**: 数据库版本管理
- **Pydantic**: 数据验证和序列化
- **PyJWT**: JWT令牌处理
- **Passlib**: 密码加密（bcrypt）

### 前端技术栈
- **Vue 3**: 渐进式JavaScript框架
- **TypeScript**: 类型安全的JavaScript
- **Element Plus**: Vue 3 UI组件库
- **Vue Router**: 官方路由管理器
- **Pinia**: Vue 3状态管理

### 安全特性
1. **密码安全**: bcrypt哈希算法，盐值随机
2. **令牌安全**: JWT签名验证，时间限制
3. **传输安全**: HTTPS加密传输（生产环境）
4. **权限控制**: 多层权限验证，角色分离
5. **状态检查**: 实时用户状态验证

### 性能优化
1. **数据库索引**: 邮箱、用户名、手机号索引
2. **令牌缓存**: 避免频繁数据库查询
3. **响应式设计**: 移动端适配
4. **代码分割**: 按需加载页面组件

---

## 📁 文件结构

```
backend/
├── app/
│   ├── api/
│   │   ├── auth.py              # 认证接口
│   │   └── users.py             # 用户管理接口
│   ├── core/
│   │   ├── permissions.py       # 权限控制
│   │   └── security.py          # JWT令牌管理
│   ├── models/
│   │   └── user.py              # 用户数据模型
│   └── schemas/
│       └── user.py              # 用户验证模式

frontend/
├── src/
│   ├── components/
│   │   └── NavigationBar.vue    # 导航栏组件
│   ├── views/
│   │   ├── LoginView.vue        # 登录注册页面
│   │   └── ProfileView.vue      # 个人中心页面
│   └── router/
│       └── index.ts             # 路由配置
```

---

## 🚀 部署和使用

### 开发环境启动
```bash
# 后端服务
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 前端服务  
cd frontend
npm run dev
```

### 数据库迁移
```bash
cd backend
alembic upgrade head
```

### 访问地址
- 前端应用: http://localhost:5173
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

---

## 📋 用户使用流程

1. **新用户注册**
   - 访问 `/login` 页面
   - 切换到注册模式
   - 填写必要信息并提交
   - 系统创建用户账户

2. **用户登录**
   - 输入邮箱/用户名和密码
   - 系统验证身份并颁发JWT令牌
   - 自动跳转到首页，导航栏显示用户信息

3. **访问受保护页面**
   - 系统自动检查登录状态
   - 验证用户权限级别
   - 允许访问对应功能模块

4. **管理个人信息**
   - 访问 `/profile` 页面
   - 编辑个人资料
   - 修改账户密码
   - 查看个人数据

5. **退出登录**
   - 点击用户下拉菜单中的"退出登录"
   - 系统清除本地令牌和用户数据
   - 跳转到首页，恢复未登录状态

---

## 🔧 扩展功能建议

1. **邮箱验证**: 注册后发送验证邮件
2. **手机验证**: 短信验证码功能
3. **第三方登录**: 微信、QQ、微博登录
4. **头像上传**: 用户头像管理
5. **登录日志**: 记录登录时间和地点
6. **密码强度**: 更复杂的密码策略
7. **双因子认证**: TOTP或短信二次验证
8. **API限流**: 防止暴力破解攻击

---

## 📊 系统监控指标

- 用户注册转化率
- 登录成功率  
- 令牌有效期利用率
- 权限拒绝统计
- 密码修改频率
- 用户活跃度统计

---

*文档最后更新时间: 2025年9月1日*
*系统版本: v1.0.0*
*作者: Claude Code Assistant*