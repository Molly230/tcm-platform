<template>
  <div class="shipping-management">
    <div class="page-header">
      <div class="header-content">
        <h2>🚚 配送管理</h2>
        <p>管理订单配送状态和物流信息</p>
      </div>
      <div class="header-actions">
        <el-button @click="loadShippings" :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-section">
      <el-form :inline="true" :model="filters" class="filter-form">
        <el-form-item label="配送状态">
          <el-select
            v-model="filters.status"
            placeholder="全部状态"
            clearable
            @change="loadShippings"
            style="width: 180px"
          >
            <el-option label="待发货" value="PENDING" />
            <el-option label="备货中" value="PREPARING" />
            <el-option label="已发货" value="SHIPPED" />
            <el-option label="运输中" value="IN_TRANSIT" />
            <el-option label="派送中" value="OUT_FOR_DELIVERY" />
            <el-option label="已送达" value="DELIVERED" />
            <el-option label="配送失败" value="FAILED" />
            <el-option label="已退回" value="RETURNED" />
          </el-select>
        </el-form-item>

        <el-form-item label="物流公司">
          <el-select
            v-model="filters.courierCompany"
            placeholder="全部快递"
            clearable
            @change="loadShippings"
            style="width: 150px"
          >
            <el-option label="顺丰速运" value="SF" />
            <el-option label="中通快递" value="ZTO" />
            <el-option label="圆通速递" value="YTO" />
            <el-option label="申通快递" value="STO" />
            <el-option label="韵达快递" value="YD" />
            <el-option label="极兔速递" value="JTSD" />
            <el-option label="京东物流" value="JD" />
            <el-option label="邮政EMS" value="EMS" />
          </el-select>
        </el-form-item>
      </el-form>
    </div>

    <!-- 配送列表 -->
    <el-table
      :data="shippings"
      v-loading="loading"
      stripe
      style="width: 100%"
      class="shipping-table"
    >
      <el-table-column prop="id" label="配送ID" width="80" />

      <el-table-column label="订单信息" width="200">
        <template #default="{ row }">
          <div class="order-cell">
            <div class="order-number">#{{ row.order?.order_number || row.order_id }}</div>
            <div class="order-amount">¥{{ row.order?.total_amount || '-' }}</div>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="物流信息" min-width="250">
        <template #default="{ row }">
          <div class="logistics-cell">
            <div class="company">
              <el-tag size="small" type="info">{{ row.courier_company_name }}</el-tag>
            </div>
            <div class="tracking-number">
              <el-icon><DocumentCopy /></el-icon>
              <span>{{ row.tracking_number }}</span>
              <el-button
                link
                type="primary"
                size="small"
                @click="copyTrackingNumber(row.tracking_number)"
              >
                复制
              </el-button>
            </div>
          </div>
        </template>
      </el-table-column>

      <el-table-column label="配送状态" width="120">
        <template #default="{ row }">
          <el-tag :type="getStatusType(row.status)" effect="dark">
            {{ getStatusLabel(row.status) }}
          </el-tag>
        </template>
      </el-table-column>

      <el-table-column label="配送员" width="150">
        <template #default="{ row }">
          <div v-if="row.courier_name" class="courier-cell">
            <div>{{ row.courier_name }}</div>
            <div class="courier-phone">{{ row.courier_phone }}</div>
          </div>
          <span v-else class="text-secondary">-</span>
        </template>
      </el-table-column>

      <el-table-column label="发货时间" width="180">
        <template #default="{ row }">
          <div v-if="row.shipped_at" class="time-cell">
            <div>{{ formatDate(row.shipped_at) }}</div>
          </div>
          <span v-else class="text-secondary">未发货</span>
        </template>
      </el-table-column>

      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button
            link
            type="primary"
            size="small"
            @click="viewTracking(row)"
          >
            <el-icon><View /></el-icon>
            查看物流
          </el-button>
          <el-button
            link
            type="success"
            size="small"
            @click="refreshTracking(row)"
            :loading="row._refreshing"
          >
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination-section">
      <el-pagination
        v-model:current-page="pagination.page"
        v-model:page-size="pagination.pageSize"
        :total="pagination.total"
        :page-sizes="[10, 20, 50, 100]"
        layout="total, sizes, prev, pager, next, jumper"
        @current-change="loadShippings"
        @size-change="loadShippings"
      />
    </div>

    <!-- 物流详情对话框 -->
    <el-dialog
      v-model="trackingDialogVisible"
      :title="`物流详情 - ${currentShipping?.tracking_number}`"
      width="700px"
    >
      <div class="tracking-dialog-content">
        <div class="shipping-summary">
          <div class="summary-item">
            <span class="label">物流公司：</span>
            <span class="value">{{ currentShipping?.courier_company_name }}</span>
          </div>
          <div class="summary-item">
            <span class="label">物流单号：</span>
            <span class="value">{{ currentShipping?.tracking_number }}</span>
          </div>
          <div class="summary-item">
            <span class="label">当前状态：</span>
            <el-tag :type="getStatusType(currentShipping?.status)">
              {{ getStatusLabel(currentShipping?.status) }}
            </el-tag>
          </div>
        </div>

        <el-divider />

        <TrackingTimeline
          :tracking-history="currentShipping?.tracking_history || []"
          :loading="trackingLoading"
          :error="trackingError"
        />
      </div>

      <template #footer>
        <el-button @click="trackingDialogVisible = false">关闭</el-button>
        <el-button type="primary" @click="refreshCurrentTracking" :loading="trackingLoading">
          <el-icon><Refresh /></el-icon>
          刷新物流
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh, DocumentCopy, View } from '@element-plus/icons-vue'
import TrackingTimeline from '@/components/TrackingTimeline.vue'

interface Shipping {
  id: number
  order_id: number
  order?: {
    order_number: string
    total_amount: number
  }
  courier_company: string
  courier_company_name: string
  tracking_number: string
  status: string
  courier_name?: string
  courier_phone?: string
  shipped_at?: string
  delivered_at?: string
  tracking_history?: any[]
  _refreshing?: boolean
}

const loading = ref(false)
const shippings = ref<Shipping[]>([])
const trackingDialogVisible = ref(false)
const currentShipping = ref<Shipping | null>(null)
const trackingLoading = ref(false)
const trackingError = ref('')

const filters = reactive({
  status: '',
  courierCompany: ''
})

const pagination = reactive({
  page: 1,
  pageSize: 20,
  total: 0
})

const statusLabels: Record<string, string> = {
  PENDING: '待发货',
  PREPARING: '备货中',
  SHIPPED: '已发货',
  IN_TRANSIT: '运输中',
  OUT_FOR_DELIVERY: '派送中',
  DELIVERED: '已送达',
  FAILED: '配送失败',
  RETURNED: '已退回',
  CANCELLED: '已取消'
}

const getStatusLabel = (status: string) => {
  return statusLabels[status] || status
}

const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    PENDING: 'warning',
    PREPARING: 'info',
    SHIPPED: 'primary',
    IN_TRANSIT: 'primary',
    OUT_FOR_DELIVERY: 'success',
    DELIVERED: 'success',
    FAILED: 'danger',
    RETURNED: 'info',
    CANCELLED: 'info'
  }
  return typeMap[status] || 'info'
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const loadShippings = async () => {
  loading.value = true
  try {
    const params: any = {
      skip: (pagination.page - 1) * pagination.pageSize,
      limit: pagination.pageSize
    }

    if (filters.status) {
      params.status = filters.status
    }

    const queryString = new URLSearchParams(params).toString()
    const response = await fetch(`/api/shipping/list?${queryString}`)

    if (!response.ok) {
      throw new Error('加载失败')
    }

    const data = await response.json()
    shippings.value = data
    pagination.total = data.length // 简化版，实际应该从后端返回total
  } catch (error) {
    console.error('加载配送列表失败:', error)
    ElMessage.error('加载配送列表失败')
  } finally {
    loading.value = false
  }
}

const copyTrackingNumber = (trackingNumber: string) => {
  navigator.clipboard.writeText(trackingNumber)
  ElMessage.success('物流单号已复制')
}

const viewTracking = async (shipping: Shipping) => {
  currentShipping.value = shipping
  trackingDialogVisible.value = true

  // 如果没有物流轨迹，自动刷新
  if (!shipping.tracking_history || shipping.tracking_history.length === 0) {
    await refreshCurrentTracking()
  }
}

const refreshTracking = async (shipping: Shipping) => {
  shipping._refreshing = true
  try {
    const response = await fetch('/api/shipping/track', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        order_id: shipping.order_id
      })
    })

    if (!response.ok) {
      throw new Error('刷新物流失败')
    }

    const data = await response.json()

    if (data.success) {
      ElMessage.success('物流信息已更新')
      // 更新当前行的数据
      const index = shippings.value.findIndex(s => s.id === shipping.id)
      if (index !== -1) {
        shippings.value[index].tracking_history = data.tracking_history
        shippings.value[index].status = data.shipping_status
      }
    } else {
      ElMessage.warning(data.error || '查询物流失败')
    }
  } catch (error: any) {
    console.error('刷新物流失败:', error)
    ElMessage.error(error.message || '刷新物流失败')
  } finally {
    shipping._refreshing = false
  }
}

const refreshCurrentTracking = async () => {
  if (!currentShipping.value) return

  trackingLoading.value = true
  trackingError.value = ''

  try {
    const response = await fetch('/api/shipping/track', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        order_id: currentShipping.value.order_id
      })
    })

    if (!response.ok) {
      throw new Error('查询失败')
    }

    const data = await response.json()

    if (data.success) {
      currentShipping.value.tracking_history = data.tracking_history
      currentShipping.value.status = data.shipping_status
      ElMessage.success('物流信息已刷新')
    } else {
      trackingError.value = data.error || '查询物流失败'
    }
  } catch (error: any) {
    console.error('刷新物流失败:', error)
    trackingError.value = error.message || '查询失败'
  } finally {
    trackingLoading.value = false
  }
}

onMounted(() => {
  loadShippings()
})
</script>

<style scoped>
.shipping-management {
  padding: 24px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.header-content h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.header-content p {
  margin: 0;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.header-actions {
  display: flex;
  gap: 12px;
}

.filter-section {
  background: white;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 16px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

.filter-form {
  margin-bottom: 0;
}

.shipping-table {
  background: white;
  border-radius: 8px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}

.order-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.order-number {
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.order-amount {
  font-size: 13px;
  color: var(--el-color-primary);
  font-weight: 600;
}

.logistics-cell {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tracking-number {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  font-family: 'Courier New', monospace;
  color: var(--el-text-color-regular);
}

.courier-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 14px;
}

.courier-phone {
  font-size: 12px;
  color: var(--el-text-color-secondary);
}

.time-cell {
  font-size: 13px;
  color: var(--el-text-color-regular);
}

.text-secondary {
  color: var(--el-text-color-placeholder);
}

.pagination-section {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
  padding: 16px;
  background: white;
  border-radius: 8px;
}

.tracking-dialog-content {
  padding: 0;
}

.shipping-summary {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 16px;
  background: var(--el-fill-color-light);
  border-radius: 8px;
}

.summary-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 14px;
}

.summary-item .label {
  color: var(--el-text-color-secondary);
  min-width: 80px;
}

.summary-item .value {
  color: var(--el-text-color-primary);
  font-weight: 500;
}
</style>
