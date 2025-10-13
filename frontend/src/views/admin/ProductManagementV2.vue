<template>
  <div class="product-management-v2">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h2>🛍️ 商品管理 V2</h2>
        <p>基于新架构的智能商品管理系统</p>
      </div>
      <div class="header-actions">
        <el-button type="primary" @click="showCreateDialog = true">
          <el-icon><Plus /></el-icon>
          新增商品
        </el-button>
        <el-button :loading="loading" @click="refreshData">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
        <el-button @click="showBatchActions = !showBatchActions">
          <el-icon><Operation /></el-icon>
          批量操作
        </el-button>
      </div>
    </div>

    <!-- 智能统计卡片 -->
    <div class="stats-section">
      <div class="stat-card" v-for="stat in productStats" :key="stat.key">
        <div class="stat-icon" :style="{ backgroundColor: stat.color }">
          {{ stat.icon }}
        </div>
        <div class="stat-info">
          <div class="stat-number">{{ stat.value }}</div>
          <div class="stat-label">{{ stat.label }}</div>
          <div v-if="stat.trend" class="stat-trend" :class="stat.trendClass">
            {{ stat.trend }}
          </div>
        </div>
      </div>
    </div>

    <!-- 智能筛选器 -->
    <div class="filter-section">
      <el-card>
        <div class="filter-content">
          <el-input
            v-model="filters.search"
            placeholder="搜索商品名称、描述..."
            style="width: 300px"
            clearable
            @input="handleSearch"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          
          <!-- 使用新的枚举选择组件 -->
          <EnumSelect
            v-model="filters.category"
            enum-type="PRODUCT_CATEGORY"
            placeholder="选择分类"
            clearable
            show-description
            @change="handleCategoryChange"
          />
          
          <EnumSelect
            v-model="filters.status"
            enum-type="PRODUCT_STATUS"
            placeholder="选择状态"
            clearable
            show-icon
            @change="handleStatusChange"
          />

          <EnumSelect
            v-model="filters.auditStatus"
            enum-type="AUDIT_STATUS"
            placeholder="审核状态"
            clearable
            show-icon
            @change="handleAuditStatusChange"
          />

          <el-button @click="resetFilters">重置</el-button>
        </div>
      </el-card>
    </div>

    <!-- 批量操作工具栏 -->
    <div v-if="showBatchActions" class="batch-toolbar">
      <el-alert
        :title="`已选择 ${selectedProducts.length} 个商品`"
        type="info"
        show-icon
        :closable="false"
      />
      
      <div class="batch-actions">
        <StatusTransition
          v-if="selectedProducts.length > 0"
          :current-status="'MIXED'"
          entity-type="product"
          :entity-ids="selectedProducts.map(p => p.id)"
          :selected-count="selectedProducts.length"
          show-batch-actions
          @batch-status-changed="handleBatchStatusChange"
        />
        
        <el-button @click="selectedProducts = []">清空选择</el-button>
      </div>
    </div>

    <!-- 商品列表表格 -->
    <div class="table-section">
      <el-card>
        <el-table
          v-loading="loading"
          :data="filteredProducts"
          @selection-change="handleSelectionChange"
          stripe
          style="width: 100%"
        >
          <el-table-column 
            v-if="showBatchActions"
            type="selection" 
            width="55"
            :selectable="canSelectProduct"
          />
          
          <el-table-column prop="id" label="ID" width="80" />
          
          <el-table-column label="商品信息" min-width="200">
            <template #default="{ row }">
              <div class="product-info">
                <div class="product-image">
                  <el-image
                    v-if="row.images?.length"
                    :src="row.images[0]"
                    :alt="row.name"
                    style="width: 40px; height: 40px"
                    fit="cover"
                  />
                  <div v-else class="no-image">无图</div>
                </div>
                <div class="product-details">
                  <div class="product-name">{{ row.name }}</div>
                  <div class="product-description">{{ row.description }}</div>
                </div>
              </div>
            </template>
          </el-table-column>
          
          <el-table-column label="分类" width="120">
            <template #default="{ row }">
              <el-tag 
                :color="getEnumColor('PRODUCT_CATEGORY', row.category)"
                effect="light"
                size="small"
              >
                {{ getEnumLabel('PRODUCT_CATEGORY', row.category) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column prop="price" label="价格" width="100">
            <template #default="{ row }">
              <span class="price">¥{{ (row.price || 0).toFixed(2) }}</span>
            </template>
          </el-table-column>
          
          <el-table-column prop="stock_quantity" label="库存" width="80">
            <template #default="{ row }">
              <span :class="getStockClass(row.stock_quantity)">
                {{ row.stock_quantity }}
              </span>
            </template>
          </el-table-column>
          
          <el-table-column label="状态" width="120">
            <template #default="{ row }">
              <StatusTransition
                :current-status="row.status"
                entity-type="product"
                :entity-id="row.id"
                @status-changed="handleSingleStatusChange"
              />
            </template>
          </el-table-column>
          
          <el-table-column label="审核状态" width="100">
            <template #default="{ row }">
              <el-tag 
                :type="getAuditStatusType(row.audit_status)"
                size="small"
              >
                {{ getEnumLabel('AUDIT_STATUS', row.audit_status) }}
              </el-tag>
            </template>
          </el-table-column>
          
          <el-table-column label="创建时间" width="180">
            <template #default="{ row }">
              {{ formatDateTime(row.created_at) }}
            </template>
          </el-table-column>
          
          <el-table-column label="操作" width="200" fixed="right">
            <template #default="{ row }">
              <div class="table-actions">
                <el-button size="small" @click="editProduct(row)">
                  编辑
                </el-button>
                <el-button 
                  size="small" 
                  type="info" 
                  @click="viewDetails(row)"
                >
                  详情
                </el-button>
                <el-dropdown @command="handleActionCommand">
                  <el-button size="small" type="text">
                    更多<el-icon><ArrowDown /></el-icon>
                  </el-button>
                  <template #dropdown>
                    <el-dropdown-menu>
                      <el-dropdown-item :command="`duplicate-${row.id}`">
                        复制商品
                      </el-dropdown-item>
                      <el-dropdown-item :command="`audit-${row.id}`">
                        审核记录
                      </el-dropdown-item>
                      <el-dropdown-item :command="`delete-${row.id}`" divided>
                        删除商品
                      </el-dropdown-item>
                    </el-dropdown-menu>
                  </template>
                </el-dropdown>
              </div>
            </template>
          </el-table-column>
        </el-table>

        <!-- 分页 -->
        <div class="pagination-wrapper">
          <el-pagination
            v-model:current-page="pagination.page"
            v-model:page-size="pagination.size"
            :page-sizes="[10, 20, 50, 100]"
            :total="pagination.total"
            layout="total, sizes, prev, pager, next, jumper"
            @size-change="handleSizeChange"
            @current-change="handlePageChange"
          />
        </div>
      </el-card>
    </div>

    <!-- 创建/编辑商品对话框 -->
    <ProductFormDialog
      v-model="showCreateDialog"
      :is-editing="isEditing"
      :product-data="editingProduct"
      @saved="handleProductSaved"
      @cancelled="handleFormCancelled"
    />

    <!-- 商品详情抽屉 -->
    <ProductDetailDrawer
      v-model="showDetailDrawer"
      :product="selectedProduct"
      @edit="editProduct"
      @status-changed="handleSingleStatusChange"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Refresh, Search, Operation, ArrowDown } from '@element-plus/icons-vue'

// 组件导入
import EnumSelect from '@/components/EnumSelect.vue'
import StatusTransition from '@/components/StatusTransition.vue'
import ProductFormDialog from './components/ProductFormDialog.vue'
import ProductDetailDrawer from './components/ProductDetailDrawer.vue'

// 服务导入
import EnumService from '@/services/EnumService'
import { useProductStore } from '@/stores/productStore'
import { useUserStore } from '@/stores/user'

// 类型定义
interface Product {
  id: number
  name: string
  description: string
  category: string
  price: number
  stock_quantity: number
  images: string[]
  status: string
  audit_status: string
  created_at: string
  updated_at: string
}

interface ProductFilters {
  search: string
  category: string
  status: string
  auditStatus: string
}

// 状态管理
const productStore = useProductStore()
const userStore = useUserStore()

// 响应式数据
const loading = ref(false)
const showBatchActions = ref(false)
const showCreateDialog = ref(false)
const showDetailDrawer = ref(false)
const isEditing = ref(false)
const editingProduct = ref<Product | null>(null)
const selectedProduct = ref<Product | null>(null)
const selectedProducts = ref<Product[]>([])

// 筛选器
const filters = ref<ProductFilters>({
  search: '',
  category: '',
  status: '',
  auditStatus: ''
})

// 分页
const pagination = ref({
  page: 1,
  size: 20,
  total: 0
})

// 商品数据
const products = ref<Product[]>([])

// 计算属性
const filteredProducts = computed(() => {
  let result = [...products.value]
  
  // 搜索过滤
  if (filters.value.search) {
    const search = filters.value.search.toLowerCase()
    result = result.filter(product => 
      product.name.toLowerCase().includes(search) ||
      product.description?.toLowerCase().includes(search)
    )
  }
  
  // 分类过滤
  if (filters.value.category) {
    result = result.filter(product => product.category === filters.value.category)
  }
  
  // 状态过滤
  if (filters.value.status) {
    result = result.filter(product => product.status === filters.value.status)
  }
  
  // 审核状态过滤
  if (filters.value.auditStatus) {
    result = result.filter(product => product.audit_status === filters.value.auditStatus)
  }
  
  pagination.value.total = result.length
  return result
})

// 统计数据
const productStats = computed(() => {
  const all = products.value
  const active = all.filter(p => p.status === 'ACTIVE')
  const lowStock = all.filter(p => p.stock_quantity <= 10)
  const pending = all.filter(p => p.audit_status === 'PENDING')
  
  return [
    {
      key: 'total',
      icon: '📦',
      label: '商品总数',
      value: all.length,
      color: '#409EFF',
      trend: '+12%',
      trendClass: 'positive'
    },
    {
      key: 'active',
      icon: '✅',
      label: '在售商品',
      value: active.length,
      color: '#67C23A',
      trend: '+8%',
      trendClass: 'positive'
    },
    {
      key: 'lowStock',
      icon: '⚠️',
      label: '库存不足',
      value: lowStock.length,
      color: '#E6A23C',
      trend: lowStock.length > 5 ? 'HIGH' : 'OK',
      trendClass: lowStock.length > 5 ? 'warning' : 'normal'
    },
    {
      key: 'pending',
      icon: '⏳',
      label: '待审核',
      value: pending.length,
      color: '#F56C6C',
      trend: pending.length > 0 ? 'ACTION' : 'CLEAR',
      trendClass: pending.length > 0 ? 'warning' : 'positive'
    }
  ]
})

// 工具方法
const getEnumLabel = (type: any, code: string) => {
  return EnumService.getEnumLabel(type, code)
}

const getEnumColor = (type: any, code: string) => {
  return EnumService.getEnumColor(type, code)
}

const getAuditStatusType = (status: string) => {
  const typeMap: Record<string, string> = {
    'PENDING': 'warning',
    'APPROVED': 'success',
    'REJECTED': 'danger'
  }
  return typeMap[status] || 'info'
}

const getStockClass = (stock: number) => {
  if (stock <= 0) return 'stock-empty'
  if (stock <= 10) return 'stock-low'
  return 'stock-normal'
}

const formatDateTime = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

const canSelectProduct = (product: Product) => {
  // 可以根据权限或状态限制选择
  return userStore.isAdmin() || product.status !== 'ACTIVE'
}

// 事件处理
const refreshData = async () => {
  loading.value = true
  try {
    // 这里调用实际的API
    // const response = await productStore.fetchProducts()
    // products.value = response.data
    
    // 模拟数据加载
    await new Promise(resolve => setTimeout(resolve, 1000))
    ElMessage.success('数据刷新成功')
  } catch (error: any) {
    ElMessage.error(`刷新失败: ${error.message}`)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  // 防抖处理已在组件内实现
}

const handleCategoryChange = (value: string) => {
  console.log('分类变更:', value)
}

const handleStatusChange = (value: string) => {
  console.log('状态变更:', value)
}

const handleAuditStatusChange = (value: string) => {
  console.log('审核状态变更:', value)
}

const resetFilters = () => {
  filters.value = {
    search: '',
    category: '',
    status: '',
    auditStatus: ''
  }
}

const handleSelectionChange = (selection: Product[]) => {
  selectedProducts.value = selection
}

const handleSingleStatusChange = (data: any) => {
  const product = products.value.find(p => p.id === data.entityId)
  if (product) {
    product.status = data.newStatus
    ElMessage.success(`商品「${product.name}」状态已更新`)
  }
}

const handleBatchStatusChange = (data: any) => {
  data.entityIds.forEach((id: number) => {
    const product = products.value.find(p => p.id === id)
    if (product) {
      product.status = data.newStatus
    }
  })
  selectedProducts.value = []
  ElMessage.success(`批量状态更新完成`)
}

const editProduct = (product: Product) => {
  isEditing.value = true
  editingProduct.value = { ...product }
  showCreateDialog.value = true
}

const viewDetails = (product: Product) => {
  selectedProduct.value = product
  showDetailDrawer.value = true
}

const handleActionCommand = async (command: string) => {
  const [action, id] = command.split('-')
  const productId = parseInt(id)
  
  switch (action) {
    case 'duplicate':
      // 复制商品逻辑
      break
    case 'audit':
      // 查看审核记录
      break
    case 'delete':
      await deleteProduct(productId)
      break
  }
}

const deleteProduct = async (id: number) => {
  try {
    await ElMessageBox.confirm('确认删除该商品？', '删除确认', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    // 调用删除API
    // await productStore.deleteProduct(id)
    
    products.value = products.value.filter(p => p.id !== id)
    ElMessage.success('商品删除成功')
  } catch {
    // 用户取消
  }
}

const handleProductSaved = (product: Product) => {
  if (isEditing.value) {
    const index = products.value.findIndex(p => p.id === product.id)
    if (index !== -1) {
      products.value[index] = product
    }
    ElMessage.success('商品更新成功')
  } else {
    products.value.unshift(product)
    ElMessage.success('商品创建成功')
  }
}

const handleFormCancelled = () => {
  isEditing.value = false
  editingProduct.value = null
}

const handlePageChange = (page: number) => {
  pagination.value.page = page
  // 重新加载数据
}

const handleSizeChange = (size: number) => {
  pagination.value.size = size
  pagination.value.page = 1
  // 重新加载数据
}

// 初始化
onMounted(async () => {
  // 初始化枚举服务
  await EnumService.initialize()
  
  // 加载产品数据
  await refreshData()
})
</script>

<style scoped>
.product-management-v2 {
  padding: 20px;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
}

.header-content h2 {
  margin: 0;
  color: #303133;
}

.header-content p {
  margin: 4px 0 0;
  color: #909399;
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
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 16px;
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  color: white;
}

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 4px;
}

.stat-label {
  color: #909399;
  font-size: 14px;
  margin-bottom: 4px;
}

.stat-trend {
  font-size: 12px;
  font-weight: 500;
}

.stat-trend.positive { color: #67C23A; }
.stat-trend.warning { color: #E6A23C; }
.stat-trend.normal { color: #909399; }

.filter-section,
.table-section {
  margin-bottom: 24px;
}

.filter-content {
  display: flex;
  gap: 16px;
  align-items: center;
  flex-wrap: wrap;
}

.batch-toolbar {
  margin-bottom: 16px;
  padding: 16px;
  background: #f5f7fa;
  border-radius: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.batch-actions {
  display: flex;
  gap: 12px;
  align-items: center;
}

.product-info {
  display: flex;
  gap: 12px;
  align-items: center;
}

.product-image {
  width: 40px;
  height: 40px;
  border-radius: 4px;
  overflow: hidden;
}

.no-image {
  width: 100%;
  height: 100%;
  background: #f5f7fa;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #909399;
}

.product-details {
  flex: 1;
}

.product-name {
  font-weight: 500;
  color: #303133;
  margin-bottom: 4px;
}

.product-description {
  color: #909399;
  font-size: 12px;
  max-width: 200px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.price {
  color: #E6A23C;
  font-weight: 500;
}

.stock-normal { color: #67C23A; }
.stock-low { color: #E6A23C; }
.stock-empty { color: #F56C6C; }

.table-actions {
  display: flex;
  gap: 8px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
</style>