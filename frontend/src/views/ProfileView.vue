<template>
  <PageContainer>
    <div class="profile-container">
      <el-row :gutter="20">
        <!-- 左侧菜单 -->
        <el-col :xs="24" :sm="6" :md="6">
          <el-card class="profile-menu">
            <div class="user-avatar">
              <el-avatar :size="80" :src="userAvatar">
                <el-icon><UserFilled /></el-icon>
              </el-avatar>
              <h3>{{ userData?.full_name || userData?.username || '用户' }}</h3>
              <p class="user-email">{{ userData?.email }}</p>
            </div>
            
            <el-menu
              default-active="profile"
              @select="handleMenuSelect"
              class="profile-nav-menu"
            >
              <el-menu-item index="profile">
                <el-icon><User /></el-icon>
                <span>基本信息</span>
              </el-menu-item>
              <el-menu-item index="security">
                <el-icon><Lock /></el-icon>
                <span>账户安全</span>
              </el-menu-item>
              <el-menu-item index="orders">
                <el-icon><Document /></el-icon>
                <span>我的订单</span>
              </el-menu-item>
              <el-menu-item index="courses">
                <el-icon><Reading /></el-icon>
                <span>我的课程</span>
              </el-menu-item>
            </el-menu>
          </el-card>
        </el-col>
        
        <!-- 右侧内容 -->
        <el-col :xs="24" :sm="18" :md="18">
          <el-card class="profile-content">
            <!-- 基本信息 -->
            <div v-if="activeMenu === 'profile'">
              <div class="section-header">
                <h2>基本信息</h2>
                <el-button v-if="!isEditing" type="primary" @click="startEdit">
                  编辑资料
                </el-button>
                <div v-else>
                  <el-button @click="cancelEdit">取消</el-button>
                  <el-button type="primary" @click="saveProfile" :loading="saving">
                    保存
                  </el-button>
                </div>
              </div>
              
              <el-form
                ref="profileFormRef"
                :model="profileForm"
                :rules="profileRules"
                label-width="100px"
                class="profile-form"
              >
                <el-form-item label="用户名" prop="username">
                  <el-input
                    v-model="profileForm.username"
                    :disabled="!isEditing"
                    placeholder="请输入用户名"
                  />
                </el-form-item>
                
                <el-form-item label="真实姓名" prop="full_name">
                  <el-input
                    v-model="profileForm.full_name"
                    :disabled="!isEditing"
                    placeholder="请输入真实姓名"
                  />
                </el-form-item>
                
                <el-form-item label="邮箱">
                  <el-input
                    v-model="profileForm.email"
                    disabled
                    placeholder="邮箱地址"
                  />
                  <small class="form-tip">邮箱地址不可修改</small>
                </el-form-item>
                
                <el-form-item label="手机号" prop="phone">
                  <el-input
                    v-model="profileForm.phone"
                    :disabled="!isEditing"
                    placeholder="请输入手机号"
                  />
                </el-form-item>
                
                <el-form-item label="性别" prop="gender">
                  <el-select
                    v-model="profileForm.gender"
                    :disabled="!isEditing"
                    placeholder="请选择性别"
                  >
                    <el-option label="男" value="male" />
                    <el-option label="女" value="female" />
                    <el-option label="其他" value="other" />
                  </el-select>
                </el-form-item>
                
                <el-form-item label="生日" prop="birthday">
                  <el-date-picker
                    v-model="profileForm.birthday"
                    type="date"
                    :disabled="!isEditing"
                    placeholder="选择生日"
                    format="YYYY-MM-DD"
                    value-format="YYYY-MM-DD"
                  />
                </el-form-item>
                
                <el-form-item label="个人简介" prop="bio">
                  <el-input
                    v-model="profileForm.bio"
                    type="textarea"
                    :rows="4"
                    :disabled="!isEditing"
                    placeholder="请输入个人简介"
                  />
                </el-form-item>
              </el-form>
            </div>
            
            <!-- 账户安全 -->
            <div v-else-if="activeMenu === 'security'">
              <div class="section-header">
                <h2>账户安全</h2>
              </div>
              
              <el-form
                ref="passwordFormRef"
                :model="passwordForm"
                :rules="passwordRules"
                label-width="120px"
                class="security-form"
              >
                <el-form-item label="当前密码" prop="old_password">
                  <el-input
                    v-model="passwordForm.old_password"
                    type="password"
                    show-password
                    placeholder="请输入当前密码"
                  />
                </el-form-item>
                
                <el-form-item label="新密码" prop="new_password">
                  <el-input
                    v-model="passwordForm.new_password"
                    type="password"
                    show-password
                    placeholder="请输入新密码"
                  />
                </el-form-item>
                
                <el-form-item label="确认新密码" prop="confirm_password">
                  <el-input
                    v-model="passwordForm.confirm_password"
                    type="password"
                    show-password
                    placeholder="请再次输入新密码"
                  />
                </el-form-item>
                
                <el-form-item>
                  <el-button type="primary" @click="changePassword" :loading="changingPassword">
                    修改密码
                  </el-button>
                </el-form-item>
              </el-form>
            </div>
            
            <!-- 其他页面 -->
            <div v-else>
              <div class="section-header">
                <h2>{{ getMenuTitle(activeMenu) }}</h2>
              </div>
              <el-result
                icon="warning"
                title="功能开发中"
                sub-title="该功能正在开发中，敬请期待！"
              >
                <template #extra>
                  <el-button type="primary" @click="activeMenu = 'profile'">
                    返回基本信息
                  </el-button>
                </template>
              </el-result>
            </div>
          </el-card>
        </el-col>
      </el-row>
    </div>
  </PageContainer>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { UserFilled, User, Lock, Document, Reading } from '@element-plus/icons-vue'
import PageContainer from '../components/PageContainer.vue'
import type { FormInstance, FormRules } from 'element-plus'

interface UserData {
  id: number
  email: string
  username: string
  full_name?: string
  phone?: string
  gender?: string
  birthday?: string
  bio?: string
  avatar?: string
  role: string
  status: string
}

const router = useRouter()
const userData = ref<UserData | null>(null)
const activeMenu = ref('profile')
const isEditing = ref(false)
const saving = ref(false)
const changingPassword = ref(false)

const profileFormRef = ref<FormInstance>()
const passwordFormRef = ref<FormInstance>()

const profileForm = reactive({
  username: '',
  full_name: '',
  email: '',
  phone: '',
  gender: '',
  birthday: '',
  bio: ''
})

const passwordForm = reactive({
  old_password: '',
  new_password: '',
  confirm_password: ''
})

const validateConfirmPassword = (rule: any, value: any, callback: any) => {
  if (value !== passwordForm.new_password) {
    callback(new Error('两次输入的密码不一致'))
  } else {
    callback()
  }
}

const profileRules = reactive<FormRules>({
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度为3-20个字符', trigger: 'blur' }
  ],
  full_name: [
    { required: true, message: '请输入真实姓名', trigger: 'blur' }
  ]
})

const passwordRules = reactive<FormRules>({
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
})

const userAvatar = ref('')

const loadUserData = () => {
  const token = localStorage.getItem('user_token')
  const userDataStr = localStorage.getItem('user_data')
  
  if (!token || !userDataStr) {
    router.push('/login')
    return
  }
  
  try {
    userData.value = JSON.parse(userDataStr)
    if (userData.value) {
      Object.assign(profileForm, {
        username: userData.value.username || '',
        full_name: userData.value.full_name || '',
        email: userData.value.email || '',
        phone: userData.value.phone || '',
        gender: userData.value.gender || '',
        birthday: userData.value.birthday || '',
        bio: userData.value.bio || ''
      })
      userAvatar.value = userData.value.avatar || ''
    }
  } catch (error) {
    console.error('解析用户数据失败:', error)
    router.push('/login')
  }
}

const handleMenuSelect = (index: string) => {
  activeMenu.value = index
  isEditing.value = false
}

const getMenuTitle = (menu: string) => {
  const titles: Record<string, string> = {
    profile: '基本信息',
    security: '账户安全',
    orders: '我的订单',
    courses: '我的课程'
  }
  return titles[menu] || '未知'
}

const startEdit = () => {
  isEditing.value = true
}

const cancelEdit = () => {
  isEditing.value = false
  loadUserData() // 重新加载数据
}

const saveProfile = async () => {
  if (!profileFormRef.value) return
  
  await profileFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    saving.value = true
    
    try {
      const token = localStorage.getItem('user_token')
      
      const response = await fetch('/api/users/me', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          username: profileForm.username,
          full_name: profileForm.full_name,
          phone: profileForm.phone || null,
          gender: profileForm.gender || null,
          birthday: profileForm.birthday || null,
          bio: profileForm.bio || null
        })
      })
      
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.detail || '更新失败')
      }
      
      // 更新本地存储
      localStorage.setItem('user_data', JSON.stringify(data))
      userData.value = data
      
      ElMessage.success('个人资料更新成功')
      isEditing.value = false
      
      // 触发导航栏更新
      window.dispatchEvent(new Event('storage'))
      
    } catch (error: any) {
      ElMessage.error(error.message || '更新失败，请稍后重试')
    } finally {
      saving.value = false
    }
  })
}

const changePassword = async () => {
  if (!passwordFormRef.value) return
  
  await passwordFormRef.value.validate(async (valid) => {
    if (!valid) return
    
    changingPassword.value = true
    
    try {
      const token = localStorage.getItem('user_token')
      
      const response = await fetch('/api/users/me/password', {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          old_password: passwordForm.old_password,
          new_password: passwordForm.new_password,
          confirm_password: passwordForm.confirm_password
        })
      })
      
      const data = await response.json()
      
      if (!response.ok) {
        throw new Error(data.detail || '密码修改失败')
      }
      
      ElMessage.success('密码修改成功')
      
      // 清空表单
      Object.assign(passwordForm, {
        old_password: '',
        new_password: '',
        confirm_password: ''
      })
      
      if (passwordFormRef.value) {
        passwordFormRef.value.resetFields()
      }
      
    } catch (error: any) {
      ElMessage.error(error.message || '密码修改失败，请稍后重试')
    } finally {
      changingPassword.value = false
    }
  })
}

onMounted(() => {
  loadUserData()
})
</script>

<style scoped>
.profile-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.profile-menu {
  margin-bottom: 20px;
}

.user-avatar {
  text-align: center;
  padding: 20px 0;
  border-bottom: 1px solid #f0f0f0;
  margin-bottom: 20px;
}

.user-avatar h3 {
  margin: 16px 0 8px 0;
  font-size: 18px;
  color: #303133;
}

.user-email {
  margin: 0;
  color: #909399;
  font-size: 14px;
}

.profile-nav-menu {
  border: none;
}

.profile-content {
  min-height: 600px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 1px solid #f0f0f0;
}

.section-header h2 {
  margin: 0;
  font-size: 20px;
  color: #303133;
}

.profile-form,
.security-form {
  max-width: 600px;
}

.form-tip {
  color: #909399;
  font-size: 12px;
  margin-top: 4px;
  display: block;
}

@media (max-width: 768px) {
  .profile-container {
    padding: 10px;
  }
  
  .section-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 15px;
  }
}
</style>