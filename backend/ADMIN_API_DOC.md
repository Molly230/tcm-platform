# 管理员后台API接口文档

## 🔐 认证说明

所有管理员API都需要管理员权限认证。需要在请求头中携带Token：

```
Authorization: Bearer YOUR_ACCESS_TOKEN
```

获取Token的方式：
```bash
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=admin@tcm.com&password=admin123
```

## 📊 数据统计

### 获取平台统计数据
```
GET /api/admin/statistics
```

返回完整的平台运营数据，包括：
- 概览数据（用户、专家、商品、订单、收入）
- 专家统计（分类、状态分布）
- 商品统计（分类、状态分布）
- 订单统计（状态、完成率、收入）
- 咨询统计（类型、状态分布）
- 用户分析（角色分布）
- 最近活动（7天、30天数据）

## 👨‍⚕️ 专家管理

### 获取专家列表
```
GET /api/admin/experts?skip=0&limit=100&status=active&category=internal
```

### 创建专家
```
POST /api/admin/experts
Content-Type: application/json

{
    "name": "专家姓名",
    "title": "主任医师",
    "category": "internal",
    "description": "专家介绍",
    "text_price": 50.0,
    "voice_price": 100.0,
    "video_price": 200.0
}
```

### 更新专家信息
```
PUT /api/admin/experts/{expert_id}
Content-Type: application/json

{
    "name": "新姓名",
    "status": "active"
}
```

### 删除专家
```
DELETE /api/admin/experts/{expert_id}
```

### 获取专家评价
```
GET /api/admin/experts/{expert_id}/reviews?skip=0&limit=50
```

### 获取专家排班
```
GET /api/admin/experts/{expert_id}/schedules?start_date=2025-01-01&end_date=2025-12-31
```

## 🛒 商品管理

### 获取商品列表
```
GET /api/admin/products?skip=0&limit=100&category=中药材&status=active
```

### 创建商品
```
POST /api/admin/products
Content-Type: application/json

{
    "name": "商品名称",
    "description": "商品描述",
    "category": "中药材",
    "price": 99.0,
    "stock_quantity": 100
}
```

### 更新商品
```
PUT /api/admin/products/{product_id}
Content-Type: application/json

{
    "price": 89.0,
    "stock_quantity": 150
}
```

### 删除商品
```
DELETE /api/admin/products/{product_id}
```

## 📦 订单管理

### 获取订单列表
```
GET /api/admin/orders?skip=0&limit=100&status=pending_payment
```

### 获取订单详情
```
GET /api/admin/orders/{order_id}
```

### 更新订单状态
```
PUT /api/admin/orders/{order_id}/status
Content-Type: application/x-www-form-urlencoded

status=shipped&tracking_number=SF1234567890&courier_company=顺丰速递
```

可用状态：
- `pending_payment` - 待支付
- `paid` - 已支付
- `processing` - 处理中
- `shipped` - 已发货
- `delivered` - 已送达
- `cancelled` - 已取消
- `refunded` - 已退款

## 💬 咨询管理

### 获取咨询列表
```
GET /api/admin/consultations?skip=0&limit=100&status=pending&type=text&expert_id=1
```

### 获取咨询详情
```
GET /api/admin/consultations/{consultation_id}
```

### 更新咨询信息
```
PUT /api/admin/consultations/{consultation_id}
Content-Type: application/json

{
    "status": "completed",
    "admin_notes": "管理员备注"
}
```

### 获取咨询消息
```
GET /api/admin/consultations/{consultation_id}/messages?skip=0&limit=100
```

## 👥 用户管理

### 获取用户列表
```
GET /api/admin/users?skip=0&limit=100
```

### 更新用户权限
```
PUT /api/admin/users/{user_id}/role
Content-Type: application/x-www-form-urlencoded

is_admin=true
```

## 🎓 课程管理

### 获取所有课程
```
GET /api/admin/courses?skip=0&limit=100
```

### 创建课程
```
POST /api/admin/courses
Content-Type: application/json

{
    "title": "课程标题",
    "description": "课程描述",
    "category": "basic",
    "price": 99.0,
    "instructor": "讲师姓名"
}
```

### 更新课程
```
PUT /api/admin/courses/{course_id}
Content-Type: application/json

{
    "title": "新标题",
    "is_published": true
}
```

### 删除课程
```
DELETE /api/admin/courses/{course_id}
```

### 课时管理
```
GET /api/admin/courses/{course_id}/lessons
POST /api/admin/courses/{course_id}/lessons
PUT /api/admin/lessons/{lesson_id}
DELETE /api/admin/lessons/{lesson_id}
```

## 📁 文件上传

### 上传视频
```
POST /api/admin/upload/video
Content-Type: multipart/form-data

file: 视频文件 (最大1GB，支持mp4, avi, mov等格式)
```

### 上传图片
```
POST /api/admin/upload/image
Content-Type: multipart/form-data

file: 图片文件 (最大20MB，支持jpg, png, gif等格式)
```

### 上传文档
```
POST /api/admin/upload/document
Content-Type: multipart/form-data

file: 文档文件 (最大50MB，支持pdf, doc, xls等格式)
```

## 📊 数据导出

### 导出用户数据
```
GET /api/admin/export/users?format=csv
GET /api/admin/export/users?format=json
```

### 导出课程数据
```
GET /api/admin/export/courses?format=csv
GET /api/admin/export/courses?format=json
```

### 导出学习记录
```
GET /api/admin/export/enrollments?format=csv
GET /api/admin/export/enrollments?format=json
```

## 🔧 系统管理

### 创建数据库备份
```
POST /api/admin/system/backup
```

### 获取系统日志
```
GET /api/admin/system/logs?lines=100
```

## 🚀 快速测试

访问 `http://localhost:8000/docs` 查看完整的Swagger API文档，可以直接在线测试所有接口。

### 测试账户
- **管理员账户**: admin@tcm.com / admin123
- **普通用户**: user1@example.com / 123456
- **医生账户**: doctor@tcm.com / doctor123

## ⚠️ 注意事项

1. 所有管理API都有权限校验，只有管理员可以访问
2. 文件上传有大小和格式限制
3. 数据导出支持CSV和JSON格式
4. 删除操作会记录操作日志
5. 敏感操作会发送通知（如果配置了邮件服务）

## 📝 操作日志

所有管理操作都会记录详细日志，包括：
- 操作时间
- 操作用户
- 操作类型
- 操作对象
- 操作结果

日志可通过 `/api/admin/system/logs` 接口查看。