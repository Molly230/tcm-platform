<template>
  <div class="products-page">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-content">
        <h1>🛍️ 中医商城</h1>
        <p>精选优质中医产品，健康生活从这里开始</p>
      </div>
      <div class="header-stats">
        <div class="stat-item">
          <span class="stat-number">{{ total }}</span>
          <span class="stat-label">商品总数</span>
          <el-button
            type="primary"
            size="small"
            @click="manualRefresh"
            :loading="loading"
            style="margin-top: 8px;"
          >
            🔄 刷新
          </el-button>
        </div>
      </div>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <el-card>
        <el-row :gutter="20" align="middle">
          <el-col :span="8">
            <el-input
              v-model="searchKeyword"
              placeholder="搜索商品名称、描述..."
              prefix-icon="Search"
              clearable
              @input="handleSearch"
            />
          </el-col>
          <el-col :span="6">
            <el-select v-model="selectedCategory" placeholder="选择分类" clearable @change="handleCategoryChange">
              <el-option label="全部分类" value="" />
              <el-option label="🌿 中药材" value="HERBS" />
              <el-option label="💊 养生产品" value="WELLNESS" />
              <el-option label="🏥 医疗器械" value="MEDICAL_DEVICE" />
              <el-option label="🍯 保健食品" value="HEALTH_FOOD" />
              <el-option label="📚 中医书籍" value="TCM_BOOKS" />
              <el-option label="🛠️ 配套用品" value="ACCESSORIES" />
            </el-select>
          </el-col>
          <el-col :span="6">
            <el-select v-model="sortBy" placeholder="排序方式" @change="handleSort">
              <el-option label="综合排序" value="default" />
              <el-option label="价格从低到高" value="price_asc" />
              <el-option label="价格从高到低" value="price_desc" />
              <el-option label="库存优先" value="stock" />
            </el-select>
          </el-col>
          <el-col :span="4">
            <el-switch
              v-model="showFeaturedOnly"
              @change="handleFeaturedFilter"
              active-text="仅显示推荐"
            />
          </el-col>
        </el-row>
      </el-card>
    </div>

    <!-- 商品网格 -->
    <div class="products-grid" v-loading="loading">
      <div
        v-for="product in displayProducts"
        :key="product.id"
        class="product-card"
        @click="goToProductDetail(product.id)"
      >
        <!-- 商品图片 -->
        <div class="product-image">
          <img :src="getProductImage(product)" :alt="product.name" />
          <div class="product-badges">
            <span v-if="product.is_featured" class="badge featured">⭐ 推荐</span>
            <span v-if="product.status === 'ACTIVE'" class="badge active">在售</span>
          </div>
        </div>

        <!-- 商品信息 -->
        <div class="product-info">
          <div class="product-category">{{ getCategoryName(product.category) }}</div>
          <h3 class="product-name">{{ product.name }}</h3>
          <p class="product-description">{{ product.description || '暂无详细描述' }}</p>

          <!-- 库存信息 -->
          <div class="product-stock">
            <span class="stock-label">库存:</span>
            <span :class="['stock-value', { 'low-stock': product.stock_quantity < 10 }]">
              {{ product.stock_quantity }}件
            </span>
          </div>

          <!-- 价格 -->
          <div class="product-price">
            <span class="current-price">¥{{ parseFloat(product.price).toFixed(2) }}</span>
          </div>

          <!-- 操作按钮 -->
          <div class="product-actions">
            <el-button
              type="primary"
              size="small"
              :disabled="product.stock_quantity <= 0"
              @click.stop="addToCart(product)"
              :loading="addingToCart[product.id]"
            >
              <el-icon><ShoppingCart /></el-icon>
              {{ product.stock_quantity > 0 ? '加入购物车' : '缺货' }}
            </el-button>
            <el-button
              size="small"
              :disabled="product.stock_quantity <= 0"
              @click.stop="buyNow(product)"
            >
              立即购买
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="!loading && displayProducts.length === 0" class="empty-state">
      <el-empty description="暂无商品数据">
        <el-button type="primary" @click="fetchProducts">刷新数据</el-button>
      </el-empty>
    </div>

    <!-- 分页 -->
    <div class="pagination-section" v-if="total > pageSize">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :page-sizes="[8, 16, 32]"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ShoppingCart } from '@element-plus/icons-vue'
import { useCartStore } from '../stores/cart'

// 商品接口定义
interface Product {
  id: number
  name: string
  description: string
  category: string
  price: string | number
  stock_quantity: number
  is_featured: boolean
  is_common: boolean
  images: string[]
  status: string
  audit_status: string
  created_at: string
  updated_at: string
  created_by: number
  is_deleted: boolean
  usage_instructions?: string
}

const router = useRouter()
const cartStore = useCartStore()

// 响应式数据
const loading = ref(false)
const products = ref<Product[]>([])
const searchKeyword = ref('')
const selectedCategory = ref('')
const sortBy = ref('default')
const showFeaturedOnly = ref(false)
const currentPage = ref(1)
const pageSize = ref(8)
const total = ref(0)
const addingToCart = ref<Record<number, boolean>>({})

// 分类名称映射
const categoryNames = {
  'HERBS': '🌿 中药材',
  'WELLNESS': '💊 养生产品',
  'MEDICAL_DEVICE': '🏥 医疗器械',
  'HEALTH_FOOD': '🍯 保健食品',
  'TCM_BOOKS': '📚 中医书籍',
  'ACCESSORIES': '🛠️ 配套用品'
}

// 计算属性
const filteredProducts = computed(() => {
  let result = products.value

  // 搜索过滤
  if (searchKeyword.value) {
    const keyword = searchKeyword.value.toLowerCase()
    result = result.filter(product =>
      product.name.toLowerCase().includes(keyword) ||
      (product.description && product.description.toLowerCase().includes(keyword))
    )
  }

  // 分类过滤
  if (selectedCategory.value) {
    result = result.filter(product => product.category === selectedCategory.value)
  }

  // 推荐过滤
  if (showFeaturedOnly.value) {
    result = result.filter(product => product.is_featured)
  }

  // 排序
  if (sortBy.value === 'price_asc') {
    result.sort((a, b) => parseFloat(a.price.toString()) - parseFloat(b.price.toString()))
  } else if (sortBy.value === 'price_desc') {
    result.sort((a, b) => parseFloat(b.price.toString()) - parseFloat(a.price.toString()))
  } else if (sortBy.value === 'stock') {
    result.sort((a, b) => b.stock_quantity - a.stock_quantity)
  }

  return result
})

// 分页显示的商品
const displayProducts = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value
  const end = start + pageSize.value
  return filteredProducts.value.slice(start, end)
})

// 方法
const fetchProducts = async () => {
  loading.value = true
  try {
    const response = await fetch('/api/products-simple/')

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()

    if (Array.isArray(data)) {
      console.log('🔍 API返回商品总数:', data.length)
      console.log('🔍 所有商品状态:', data.map(p => ({id: p.id, name: p.name, status: p.status})))

      // 只显示ACTIVE状态的商品
      products.value = data.filter(product => product.status === 'ACTIVE')
      total.value = products.value.length

      console.log('✅ ACTIVE商品过滤后数量:', products.value.length, '个商品')
      console.log('✅ 过滤后商品列表:', products.value.map(p => ({id: p.id, name: p.name, status: p.status})))
    } else {
      console.error('API返回的数据格式不正确:', data)
      ElMessage.error('商品数据格式错误')
    }
  } catch (error) {
    console.error('获取商品列表失败:', error)
    ElMessage.error('获取商品列表失败，请检查网络连接')
  } finally {
    loading.value = false
  }
}

const getCategoryName = (category: string) => {
  return categoryNames[category] || category
}

const getProductImage = (product: Product) => {
  if (product.images && product.images.length > 0) {
    return product.images[0]
  }
  // 默认图片
  return 'https://via.placeholder.com/300x200?text=' + encodeURIComponent(product.name)
}

const addToCart = async (product: Product) => {
  if (product.stock_quantity <= 0) {
    ElMessage.warning('商品库存不足')
    return
  }

  addingToCart.value[product.id] = true

  try {
    cartStore.addToCart(product, 1)
    ElMessage.success(`${product.name} 已加入购物车`)
  } catch (error) {
    ElMessage.error(error.message || '加入购物车失败')
  } finally {
    addingToCart.value[product.id] = false
  }
}

const buyNow = (product: Product) => {
  if (product.stock_quantity <= 0) {
    ElMessage.warning('商品库存不足')
    return
  }

  // 立即购买：跳转到结算页面，使用查询参数传递商品信息
  router.push({
    path: '/checkout',
    query: {
      productId: product.id.toString(),
      quantity: '1',
      from: 'direct'
    }
  })
}

const goToProductDetail = (productId: number) => {
  router.push(`/products/${productId}`)
}

const handleSearch = () => {
  currentPage.value = 1
}

const handleCategoryChange = () => {
  currentPage.value = 1
}

const handleSort = () => {
  currentPage.value = 1
}

const handleFeaturedFilter = () => {
  currentPage.value = 1
}

const handleSizeChange = (size: number) => {
  pageSize.value = size
  currentPage.value = 1
}

const handleCurrentChange = (page: number) => {
  currentPage.value = page
}

// 定时刷新
const refreshInterval = ref(null)

// 启动定时刷新
const startAutoRefresh = () => {
  refreshInterval.value = setInterval(() => {
    fetchProducts()
    console.log('🔄 自动刷新商品数据')
  }, 30000) // 每30秒刷新一次
}

// 停止定时刷新
const stopAutoRefresh = () => {
  if (refreshInterval.value) {
    clearInterval(refreshInterval.value)
    refreshInterval.value = null
  }
}

// 手动刷新
const manualRefresh = () => {
  fetchProducts()
  ElMessage.success('商品数据已刷新')
}

// 生命周期
onMounted(() => {
  fetchProducts()
  startAutoRefresh()
})

// 组件卸载时清理定时器
onUnmounted(() => {
  stopAutoRefresh()
})
</script>

<style scoped>
.products-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f5f7fa;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  color: white;
}

.header-content h1 {
  margin: 0 0 8px 0;
  font-size: 2.5em;
  font-weight: 700;
}

.header-content p {
  margin: 0;
  opacity: 0.9;
  font-size: 1.1em;
}

.header-stats {
  text-align: center;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-number {
  font-size: 2em;
  font-weight: bold;
  color: #FFD700;
}

.stat-label {
  font-size: 0.9em;
  opacity: 0.8;
}

.filter-section {
  margin-bottom: 30px;
}

.filter-section .el-card {
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.product-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
}

.product-image {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.product-card:hover .product-image img {
  transform: scale(1.05);
}

.product-badges {
  position: absolute;
  top: 12px;
  left: 12px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.badge {
  padding: 4px 8px;
  border-radius: 8px;
  font-size: 0.75em;
  font-weight: 600;
  color: white;
}

.badge.featured {
  background: linear-gradient(45deg, #ff6b6b, #ee5a52);
}

.badge.active {
  background: linear-gradient(45deg, #51cf66, #40c057);
}

.product-info {
  padding: 20px;
}

.product-category {
  font-size: 0.8em;
  color: #667eea;
  font-weight: 600;
  margin-bottom: 8px;
}

.product-name {
  margin: 0 0 8px 0;
  font-size: 1.2em;
  font-weight: 600;
  color: #2d3748;
  line-height: 1.4;
}

.product-description {
  margin: 0 0 12px 0;
  color: #718096;
  font-size: 0.9em;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-stock {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.stock-label {
  font-size: 0.85em;
  color: #718096;
}

.stock-value {
  font-size: 0.85em;
  font-weight: 600;
  color: #48bb78;
}

.stock-value.low-stock {
  color: #f56565;
}

.product-price {
  margin-bottom: 16px;
}

.current-price {
  font-size: 1.5em;
  font-weight: 700;
  color: #e53e3e;
}

.product-actions {
  display: flex;
  gap: 8px;
}

.product-actions .el-button {
  flex: 1;
  border-radius: 8px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
}

.pagination-section {
  display: flex;
  justify-content: center;
  margin-top: 40px;
  padding-top: 30px;
  border-top: 1px solid #e2e8f0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .products-page {
    padding: 15px;
  }

  .page-header {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }

  .filter-section .el-row {
    flex-direction: column;
    gap: 15px;
  }

  .filter-section .el-col {
    width: 100% !important;
  }

  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 16px;
  }
}
</style>