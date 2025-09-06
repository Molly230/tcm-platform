<template>
  <div class="login-container">
    <el-card class="login-card">
      <template #header>
        <div class="card-header">
          <h2>{{ isLoginMode ? '用户登录' : '用户注册' }}</h2>
          <p class="subtitle">{{ isLoginMode ? '欢迎回来，请输入您的账号信息' : '创建新账户，加入我们的中医健康平台' }}</p>
        </div>
      </template>

      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
        class="login-form"
      >
        <!-- 注册模式下的额外字段 -->
        <template v-if="!isLoginMode">
          <el-form-item label="用户名" prop="username">
            <el-input
              v-model="form.username"
              placeholder="请输入用户名"
              size="large"
              prefix-icon="User"
            />
          </el-form-item>
          
          <el-form-item label="真实姓名" prop="full_name">
            <el-input
              v-model="form.full_name"
              placeholder="请输入真实姓名"
              size="large"
              prefix-icon="UserFilled"
            />
          </el-form-item>
          
          <el-form-item label="手机号" prop="phone">
            <el-input
              v-model="form.phone"
              placeholder="请输入手机号（可选）"
              size="large"
              prefix-icon="Phone"
            />
          </el-form-item>
        </template>

        <!-- 通用字段 -->
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="form.email"
            placeholder="请输入邮箱地址"
            size="large"
            prefix-icon="Message"
            type="email"
          />
        </el-form-item>

        <el-form-item label="密码" prop="password">
          <el-input
            v-model="form.password"
            placeholder="请输入密码"
            size="large"
            prefix-icon="Lock"
            type="password"
            show-password
          />
        </el-form-item>

        <!-- 注册模式下的确认密码 -->
        <el-form-item v-if="!isLoginMode" label="确认密码" prop="confirm_password">
          <el-input
            v-model="form.confirm_password"
            placeholder="请再次输入密码"
            size="large"
            prefix-icon="Lock"
            type="password"
            show-password
          />
        </el-form-item>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-button"
            :loading="loading"
            @click="handleSubmit"
          >
            {{ isLoginMode ? '登录' : '注册' }}
          </el-button>
        </el-form-item>
      </el-form>

      <div class="login-footer">
        <el-button type="text" @click="toggleMode">
          {{ isLoginMode ? '没有账户？点击注册' : '已有账户？点击登录' }}
        </el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import { useUserStore } from '../stores/user'
import type { FormInstance, FormRules } from 'element-plus'

interface LoginForm {
  email: string
  password: string
  username?: string
  full_name?: string
  phone?: string
  confirm_password?: string
}

const router = useRouter()
const userStore = useUserStore()
const formRef = ref<FormInstance>()
const loading = ref(false)
const isLoginMode = ref(true)

const form = reactive<LoginForm>({
  email: '',
  password: '',
  username: '',
  full_name: '',
  phone: '',
  confirm_password: ''
})

const validateConfirmPassword = (rule: any, value: any, callback: any) => {
  if (value !== form.password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const rules = reactive<FormRules<LoginForm>>({
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少为6个字符', trigger: 'blur' }
  ],
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度为3-20个字符', trigger: 'blur' }
  ],
  full_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    { validator: validateConfirmPassword, trigger: 'blur' }
  ]
})

const toggleMode = () => {
  isLoginMode.value = !isLoginMode.value
  // 清空表单
  if (formRef.value) {
    formRef.value.resetFields()
  }
  Object.keys(form).forEach(key => {
    form[key as keyof LoginForm] = ''
  })
}

const handleLogin = async () => {
  try {
    const response = await fetch('/api/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email_or_username: form.email,
        password: form.password,
      }),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || '登录失败')
    }

    // 使用用户状态管理保存用户信息
    userStore.setUser(data.user, data.access_token)

    ElMessage.success('登录成功')
    
    // 跳转到首页或者用户中心
    router.push('/')
  } catch (error: any) {
    ElMessage.error(error.message || '登录失败，请稍后重试')
  }
}

const handleRegister = async () => {
  try {
    const registerData = {
      email: form.email,
      username: form.username,
      password: form.password,
      confirm_password: form.confirm_password,
      full_name: form.full_name,
      phone: form.phone || undefined
    }

    const response = await fetch('/api/auth/register', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(registerData),
    })

    const data = await response.json()

    if (!response.ok) {
      throw new Error(data.detail || '注册失败')
    }

    ElMessage.success('注册成功，请登录')
    
    // 切换到登录模式
    isLoginMode.value = true
    form.email = data.email
    form.password = ''
  } catch (error: any) {
    ElMessage.error(error.message || '注册失败，请稍后重试')
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate((valid) => {
    if (valid) {
      loading.value = true
      
      if (isLoginMode.value) {
        handleLogin().finally(() => {
          loading.value = false
        })
      } else {
        handleRegister().finally(() => {
          loading.value = false
        })
      }
    }
  })
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-card {
  width: 100%;
  max-width: 480px;
  border-radius: 12px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}

.card-header {
  text-align: center;
  padding: 0 0 20px 0;
}

.card-header h2 {
  color: #303133;
  margin: 0 0 8px 0;
  font-size: 28px;
  font-weight: 600;
}

.subtitle {
  color: #606266;
  margin: 0;
  font-size: 14px;
  line-height: 1.4;
}

.login-form {
  padding: 0 20px;
}

.login-button {
  width: 100%;
  height: 48px;
  font-size: 16px;
  font-weight: 600;
  margin-top: 8px;
}

.login-footer {
  text-align: center;
  padding: 20px 0 0 0;
  border-top: 1px solid #f0f0f0;
  margin-top: 20px;
}

:deep(.el-form-item__label) {
  font-weight: 600;
  color: #303133;
}

:deep(.el-input__wrapper) {
  border-radius: 8px;
}

:deep(.el-button--primary) {
  border-radius: 8px;
}
</style>