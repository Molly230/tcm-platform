# 枚举值定义和命名规范

> **创建时间**: 2025-09-06  
> **目的**: 统一前后端枚举值的定义、命名和使用规范，避免字段不匹配问题

---

## 🎯 核心原则

### 1. 一致性原则
- **前后端必须使用相同的枚举值**
- **大小写必须完全一致**
- **命名风格必须统一**

### 2. 可维护性原则
- **集中定义，避免重复**
- **使用有意义的英文名称作为键**
- **支持国际化的中文显示**

### 3. 扩展性原则
- **预留扩展空间**
- **向后兼容**
- **支持业务发展**

---

## 📋 标准枚举值定义

### 1. 用户管理枚举

#### UserRole (用户角色)
```python
# 后端定义 (backend/app/models/user.py & backend/app/schemas/user.py)
class UserRole(str, Enum):
    USER = "USER"                 # 普通用户
    VIP = "VIP"                   # VIP用户  
    DOCTOR = "DOCTOR"             # 医生用户
    ADMIN = "ADMIN"               # 管理员
    SUPER_ADMIN = "SUPER_ADMIN"   # 超级管理员
```

```vue
<!-- 前端使用 (UserManagement.vue) -->
<el-option label="普通用户" value="USER" />
<el-option label="VIP用户" value="VIP" />
<el-option label="医生用户" value="DOCTOR" />
<el-option label="管理员" value="ADMIN" />
<el-option label="超级管理员" value="SUPER_ADMIN" />
```

#### UserStatus (用户状态)
```python
# 后端定义
class UserStatus(str, Enum):
    ACTIVE = "ACTIVE"         # 活跃状态
    INACTIVE = "INACTIVE"     # 非活跃状态
    SUSPENDED = "SUSPENDED"   # 已暂停
    BANNED = "BANNED"         # 已禁用
```

```vue
<!-- 前端使用 -->
<el-option label="活跃" value="ACTIVE" />
<el-option label="非活跃" value="INACTIVE" />
<el-option label="已暂停" value="SUSPENDED" />
<el-option label="已禁用" value="BANNED" />
```

**⚠️ 发现问题**: 前端UserManagement.vue缺少`SUSPENDED`状态选项

### 2. 课程管理枚举

#### CourseCategory (课程分类)
```python
# 后端定义
class CourseCategory(str, Enum):
    BASIC = "basic"                    # 基础理论
    SEASONAL = "seasonal"              # 四季养生
    DIET = "diet"                     # 食疗养生
    MASSAGE = "massage"               # 按摩推拿
    HERB = "herb"                     # 中草药
    DISEASE_FOCUSED = "逐病精讲"       # 逐病精讲
    COMPREHENSIVE = "全面学医"         # 全面学医
```

```vue
<!-- 前端使用 -->
<el-option label="基础理论" value="basic" />
<el-option label="四季养生" value="seasonal" />
<el-option label="食疗养生" value="diet" />
<el-option label="按摩推拿" value="massage" />
<el-option label="中草药" value="herb" />
<el-option label="逐病精讲" value="逐病精讲" />
<el-option label="全面学医" value="全面学医" />
```

**✅ 已修复**: 前端已添加缺失的"逐病精讲"和"全面学医"分类

### 3. 产品管理枚举

#### ProductCategory (产品分类) - 需要扩展
```python
# 当前后端定义（过于简化）
class ProductCategory(str, Enum):
    PRODUCT = "产品"
```

**🚨 建议修改为**:
```python
# 建议的新定义
class ProductCategory(str, Enum):
    HERBS = "中草药"              # 中草药
    HEALTH_PRODUCTS = "保健产品"   # 保健产品
    MEDICAL_DEVICES = "医疗器械"   # 医疗器械
    HEALTH_FOODS = "健康食品"      # 健康食品
    TCM_BOOKS = "中医书籍"        # 中医书籍
    OTHER_PRODUCTS = "其他产品"    # 其他产品
```

#### ProductStatus (产品状态)
```python
# 后端定义
class ProductStatus(str, Enum):
    ACTIVE = "active"           # 在售
    INACTIVE = "inactive"       # 下架
    OUT_OF_STOCK = "out_of_stock"  # 缺货
```

```vue
<!-- 前端使用 -->
<el-option label="在售" value="active" />
<el-option label="下架" value="inactive" />
<el-option label="缺货" value="out_of_stock" />
```

**✅ 已修复**: 前端已统一使用`out_of_stock`替代`low_stock`

#### AuditStatus (审核状态)
```python
# 后端定义
class AuditStatus(str, Enum):
    PENDING = "pending"       # 待审核
    APPROVED = "approved"     # 审核通过
    REJECTED = "rejected"     # 审核拒绝
    REVISION = "revision"     # 需要修改
```

**⚠️ 需要检查**: 前端是否有相应的审核状态选项

### 4. 订单管理枚举

#### OrderStatus (订单状态)
```python
# 后端定义
class OrderStatus(str, Enum):
    PENDING_PAYMENT = "pending_payment"  # 待支付
    PAID = "paid"                       # 已支付
    PROCESSING = "processing"           # 处理中
    SHIPPED = "shipped"                 # 已发货
    DELIVERED = "delivered"             # 已送达
    CANCELLED = "cancelled"             # 已取消
    REFUNDED = "refunded"               # 已退款
```

#### PaymentMethod (支付方式)
```python
# 后端定义
class PaymentMethod(str, Enum):
    WECHAT_PAY = "wechat_pay"         # 微信支付
    ALIPAY = "alipay"                 # 支付宝
    UNION_PAY = "union_pay"           # 银联支付
    DIGITAL_CURRENCY = "digital_currency"  # 数字人民币
```

### 5. 视频/课时枚举

#### VideoStatus (视频状态)
```python
# 后端定义
class VideoStatus(str, Enum):
    PROCESSING = "processing"   # 处理中
    READY = "ready"            # 就绪
    ERROR = "error"            # 错误
```

---

## 🔧 实现规范

### 1. 后端实现规范

#### Models文件 (`backend/app/models/*.py`)
```python
import enum
from sqlalchemy import Enum

class UserRole(str, enum.Enum):
    USER = "USER"
    VIP = "VIP"
    # ... 其他值

# 在Model中使用
class User(Base):
    role = Column(Enum(UserRole), default=UserRole.USER)
```

#### Schemas文件 (`backend/app/schemas/*.py`)
```python
from enum import Enum
from pydantic import BaseModel

class UserRole(str, Enum):
    USER = "USER"  # 必须与Models完全一致
    VIP = "VIP"
    # ... 其他值

class UserBase(BaseModel):
    role: UserRole = UserRole.USER
```

### 2. 前端实现规范

#### Vue组件中使用
```vue
<template>
  <!-- 下拉选择 -->
  <el-select v-model="form.role">
    <el-option 
      v-for="option in roleOptions" 
      :key="option.value"
      :label="option.label" 
      :value="option.value" 
    />
  </el-select>
  
  <!-- 单选按钮 -->
  <el-radio-group v-model="form.status">
    <el-radio 
      v-for="option in statusOptions"
      :key="option.value"
      :label="option.value"
    >
      {{ option.label }}
    </el-radio>
  </el-radio-group>
</template>

<script setup>
// 集中定义选项数据
const roleOptions = [
  { label: '普通用户', value: 'USER' },
  { label: 'VIP用户', value: 'VIP' },
  { label: '医生用户', value: 'DOCTOR' },
  { label: '管理员', value: 'ADMIN' },
  { label: '超级管理员', value: 'SUPER_ADMIN' }
]

const statusOptions = [
  { label: '活跃', value: 'ACTIVE' },
  { label: '非活跃', value: 'INACTIVE' },
  { label: '已暂停', value: 'SUSPENDED' },
  { label: '已禁用', value: 'BANNED' }
]
</script>
```

---

## 🚨 当前发现的问题

### 1. 需要立即修复的问题

#### UserManagement.vue 缺少 SUSPENDED 状态
```vue
<!-- 需要添加 -->
<el-option label="已暂停" value="SUSPENDED" />
```

#### ProductCategory 需要扩展
后端ProductCategory过于简化，需要扩展以匹配前端的实际需求。

### 2. 需要验证的问题

#### AuditStatus 在前端的使用
需要检查前端是否有审核相关的界面和选项。

#### 订单和支付枚举的前端实现
需要检查订单管理和支付相关页面的枚举值使用。

---

## ✅ 检查清单

### 开发时必须检查的项目：

- [ ] 新增枚举值时，同时更新Models和Schemas
- [ ] 新增枚举值时，同时更新前端所有相关页面
- [ ] 修改枚举值时，检查数据库兼容性
- [ ] 提交代码前运行字段一致性检查脚本
- [ ] 更新此文档记录变更

### 部署时必须检查的项目：

- [ ] 数据库迁移脚本包含枚举值更新
- [ ] API文档更新了新的枚举值
- [ ] 前端构建包含了最新的枚举值
- [ ] 生产环境数据兼容性测试

---

## 📝 变更记录

### 2025-09-06
- ✅ 创建枚举值标准文档
- ✅ 发现UserManagement.vue缺少SUSPENDED状态
- ✅ 发现ProductCategory定义过于简化
- ⚠️ 需要验证AuditStatus和订单相关枚举的前端实现

---

## 🔄 持续改进

### 短期计划 (1周内)
1. 修复UserManagement.vue缺少的SUSPENDED状态选项
2. 扩展ProductCategory枚举定义
3. 验证所有审核和订单相关枚举的前端实现

### 中期计划 (1个月内)
1. 建立枚举值的自动化测试
2. 创建枚举值变更的CI/CD检查
3. 建立枚举值的版本管理机制

### 长期计划 (3个月内)
1. 考虑建立独立的枚举值配置服务
2. 支持枚举值的动态配置和热更新
3. 建立多语言支持的枚举值系统