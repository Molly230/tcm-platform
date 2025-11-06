<template>
  <div class="order-management">
    <div class="page-header">
      <div class="header-content">
        <h2>📋 订单管理</h2>
        <p>管理平台订单状态、支付和发货信息</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="exportOrders">
          <el-icon><Download /></el-icon>
          导出订单
        </el-button>
        <el-button @click="loadOrders" :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <div class="stat-card" @click="filterByStatus('')">
        <div class="stat-icon total">📋</div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.total }}</div>
          <div class="stat-label">订单总数</div>
        </div>
      </div>

      <div class="stat-card" @click="filterByStatus('PENDING')">
        <div class="stat-icon pending">⏳</div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.pending }}</div>
          <div class="stat-label">待支付</div>
        </div>
      </div>

      <div class="stat-card" @click="filterByStatus('SHIPPED')">
        <div class="stat-icon shipped">🚚</div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.shipped }}</div>
          <div class="stat-label">已发货</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon revenue">💰</div>
        <div class="stat-info">
          <div class="stat-number">¥{{ stats.revenue }}</div>
          <div class="stat-label">订单总额</div>
        </div>
      </div>
    </div>

    <!-- 筛选栏 -->
    <div class="filter-section">
      <el-input
        v-model="searchText"
        placeholder="搜索订单号..."
        clearable
        style="width: 300px; margin-right: 12px;"
        @input="handleSearch"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
      </el-input>

      <el-select
        v-model="statusFilter"
        placeholder="订单状态"
        clearable
        style="width: 150px;"
        @change="handleFilter"
      >
        <el-option label="全部状态" value="" />
        <el-option label="待支付" value="PENDING" />
        <el-option label="已支付" value="PAID" />
        <el-option label="已发货" value="SHIPPED" />
        <el-option label="已送达" value="DELIVERED" />
        <el-option label="已完成" value="COMPLETED" />
        <el-option label="已取消" value="CANCELLED" />
        <el-option label="已退货" value="RETURNED" />
      </el-select>
    </div>

    <!-- 订单表格 -->
    <div class="table-section">
      <el-table
        :data="paginatedOrders"
        v-loading="loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="order_number" label="订单号" width="220" />

        <el-table-column label="订单信息" min-width="200">
          <template #default="scope">
            <div>
              <div style="font-weight: 500; margin-bottom: 4px;">
                {{ getOrderItemsText(scope.row) }}
              </div>
              <div style="font-size: 12px; color: #666;">
                数量：{{ getOrderItemsCount(scope.row) }} 件
              </div>
            </div>
          </template>
        </el-table-column>

        <el-table-column label="金额" width="120">
          <template #default="scope">
            <div style="font-weight: 500; color: #f56c6c;">
              ¥{{ scope.row.total_amount }}
            </div>
          </template>
        </el-table-column>

        <el-table-column label="状态" width="120">
          <template #default="scope">
            <el-tag :type="getStatusTagType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>

        <el-table-column label="用户ID" width="100" prop="user_id" />

        <el-table-column label="下单时间" width="180">
          <template #default="scope">
            {{ formatDate(scope.row.created_at) }}
          </template>
        </el-table-column>

        <el-table-column label="操作" width="320" fixed="right">
          <template #default="scope">
            <el-button size="small" @click="viewOrder(scope.row)">
              详情
            </el-button>
            <el-button
              v-if="scope.row.status === 'PAID'"
              size="small"
              type="warning"
              @click="handleShipOrder(scope.row)"
            >
              📦 发货
            </el-button>
            <el-dropdown @command="(cmd) => handleOrderAction(cmd, scope.row)">
              <el-button size="small" type="primary">
                更新状态<el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="PAID" v-if="scope.row.status === 'PENDING'">
                    标记已支付
                  </el-dropdown-item>
                  <el-dropdown-item command="SHIPPED" v-if="scope.row.status === 'PAID'">
                    标记已发货
                  </el-dropdown-item>
                  <el-dropdown-item command="DELIVERED" v-if="scope.row.status === 'SHIPPED'">
                    标记已送达
                  </el-dropdown-item>
                  <el-dropdown-item command="COMPLETED" v-if="scope.row.status === 'DELIVERED'">
                    标记已完成
                  </el-dropdown-item>
                  <el-dropdown-item command="CANCELLED" v-if="scope.row.status === 'PENDING'" divided>
                    取消订单
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination-section">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :page-sizes="[10, 20, 50, 100]"
          :total="filteredOrders.length"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </div>

    <!-- 订单详情对话框 -->
    <el-dialog
      v-model="showDetailDialog"
      title="订单详情"
      width="800px"
    >
      <div v-if="currentOrder" class="order-detail">
        <!-- 订单基本信息 -->
        <div class="detail-section">
          <h4>订单信息</h4>
          <div class="info-grid">
            <div class="info-item">
              <span class="label">订单号：</span>
              <span class="value">{{ currentOrder.order_number }}</span>
            </div>
            <div class="info-item">
              <span class="label">订单状态：</span>
              <el-tag :type="getStatusTagType(currentOrder.status)">
                {{ getStatusText(currentOrder.status) }}
              </el-tag>
            </div>
            <div class="info-item">
              <span class="label">下单时间：</span>
              <span class="value">{{ formatDate(currentOrder.created_at) }}</span>
            </div>
            <div class="info-item">
              <span class="label">用户ID：</span>
              <span class="value">{{ currentOrder.user_id }}</span>
            </div>
          </div>
        </div>

        <!-- 商品列表 -->
        <div class="detail-section">
          <h4>商品清单</h4>
          <el-table :data="currentOrder.items" stripe>
            <el-table-column prop="product_name" label="商品名称" />
            <el-table-column prop="product_price" label="单价" width="100">
              <template #default="scope">
                ¥{{ scope.row.product_price }}
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" width="80" />
            <el-table-column label="小计" width="100">
              <template #default="scope">
                ¥{{ (scope.row.product_price * scope.row.quantity).toFixed(2) }}
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 金额信息 -->
        <div class="detail-section">
          <h4>金额信息</h4>
          <div class="amount-info">
            <div class="amount-row">
              <span>商品总额：</span>
              <span>¥{{ currentOrder.total_amount }}</span>
            </div>
            <div class="amount-row" v-if="currentOrder.shipping_fee">
              <span>运费：</span>
              <span>¥{{ currentOrder.shipping_fee }}</span>
            </div>
            <div class="amount-row" v-if="currentOrder.discount_amount">
              <span>优惠金额：</span>
              <span style="color: #67c23a;">-¥{{ currentOrder.discount_amount }}</span>
            </div>
            <div class="amount-row total">
              <span>订单总额：</span>
              <span style="color: #f56c6c; font-size: 18px; font-weight: 600;">
                ¥{{ currentOrder.total_amount }}
              </span>
            </div>
          </div>
        </div>

        <!-- 收货信息 -->
        <div class="detail-section" v-if="currentOrder.shipping_address">
          <h4>收货信息</h4>
          <div class="shipping-info">
            {{ currentOrder.shipping_address }}
          </div>
        </div>

        <!-- 备注 -->
        <div class="detail-section" v-if="currentOrder.notes">
          <h4>订单备注</h4>
          <p class="notes">{{ currentOrder.notes }}</p>
        </div>
      </div>

      <template #footer>
        <el-button @click="showDetailDialog = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 发货对话框 -->
    <ShipOrderDialog
      v-model:visible="showShipDialog"
      :order="orderToShip"
      @success="handleShipSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { Download, Refresh, Search, ArrowDown } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import ShipOrderDialog from '@/components/ShipOrderDialog.vue'

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

const loading = ref(false)
const orders = ref<Order[]>([])
const filteredOrders = ref<Order[]>([])
const currentPage = ref(1)
const pageSize = ref(10)
const searchText = ref('')
const statusFilter = ref('')

const showDetailDialog = ref(false)
const currentOrder = ref<Order | null>(null)

// 发货对话框相关
const showShipDialog = ref(false)
const orderToShip = ref<Order | null>(null)

// 统计数据
const stats = computed(() => {
  const total = orders.value.length
  const pending = orders.value.filter(o => o.status === 'PENDING').length
  const shipped = orders.value.filter(o => o.status === 'SHIPPED').length
  const revenue = orders.value.reduce((sum, o) => sum + Number(o.total_amount), 0).toFixed(2)

  return { total, pending, shipped, revenue }
})

// 分页数据
const paginatedOrders = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredOrders.value.slice(start, end)
})

// 加载订单列表
const loadOrders = async () => {
  loading.value = true
  try {
    // 暂时使用 user/1 接口获取所有订单（该接口返回用户的所有订单）
    // TODO: 后续添加专门的管理员接口
    const response = await fetch('/api/orders/user/1?limit=1000')

    if (!response.ok) {
      throw new Error('加载失败')
    }

    orders.value = await response.json()
    filteredOrders.value = orders.value
    ElMessage.success('加载成功')
  } catch (error: any) {
    console.error('加载订单失败:', error)
    ElMessage.error('加载失败：' + (error.message || '网络错误'))
  } finally {
    loading.value = false
  }
}

// 查看订单详情
const viewOrder = async (order: Order) => {
  try {
    const response = await fetch(`/api/orders/${order.id}`)

    if (!response.ok) {
      throw new Error('获取详情失败')
    }

    currentOrder.value = await response.json()
    showDetailDialog.value = true
  } catch (error: any) {
    console.error('获取订单详情失败:', error)
    ElMessage.error('获取详情失败：' + (error.message || '网络错误'))
  }
}

// 更新订单状态
const handleOrderAction = async (status: string, order: Order) => {
  try {
    await ElMessageBox.confirm(
      `确定要将订单状态更新为"${getStatusText(status)}"吗？`,
      '确认操作',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const response = await fetch(`/api/orders/${order.id}/status`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ status_update: status })
    })

    if (!response.ok) {
      throw new Error('更新失败')
    }

    ElMessage.success('状态更新成功')
    await loadOrders()
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('更新状态失败:', error)
      ElMessage.error('更新失败：' + (error.message || '网络错误'))
    }
  }
}

// 发货处理
const handleShipOrder = (order: Order) => {
  orderToShip.value = order
  showShipDialog.value = true
}

// 发货成功回调
const handleShipSuccess = () => {
  loadOrders()
  showShipDialog.value = false
}

// 搜索
const handleSearch = () => {
  applyFilters()
}

// 过滤
const handleFilter = () => {
  applyFilters()
}

const applyFilters = () => {
  let result = [...orders.value]

  if (searchText.value) {
    const search = searchText.value.toLowerCase()
    result = result.filter(order =>
      order.order_number.toLowerCase().includes(search)
    )
  }

  if (statusFilter.value) {
    result = result.filter(order => order.status === statusFilter.value)
  }

  filteredOrders.value = result
  currentPage.value = 1
}

const filterByStatus = (status: string) => {
  statusFilter.value = status
  applyFilters()
}

// 分页
const handleSizeChange = () => {
  // 页面大小变化时重置到第一页
  currentPage.value = 1
}

const handlePageChange = () => {
  // 页码变化，不需要额外操作
}

// 导出订单
const exportOrders = () => {
  ElMessage.info('导出功能开发中...')
}

// 工具方法
const getStatusText = (status: string) => {
  const statusMap: Record<string, string> = {
    'PENDING': '待支付',
    'PAID': '已支付',
    'SHIPPED': '已发货',
    'DELIVERED': '已送达',
    'COMPLETED': '已完成',
    'CANCELLED': '已取消',
    'RETURNED': '已退货'
  }
  return statusMap[status] || status
}

const getStatusTagType = (status: string) => {
  const typeMap: Record<string, string> = {
    'PENDING': 'warning',
    'PAID': 'primary',
    'SHIPPED': 'info',
    'DELIVERED': 'success',
    'COMPLETED': 'success',
    'CANCELLED': 'danger',
    'RETURNED': 'danger'
  }
  return typeMap[status] || 'info'
}

const getOrderItemsText = (order: Order) => {
  if (!order.items || order.items.length === 0) {
    return '暂无商品信息'
  }

  const firstItem = order.items[0]
  const more = order.items.length > 1 ? ` 等${order.items.length}件商品` : ''
  return `${firstItem.product_name}${more}`
}

const getOrderItemsCount = (order: Order) => {
  if (!order.items) return 0
  return order.items.reduce((sum, item) => sum + item.quantity, 0)
}

const formatDate = (dateStr: string) => {
  if (!dateStr) return '-'
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN')
}

onMounted(() => {
  loadOrders()
})
</script>

<style scoped>
.order-management {
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
  cursor: pointer;
  transition: all 0.3s ease;
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
.stat-icon.pending { background: #fff0e6; }
.stat-icon.shipped { background: #f6ffed; }
.stat-icon.revenue { background: #f9f0ff; }

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

/* 订单详情样式 */
.order-detail {
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

.info-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
}

.info-item {
  display: flex;
  align-items: center;
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

.amount-info {
  padding: 16px;
  background: #f9f9f9;
  border-radius: 4px;
}

.amount-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.amount-row.total {
  margin-top: 12px;
  padding-top: 12px;
  border-top: 1px dashed #ddd;
  font-size: 16px;
}

.shipping-info {
  padding: 12px;
  background: #f9f9f9;
  border-radius: 4px;
  color: #333;
  line-height: 1.6;
}

.notes {
  margin: 0;
  padding: 12px;
  background: #f9f9f9;
  border-radius: 4px;
  color: #666;
  line-height: 1.6;
}
</style>
