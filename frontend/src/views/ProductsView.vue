<template>
  <div class="products">
    <PageContainer>
      <div class="products-content" v-loading="loading">
        <div class="products-header">
          <h2>中医商城</h2>
          <p>精选中药材、养生产品，传承千年中医智慧</p>
          
          <!-- 搜索和筛选 -->
          <div class="search-filters">
            <el-input
              v-model="searchText"
              placeholder="搜索商品..."
              clearable
              @input="onSearch"
              class="search-input"
            >
              <template #prefix>
                <el-icon><Search /></el-icon>
              </template>
            </el-input>
            
          </div>
        </div>
        
        <!-- 常用产品快选区域 -->
        <div class="common-products" v-if="commonProducts.length > 0">
          <h3>常用产品</h3>
          <div class="common-products-grid">
            <div 
              v-for="product in commonProducts" 
              :key="product.id"
              class="common-product-card"
              @click="addToCart(product)"
            >
              <img :src="product.images?.[0] || '/default-product.jpg'" :alt="product.name">
              <div class="product-name">{{ product.name }}</div>
              <div class="product-price">¥{{ product.price }}</div>
            </div>
          </div>
        </div>
        
        <!-- 商品网格 -->
        <div class="products-grid">
          <el-card 
            class="product-card" 
            v-for="product in displayProducts" 
            :key="product.id"
            shadow="hover"
            @click="viewProduct(product.id)"
          >
            <div class="product-image">
              <img :src="getProductImage(product)" :alt="product.name">
              <div class="product-badges">
                <span v-if="product.is_featured" class="badge featured">推荐</span>
                <span v-if="product.discount < 1" class="badge discount">
                  {{ Math.round(product.discount * 10) }}折
                </span>
              </div>
            </div>
            
            <div class="product-info">
              <h3 class="product-name">{{ product.name }}</h3>
              <p class="product-description">{{ product.description }}</p>
              
              <div class="product-features" v-if="product.features?.length">
                <el-tag 
                  v-for="feature in product.features.slice(0, 2)" 
                  :key="feature"
                  size="small"
                  type="success"
                >
                  {{ feature }}
                </el-tag>
              </div>
              
              <div class="product-specs" v-if="product.specifications">
                <span v-if="product.specifications.weight" class="spec">
                  重量: {{ product.specifications.weight }}
                </span>
                <span v-if="product.specifications.origin" class="spec">
                  产地: {{ product.specifications.origin }}
                </span>
              </div>
              
              <div class="product-meta">
                <div class="product-rating">
                  <el-rate 
                    v-model="product.rating" 
                    disabled 
                    show-score 
                    score-template="{value}"
                    size="small"
                  />
                  <span class="review-count">({{ product.review_count }}评价)</span>
                </div>
                <div class="product-sales">已售{{ product.sales_count }}件</div>
              </div>
              
              <div class="product-price">
                <span class="current-price">¥{{ product.price }}</span>
                <span 
                  v-if="product.original_price && product.original_price > product.price" 
                  class="original-price"
                >
                  ¥{{ product.original_price }}
                </span>
              </div>
              
              <div class="product-actions">
                <el-button 
                  type="primary" 
                  size="small"
                  @click.stop="addToCart(product)"
                  :loading="cartLoading[product.id]"
                >
                  加入购物车
                </el-button>
                <el-button 
                  size="small"
                  @click.stop="buyNow(product)"
                >
                  立即购买
                </el-button>
              </div>
            </div>
          </el-card>
        </div>
        
        <!-- 空状态 -->
        <div v-if="displayProducts.length === 0 && !loading" class="empty-state">
          <el-empty description="暂无相关商品">
            <el-button type="primary" @click="resetFilters">查看全部商品</el-button>
          </el-empty>
        </div>
        
        <!-- 加载更多 -->
        <div class="load-more" v-if="displayProducts.length > 0 && hasMore">
          <el-button 
            @click="loadMore" 
            :loading="loadingMore"
            size="large"
          >
            加载更多商品
          </el-button>
        </div>
      </div>
    </PageContainer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Search } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import PageContainer from '../components/PageContainer.vue'

const router = useRouter()

// 响应式数据
const activeTab = ref('all')
const searchText = ref('')
const selectedCategory = ref('')
const loading = ref(true)
const loadingMore = ref(false)
const allProducts = ref<any[]>([])
const currentPage = ref(1)
const pageSize = ref(4)
const hasMore = ref(true)
const cartLoading = ref<Record<number, boolean>>({})
const commonProducts = ref<any[]>([]) // 常用产品

// 计算属性 - 筛选后的商品
const displayProducts = computed(() => {
  console.log('计算displayProducts - allProducts长度:', allProducts.value.length)
  console.log('搜索文本:', searchText.value)
  
  let filtered = allProducts.value

  // 搜索筛选
  if (searchText.value) {
    filtered = filtered.filter(product => 
      product.name.toLowerCase().includes(searchText.value.toLowerCase()) ||
      (product.features && product.features.join(' ').includes(searchText.value))
    )
  }

  console.log('过滤后商品数量:', filtered.length)
  return filtered
})

// 获取常用产品
const fetchCommonProducts = async () => {
  try {
    const response = await fetch('/api/products/common')
    if (response.ok) {
      commonProducts.value = await response.json()
    }
  } catch (error) {
    console.error('获取常用产品失败:', error)
  }
}

// 获取商品数据
const fetchProducts = async (page = 1, append = false) => {
  try {
    if (page === 1) loading.value = true
    else loadingMore.value = true

    console.log('正在获取商品数据...')
    const response = await fetch(`/api/products/?skip=${(page - 1) * pageSize.value}&limit=${pageSize.value}`)
    console.log('API响应状态:', response.status, response.ok)
    
    if (!response.ok) {
      throw new Error(`API错误: ${response.status}`)
    }
    
    const products = await response.json()
    console.log('获取到商品数据:', products.length, '个商品')
    
    if (append) {
      allProducts.value.push(...products)
    } else {
      allProducts.value = products
    }
    
    hasMore.value = products.length === pageSize.value
    currentPage.value = page
    
    console.log('商品数据设置完成:', allProducts.value.length)
    
  } catch (error) {
    console.error('获取商品失败:', error)
    ElMessage.error(`获取商品失败: ${error.message}`)
  } finally {
    loading.value = false
    loadingMore.value = false
  }
}

// 获取商品图片
const getProductImage = (product: any) => {
  if (product.images && product.images.length > 0) {
    return product.images[0]
  }
  // 默认占位图
  return `https://via.placeholder.com/300x200/4CAF50/FFFFFF?text=${encodeURIComponent(product.name)}`
}

// 事件处理
const onSearch = () => {
  // 搜索是响应式的，通过computed自动过滤
}

const onCategoryChange = () => {
  // 分类变化时同步更新标签
  activeTab.value = selectedCategory.value || 'all'
}

const onTabChange = (tabName: string) => {
  selectedCategory.value = tabName === 'all' ? '' : tabName
}

const resetFilters = () => {
  activeTab.value = 'all'
  selectedCategory.value = ''
  searchText.value = ''
}

const loadMore = () => {
  fetchProducts(currentPage.value + 1, true)
}

// 商品操作
const viewProduct = (productId: number) => {
  router.push(`/products/${productId}`)
}

const addToCart = async (product: any) => {
  try {
    cartLoading.value[product.id] = true
    
    // 获取现有购物车数据
    const existingCart = JSON.parse(localStorage.getItem('cart') || '[]')
    
    // 检查商品是否已存在
    const existingItemIndex = existingCart.findIndex((item: any) => item.id === product.id)
    
    if (existingItemIndex > -1) {
      // 如果已存在，增加数量
      existingCart[existingItemIndex].quantity += 1
    } else {
      // 如果不存在，添加新商品
      existingCart.push({
        id: product.id,
        product: product,
        quantity: 1,
        selected: true
      })
    }
    
    // 保存到本地存储
    localStorage.setItem('cart', JSON.stringify(existingCart))
    
    // 触发购物车更新事件
    window.dispatchEvent(new CustomEvent('cartUpdated'))
    
    ElMessage.success('已加入购物车')
  } catch (error) {
    console.error('加入购物车失败:', error)
    ElMessage.error('加入购物车失败')
  } finally {
    cartLoading.value[product.id] = false
  }
}

const buyNow = (product: any) => {
  // 创建临时购物车数据用于直接购买
  const buyNowData = [{
    id: product.id,
    product: product,
    quantity: 1,
    selected: true
  }]
  
  // 保存到本地存储（临时）
  localStorage.setItem('cart', JSON.stringify(buyNowData))
  
  // 跳转到结算页面
  router.push('/checkout')
}

// 组件挂载时获取数据
onMounted(() => {
  fetchProducts()
  fetchCommonProducts()
})
</script>

<style scoped>
.products {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.products-content {
  max-width: 1200px;
  margin: 0 auto;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.products-header {
  padding: 30px;
  border-bottom: 1px solid #eee;
}

.products-header h2 {
  color: #333;
  margin-bottom: 10px;
  font-size: 28px;
}

.products-header p {
  color: #666;
  margin-bottom: 20px;
}

.search-filters {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.search-input {
  flex: 1;
  max-width: 400px;
}

.category-select {
  width: 200px;
}

.category-tabs {
  padding: 0 30px;
  margin-bottom: 20px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  padding: 0 30px 30px;
}

.product-card {
  cursor: pointer;
  transition: all 0.3s ease;
  height: fit-content;
}

.product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
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
}

.product-badges {
  position: absolute;
  top: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.badge {
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 12px;
  color: white;
}

.badge.featured {
  background-color: #f56c6c;
}

.badge.discount {
  background-color: #e6a23c;
}

.product-info {
  padding: 15px;
}

.product-name {
  font-size: 16px;
  font-weight: 600;
  color: #333;
  margin-bottom: 8px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-description {
  color: #666;
  font-size: 14px;
  margin-bottom: 10px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  line-height: 1.4;
}

.product-features {
  margin-bottom: 10px;
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
}

.product-specs {
  margin-bottom: 10px;
  font-size: 12px;
  color: #999;
}

.spec {
  margin-right: 10px;
}

.product-meta {
  margin-bottom: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: #999;
}

.product-rating {
  display: flex;
  align-items: center;
  gap: 5px;
}

.review-count {
  margin-left: 5px;
}

.product-price {
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.current-price {
  color: #f56c6c;
  font-size: 18px;
  font-weight: 600;
}

.original-price {
  color: #999;
  text-decoration: line-through;
  font-size: 14px;
}

.product-actions {
  display: flex;
  gap: 10px;
}

.product-actions .el-button {
  flex: 1;
}

.empty-state {
  padding: 60px 30px;
  text-align: center;
}

.load-more {
  padding: 30px;
  text-align: center;
}

/* 常用产品样式 */
.common-products {
  margin: 30px 0;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.common-products h3 {
  margin: 0 0 15px 0;
  color: #333;
  font-size: 18px;
}

.common-products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 15px;
}

.common-product-card {
  background: white;
  border-radius: 6px;
  padding: 10px;
  cursor: pointer;
  transition: transform 0.2s;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.common-product-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.common-product-card img {
  width: 60px;
  height: 60px;
  object-fit: cover;
  border-radius: 4px;
  margin-bottom: 8px;
}

.common-product-card .product-name {
  font-size: 12px;
  color: #333;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.common-product-card .product-price {
  font-size: 14px;
  color: #f56c6c;
  font-weight: 600;
}

@media (max-width: 768px) {
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 15px;
    padding: 0 15px 20px;
  }
  
  .search-filters {
    flex-direction: column;
  }
  
  .search-input,
  .category-select {
    max-width: none;
    width: 100%;
  }
  
  .product-actions {
    flex-direction: column;
  }
}
</style>