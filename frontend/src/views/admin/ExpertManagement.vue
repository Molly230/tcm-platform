<template>
  <div class="expert-management">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h2>👨‍⚕️ 专家管理</h2>
        <p>管理平台专家信息、资质认证和服务状态</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新增专家
        </el-button>
        <el-button @click="refreshExperts" :loading="loading">
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
          placeholder="搜索专家姓名或专长"
          style="width: 300px"
          clearable
          @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        
        <el-select
          v-model="categoryFilter"
          placeholder="专业领域"
          style="width: 150px"
          clearable
          @change="handleFilter"
        >
          <el-option label="全部领域" value="" />
          <el-option label="中医内科" value="internal" />
          <el-option label="中医外科" value="external" />
          <el-option label="针灸推拿" value="acupuncture" />
          <el-option label="中药方剂" value="pharmacy" />
          <el-option label="养生保健" value="wellness" />
        </el-select>
        
        <el-select
          v-model="statusFilter"
          placeholder="认证状态"
          style="width: 120px"
          clearable
          @change="handleFilter"
        >
          <el-option label="全部状态" value="" />
          <el-option label="已认证" value="verified" />
          <el-option label="待认证" value="pending" />
          <el-option label="未通过" value="rejected" />
        </el-select>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <div class="stat-card" @click="filterByStatus('all')">
        <div class="stat-icon total">👨‍⚕️</div>
        <div class="stat-info">
          <div class="stat-number">{{ totalExperts }}</div>
          <div class="stat-label">专家总数</div>
        </div>
      </div>
      
      <div class="stat-card" @click="filterByStatus('verified')">
        <div class="stat-icon verified">✅</div>
        <div class="stat-info">
          <div class="stat-number">{{ verifiedExperts }}</div>
          <div class="stat-label">已认证</div>
        </div>
      </div>
      
      <div class="stat-card" @click="filterByStatus('pending')">
        <div class="stat-icon pending">⏳</div>
        <div class="stat-info">
          <div class="stat-number">{{ pendingExperts }}</div>
          <div class="stat-label">待认证</div>
        </div>
      </div>
      
      <div class="stat-card" @click="filterByStatus('active')">
        <div class="stat-icon active">🟢</div>
        <div class="stat-info">
          <div class="stat-number">{{ activeExperts }}</div>
          <div class="stat-label">在线服务</div>
        </div>
      </div>
    </div>

    <!-- 专家表格 -->
    <div class="table-section">
      <el-table
        :data="paginatedExperts"
        style="width: 100%"
        v-loading="loading"
        row-key="id"
      >
        <el-table-column prop="id" label="ID" width="80" />
        
        <el-table-column label="专家信息" min-width="300">
          <template #default="scope">
            <div class="expert-info">
              <div class="expert-avatar">
                <el-avatar :size="50" :src="scope.row.avatar">
                  <span>{{ scope.row.name?.charAt(0) || 'E' }}</span>
                </el-avatar>
              </div>
              <div class="expert-details">
                <div class="expert-name">
                  <strong>{{ scope.row.name }}</strong>
                  <el-tag 
                    v-if="scope.row.is_verified" 
                    type="success" 
                    size="small"
                    style="margin-left: 8px"
                  >
                    已认证
                  </el-tag>
                </div>
                <div class="expert-title">{{ scope.row.title || '专家' }}</div>
                <div class="expert-hospital">{{ scope.row.hospital || '医院信息未填写' }}</div>
                <div class="expert-specialties">
                  <span v-for="specialty in scope.row.specialties?.slice(0, 3)" :key="specialty" class="specialty-tag">
                    {{ specialty }}
                  </span>
                </div>
              </div>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="专业领域" width="120">
          <template #default="scope">
            <el-tag :type="getCategoryTagType(scope.row.category)" size="small">
              {{ getCategoryText(scope.row.category) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="认证状态" width="100">
          <template #default="scope">
            <el-tag :type="getVerificationTagType(scope.row.verification_status)" size="small">
              {{ getVerificationText(scope.row.verification_status) }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="服务状态" width="100">
          <template #default="scope">
            <el-switch
              v-model="scope.row.is_active"
              @change="toggleExpertStatus(scope.row)"
            />
          </template>
        </el-table-column>
        
        <el-table-column label="咨询次数" width="100">
          <template #default="scope">
            <div class="consultation-count">
              {{ scope.row.consultation_count || 0 }}
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="created_at" label="加入时间" width="120">
          <template #default="scope">
            {{ formatSimpleDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <div class="action-buttons">
              <el-button size="small" @click="viewExpert(scope.row)">
                <el-icon><View /></el-icon>
                查看
              </el-button>
              <el-button size="small" type="primary" @click="editExpert(scope.row)">
                <el-icon><Edit /></el-icon>
                编辑
              </el-button>
              <el-dropdown @command="handleExpertAction">
                <el-button size="small" type="info">
                  更多<el-icon class="el-icon--right"><ArrowDown /></el-icon>
                </el-button>
                <template #dropdown>
                  <el-dropdown-menu>
                    <el-dropdown-item :command="`verify-${scope.row.id}`">认证管理</el-dropdown-item>
                    <el-dropdown-item :command="`schedule-${scope.row.id}`">排班设置</el-dropdown-item>
                    <el-dropdown-item divided :command="`delete-${scope.row.id}`">删除专家</el-dropdown-item>
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
          :total="filteredExperts.length"
          layout="total, sizes, prev, pager, next, jumper"
        />
      </div>
    </div>

    <!-- 专家详情对话框 -->
    <el-dialog v-model="showDetailDialog" title="专家详情" width="700px">
      <div v-if="currentExpert" class="expert-detail">
        <!-- 基本信息 -->
        <div class="detail-section">
          <h4>基本信息</h4>
          <div class="expert-profile">
            <div class="profile-avatar">
              <el-avatar :size="80" :src="currentExpert.avatar">
                <span style="font-size: 32px">{{ currentExpert.name?.charAt(0) || 'E' }}</span>
              </el-avatar>
            </div>
            <div class="profile-info">
              <h3>{{ currentExpert.name }}</h3>
              <p class="title">{{ currentExpert.title }}</p>
              <p class="hospital">{{ currentExpert.hospital }}</p>
              <div class="tags">
                <el-tag :type="getCategoryTagType(currentExpert.category)">
                  {{ getCategoryText(currentExpert.category) }}
                </el-tag>
                <el-tag :type="getVerificationTagType(currentExpert.verification_status)">
                  {{ getVerificationText(currentExpert.verification_status) }}
                </el-tag>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 专业信息 -->
        <div class="detail-section">
          <h4>专业信息</h4>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">专业领域：</span>
              <span class="value">{{ getCategoryText(currentExpert.category) }}</span>
            </div>
            <div class="info-item">
              <span class="label">从业年限：</span>
              <span class="value">{{ currentExpert.experience_years || '未填写' }}年</span>
            </div>
            <div class="info-item">
              <span class="label">咨询价格：</span>
              <span class="value">¥{{ currentExpert.consultation_fee || 0 }}/次</span>
            </div>
            <div class="info-item">
              <span class="label">咨询次数：</span>
              <span class="value">{{ currentExpert.consultation_count || 0 }}次</span>
            </div>
          </div>
        </div>
        
        <!-- 专长介绍 -->
        <div class="detail-section" v-if="currentExpert.specialties?.length">
          <h4>专业特长</h4>
          <div class="specialties-list">
            <el-tag v-for="specialty in currentExpert.specialties" :key="specialty" style="margin: 4px">
              {{ specialty }}
            </el-tag>
          </div>
        </div>
        
        <!-- 个人简介 -->
        <div class="detail-section" v-if="currentExpert.description">
          <h4>个人简介</h4>
          <p class="description">{{ currentExpert.description }}</p>
        </div>
      </div>
      
      <template #footer>
        <el-button @click="showDetailDialog = false">关闭</el-button>
        <el-button type="primary" @click="editExpert(currentExpert)">编辑</el-button>
      </template>
    </el-dialog>

    <!-- 编辑专家对话框 -->
    <el-dialog 
      v-model="showEditDialog" 
      :title="editingExpertId ? '编辑专家' : '新增专家'" 
      width="600px"
    >
      <el-form :model="expertForm" :rules="expertRules" ref="expertFormRef" label-width="100px">
        <el-form-item label="专家姓名" prop="name">
          <el-input v-model="expertForm.name" placeholder="请输入专家姓名" />
        </el-form-item>
        
        <el-form-item label="职称" prop="title">
          <el-input v-model="expertForm.title" placeholder="如：主任医师、教授等" />
        </el-form-item>
        
        <el-form-item label="所在医院" prop="hospital">
          <el-input v-model="expertForm.hospital" placeholder="请输入所在医院" />
        </el-form-item>
        
        <el-form-item label="专业领域" prop="category">
          <el-select v-model="expertForm.category" style="width: 100%">
            <el-option label="中医内科" value="internal" />
            <el-option label="中医外科" value="external" />
            <el-option label="针灸推拿" value="acupuncture" />
            <el-option label="中药方剂" value="pharmacy" />
            <el-option label="养生保健" value="wellness" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="从业年限">
          <el-input-number v-model="expertForm.experience_years" :min="0" :max="50" />
          <span style="margin-left: 8px">年</span>
        </el-form-item>
        
        <el-form-item label="咨询费用">
          <el-input-number v-model="expertForm.consultation_fee" :min="0" :precision="2" />
          <span style="margin-left: 8px">元/次</span>
        </el-form-item>
        
        <el-form-item label="个人简介">
          <el-input 
            v-model="expertForm.description" 
            type="textarea" 
            :rows="4"
            placeholder="请输入个人简介"
            show-word-limit
            maxlength="500"
          />
        </el-form-item>
        
        <el-form-item label="认证状态" v-if="editingExpertId">
          <el-select v-model="expertForm.verification_status" style="width: 100%">
            <el-option label="待认证" value="pending" />
            <el-option label="已认证" value="verified" />
            <el-option label="未通过" value="rejected" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="服务状态">
          <el-switch
            v-model="expertForm.is_active"
            active-text="在线服务"
            inactive-text="暂停服务"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <el-button @click="showEditDialog = false">取消</el-button>
        <el-button type="primary" @click="saveExpert" :loading="saving">保存</el-button>
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
const experts = ref([])
const filteredExperts = ref([])
const loading = ref(false)
const saving = ref(false)

// 搜索和筛选
const searchText = ref('')
const categoryFilter = ref('')
const statusFilter = ref('')

// 分页
const currentPage = ref(1)
const pageSize = ref(20)

// 对话框状态
const showDetailDialog = ref(false)
const showEditDialog = ref(false)
const showCreateDialog = ref(false)
const currentExpert = ref(null)
const editingExpertId = ref(null)

// 表单数据
const expertForm = ref({
  name: '',
  title: '',
  hospital: '',
  category: 'internal',
  experience_years: 0,
  consultation_fee: 0,
  description: '',
  verification_status: 'pending',
  is_active: true
})

// 表单验证规则
const expertRules = {
  name: [
    { required: true, message: '请输入专家姓名', trigger: 'blur' }
  ],
  title: [
    { required: true, message: '请输入职称', trigger: 'blur' }
  ],
  hospital: [
    { required: true, message: '请输入所在医院', trigger: 'blur' }
  ],
  category: [
    { required: true, message: '请选择专业领域', trigger: 'change' }
  ]
}

// 计算属性
const totalExperts = computed(() => experts.value.length)
const verifiedExperts = computed(() => experts.value.filter(e => e.verification_status === 'verified').length)
const pendingExperts = computed(() => experts.value.filter(e => e.verification_status === 'pending').length)
const activeExperts = computed(() => experts.value.filter(e => e.is_active).length)

const paginatedExperts = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredExperts.value.slice(start, end)
})

// 方法
const loadExperts = async () => {
  try {
    loading.value = true
    // 使用模拟数据
    experts.value = generateMockExperts()
    filteredExperts.value = experts.value
  } catch (error) {
    console.error('加载专家失败:', error)
    ElMessage.error('加载专家失败')
  } finally {
    loading.value = false
  }
}

const generateMockExperts = () => {
  const categories = ['internal', 'external', 'acupuncture', 'pharmacy', 'wellness']
  const titles = ['主任医师', '副主任医师', '主治医师', '教授', '副教授', '博士', '硕士']
  const hospitals = ['北京中医院', '上海中医院', '广州中医院', '深圳中医院', '杭州中医院']
  const names = ['张明', '李华', '王芳', '赵军', '陈静', '刘伟', '杨丽', '周强', '吴敏', '郑涛']
  const statuses = ['verified', 'pending', 'rejected']
  
  const specialties = {
    internal: ['内科疾病', '脾胃病', '心脑血管', '呼吸系统'],
    external: ['外科手术', '骨伤科', '皮肤病', '肛肠科'],
    acupuncture: ['针灸治疗', '推拿按摩', '理疗康复', '疼痛治疗'],
    pharmacy: ['中药配方', '药物研究', '临床药学', '方剂学'],
    wellness: ['养生保健', '营养调理', '体质辨识', '健康管理']
  }
  
  return Array.from({ length: 30 }, (_, i) => {
    const category = categories[i % categories.length]
    return {
      id: i + 1,
      name: names[i % names.length],
      title: titles[i % titles.length],
      hospital: hospitals[i % hospitals.length],
      category: category,
      experience_years: Math.floor(Math.random() * 20) + 5,
      consultation_fee: Math.floor(Math.random() * 200) + 50,
      description: `资深${getCategoryText(category)}专家，从事临床工作多年，擅长各种疑难杂症的诊治。`,
      specialties: specialties[category].slice(0, Math.floor(Math.random() * 3) + 2),
      verification_status: statuses[i % statuses.length],
      is_verified: i % 3 !== 2,
      is_active: i % 4 !== 0,
      consultation_count: Math.floor(Math.random() * 500) + 10,
      avatar: `https://api.dicebear.com/7.x/avataaars/svg?seed=${i}`,
      created_at: new Date(Date.now() - Math.random() * 365 * 24 * 60 * 60 * 1000)
    }
  })
}

const refreshExperts = () => {
  loadExperts()
}

const handleSearch = () => {
  applyFilters()
}

const handleFilter = () => {
  applyFilters()
}

const applyFilters = () => {
  let result = [...experts.value]
  
  if (searchText.value) {
    const search = searchText.value.toLowerCase()
    result = result.filter(expert =>
      expert.name.toLowerCase().includes(search) ||
      (expert.specialties && expert.specialties.some(s => s.toLowerCase().includes(search)))
    )
  }
  
  if (categoryFilter.value) {
    result = result.filter(expert => expert.category === categoryFilter.value)
  }
  
  if (statusFilter.value) {
    result = result.filter(expert => expert.verification_status === statusFilter.value)
  }
  
  filteredExperts.value = result
  currentPage.value = 1
}

const filterByStatus = (status: string) => {
  if (status === 'all') {
    statusFilter.value = ''
  } else if (status === 'active') {
    // 特殊处理：筛选在线服务的专家
    filteredExperts.value = experts.value.filter(expert => expert.is_active)
    return
  } else {
    statusFilter.value = status
  }
  applyFilters()
}

const viewExpert = (expert: any) => {
  currentExpert.value = expert
  showDetailDialog.value = true
}

const editExpert = (expert: any) => {
  editingExpertId.value = expert.id
  expertForm.value = {
    name: expert.name,
    title: expert.title,
    hospital: expert.hospital,
    category: expert.category,
    experience_years: expert.experience_years || 0,
    consultation_fee: expert.consultation_fee || 0,
    description: expert.description || '',
    verification_status: expert.verification_status,
    is_active: expert.is_active
  }
  showEditDialog.value = true
  showDetailDialog.value = false
}

const saveExpert = async () => {
  saving.value = true
  try {
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success(editingExpertId.value ? '专家更新成功' : '专家创建成功')
    showEditDialog.value = false
    editingExpertId.value = null
    await loadExperts()
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

const toggleExpertStatus = async (expert: any) => {
  try {
    ElMessage.success(`专家 ${expert.name} 服务状态已更新`)
  } catch (error) {
    ElMessage.error('状态更新失败')
    expert.is_active = !expert.is_active
  }
}

const handleExpertAction = (command: string) => {
  const [action, expertId] = command.split('-')
  
  switch (action) {
    case 'verify':
      ElMessage.info('认证管理功能开发中...')
      break
    case 'schedule':
      ElMessage.info('排班设置功能开发中...')
      break
    case 'delete':
      handleDeleteExpert(parseInt(expertId))
      break
  }
}

const handleDeleteExpert = async (expertId: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个专家吗？', '删除确认', {
      confirmButtonText: '确定删除',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    ElMessage.success('专家删除成功')
    await loadExperts()
  } catch {
    // 用户取消删除
  }
}

// 工具方法
const getCategoryText = (category: string) => {
  const categoryMap = {
    'internal': '中医内科',
    'external': '中医外科',
    'acupuncture': '针灸推拿',
    'pharmacy': '中药方剂',
    'wellness': '养生保健'
  }
  return categoryMap[category] || category
}

const getCategoryTagType = (category: string) => {
  const typeMap = {
    'internal': 'primary',
    'external': 'success',
    'acupuncture': 'warning',
    'pharmacy': 'info',
    'wellness': 'danger'
  }
  return typeMap[category] || 'info'
}

const getVerificationText = (status: string) => {
  const statusMap = {
    'verified': '已认证',
    'pending': '待认证',
    'rejected': '未通过'
  }
  return statusMap[status] || status
}

const getVerificationTagType = (status: string) => {
  const typeMap = {
    'verified': 'success',
    'pending': 'warning',
    'rejected': 'danger'
  }
  return typeMap[status] || ''
}

const formatSimpleDate = (date: string | Date) => {
  if (!date) return '—'
  return new Date(date).toLocaleDateString('zh-CN', {
    month: '2-digit',
    day: '2-digit'
  })
}

// 生命周期
onMounted(() => {
  loadExperts()
})
</script>

<style scoped>
.expert-management {
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
  flex-wrap: wrap;
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
.stat-icon.verified { background: #f6ffed; }
.stat-icon.pending { background: #fff0e6; }
.stat-icon.active { background: #f9f0ff; }

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #333;
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

.expert-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.expert-details {
  flex: 1;
  min-width: 0;
}

.expert-name {
  display: flex;
  align-items: center;
  font-size: 14px;
  margin-bottom: 4px;
}

.expert-title {
  font-size: 12px;
  color: #666;
  margin-bottom: 2px;
}

.expert-hospital {
  font-size: 12px;
  color: #999;
  margin-bottom: 4px;
}

.expert-specialties {
  display: flex;
  gap: 4px;
  flex-wrap: wrap;
}

.specialty-tag {
  font-size: 10px;
  color: #666;
  background: #f0f0f0;
  padding: 2px 6px;
  border-radius: 4px;
}

.consultation-count {
  text-align: center;
  font-weight: 500;
}

.action-buttons {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.pagination-section {
  padding: 20px;
  display: flex;
  justify-content: center;
}

/* 专家详情对话框 */
.expert-detail {
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

.expert-profile {
  display: flex;
  gap: 20px;
}

.profile-avatar {
  flex-shrink: 0;
}

.profile-info h3 {
  margin: 0 0 8px 0;
  font-size: 20px;
  color: #333;
}

.profile-info .title {
  margin: 0 0 4px 0;
  color: #666;
  font-size: 14px;
}

.profile-info .hospital {
  margin: 0 0 12px 0;
  color: #999;
  font-size: 14px;
}

.tags {
  display: flex;
  gap: 8px;
}

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.info-item {
  display: flex;
  gap: 8px;
}

.info-item .label {
  color: #666;
  font-size: 14px;
  min-width: 80px;
}

.info-item .value {
  color: #333;
  font-size: 14px;
  font-weight: 500;
}

.specialties-list {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.description {
  margin: 0;
  color: #666;
  line-height: 1.6;
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
  
  .expert-profile {
    flex-direction: column;
  }
  
  .info-grid {
    grid-template-columns: 1fr;
  }
  
  .action-buttons {
    flex-direction: column;
  }
}
</style>