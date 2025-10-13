# 🔧 管理后台登录问题排查

## 问题描述
登录管理后台后跳转到了客户端页面，而不是管理后台页面。

## 🔍 排查步骤

### 1. 清除浏览器缓存和localStorage
```javascript
// 在浏览器控制台执行以下命令：
localStorage.clear()
sessionStorage.clear()
location.reload()
```

### 2. 检查当前localStorage状态
```javascript
// 在浏览器控制台查看：
console.log('admin_token:', localStorage.getItem('admin_token'))
console.log('admin_user:', localStorage.getItem('admin_user'))
console.log('user_token:', localStorage.getItem('user_token'))
console.log('user_data:', localStorage.getItem('user_data'))
```

### 3. 手动设置管理员信息
如果自动登录有问题，可以手动设置：

```javascript
// 获取管理员token (替换为实际的token)
const adminToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
const adminUser = {
  "email": "admin@tcm.com",
  "username": "admin", 
  "id": 1,
  "role": "admin",
  "is_admin": true,
  "is_super_admin": true
}

// 设置localStorage
localStorage.setItem('admin_token', adminToken)
localStorage.setItem('admin_user', JSON.stringify(adminUser))

// 清除普通用户数据
localStorage.removeItem('user_token')
localStorage.removeItem('user_data')

// 跳转到管理后台
window.location.href = '/admin/dashboard'
```

## 🚀 快速解决方案

### 方案1: 直接访问管理后台
1. 打开浏览器开发者工具 (F12)
2. 打开 Console 标签
3. 执行以下代码：

```javascript
// 清除所有数据
localStorage.clear()

// 设置管理员登录信息
fetch('/api/auth/login', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email_or_username: 'admin@tcm.com',
    password: 'admin123'
  })
})
.then(response => response.json())
.then(data => {
  if (data.access_token) {
    localStorage.setItem('admin_token', data.access_token)
    localStorage.setItem('admin_user', JSON.stringify(data.user))
    window.location.href = '/admin/dashboard'
  }
})
```

### 方案2: 修改登录跳转逻辑
如果问题持续存在，可以修改AdminLogin.vue中的跳转逻辑：

```javascript
// 在登录成功后，先清除普通用户数据
localStorage.removeItem('user_token')
localStorage.removeItem('user_data')

// 再设置管理员数据
localStorage.setItem('admin_token', result.access_token)
localStorage.setItem('admin_user', JSON.stringify(userData))

// 强制跳转
window.location.replace('/admin/dashboard')
```

## ✅ 验证修复结果

登录后应该看到：
1. URL显示: `http://localhost:3001/admin/dashboard`  
2. 页面标题: "中医健康服务平台 - 管理后台"
3. 左侧菜单显示管理功能
4. 右上角显示管理员信息

## 🔧 预防措施

1. **分离存储**: 管理员和用户使用不同的localStorage key
2. **清理机制**: 登录时自动清理冲突数据  
3. **权限验证**: 路由守卫严格验证权限
4. **错误处理**: 添加详细的错误日志

## 📞 如果问题仍然存在

请提供以下信息：
1. 浏览器控制台的错误信息
2. Network标签中的API请求响应
3. localStorage中的实际数据
4. 当前URL和期望URL