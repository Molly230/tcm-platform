<template>
  <div class="consultation-management">
    <div class="page-header">
      <div class="header-content">
        <h2>💬 咨询管理</h2>
        <p>管理用户咨询记录、专家回复和服务质量</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="loadConsultations">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <div class="stat-card">
        <div class="stat-icon total">💬</div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.total }}</div>
          <div class="stat-label">咨询总数</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon ai">🤖</div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.ai }}</div>
          <div class="stat-label">AI咨询</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon expert">👨‍⚕️</div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.expert }}</div>
          <div class="stat-label">专家咨询</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon satisfaction">⭐</div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.avgRating }}</div>
          <div class="stat-label">平均评分</div>
        </div>
      </div>
    </div>

    <!-- 搜索和过滤 -->
    <div class="filter-section">
      <el-input
        v-model="searchQuery"
        placeholder="搜索咨询单号、标题..."
        clearable
        style="width: 300px; margin-right: 12px;"
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-select
        v-model="filterType"
        placeholder="咨询类型"
        clearable
        style="width: 150px; margin-right: 12px;"
        @change="handleFilter"
      >
        <el-option label="AI咨询" value="AI" />
        <el-option label="专家咨询" value="EXPERT" />
        <el-option label="视频咨询" value="VIDEO" />
      </el-select>

      <el-select
        v-model="filterStatus"
        placeholder="咨询状态"
        clearable
        style="width: 150px;"
        @change="handleFilter"
      >
        <el-option label="待处理" value="PENDING" />
        <el-option label="进行中" value="IN_PROGRESS" />
        <el-option label="已完成" value="COMPLETED" />
        <el-option label="已取消" value="CANCELLED" />
      </el-select>
    </div>

    <!-- 数据表格 -->
    <div class="table-section">
      <el-table
        :data="consultations"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="consultation_number" label="咨询单号" width="180" />
        <el-table-column prop="title" label="标题" min-width="200" show-overflow-tooltip />
        <el-table-column label="类型" width="120">
          <template #default="scope">
            <el-tag :type="getTypeTagType(scope.row.type)">
              {{ getTypeText(scope.row.type) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="120">
          <template #default="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="user_id" label="用户ID" width="100" />
        <el-table-column prop="expert_id" label="专家ID" width="100" />
        <el-table-column label="评分" width="100">
          <template #default="scope">
            <el-rate
              v-if="scope.row.user_rating"
              :model-value="scope.row.user_rating"
              disabled
              show-score
              text-color="#ff9900"
              score-template="{value}"
            />
            <span v-else style="color: #999;">-</span>
          </template>
        </el-table-column>
        <el-table-column label="创建时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              link
              @click="viewConsultation(scope.row)"
            >
              查看
            </el-button>
            <el-button
              type="warning"
              size="small"
              link
              @click="editConsultation(scope.row)"
            >
              编辑
            </el-button>
            <el-popconfirm
              title="确定要删除这条咨询记录吗？"
              confirm-button-text="确定"
              cancel-button-text="取消"
              @confirm="deleteConsultation(scope.row.id)"
            >
              <template #reference>
                <el-button
                  type="danger"
                  size="small"
                  link
                >
                  删除
                </el-button>
              </template>
            </el-popconfirm>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { ChatLineRound, Refresh, Search } from '@element-plus/icons-vue'

interface Consultation {
  id: number
  consultation_number: string
  title: string
  type: string
  status: string
  user_id: number
  expert_id?: number
  user_rating?: number
  created_at: string
  [key: string]: any
}

const loading = ref(false)
const consultations = ref<Consultation[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const searchQuery = ref('')
const filterType = ref('')
const filterStatus = ref('')

// 统计数据
const stats = computed(() => {
  const total = consultations.value.length
  const ai = consultations.value.filter(c => c.type === 'AI').length
  const expert = consultations.value.filter(c => c.type === 'EXPERT' || c.type === 'VIDEO').length
  const ratings = consultations.value.filter(c => c.user_rating).map(c => c.user_rating)
  const avgRating = ratings.length > 0
    ? (ratings.reduce((sum, r) => sum + r, 0) / ratings.length).toFixed(1)
    : '0.0'

  return { total, ai, expert, avgRating }
})

// 加载咨询列表
const loadConsultations = async () => {
  loading.value = true
  try {
    const response = await fetch(`/api/consultations/?skip=${(currentPage.value - 1) * pageSize.value}&limit=${pageSize.value}`)

    if (!response.ok) {
      throw new Error('加载失败')
    }

    consultations.value = await response.json()
    total.value = consultations.value.length
    ElMessage.success('加载成功')
  } catch (error: any) {
    console.error('加载咨询列表失败:', error)
    ElMessage.error('加载失败：' + (error.message || '网络错误'))
  } finally {
    loading.value = false
  }
}

// 删除咨询
const deleteConsultation = async (id: number) => {
  try {
    const response = await fetch(`/api/consultations/${id}`, {
      method: 'DELETE'
    })

    if (!response.ok) {
      throw new Error('删除失败')
    }

    ElMessage.success('删除成功')
    loadConsultations()
  } catch (error: any) {
    console.error('删除失败:', error)
    ElMessage.error('删除失败：' + (error.message || '网络错误'))
  }
}

// 查看咨询详情
const viewConsultation = (consultation: Consultation) => {
  ElMessage.info(`查看咨询 #${consultation.id} 的详情（功能开发中）`)
}

// 编辑咨询
const editConsultation = (consultation: Consultation) => {
  ElMessage.info(`编辑咨询 #${consultation.id}（功能开发中）`)
}

// 搜索
const handleSearch = () => {
  loadConsultations()
}

// 过滤
const handleFilter = () => {
  loadConsultations()
}

// 分页
const handleSizeChange = () => {
  loadConsultations()
}

const handlePageChange = () => {
  loadConsultations()
}

// 类型标签样式
const getTypeTagType = (type: string) => {
  const typeMap: Record<string, string> = {
    'AI': 'primary',
    'EXPERT': 'success',
    'VIDEO': 'warning'
  }
  return typeMap[type] || 'info'
}

// 类型文本
const getTypeText = (type: string) => {
  const typeMap: Record<string, string> = {
    'AI': 'AI咨询',
    'EXPERT': '专家咨询',
    'VIDEO': '视频咨询'
  }
  return typeMap[type] || type
}

// 状态标签样式
const getStatusTagType = (status: string) => {
  const statusMap: Record<string, string> = {
    'PENDING': 'info',
    'IN_PROGRESS': 'warning',
    'COMPLETED': 'success',
    'CANCELLED': 'danger'
  }
  return statusMap[status] || 'info'
}

// 状态文本
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'PENDING': '待处理',
    'IN_PROGRESS': '进行中',
    'COMPLETED': '已完成',
    'CANCELLED': '已取消'
  }
  return statusMap[status] || status
}

// 格式化日期
const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadConsultations()
})
</script>

<style scoped>
.consultation-management {
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
.stat-icon.ai { background: #f9f0ff; }
.stat-icon.expert { background: #fff0e6; }
.stat-icon.satisfaction { background: #f6ffed; }

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

.filter-section {
  background: white;
  padding: 20px;
  margin-bottom: 16px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.table-section {
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.pagination-section {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>