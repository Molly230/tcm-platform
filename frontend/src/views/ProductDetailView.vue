<template>
  <div class="product-detail">
    <PageContainer>
      <template #breadcrumb>
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">首页</el-breadcrumb-item>
          <el-breadcrumb-item :to="{ path: '/products' }">商城</el-breadcrumb-item>
          <el-breadcrumb-item>{{ product?.name }}</el-breadcrumb-item>
        </el-breadcrumb>
      </template>

      <div class="product-content" v-if="product" v-loading="loading">
        <!-- 商品主要信息 -->
        <div class="product-main">
          <!-- 商品图片区 -->
          <div class="product-images">
            <div class="main-image">
              <img :src="currentImage" :alt="product.name" />
              <div class="image-badges">
                <span v-if="product.is_featured" class="badge featured">推荐</span>
                <span v-if="product.discount < 1" class="badge discount">
                  {{ Math.round(product.discount * 10) }}折
                </span>
              </div>
            </div>
            <div class="thumbnail-list" v-if="product.images && product.images.length > 1">
              <div 
                v-for="(image, index) in product.images" 
                :key="index"
                class="thumbnail"
                :class="{ active: currentImageIndex === index }"
                @click="selectImage(index)"
              >
                <img :src="image" :alt="`${product.name} ${index + 1}`" />
              </div>
            </div>
          </div>

          <!-- 商品信息区 -->
          <div class="product-info">
            <div class="product-header">
              <h1>{{ product.name }}</h1>
              <div class="product-category">
                <el-tag type="success">{{ product.category }}</el-tag>
              </div>
            </div>

            <div class="product-description">
              <p>{{ product.description }}</p>
            </div>

            <!-- 功效特点 -->
            <div class="product-features" v-if="product.features && product.features.length">
              <h3>主要功效</h3>
              <div class="features-list">
                <el-tag 
                  v-for="feature in product.features" 
                  :key="feature"
                  type="success"
                  effect="plain"
                >
                  {{ feature }}
                </el-tag>
              </div>
            </div>

            <!-- 商品规格 -->
            <div class="product-specs" v-if="product.specifications">
              <h3>商品规格</h3>
              <div class="specs-table">
                <div 
                  v-for="(value, key) in product.specifications" 
                  :key="key"
                  class="spec-row"
                >
                  <span class="spec-label">{{ key }}:</span>
                  <span class="spec-value">{{ value }}</span>
                </div>
              </div>
            </div>

            <!-- 用法用量 -->
            <div class="usage-instructions" v-if="product.usage_instructions">
              <h3>用法用量</h3>
              <p>{{ product.usage_instructions }}</p>
            </div>

            <!-- 评价信息 -->
            <div class="product-rating">
              <div class="rating-summary">
                <el-rate 
                  v-model="product.rating" 
                  disabled 
                  show-score 
                  score-template="{value}"
                />
                <span class="rating-text">{{ product.rating }}分</span>
                <span class="review-count">({{ product.review_count }}人评价)</span>
                <span class="sales-count">已售{{ product.sales_count }}件</span>
              </div>
            </div>

            <!-- 价格信息 -->
            <div class="product-price">
              <div class="price-main">
                <span class="current-price">¥{{ product.price }}</span>
                <span 
                  v-if="product.original_price && product.original_price > product.price" 
                  class="original-price"
                >
                  ¥{{ product.original_price }}
                </span>
              </div>
              <div class="price-save" v-if="product.original_price && product.original_price > product.price">
                节省 ¥{{ (product.original_price - product.price).toFixed(2) }}
              </div>
            </div>

            <!-- 库存信息 -->
            <div class="stock-info">
              <span class="stock-label">库存:</span>
              <span class="stock-count" :class="{ 'low-stock': product.stock_quantity < 10 }">
                {{ product.stock_quantity }}件
              </span>
              <span v-if="product.stock_quantity < 10" class="low-stock-warning">
                （库存紧张）
              </span>
            </div>

            <!-- 购买区域 -->
            <div class="purchase-section">
              <div class="quantity-selector">
                <span class="quantity-label">数量:</span>
                <el-input-number 
                  v-model="quantity" 
                  :min="1" 
                  :max="Math.min(product.stock_quantity, 99)"
                  controls-position="right"
                />
              </div>

              <div class="purchase-buttons">
                <el-button 
                  type="primary" 
                  size="large"
                  :loading="cartLoading"
                  @click="addToCart"
                  :disabled="product.stock_quantity === 0"
                >
                  <el-icon><ShoppingCart /></el-icon>
                  加入购物车
                </el-button>
                <el-button 
                  type="danger" 
                  size="large"
                  :loading="buyLoading"
                  @click="buyNow"
                  :disabled="product.stock_quantity === 0"
                >
                  立即购买
                </el-button>
              </div>

              <!-- 缺货提示 -->
              <div v-if="product.stock_quantity === 0" class="out-of-stock">
                <el-alert 
                  title="商品暂时缺货" 
                  type="warning" 
                  show-icon 
                  :closable="false"
                />
              </div>

              <!-- 处方药提示 -->
              <div v-if="product.is_prescription_required" class="prescription-notice">
                <el-alert 
                  title="此商品需要医师处方，购买前请咨询专业医师" 
                  type="info" 
                  show-icon 
                  :closable="false"
                />
              </div>
            </div>
          </div>
        </div>

        <!-- 详细信息标签页 -->
        <div class="product-details">
          <el-tabs v-model="activeDetailTab">
            <el-tab-pane label="商品详情" name="details">
              <div class="detail-content">
                <div class="detail-section">
                  <h3>商品介绍</h3>
                  <p>{{ product.description }}</p>
                </div>

                <div class="detail-section" v-if="product.features">
                  <h3>主要功效</h3>
                  <ul class="features-detail">
                    <li v-for="feature in product.features" :key="feature">
                      {{ feature }}
                    </li>
                  </ul>
                </div>

                <div class="detail-section" v-if="product.usage_instructions">
                  <h3>用法用量</h3>
                  <div class="usage-detail">
                    {{ product.usage_instructions }}
                  </div>
                </div>

                <div class="detail-section">
                  <h3>注意事项</h3>
                  <ul class="precautions">
                    <li>请放置于儿童不能接触的地方</li>
                    <li>请存放于阴凉干燥处，避免阳光直射</li>
                    <li>孕妇、哺乳期妇女及儿童使用前请咨询医师</li>
                    <li>如有不适请立即停用并咨询医师</li>
                    <li v-if="product.is_prescription_required">本品为处方药，需凭医师处方购买和使用</li>
                  </ul>
                </div>
              </div>
            </el-tab-pane>

            <el-tab-pane label="规格参数" name="specifications">
              <div class="specs-content">
                <table class="specs-table-detail" v-if="product.specifications">
                  <tbody>
                    <tr v-for="(value, key) in product.specifications" :key="key">
                      <td class="spec-label">{{ key }}</td>
                      <td class="spec-value">{{ value }}</td>
                    </tr>
                  </tbody>
                </table>
                <div class="additional-specs">
                  <table class="specs-table-detail">
                    <tbody>
                      <tr>
                        <td class="spec-label">商品分类</td>
                        <td class="spec-value">{{ product.category }}</td>
                      </tr>
                      <tr>
                        <td class="spec-label">是否处方药</td>
                        <td class="spec-value">{{ product.is_prescription_required ? '是' : '否' }}</td>
                      </tr>
                      <tr>
                        <td class="spec-label">商品状态</td>
                        <td class="spec-value">{{ product.status === 'active' ? '在售' : '下架' }}</td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </el-tab-pane>

            <el-tab-pane label="用户评价" name="reviews">
              <div class="reviews-content">
                <div class="reviews-summary">
                  <div class="rating-overview">
                    <div class="rating-score">{{ product.rating }}</div>
                    <el-rate v-model="product.rating" disabled />
                    <div class="rating-count">基于{{ product.review_count }}个评价</div>
                  </div>
                </div>
                
                <!-- 评价列表占位 -->
                <div class="reviews-list">
                  <el-empty description="暂无用户评价">
                    <el-button type="primary" @click="$router.push('/products')">
                      查看其他商品
                    </el-button>
                  </el-empty>
                </div>
              </div>
            </el-tab-pane>
          </el-tabs>
        </div>
      </div>

      <!-- 加载状态 -->
      <div class="loading" v-else-if="loading">
        <el-loading element-loading-text="加载商品信息..."></el-loading>
      </div>

      <!-- 商品不存在 -->
      <div class="not-found" v-else>
        <el-empty description="商品不存在或已下架">
          <el-button type="primary" @click="$router.push('/products')">
            返回商城
          </el-button>
        </el-empty>
      </div>
    </PageContainer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { PLACEHOLDER_IMAGES } from '@/utils/placeholder'
import { useRoute, useRouter } from 'vue-router'
import { ShoppingCart } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import PageContainer from '../components/PageContainer.vue'

const route = useRoute()
const router = useRouter()

// 响应式数据 
const product = ref<any>(null)
const loading = ref(true)
const cartLoading = ref(false)
const buyLoading = ref(false)
const quantity = ref(1)
const currentImageIndex = ref(0)
const activeDetailTab = ref('details')

// 计算属性
const currentImage = computed(() => {
  if (!product.value?.images || product.value.images.length === 0) {
    return PLACEHOLDER_IMAGES.product
  }
  return product.value.images[currentImageIndex.value]
})

// 获取商品详情
const fetchProduct = async () => {
  try {
    loading.value = true
    const productId = route.params.id
    const response = await fetch(`/api/products/${productId}`)
    
    if (response.ok) {
      product.value = await response.json()
    } else if (response.status === 404) {
      product.value = null
    } else {
      throw new Error('获取商品信息失败')
    }
  } catch (error) {
    console.error('获取商品失败:', error)
    ElMessage.error('获取商品信息失败')
    product.value = null
  } finally {
    loading.value = false
  }
}

// 选择图片
const selectImage = (index: number) => {
  currentImageIndex.value = index
}

// 加入购物车
const addToCart = async () => {
  if (!product.value) return
  
  try {
    cartLoading.value = true
    
    // 获取现有购物车数据
    const existingCart = JSON.parse(localStorage.getItem('cart') || '[]')
    
    // 检查商品是否已存在
    const existingItemIndex = existingCart.findIndex((item: any) => item.id === product.value.id)
    
    if (existingItemIndex > -1) {
      // 如果已存在，增加数量
      existingCart[existingItemIndex].quantity += quantity.value
    } else {
      // 如果不存在，添加新商品
      existingCart.push({
        id: product.value.id,
        product: product.value,
        quantity: quantity.value,
        selected: true
      })
    }
    
    // 保存到本地存储
    localStorage.setItem('cart', JSON.stringify(existingCart))
    
    ElMessage.success(`已将 ${quantity.value} 件商品加入购物车`)
  } catch (error) {
    console.error('加入购物车失败:', error)
    ElMessage.error('加入购物车失败')
  } finally {
    cartLoading.value = false
  }
}

// 立即购买
const buyNow = async () => {
  if (!product.value) return
  
  try {
    buyLoading.value = true
    
    // 创建临时购物车数据用于直接购买
    const buyNowData = [{
      id: product.value.id,
      product: product.value,
      quantity: quantity.value,
      selected: true
    }]
    
    // 保存到本地存储（临时）
    localStorage.setItem('cart', JSON.stringify(buyNowData))
    
    // 跳转到结算页面
    router.push('/checkout')
  } catch (error) {
    console.error('购买失败:', error)
    ElMessage.error('购买失败')
  } finally {
    buyLoading.value = false
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchProduct()
})
</script>

<style scoped>
.product-detail {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.product-content {
  max-width: 1200px;
  margin: 0 auto;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.product-main {
  display: flex;
  gap: 40px;
  padding: 30px;
  border-bottom: 1px solid #eee;
}

.product-images {
  flex: 0 0 500px;
}

.main-image {
  position: relative;
  width: 100%;
  height: 400px;
  border: 1px solid #eee;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 15px;
}

.main-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.image-badges {
  position: absolute;
  top: 15px;
  right: 15px;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.badge {
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 12px;
  color: white;
  font-weight: 500;
}

.badge.featured {
  background-color: #f56c6c;
}

.badge.discount {
  background-color: #e6a23c;
}

.thumbnail-list {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.thumbnail {
  width: 80px;
  height: 80px;
  border: 2px solid #eee;
  border-radius: 6px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.thumbnail.active,
.thumbnail:hover {
  border-color: #409eff;
}

.thumbnail img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-info {
  flex: 1;
}

.product-header {
  margin-bottom: 20px;
}

.product-header h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 10px;
  line-height: 1.3;
}

.product-description {
  margin-bottom: 25px;
  font-size: 16px;
  color: #666;
  line-height: 1.6;
}

.product-features,
.product-specs,
.usage-instructions {
  margin-bottom: 25px;
}

.product-features h3,
.product-specs h3,
.usage-instructions h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 15px;
}

.features-list {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.specs-table {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 10px;
}

.spec-row {
  display: flex;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.spec-label {
  font-weight: 500;
  color: #333;
  min-width: 80px;
}

.spec-value {
  color: #666;
  margin-left: 10px;
}

.usage-instructions p {
  color: #666;
  line-height: 1.6;
}

.product-rating {
  margin-bottom: 20px;
}

.rating-summary {
  display: flex;
  align-items: center;
  gap: 15px;
  font-size: 14px;
  color: #666;
}

.rating-text {
  font-weight: 600;
  color: #333;
}

.product-price {
  margin-bottom: 20px;
}

.price-main {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 5px;
}

.current-price {
  font-size: 32px;
  font-weight: 700;
  color: #f56c6c;
}

.original-price {
  font-size: 18px;
  color: #999;
  text-decoration: line-through;
}

.price-save {
  font-size: 14px;
  color: #67c23a;
}

.stock-info {
  margin-bottom: 25px;
  font-size: 16px;
}

.stock-label {
  color: #333;
  font-weight: 500;
}

.stock-count {
  margin-left: 8px;
  font-weight: 600;
  color: #67c23a;
}

.stock-count.low-stock {
  color: #e6a23c;
}

.low-stock-warning {
  margin-left: 8px;
  color: #e6a23c;
  font-size: 14px;
}

.purchase-section {
  border-top: 1px solid #eee;
  padding-top: 25px;
}

.quantity-selector {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
  gap: 15px;
}

.quantity-label {
  font-weight: 500;
  color: #333;
}

.purchase-buttons {
  display: flex;
  gap: 15px;
  margin-bottom: 15px;
}

.purchase-buttons .el-button {
  flex: 1;
  height: 50px;
  font-size: 16px;
  font-weight: 600;
}

.out-of-stock,
.prescription-notice {
  margin-top: 15px;
}

.product-details {
  padding: 30px;
}

.detail-content,
.specs-content,
.reviews-content {
  padding: 20px 0;
}

.detail-section {
  margin-bottom: 30px;
}

.detail-section h3 {
  font-size: 18px;
  color: #333;
  margin-bottom: 15px;
  padding-bottom: 8px;
  border-bottom: 2px solid #409eff;
}

.features-detail,
.precautions {
  padding-left: 20px;
  line-height: 1.8;
  color: #666;
}

.features-detail li,
.precautions li {
  margin-bottom: 8px;
}

.usage-detail {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 6px;
  border-left: 4px solid #409eff;
  color: #666;
  line-height: 1.6;
}

.specs-table-detail {
  width: 100%;
  border-collapse: collapse;
}

.specs-table-detail td {
  padding: 12px 15px;
  border-bottom: 1px solid #eee;
}

.specs-table-detail .spec-label {
  background: #f8f9fa;
  font-weight: 500;
  width: 200px;
}

.additional-specs {
  margin-top: 20px;
}

.reviews-summary {
  margin-bottom: 30px;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 8px;
}

.rating-overview {
  display: flex;
  align-items: center;
  gap: 20px;
}

.rating-score {
  font-size: 48px;
  font-weight: 700;
  color: #f56c6c;
}

.rating-count {
  color: #666;
  font-size: 14px;
}

.loading,
.not-found {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 768px) {
  .product-main {
    flex-direction: column;
    gap: 20px;
    padding: 20px;
  }
  
  .product-images {
    flex: none;
  }
  
  .main-image {
    height: 300px;
  }
  
  .purchase-buttons {
    flex-direction: column;
  }
  
  .rating-overview {
    flex-direction: column;
    text-align: center;
    gap: 15px;
  }
  
  .product-details {
    padding: 20px;
  }
}
</style>