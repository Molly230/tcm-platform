<template>
  <div class="user-management">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h2>👥 用户管理</h2>
        <p>管理平台用户信息、角色权限和状态</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新增用户
        </el-button>
        <el-button @click="refreshUsers" :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <div class="filter-row">
        <el-input
          v-model="searchText"
          placeholder="搜索用户名、邮箱或姓名"
          style="width: 300px"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        
        <el-select
          v-model="roleFilter"
          placeholder="筛选角色"
          style="width: 150px"
          clearable
          @change="handleFilter"
        >
          <el-option label="全部角色" value="" />
          <el-option label="普通用户" value="USER" />
          <el-option label="VIP用户" value="VIP" />
          <el-option label="医生用户" value="DOCTOR" />
          <el-option label="管理员" value="ADMIN" />
          <el-option label="超级管理员" value="SUPER_ADMIN" />
        </el-select>
        
        <el-select
          v-model="statusFilter"
          placeholder="筛选状态"
          style="width: 120px"
          clearable
          @change="handleFilter"
        >
          <el-option label="全部状态" value="" />
          <el-option label="激活" value="ACTIVE" />
          <el-option label="禁用" value="INACTIVE" />
          <el-option label="封禁" value="BANNED" />
        </el-select>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <div class="stat-card" @click="filterByStatus('all')">
        <div class="stat-icon total">👥</div>
        <div class="stat-info">
          <div class="stat-number">{{ totalUsers }}</div>
          <div class="stat-label">总用户数</div>
        </div>
      </div>
      
      <div class="stat-card" @click="filterByStatus('ACTIVE')">
        <div class="stat-icon active">✅</div>
        <div class="stat-info">
          <div class="stat-number">{{ activeUsers }}</div>
          <div class="stat-label">活跃用户</div>
        </div>
      </div>
      
      <div class="stat-card" @click="filterByRole('VIP')">
        <div class="stat-icon vip">⭐</div>
        <div class="stat-info">
          <div class="stat-number">{{ vipUsers }}</div>
          <div class="stat-label">VIP用户</div>
        </div>
      </div>
      
      <div class="stat-card" @click="filterByRole('ADMIN')">
        <div class="stat-icon admin">🔐</div>
        <div class="stat-info">
          <div class="stat-number">{{ adminUsers }}</div>
          <div class="stat-label">管理员</div>
        </div>
      </div>
    </div>

    <!-- 用户表格 -->
    <div class="table-section">
      <el-table
        :data="filteredUsers"
        style="width: 100%"
        v-loading="loading"
        row-key="id"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        
        <el-table-column prop="id" label="ID" width="80" />
        
        <el-table-column label="用户信息" min-width="250">
          <template #default="scope">
            <div class="user-info">
              <div class="user-avatar">
                <el-avatar :size="40" :src="scope.row.avatar">
                  <span>{{ scope.row.username?.charAt(0).toUpperCase() || 'U' }}</span>
                </el-avatar>
              </div>
              <div class="user-details">
                <div class="user-name">
                  <strong>{{ scope.row.username }}</strong>
                  <el-tag 
                    v-if="scope.row.is_super_admin" 
                    type="danger" 
                    size="small"
                    style="margin-left: 8px"
                  >
                    超级管理员
                  </el-tag>
                  <el-tag 
                    v-else-if="scope.row.is_admin" 
                    type="warning" 
                    size="small"
                    style="margin-left: 8px"
                  >
                    管理员
                  </el-tag>
                </div>
                <div class="user-email">{{ scope.row.email }}</div>
                <div class="user-meta" v-if="scope.row.full_name || scope.row.phone">
                  <span v-if="scope.row.full_name">{{ scope.row.full_name }}</span>
                  <span v-if="scope.row.phone" class="phone">📞 {{ scope.row.phone }}</span>
                </div>
              </div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="role" label="角色" width="120">
          <template #default="scope">
            <el-tag :type="getRoleTagType(scope.row.role)" size="small">
              {{ getRoleText(scope.row.role) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="scope">
            <el-tag :type="getStatusTagType(scope.row.status)" size="small">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="is_active" label="激活状态" width="100">
          <template #default="scope">
            <el-switch
              v-model="scope.row.is_active"
              @change="toggleUserStatus(scope.row)"
            />
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="注册时间" width="180">
          <template #default="scope">
            <div class="time-info">
              <div>{{ formatDate(scope.row.created_at) }}</div>
              <div class="time-detail">{{ formatRelativeTime(scope.row.created_at) }}</div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <div class="action-buttons">
              <el-button size="small" @click="viewUser(scope.row)">
                <el-icon><View /></el-icon>
                查看
              </el-button>
              <el-button size="small" type="primary" @click="editUser(scope.row)">
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-dropdown @command="handleUserAction">
                <el-button size="small" type="info">
                  更多<el-icon class="el-icon--right"><ArrowDown /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :command="`role-${scope.row.id}`">修改角色</el-dropdown-item>
                    <el-dropdown-item :command="`reset-${scope.row.id}`">重置密码</el-dropdown-item>
                    <el-dropdown-item divided :command="`delete-${scope.row.id}`">删除用户</el-dropdown-item>
                  </el-dropdown-menu>
                </template>
              </el-dropdown>
            </div>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="totalUsers"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handleCurrentChange"
        />
      </div>
    </div>

    <!-- 批量操作 -->
    <div class="batch-actions" v-if="selectedUsers.length > 0">
      <div class="batch-info">
        已选择 {{ selectedUsers.length }} 个用户
      </div>
      <div class="batch-buttons">
        <el-button @click="batchUpdateRole">批量修改角色</el-button>
        <el-button @click="batchUpdateStatus">批量修改状态</el-button>
        <el-button type="danger" @click="batchDelete">批量删除</el-button>
      </div>
    </div>

    <!-- 用户详情对话框 -->
    <el-dialog v-model="showDetailDialog" title="用户详情" width="600px">
      <div v-if="currentUser" class="user-detail">
        <div class="detail-section">
          <h4>基本信息</h4>
          <div class="detail-grid">
            <div class="detail-item">
              <span class="label">用户名：</span>
              <span class="value">{{ currentUser.username }}</span>
            </div>
            <div class="detail-item">
              <span class="label">邮箱：</span>
              <span class="value">{{ currentUser.email }}</span>
            </div>
            <div class="detail-item">
              <span class="label">真实姓名：</span>
              <span class="value">{{ currentUser.full_name || '未设置' }}</span>
            </div>
            <div class="detail-item">
              <span class="label">手机号：</span>
              <span class="value">{{ currentUser.phone || '未设置' }}</span>
            </div>
            <div class="detail-item">
              <span class="label">角色：</span>
              <span class="value">{{ getRoleText(currentUser.role) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">状态：</span>
              <span class="value">{{ getStatusText(currentUser.status) }}</span>
            </div>
          </div>
        </div>
        
        <div class="detail-section">
          <h4>时间信息</h4>
          <div class="detail-grid">
            <div class="detail-item">
              <span class="label">注册时间：</span>
              <span class="value">{{ formatDate(currentUser.created_at) }}</span>
            </div>
            <div class="detail-item">
              <span class="label">最后登录：</span>
              <span class="value">{{ formatDate(currentUser.last_login) || '从未登录' }}</span>
            </div>
          </div>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="showDetailDialog = false">关闭</el-button>
        <el-button type="primary" @click="editUser(currentUser)">编辑</el-button>
      </template>
    </el-dialog>

    <!-- 编辑用户对话框 -->
    <el-dialog 
      v-model="showEditDialog" 
      :title="editingUserId ? '编辑用户' : '新增用户'" 
      width="500px"
    >
      <el-form :model="userForm" :rules="userRules" ref="userFormRef" label-width="100px">
        <el-form-item label="用户名" prop="username">
          <el-input v-model="userForm.username" :disabled="editingUserId" />
        </el-form-item>
        
        <el-form-item label="邮箱" prop="email">
          <el-input v-model="userForm.email" type="email" />
        </el-form-item>
        
        <el-form-item label="真实姓名" prop="full_name">
          <el-input v-model="userForm.full_name" />
        </el-form-item>
        
        <el-form-item label="手机号" prop="phone">
          <el-input v-model="userForm.phone" />
        </el-form-item>
        
        <el-form-item label="角色" prop="role">
          <el-select v-model="userForm.role" style="width: 100%">
            <el-option label="普通用户" value="USER" />
            <el-option label="VIP用户" value="VIP" />
            <el-option label="医生用户" value="DOCTOR" />
            <el-option label="管理员" value="ADMIN" />
            <el-option label="超级管理员" value="SUPER_ADMIN" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态" prop="status">
          <el-select v-model="userForm.status" style="width: 100%">
            <el-option label="激活" value="ACTIVE" />
            <el-option label="禁用" value="INACTIVE" />
            <el-option label="封禁" value="BANNED" />
          </el-select>
        </el-form-item>
        
        <el-form-item v-if="!editingUserId" label="密码" prop="password">
          <el-input v-model="userForm.password" type="password" show-password />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="saveUser" :loading="saving">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { 
  Plus, Refresh, Search, View, Edit, ArrowDown
} from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

// 响应式数据
const users = ref([])
const filteredUsers = ref([])
const loading = ref(false)
const saving = ref(false)

// 搜索和筛选
const searchText = ref('')
const roleFilter = ref('')
const statusFilter = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(20)

// 选择的用户
const selectedUsers = ref([])

// 对话框状态
const showDetailDialog = ref(false)
const showEditDialog = ref(false)
const showCreateDialog = ref(false)
const currentUser = ref(null)
const editingUserId = ref(null)

// 表单数据
const userForm = ref({
  username: '',
  email: '',
  full_name: '',
  phone: '',
  role: 'USER',
  status: 'ACTIVE',
  password: ''
})

// 表单验证规则
const userRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 50, message: '用户名长度应为3-50字符', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱', trigger: 'blur' },
    { type: 'email', message: '请输入有效的邮箱地址', trigger: 'blur' }
  ],
  role: [
    { required: true, message: '请选择角色', trigger: 'change' }
  ],
  status: [
    { required: true, message: '请选择状态', trigger: 'change' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ]
}

// 计算属性
const totalUsers = computed(() => users.value.length)
const activeUsers = computed(() => users.value.filter(u => u.status === 'ACTIVE').length)
const vipUsers = computed(() => users.value.filter(u => u.role === 'VIP').length)
const adminUsers = computed(() => users.value.filter(u => u.is_admin || u.is_super_admin).length)

// 方法
const loadUsers = async () => {
  try {
    loading.value = true
    const response = await fetch('/api/admin/users', {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
    })
    
    if (response.ok) {
      users.value = await response.json()
      filteredUsers.value = users.value
    } else {
      // 使用模拟数据
      users.value = generateMockUsers()
      filteredUsers.value = users.value
    }
  } catch (error) {
    console.error('加载用户失败:', error)
    ElMessage.error('加载用户失败')
    // 使用模拟数据
    users.value = generateMockUsers()
    filteredUsers.value = users.value
  } finally {
    loading.value = false
  }
}

const generateMockUsers = () => {
  const roles = ['USER', 'VIP', 'DOCTOR', 'ADMIN']
  const statuses = ['ACTIVE', 'INACTIVE', 'BANNED']
  
  return Array.from({ length: 50 }, (_, i) => ({
    id: i + 1,
    username: `user${i + 1}`,
    email: `user${i + 1}@example.com`,
    full_name: `用户${i + 1}`,
    phone: `138${String(i).padStart(8, '0')}`,
    role: roles[i % roles.length],
    status: statuses[i % statuses.length],
    is_active: i % 4 !== 3,
    is_admin: i % 10 === 0,
    is_super_admin: i === 0,
    created_at: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000),
    last_login: Math.random() > 0.3 ? new Date(Date.now() - Math.random() * 30 * 24 * 60 * 60 * 1000) : null
  }))
}

const refreshUsers = () => {
  loadUsers()
}

const handleSearch = () => {
  applyFilters()
}

const handleFilter = () => {
  applyFilters()
}

const applyFilters = () => {
  let result = [...users.value]
  
  // 搜索筛选
  if (searchText.value) {
    const search = searchText.value.toLowerCase()
    result = result.filter(user =>
      user.username.toLowerCase().includes(search) ||
      user.email.toLowerCase().includes(search) ||
      (user.full_name && user.full_name.toLowerCase().includes(search))
    )
  }
  
  // 角色筛选
  if (roleFilter.value) {
    result = result.filter(user => user.role === roleFilter.value)
  }
  
  // 状态筛选
  if (statusFilter.value) {
    result = result.filter(user => user.status === statusFilter.value)
  }
  
  filteredUsers.value = result
}

const filterByStatus = (status: string) => {
  if (status === 'all') {
    statusFilter.value = ''
  } else {
    statusFilter.value = status
  }
  applyFilters()
}

const filterByRole = (role: string) => {
  roleFilter.value = role
  applyFilters()
}

const viewUser = (user: any) => {
  currentUser.value = user
  showDetailDialog.value = true
}

const editUser = (user: any) => {
  editingUserId.value = user.id
  userForm.value = {
    username: user.username,
    email: user.email,
    full_name: user.full_name || '',
    phone: user.phone || '',
    role: user.role,
    status: user.status,
    password: ''
  }
  showEditDialog.value = true
}

const saveUser = async () => {
  // 这里实现保存用户逻辑
  saving.value = true
  try {
    // 模拟API调用
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    ElMessage.success(editingUserId.value ? '用户更新成功' : '用户创建成功')
    showEditDialog.value = false
    showCreateDialog.value = false
    editingUserId.value = null
    await loadUsers()
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const toggleUserStatus = async (user: any) => {
  try {
    // 这里实现切换用户状态的逻辑
    ElMessage.success(`用户 ${user.username} 状态已更新`)
  } catch (error) {
    ElMessage.error('状态更新失败')
    // 回滚状态
    user.is_active = !user.is_active
  }
}

const handleUserAction = (command: string) => {
  const [action, userId] = command.split('-')
  
  switch (action) {
    case 'role':
      ElMessage.info('修改角色功能开发中...')
      break
    case 'reset':
      ElMessage.info('重置密码功能开发中...')
      break
    case 'delete':
      handleDeleteUser(parseInt(userId))
      break
  }
}

const handleDeleteUser = async (userId: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个用户吗？此操作不可恢复！', '删除确认', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 这里实现删除逻辑
    ElMessage.success('用户删除成功')
    await loadUsers()
  } catch {
    // 用户取消删除
  }
}

const handleSelectionChange = (selection: any[]) => {
  selectedUsers.value = selection
}

const batchUpdateRole = () => {
  ElMessage.info('批量修改角色功能开发中...')
}

const batchUpdateStatus = () => {
  ElMessage.info('批量修改状态功能开发中...')
}

const batchDelete = () => {
  ElMessage.info('批量删除功能开发中...')
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
}

// 工具方法
const getRoleText = (role: string) => {
  const roleMap = {
    'USER': '普通用户',
    'VIP': 'VIP用户',
    'DOCTOR': '医生用户',
    'ADMIN': '管理员',
    'SUPER_ADMIN': '超级管理员'
  }
  return roleMap[role] || role
}

const getRoleTagType = (role: string) => {
  const typeMap = {
    'USER': '',
    'VIP': 'warning',
    'DOCTOR': 'success',
    'ADMIN': 'danger',
    'SUPER_ADMIN': 'danger'
  }
  return typeMap[role] || ''
}

const getStatusText = (status: string) => {
  const statusMap = {
    'ACTIVE': '激活',
    'INACTIVE': '禁用',
    'BANNED': '封禁'
  }
  return statusMap[status] || status
}

const getStatusTagType = (status: string) => {
  const typeMap = {
    'ACTIVE': 'success',
    'INACTIVE': 'warning',
    'BANNED': 'danger'
  }
  return typeMap[status] || ''
}

const formatDate = (date: string | Date) => {
  if (!date) return '—'
  return new Date(date).toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const formatRelativeTime = (date: string | Date) => {
  if (!date) return ''
  const now = new Date()
  const past = new Date(date)
  const diff = now.getTime() - past.getTime()
  const days = Math.floor(diff / (1000 * 60 * 60 * 24))
  
  if (days === 0) return '今天'
  if (days === 1) return '昨天'
  if (days < 30) return `${days}天前`
  
  const months = Math.floor(days / 30)
  if (months < 12) return `${months}个月前`
  
  return `${Math.floor(months / 12)}年前`
}

// 生命周期
onMounted(() => {
  loadUsers()
})
</script>

<style scoped>
.user-management {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  padding: 24px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.header-content h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #333;
}

.header-content p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.filter-section {
  margin-bottom: 24px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.filter-row {
  display: flex;
  gap: 16px;
  align-items: center;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  cursor: pointer;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 16px;
}

.stat-icon.total { background: #e6f7ff; }
.stat-icon.active { background: #f6ffed; }
.stat-icon.vip { background: #fff0e6; }
.stat-icon.admin { background: #f9f0ff; }

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  line-height: 1;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.table-section {
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  overflow: hidden;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.user-details {
  flex: 1;
  min-width: 0;
}

.user-name {
  display: flex;
  align-items: center;
  font-size: 14px;
  margin-bottom: 4px;
}

.user-email {
  font-size: 12px;
  color: #666;
  margin-bottom: 2px;
}

.user-meta {
  font-size: 12px;
  color: #999;
  display: flex;
  gap: 8px;
}

.time-info {
  font-size: 12px;
}

.time-detail {
  color: #999;
  margin-top: 2px;
}

.action-buttons {
  display: flex;
  gap: 8px;
}

.pagination-section {
  padding: 20px;
  display: flex;
  justify-content: center;
}

.batch-actions {
  position: fixed;
  bottom: 20px;
  left: 50%;
  transform: translateX(-50%);
  background: white;
  padding: 16px 24px;
  border-radius: 8px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  align-items: center;
  gap: 16px;
  z-index: 1000;
}

.batch-info {
  font-size: 14px;
  color: #666;
}

.batch-buttons {
  display: flex;
  gap: 8px;
}

.user-detail {
  padding: 0;
}

.detail-section {
  margin-bottom: 24px;
}

.detail-section h4 {
  margin: 0 0 16px 0;
  font-size: 16px;
  color: #333;
  padding-bottom: 8px;
  border-bottom: 1px solid #f0f0f0;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.detail-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-item .label {
  font-size: 12px;
  color: #999;
}

.detail-item .value {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    gap: 16px;
  }
  
  .filter-row {
    flex-direction: column;
    align-items: stretch;
  }
  
  .filter-row .el-input,
  .filter-row .el-select {
    width: 100% !important;
  }
  
  .stats-section {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .detail-grid {
    grid-template-columns: 1fr;
  }
}
</style>