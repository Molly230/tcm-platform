# 前后端字段对照表文档

> **创建时间**: 2025-09-06  
> **最后更新**: 2025-09-06  
> **目的**: 确保前后端数据字段的一致性，避免字段不匹配导致的功能异常

---

## 🚨 重要发现的问题记录

### 已修复的问题
- ✅ **课程分类不匹配**: 前端缺少"逐病精讲"和"全面学医"分类选项
- ✅ **产品状态不匹配**: 前端筛选用错误的`low_stock`值，应为`out_of_stock`
- ✅ **产品表单状态不完整**: 缺少`out_of_stock`状态选项

### 需要继续关注的问题
- ⚠️ **用户枚举值大小写**: 日志显示Models使用大写，Schema期望小写

---

## 📊 枚举字段对照表

### 1. 用户管理 (User)

#### UserRole (用户角色)
| 显示名称 | 后端Models值 | 后端Schema值 | 前端管理界面值 | 状态 |
|---------|-------------|-------------|---------------|------|
| 普通用户 | `USER` | `USER` | `"USER"` | ✅ |
| VIP用户 | `VIP` | `VIP` | `"VIP"` | ✅ |
| 医生用户 | `DOCTOR` | `DOCTOR` | `"DOCTOR"` | ✅ |
| 管理员 | `ADMIN` | `ADMIN` | `"ADMIN"` | ✅ |
| 超级管理员 | `SUPER_ADMIN` | `SUPER_ADMIN` | 缺失 | ⚠️ |

#### UserStatus (用户状态)
| 显示名称 | 后端Models值 | 后端Schema值 | 前端管理界面值 | 状态 |
|---------|-------------|-------------|---------------|------|
| 活跃 | `ACTIVE` | `ACTIVE` | 需检查 | ⚠️ |
| 非活跃 | `INACTIVE` | `INACTIVE` | 需检查 | ⚠️ |
| 已暂停 | `SUSPENDED` | `SUSPENDED` | 需检查 | ⚠️ |
| 已禁用 | `BANNED` | `BANNED` | 需检查 | ⚠️ |

### 2. 课程管理 (Course)

#### CourseCategory (课程分类)
| 显示名称 | 后端Models值 | 后端Schema值 | 前端管理界面值 | 前端用户界面 | 状态 |
|---------|-------------|-------------|---------------|-------------|------|
| 基础理论 | `basic` | `basic` | `"basic"` | 基础课程 | ✅ |
| 四季养生 | `seasonal` | `seasonal` | `"seasonal"` | 基础课程 | ✅ |
| 食疗养生 | `diet` | `diet` | `"diet"` | 基础课程 | ✅ |
| 按摩推拿 | `massage` | `massage` | `"massage"` | 基础课程 | ✅ |
| 中草药 | `herb` | `herb` | `"herb"` | 基础课程 | ✅ |
| 逐病精讲 | `逐病精讲` | `逐病精讲` | `"逐病精讲"` | 专题标签页 | ✅ |
| 全面学医 | `全面学医` | `全面学医` | `"全面学医"` | 专题标签页 | ✅ |

### 3. 产品管理 (Product)

#### ProductCategory (产品分类)
| 显示名称 | 后端Models值 | 后端Schema值 | 前端管理界面值 | 状态 |
|---------|-------------|-------------|---------------|------|
| 产品 | `产品` | `产品` | 需检查 | ⚠️ |

#### ProductStatus (产品状态)
| 显示名称 | 后端Models值 | 后端Schema值 | 前端筛选值 | 前端表单值 | 状态 |
|---------|-------------|-------------|-----------|-----------|------|
| 在售 | `active` | `active` | `"active"` | `"active"` | ✅ |
| 下架 | `inactive` | `inactive` | `"inactive"` | `"inactive"` | ✅ |
| 缺货 | `out_of_stock` | `out_of_stock` | `"out_of_stock"` | `"out_of_stock"` | ✅ |

#### AuditStatus (审核状态)
| 显示名称 | 后端Models值 | 后端Schema值 | 前端界面值 | 状态 |
|---------|-------------|-------------|-----------|------|
| 待审核 | `pending` | `pending` | 需检查 | ⚠️ |
| 审核通过 | `approved` | `approved` | 需检查 | ⚠️ |
| 审核拒绝 | `rejected` | `rejected` | 需检查 | ⚠️ |
| 需要修改 | `revision` | `revision` | 需检查 | ⚠️ |

### 4. 订单管理 (Order)

#### OrderStatus (订单状态)
| 显示名称 | 后端Models值 | 后端Schema值 | 前端界面值 | 状态 |
|---------|-------------|-------------|-----------|------|
| 待支付 | `pending_payment` | `pending_payment` | 需检查 | ⚠️ |
| 已支付 | `paid` | `paid` | 需检查 | ⚠️ |
| 处理中 | `processing` | `processing` | 需检查 | ⚠️ |
| 已发货 | `shipped` | `shipped` | 需检查 | ⚠️ |
| 已送达 | `delivered` | `delivered` | 需检查 | ⚠️ |
| 已取消 | `cancelled` | `cancelled` | 需检查 | ⚠️ |
| 已退款 | `refunded` | `refunded` | 需检查 | ⚠️ |

#### PaymentMethod (支付方式)
| 显示名称 | 后端Models值 | 后端Schema值 | 前端界面值 | 状态 |
|---------|-------------|-------------|-----------|------|
| 微信支付 | `wechat_pay` | `wechat_pay` | 需检查 | ⚠️ |
| 支付宝 | `alipay` | `alipay` | 需检查 | ⚠️ |
| 银联支付 | `union_pay` | `union_pay` | 需检查 | ⚠️ |
| 数字人民币 | `digital_currency` | `digital_currency` | 需检查 | ⚠️ |

### 5. 视频/课时管理 (Lesson)

#### VideoStatus (视频状态)
| 显示名称 | 后端Models值 | 后端Schema值 | 前端界面值 | 状态 |
|---------|-------------|-------------|-----------|------|
| 处理中 | `processing` | `processing` | 需检查 | ⚠️ |
| 就绪 | `ready` | `ready` | 需检查 | ⚠️ |
| 错误 | `error` | `error` | 需检查 | ⚠️ |

---

## 🔧 文件路径对照

### 后端文件
- **Models**: `backend/app/models/`
  - `user.py` - 用户相关模型
  - `course.py` - 课程相关模型
  - `product.py` - 产品相关模型
  
- **Schemas**: `backend/app/schemas/`
  - `user.py` - 用户相关Schema
  - `course.py` - 课程相关Schema
  - `product.py` - 产品相关Schema

### 前端文件
- **管理界面**: `frontend/src/views/admin/`
  - `UserManagement.vue` - 用户管理
  - `CourseManagement.vue` - 课程管理
  - `ProductManagement.vue` - 产品管理
  - `AdminDashboard.vue` - 管理仪表板
  
- **用户界面**: `frontend/src/views/`
  - `CoursesView.vue` - 课程展示
  - `ProductsView.vue` - 产品展示

---

## 📝 更新记录

### 2025-09-06
- ✅ 创建初始字段对照表
- ✅ 修复课程分类不匹配问题
- ✅ 修复产品状态不匹配问题
- ⚠️ 发现用户枚举值潜在问题，需进一步调查

---

## 🚀 下一步计划

1. **创建自动化字段一致性检查脚本**
2. **完善所有枚举值的前端界面检查**
3. **建立字段变更的版本控制流程**
4. **增加API响应字段的自动验证**

---

## ⚠️ 重要提醒

**在修改任何枚举值之前，请务必：**
1. 更新此文档
2. 运行字段一致性检查脚本
3. 测试相关的前后端功能
4. 更新相关的API文档

**字段不匹配可能导致的问题：**
- 用户无法正常登录或权限验证失败
- 数据筛选和显示异常
- 表单提交失败
- 业务逻辑错误执行