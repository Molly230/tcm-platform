<template>
  <div class="my-orders">
    <PageContainer>
      <div class="orders-header">
        <h2>我的订单</h2>
        <p>查看和管理您的订单</p>
      </div>

      <!-- 订单状态筛选 -->
      <div class="status-tabs">
        <el-tabs v-model="activeTab" @tab-change="handleTabChange">
          <el-tab-pane label="全部订单" name="ALL" />
          <el-tab-pane label="待付款" name="PENDING" />
          <el-tab-pane label="待发货" name="PAID" />
          <el-tab-pane label="待收货" name="SHIPPED" />
          <el-tab-pane label="已完成" name="COMPLETED" />
        </el-tabs>
      </div>

      <!-- 订单列表 -->
      <div v-loading="loading" class="orders-list">
        <div v-if="orders.length === 0" class="empty-state">
          <el-empty description="暂无订单" />
        </div>

        <el-card
          v-for="order in orders"
          :key="order.id"
          class="order-card"
          shadow="hover"
        >
          <div class="order-header">
            <div class="order-info">
              <span class="order-number">订单号：{{ order.order_number }}</span>
              <span class="order-date">{{ formatDate(order.created_at) }}</span>
            </div>
            <el-tag :type="getStatusType(order.status)">
              {{ getStatusText(order.status) }}
            </el-tag>
          </div>

          <el-divider />

          <div class="order-items">
            <div
              v-for="item in order.items"
              :key="item.id"
              class="order-item"
            >
              <div class="item-info">
                <span class="item-name">{{ item.product_name }}</span>
                <span class="item-quantity">x{{ item.quantity }}</span>
              </div>
              <div class="item-price">¥{{ item.product_price }}</div>
            </div>
          </div>

          <el-divider />

          <div class="order-footer">
            <div class="order-total">
              <span class="label">订单金额：</span>
              <span class="amount">¥{{ order.total_amount }}</span>
            </div>
            <div class="order-actions">
              <el-button size="small" @click="viewOrderDetail(order)">
                查看详情
              </el-button>
              <el-button
                v-if="order.status === 'SHIPPED' || order.status === 'DELIVERED'"
                size="small"
                type="primary"
                @click="viewTracking(order)"
              >
                <el-icon><Van /></el-icon>
                查看物流
              </el-button>
              <el-button
                v-if="order.status === 'PENDING'"
                size="small"
                type="primary"
              >
                立即付款
              </el-button>
            </div>
          </div>
        </el-card>
      </div>

      <!-- 分页 -->
      <div v-if="total > pageSize" class="pagination">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          layout="prev, pager, next"
          @current-change="loadOrders"
        />
      </div>
    </PageContainer>

    <!-- 订单详情对话框 -->
    <el-dialog
      v-model="detailDialogVisible"
      title="订单详情"
      width="700px"
    >
      <div v-if="currentOrder" class="order-detail">
        <div class="detail-section">
          <h3>订单信息</h3>
          <div class="info-row">
            <span class="label">订单号：</span>
            <span class="value">{{ currentOrder.order_number }}</span>
          </div>
          <div class="info-row">
            <span class="label">下单时间：</span>
            <span class="value">{{ formatDate(currentOrder.created_at) }}</span>
          </div>
          <div class="info-row">
            <span class="label">订单状态：</span>
            <el-tag :type="getStatusType(currentOrder.status)">
              {{ getStatusText(currentOrder.status) }}
            </el-tag>
          </div>
        </div>

        <el-divider />

        <div class="detail-section">
          <h3>商品信息</h3>
          <div
            v-for="item in currentOrder.items"
            :key="item.id"
            class="detail-item"
          >
            <div class="item-row">
              <span class="item-name">{{ item.product_name }}</span>
              <span class="item-quantity">x{{ item.quantity }}</span>
              <span class="item-price">¥{{ item.product_price }}</span>
            </div>
          </div>
        </div>

        <el-divider />

        <div class="detail-section">
          <h3>收货信息</h3>
          <div class="info-row">
            <span class="label">收货地址：</span>
            <span class="value">{{ currentOrder.shipping_address || '未填写' }}</span>
          </div>
          <div v-if="currentOrder.notes" class="info-row">
            <span class="label">订单备注：</span>
            <span class="value">{{ currentOrder.notes }}</span>
          </div>
        </div>

        <el-divider />

        <div class="detail-section">
          <h3>费用明细</h3>
          <div class="info-row">
            <span class="label">商品金额：</span>
            <span class="value">¥{{ currentOrder.total_amount }}</span>
          </div>
          <div class="info-row">
            <span class="label">运费：</span>
            <span class="value">¥{{ currentOrder.shipping_fee || 0 }}</span>
          </div>
          <div v-if="currentOrder.discount_amount" class="info-row">
            <span class="label">优惠：</span>
            <span class="value discount">-¥{{ currentOrder.discount_amount }}</span>
          </div>
          <div class="info-row total-row">
            <span class="label">实付金额：</span>
            <span class="value total">¥{{ currentOrder.total_amount }}</span>
          </div>
        </div>

        <!-- 物流信息区域 -->
        <div
          v-if="currentOrder.status === 'SHIPPED' || currentOrder.status === 'DELIVERED'"
          class="detail-section"
        >
          <div class="section-header">
            <h3>物流信息</h3>
            <el-button
              size="small"
              type="primary"
              :loading="trackingLoading"
              @click="refreshTracking"
            >
              <el-icon><Refresh /></el-icon>
              刷新物流
            </el-button>
          </div>

          <div v-if="shippingInfo" class="shipping-info">
            <div class="info-row">
              <span class="label">物流公司：</span>
              <span class="value">{{ shippingInfo.courier_company_name }}</span>
            </div>
            <div class="info-row">
              <span class="label">物流单号：</span>
              <span class="value tracking-number">
                {{ shippingInfo.tracking_number }}
                <el-button
                  link
                  type="primary"
                  size="small"
                  @click="copyTrackingNumber(shippingInfo.tracking_number)"
                >
                  复制
                </el-button>
              </span>
            </div>
            <div class="info-row">
              <span class="label">配送状态：</span>
              <el-tag :type="getShippingStatusType(shippingInfo.status)">
                {{ getShippingStatusText(shippingInfo.status) }}
              </el-tag>
            </div>
          </div>

          <el-divider />

          <TrackingTimeline
            :tracking-history="trackingHistory"
            :loading="trackingLoading"
            :error="trackingError"
          />
        </div>
      </div>

      <template #footer>
        <el-button @click="detailDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { Van, Refresh } from '@element-plus/icons-vue'
import PageContainer from '../components/PageContainer.vue'
import TrackingTimeline from '../components/TrackingTimeline.vue'

interface OrderItem {
  id: number
  product_id: number
  product_name: string
  product_price: number
  quantity: number
}

interface Order {
  id: number
  order_number: string
  user_id: number
  total_amount: number
  shipping_fee?: number
  discount_amount?: number
  shipping_address?: string
  notes?: string
  status: string
  created_at: string
  items?: OrderItem[]
}

interface ShippingInfo {
  id: number
  order_id: number
  courier_company: string
  courier_company_name: string
  tracking_number: string
  status: string
  tracking_history?: any[]
}

const loading = ref(false)
const orders = ref<Order[]>([])
const activeTab = ref('ALL')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

const detailDialogVisible = ref(false)
const currentOrder = ref<Order | null>(null)
const shippingInfo = ref<ShippingInfo | null>(null)
const trackingHistory = ref<any[]>([])
const trackingLoading = ref(false)
const trackingError = ref('')

const statusLabels: Record<string, string> = {
  PENDING: '待付款',
  PAID: '已付款',
  SHIPPED: '已发货',
  DELIVERED: '已送达',
  COMPLETED: '已完成',
  CANCELLED: '已取消',
  RETURNED: '已退货'
}

const shippingStatusLabels: Record<string, string> = {
  PENDING: '待发货',
  PREPARING: '备货中',
  SHIPPED: '已发货',
  IN_TRANSIT: '运输中',
  OUT_FOR_DELIVERY: '派送中',
  DELIVERED: '已送达',
  FAILED: '配送失败',
  RETURNED: '已退回'
}

const getStatusText = (status: string) => {
  return statusLabels[status] || status
}

const getStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    PENDING: 'warning',
    PAID: 'info',
    SHIPPED: 'primary',
    DELIVERED: 'success',
    COMPLETED: 'success',
    CANCELLED: 'info',
    RETURNED: 'danger'
  }
  return typeMap[status] || 'info'
}

const getShippingStatusText = (status: string) => {
  return shippingStatusLabels[status] || status
}

const getShippingStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    PENDING: 'warning',
    PREPARING: 'info',
    SHIPPED: 'primary',
    IN_TRANSIT: 'primary',
    OUT_FOR_DELIVERY: 'success',
    DELIVERED: 'success',
    FAILED: 'danger',
    RETURNED: 'info'
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

const handleTabChange = () => {
  currentPage.value = 1
  loadOrders()
}

const loadOrders = async () => {
  loading.value = true
  try {
    const params: any = {
      skip: (currentPage.value - 1) * pageSize.value,
      limit: pageSize.value
    }

    if (activeTab.value !== 'ALL') {
      params.status = activeTab.value
    }

    const queryString = new URLSearchParams(params).toString()
    const response = await fetch(`/api/orders/my-orders?${queryString}`)

    if (!response.ok) {
      throw new Error('加载订单失败')
    }

    const data = await response.json()
    orders.value = data.orders || data
    total.value = data.total || orders.value.length
  } catch (error: any) {
    console.error('加载订单失败:', error)
    ElMessage.error(error.message || '加载订单失败')
  } finally {
    loading.value = false
  }
}

const viewOrderDetail = async (order: Order) => {
  currentOrder.value = order
  detailDialogVisible.value = true

  // 如果订单已发货，加载物流信息
  if (order.status === 'SHIPPED' || order.status === 'DELIVERED') {
    await loadShippingInfo(order.id)
  }
}

const viewTracking = async (order: Order) => {
  currentOrder.value = order
  detailDialogVisible.value = true
  await loadShippingInfo(order.id)
}

const loadShippingInfo = async (orderId: number) => {
  try {
    const response = await fetch(`/api/shipping/order/${orderId}`)

    if (!response.ok) {
      throw new Error('加载物流信息失败')
    }

    const data = await response.json()
    shippingInfo.value = data
    trackingHistory.value = data.tracking_history || []

    // 如果没有物流轨迹，自动刷新
    if (!trackingHistory.value || trackingHistory.value.length === 0) {
      await refreshTracking()
    }
  } catch (error: any) {
    console.error('加载物流信息失败:', error)
    // 不显示错误，可能订单还没有物流信息
    shippingInfo.value = null
    trackingHistory.value = []
  }
}

const refreshTracking = async () => {
  if (!currentOrder.value) return

  trackingLoading.value = true
  trackingError.value = ''

  try {
    const response = await fetch('/api/shipping/track', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        order_id: currentOrder.value.id
      })
    })

    if (!response.ok) {
      throw new Error('查询物流失败')
    }

    const data = await response.json()

    if (data.success) {
      trackingHistory.value = data.tracking_history || []
      if (shippingInfo.value) {
        shippingInfo.value.status = data.shipping_status
      }
      ElMessage.success('物流信息已更新')
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

const copyTrackingNumber = (trackingNumber: string) => {
  navigator.clipboard.writeText(trackingNumber)
  ElMessage.success('物流单号已复制')
}

onMounted(() => {
  loadOrders()
})
</script>

<style scoped>
.my-orders {
  min-height: 100vh;
  background: #f5f7fa;
  padding-bottom: 40px;
}

.orders-header {
  padding: 20px 0;
}

.orders-header h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.orders-header p {
  margin: 0;
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.status-tabs {
  background: white;
  border-radius: 8px;
  padding: 0 20px;
  margin-bottom: 20px;
}

.orders-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.order-card {
  transition: all 0.3s;
}

.order-card:hover {
  transform: translateY(-2px);
}

.order-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.order-number {
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.order-date {
  font-size: 13px;
  color: var(--el-text-color-secondary);
}

.order-items {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding: 12px 0;
}

.order-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-info {
  display: flex;
  gap: 12px;
  align-items: center;
}

.item-name {
  font-size: 14px;
  color: var(--el-text-color-primary);
}

.item-quantity {
  font-size: 13px;
  color: var(--el-text-color-secondary);
}

.item-price {
  font-weight: 500;
  color: var(--el-text-color-primary);
}

.order-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
}

.order-total {
  display: flex;
  align-items: center;
  gap: 8px;
}

.order-total .label {
  color: var(--el-text-color-secondary);
  font-size: 14px;
}

.order-total .amount {
  font-size: 18px;
  font-weight: 600;
  color: var(--el-color-primary);
}

.order-actions {
  display: flex;
  gap: 8px;
}

.pagination {
  display: flex;
  justify-content: center;
  margin-top: 32px;
}

.empty-state {
  padding: 60px 20px;
}

/* 订单详情样式 */
.order-detail {
  max-height: 70vh;
  overflow-y: auto;
}

.detail-section {
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.detail-section h3 {
  margin: 0 0 16px 0;
  font-size: 16px;
  font-weight: 600;
  color: var(--el-text-color-primary);
}

.info-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  font-size: 14px;
}

.info-row .label {
  color: var(--el-text-color-secondary);
  min-width: 80px;
}

.info-row .value {
  color: var(--el-text-color-primary);
  flex: 1;
}

.info-row .discount {
  color: var(--el-color-danger);
}

.total-row {
  padding-top: 12px;
  border-top: 1px dashed var(--el-border-color);
}

.total-row .value.total {
  font-size: 18px;
  font-weight: 600;
  color: var(--el-color-danger);
}

.detail-item {
  padding: 8px 0;
}

.item-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 12px;
}

.shipping-info {
  padding: 16px;
  background: var(--el-fill-color-light);
  border-radius: 8px;
  margin-bottom: 16px;
}

.tracking-number {
  font-family: 'Courier New', monospace;
  display: flex;
  align-items: center;
  gap: 8px;
}
</style>
