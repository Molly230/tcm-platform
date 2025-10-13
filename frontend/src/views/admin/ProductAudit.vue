<template>
  <div class="product-audit">
    <PageContainer>
      <div class="audit-header">
        <h2>产品审核管理</h2>
        <div class="stats">
          <el-statistic title="待审核" :value="pendingCount" class="stat-item" />
          <el-statistic title="今日审核" :value="todayAuditCount" class="stat-item" />
        </div>
      </div>

      <!-- 筛选条件 -->
      <el-card class="filter-card" shadow="never">
        <el-form :inline="true" @submit.prevent>
          <el-form-item label="审核状态:">
            <el-select v-model="filterStatus" placeholder="全部状态" clearable @change="loadProducts">
              <el-option label="待审核" value="pending" />
              <el-option label="审核通过" value="approved" />
              <el-option label="审核拒绝" value="rejected" />
              <el-option label="需要修改" value="revision" />
            </el-select>
          </el-form-item>
          <el-form-item label="提交人:">
            <el-input v-model="filterSubmitter" placeholder="输入提交人" clearable @change="loadProducts" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="loadProducts">搜索</el-button>
          </el-form-item>
        </el-form>
      </el-card>

      <!-- 产品审核列表 -->
      <el-card class="products-card" shadow="never">
        <div v-loading="loading">
          <el-table :data="products" stripe>
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column label="产品信息" min-width="200">
              <template #default="{ row }">
                <div class="product-info">
                  <img :src="row.images?.[0] || '/default-product.jpg'" class="product-image" />
                  <div class="product-details">
                    <div class="product-name">{{ row.name }}</div>
                    <div class="product-price">¥{{ row.price }}</div>
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="submitted_by" label="提交人" width="120" />
            <el-table-column prop="submitted_at" label="提交时间" width="160">
              <template #default="{ row }">
                {{ formatDate(row.submitted_at) }}
              </template>
            </el-table-column>
            <el-table-column prop="audit_status" label="状态" width="120">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.audit_status)">
                  {{ getStatusText(row.audit_status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="reviewed_by" label="审核人" width="120" />
            <el-table-column prop="reviewed_at" label="审核时间" width="160">
              <template #default="{ row }">
                {{ formatDate(row.reviewed_at) }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200" fixed="right">
              <template #default="{ row }">
                <el-button size="small" @click="viewProduct(row)">查看</el-button>
                <el-button 
                  v-if="row.audit_status === 'PENDING' || row.audit_status === 'pending'"
                  size="small" 
                  type="success" 
                  @click="openAuditDialog(row, 'approve')"
                >
                  通过
                </el-button>
                <el-button 
                  v-if="row.audit_status === 'PENDING' || row.audit_status === 'pending'"
                  size="small" 
                  type="warning" 
                  @click="openAuditDialog(row, 'revision')"
                >
                  修改
                </el-button>
                <el-button 
                  v-if="row.audit_status === 'PENDING' || row.audit_status === 'pending'"
                  size="small" 
                  type="danger" 
                  @click="openAuditDialog(row, 'reject')"
                >
                  拒绝
                </el-button>
              </template>
            </el-table-column>
          </el-table>

          <!-- 分页 -->
          <div class="pagination">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50, 100]"
              :total="total"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="loadProducts"
              @current-change="loadProducts"
            />
          </div>
        </div>
      </el-card>
    </PageContainer>

    <!-- 审核对话框 -->
    <el-dialog
      v-model="auditDialogVisible"
      :title="`产品${auditActionText}`"
      width="600px"
      :before-close="handleAuditDialogClose"
    >
      <div v-if="selectedProduct" class="audit-dialog-content">
        <div class="product-preview">
          <img :src="selectedProduct.images?.[0] || '/default-product.jpg'" class="preview-image" />
          <div class="preview-info">
            <h3>{{ selectedProduct.name }}</h3>
            <p class="price">¥{{ selectedProduct.price }}</p>
            <p class="description">{{ selectedProduct.description }}</p>
          </div>
        </div>

        <el-form ref="auditForm" :model="auditForm" label-width="80px">
          <el-form-item label="审核结果">
            <el-tag :type="getActionType(auditAction)">
              {{ auditActionText }}
            </el-tag>
          </el-form-item>
          <el-form-item label="审核备注" :required="auditAction !== 'approve'">
            <el-input
              v-model="auditForm.notes"
              type="textarea"
              :rows="4"
              :placeholder="getNotesPlaceholder(auditAction)"
            />
          </el-form-item>
        </el-form>
      </div>

      <template #footer>
        <div class="dialog-footer">
          <el-button @click="auditDialogVisible = false">取消</el-button>
          <el-button 
            type="primary" 
            @click="submitAudit"
            :loading="auditing"
            :disabled="auditAction !== 'approve' && !auditForm.notes"
          >
            确认{{ auditActionText }}
          </el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 产品详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="产品详情"
      width="800px"
    >
      <div v-if="selectedProduct" class="product-detail">
        <div class="detail-images">
          <el-image
            v-for="(image, index) in selectedProduct.images || ['/default-product.jpg']"
            :key="index"
            :src="image"
            fit="cover"
            class="detail-image"
          />
        </div>
        <div class="detail-info">
          <h2>{{ selectedProduct.name }}</h2>
          <div class="detail-row">
            <span class="label">价格:</span>
            <span class="value">¥{{ selectedProduct.price }}</span>
          </div>
          <div class="detail-row">
            <span class="label">描述:</span>
            <span class="value">{{ selectedProduct.description }}</span>
          </div>
          <div class="detail-row">
            <span class="label">功效:</span>
            <span class="value">{{ selectedProduct.features?.join(', ') }}</span>
          </div>
          <div class="detail-row">
            <span class="label">使用方法:</span>
            <span class="value">{{ selectedProduct.usage_instructions }}</span>
          </div>
          <div class="detail-row">
            <span class="label">提交人:</span>
            <span class="value">{{ selectedProduct.submitted_by }}</span>
          </div>
          <div v-if="selectedProduct.audit_notes" class="detail-row">
            <span class="label">审核备注:</span>
            <span class="value">{{ selectedProduct.audit_notes }}</span>
          </div>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import PageContainer from '../../components/PageContainer.vue'
import { adminApi } from '../../utils/api'

// 响应式数据
const loading = ref(true)
const auditing = ref(false)
const products = ref<any[]>([])
const total = ref(0)
const currentPage = ref(1)
const pageSize = ref(20)

// 筛选条件
const filterStatus = ref('')
const filterSubmitter = ref('')

// 统计数据
const pendingCount = ref(0)
const todayAuditCount = ref(0)

// 对话框相关
const auditDialogVisible = ref(false)
const detailDialogVisible = ref(false)
const selectedProduct = ref<any>(null)
const auditAction = ref<'approve' | 'reject' | 'revision'>('approve')
const auditForm = ref({
  notes: ''
})

// 计算属性
const auditActionText = computed(() => {
  const map = {
    approve: '通过',
    reject: '拒绝',
    revision: '要求修改'
  }
  return map[auditAction.value]
})

// 方法
const loadProducts = async () => {
  loading.value = true
  try {
    // 使用新的审核API获取待审核产品
    const result = await adminApi.audit.getPending('product')
    
    if (result.success && result.data) {
      // 新API返回的数据结构：{ course: [], expert: [], product: [] }
      let productList = result.data.product || []
      
      // 应用前端过滤（可以考虑后端支持这些过滤）
      if (filterStatus.value) {
        const statusMap = {
          'pending': 'PENDING',
          'approved': 'APPROVED', 
          'rejected': 'REJECTED'
        }
        const targetStatus = statusMap[filterStatus.value]
        if (targetStatus) {
          productList = productList.filter(p => p.audit_status === targetStatus)
        }
      }
      
      if (filterSubmitter.value) {
        productList = productList.filter(p => 
          p.submitted_by?.toLowerCase().includes(filterSubmitter.value.toLowerCase())
        )
      }
      
      // 分页处理（前端分页，后端可以优化）
      const start = (currentPage.value - 1) * pageSize.value
      const end = start + pageSize.value
      products.value = productList.slice(start, end)
      total.value = productList.length
    } else {
      ElMessage.error(result.message || '获取产品列表失败')
      products.value = []
      total.value = 0
    }
  } catch (error) {
    console.error('加载产品失败:', error)
    ElMessage.error('加载产品失败')
    products.value = []
    total.value = 0
  } finally {
    loading.value = false
  }
}

const loadStats = async () => {
  try {
    // 使用新的审核统计API
    const result = await adminApi.audit.getStats()
    
    if (result.success && result.data) {
      const stats = result.data
      // 待审核产品数量
      pendingCount.value = stats.entity_stats?.product?.PENDING || 0
      
      // 最近7天的审核数量
      todayAuditCount.value = stats.recent_activity?.total_actions || 0
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
  }
}

const viewProduct = (product: any) => {
  selectedProduct.value = product
  detailDialogVisible.value = true
}

const openAuditDialog = (product: any, action: 'approve' | 'reject' | 'revision') => {
  selectedProduct.value = product
  auditAction.value = action
  auditForm.value.notes = ''
  auditDialogVisible.value = true
}

const submitAudit = async () => {
  if (auditAction.value !== 'approve' && !auditForm.value.notes) {
    ElMessage.warning('请填写审核备注')
    return
  }

  auditing.value = true
  try {
    // 映射前端action到后端action
    const actionMap = {
      'approve': 'approve',
      'reject': 'reject', 
      'revision': 'reject'  // 前端的"要求修改"映射到后端的reject
    }
    
    const backendAction = actionMap[auditAction.value] || auditAction.value
    
    // 使用新的审核API
    const result = await adminApi.audit.performAudit(
      'product',
      selectedProduct.value.id,
      backendAction,
      auditForm.value.notes, // reason
      auditForm.value.notes  // notes
    )

    if (result.success) {
      ElMessage.success(`产品${auditActionText.value}成功`)
      auditDialogVisible.value = false
      loadProducts()
      loadStats()
    } else {
      ElMessage.error(result.message || '审核失败')
    }
  } catch (error) {
    console.error('审核失败:', error)
    ElMessage.error('审核失败')
  } finally {
    auditing.value = false
  }
}

const handleAuditDialogClose = () => {
  if (auditing.value) return false
  auditDialogVisible.value = false
  return true
}

const getStatusType = (status: string) => {
  const map: Record<string, string> = {
    'DRAFT': 'info',
    'PENDING': 'warning', 
    'APPROVED': 'success',
    'REJECTED': 'danger',
    'PUBLISHED': 'primary',
    'OFFLINE': 'info',
    // 向后兼容旧状态
    'pending': 'warning',
    'approved': 'success',
    'rejected': 'danger',
    'revision': 'info'
  }
  return map[status] || ''
}

const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    'DRAFT': '草稿',
    'PENDING': '待审核',
    'APPROVED': '已通过', 
    'REJECTED': '已拒绝',
    'PUBLISHED': '已发布',
    'OFFLINE': '已下架',
    // 向后兼容旧状态
    'pending': '待审核',
    'approved': '已通过',
    'rejected': '已拒绝',
    'revision': '需修改'
  }
  return map[status] || status
}

const getActionType = (action: string) => {
  const map: Record<string, string> = {
    approve: 'success',
    reject: 'danger',
    revision: 'warning'
  }
  return map[action] || ''
}

const getNotesPlaceholder = (action: string) => {
  const map: Record<string, string> = {
    approve: '审核通过原因（可选）',
    reject: '请说明拒绝原因',
    revision: '请说明需要修改的地方'
  }
  return map[action] || ''
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  loadProducts()
  loadStats()
})
</script>

<style scoped>
.product-audit {
  padding: 20px;
}

.audit-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.stats {
  display: flex;
  gap: 30px;
}

.stat-item {
  text-align: center;
}

.filter-card, .products-card {
  margin-bottom: 20px;
}

.product-info {
  display: flex;
  align-items: center;
  gap: 12px;
}

.product-image {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 6px;
}

.product-details {
  flex: 1;
}

.product-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.product-price {
  color: #f56c6c;
  font-weight: 600;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}

/* 审核对话框样式 */
.audit-dialog-content {
  padding: 10px 0;
}

.product-preview {
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
  padding: 15px;
  background: #fafafa;
  border-radius: 6px;
}

.preview-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 6px;
}

.preview-info h3 {
  margin: 0 0 8px 0;
  color: #303133;
}

.preview-info .price {
  color: #f56c6c;
  font-weight: 600;
  font-size: 16px;
  margin: 0 0 8px 0;
}

.preview-info .description {
  color: #606266;
  font-size: 14px;
  margin: 0;
}

/* 产品详情样式 */
.product-detail {
  padding: 10px 0;
}

.detail-images {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.detail-image {
  width: 100px;
  height: 100px;
  border-radius: 6px;
}

.detail-info h2 {
  margin: 0 0 20px 0;
  color: #303133;
}

.detail-row {
  display: flex;
  margin-bottom: 12px;
  align-items: flex-start;
}

.detail-row .label {
  width: 80px;
  color: #606266;
  flex-shrink: 0;
}

.detail-row .value {
  flex: 1;
  color: #303133;
}
</style>