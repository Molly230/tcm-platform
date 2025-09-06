<template>
  <div class="admin-login">
    <div class="login-container">
      <div class="login-header">
        <h2>管理后台登录</h2>
        <p>中医健康服务平台</p>
      </div>

      <el-form
        :model="loginForm"
        :rules="loginRules"
        ref="loginFormRef"
        class="login-form"
        @submit.prevent="handleLogin"
      >
        <el-form-item prop="email">
          <el-input
            v-model="loginForm.email"
            placeholder="管理员邮箱"
            size="large"
            prefix-icon="User"
          />
        </el-form-item>

        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            size="large"
            prefix-icon="Lock"
            show-password
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            style="width: 100%"
            :loading="logging"
            @click="handleLogin"
          >
            {{ logging ? '登录中...' : '登录' }}
          </el-button>
        </el-form-item>
      </el-form>

      <div class="login-tips">
        <p>🔐 仅限管理员访问</p>
        <p>默认账号: admin@tcm.com / password: admin123</p>
      </div>
    </div>

    <div class="login-bg">
      <div class="bg-decoration">
        <div class="circle circle-1"></div>
        <div class="circle circle-2"></div>
        <div class="circle circle-3"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

const logging = ref(false)
const loginFormRef = ref()

const loginForm = ref({
  email: '',
  password: ''
})

const loginRules = {
  email: [
    { required: true, message: '请输入管理员邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度不能少于6位', trigger: 'blur' }
  ]
}

const handleLogin = async () => {
  if (!loginFormRef.value) return
  
  try {
    const valid = await loginFormRef.value.validate()
    if (!valid) return

    logging.value = true

    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email_or_username: loginForm.value.email,
        password: loginForm.value.password
      })
    })

    const result = await response.json()

    if (response.ok) {
      // 验证是否为管理员
      const userResponse = await fetch('/api/users/me', {
        headers: {
          'Authorization': `Bearer ${result.access_token}`
        }
      })
      
      const userData = await userResponse.json()
      
      if (!userData.is_admin && !userData.is_super_admin) {
        ElMessage.error('权限不足，仅限管理员登录')
        return
      }

      // 清除普通用户数据，避免冲突
      localStorage.removeItem('user_token')
      localStorage.removeItem('user_data')
      
      // 保存管理员token
      localStorage.setItem('admin_token', result.access_token)
      localStorage.setItem('admin_user', JSON.stringify(userData))
      
      ElMessage.success('登录成功')
      
      // 强制跳转到管理后台
      window.location.replace('/admin/dashboard')
      
    } else {
      ElMessage.error(result.detail || '登录失败')
    }
  } catch (error) {
    console.error('登录失败:', error)
    ElMessage.error('网络错误，请重试')
  } finally {
    logging.value = false
  }
}
</script>

<style scoped>
.admin-login {
  height: 100vh;
  display: flex;
  position: relative;
  overflow: hidden;
}

.login-container {
  width: 400px;
  margin: auto;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  padding: 40px;
  z-index: 10;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  color: #333;
  margin-bottom: 8px;
  font-size: 24px;
  font-weight: 600;
}

.login-header p {
  color: #666;
  font-size: 14px;
}

.login-form {
  margin-bottom: 20px;
}

.login-tips {
  text-align: center;
  color: #666;
  font-size: 12px;
}

.login-tips p {
  margin: 5px 0;
}

.login-bg {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  z-index: 1;
}

.bg-decoration {
  position: relative;
  width: 100%;
  height: 100%;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.1);
  animation: float 6s ease-in-out infinite;
}

.circle-1 {
  width: 200px;
  height: 200px;
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.circle-2 {
  width: 150px;
  height: 150px;
  top: 60%;
  right: 15%;
  animation-delay: -2s;
}

.circle-3 {
  width: 100px;
  height: 100px;
  bottom: 20%;
  left: 60%;
  animation-delay: -4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0px) rotate(0deg);
    opacity: 0.7;
  }
  50% {
    transform: translateY(-20px) rotate(180deg);
    opacity: 1;
  }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .login-container {
    width: 90%;
    margin: 20px;
    padding: 30px 20px;
  }
}
</style>