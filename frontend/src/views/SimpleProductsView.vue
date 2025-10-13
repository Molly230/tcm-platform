<template>
  <div class="simple-products">
    <div class="products-header">
      <h1>🛍️ 商品商城</h1>
      <p>精选中医保健品，品质保证</p>
    </div>

    <!-- 商品列表 -->
    <div class="products-grid" v-loading="loading">
      <div 
        v-for="product in products" 
        :key="product.id"
        class="product-card"
        @click="viewProduct(product.id)"
      >
        <div class="product-image">
          <img :src="getProductImage(product)" :alt="product.name">
          <div class="product-badges">
            <span v-if="product.original_price && product.original_price > parseFloat(product.price)" class="discount-badge">
              {{ Math.round((1 - parseFloat(product.price) / parseFloat(product.original_price)) * 100) }}% OFF
            </span>
          </div>
        </div>
        
        <div class="product-info">
          <h3 class="product-name">{{ product.name }}</h3>
          <p class="product-description">{{ product.description }}</p>
          
          <div class="product-price">
            <span class="current-price">¥{{ parseFloat(product.price).toFixed(2) }}</span>
            <span v-if="product.original_price && product.original_price > product.price" class="original-price">
              ¥{{ parseFloat(product.original_price).toFixed(2) }}
            </span>
          </div>

          <div class="product-meta">
            <span class="stock">库存: {{ product.stock_quantity }}件</span>
            <span class="category">{{ product.category }}</span>
          </div>

          <div class="product-actions">
            <el-button
              type="primary"
              size="small"
              @click.stop="addToCart(product)"
              :loading="cartLoading[product.id]"
              :disabled="product.stock_quantity === 0"
            >
              {{ product.stock_quantity === 0 ? '缺货' : '加入购物车' }}
            </el-button>
            <el-button
              size="small"
              @click.stop="buyNow(product)"
              :disabled="product.stock_quantity === 0"
            >
              立即购买
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-if="products.length === 0 && !loading" class="empty-state">
      <el-empty description="暂无商品">
        <el-button type="primary" @click="loadProducts">刷新</el-button>
      </el-empty>
    </div>

    <!-- 购物车按钮 -->
    <div class="cart-fab" @click="goToCart" v-if="cartCount > 0">
      <el-badge :value="cartCount" class="cart-badge">
        <el-button type="primary" circle size="large">
          🛒
        </el-button>
      </el-badge>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 响应式数据
const loading = ref(true)
const products = ref<any[]>([])
const cartLoading = ref<Record<number, boolean>>({})
const cart = ref<any[]>([])

// 计算属性
const cartCount = computed(() => {
  return cart.value.reduce((total, item) => total + item.quantity, 0)
})

// 获取商品列表
const loadProducts = async () => {
  try {
    loading.value = true
    const response = await fetch('/api/products-simple/')
    
    if (response.ok) {
      products.value = await response.json()
    } else {
      throw new Error('获取商品失败')
    }
  } catch (error) {
    console.error('获取商品失败:', error)
    ElMessage.error('获取商品失败')
  } finally {
    loading.value = false
  }
}

// 获取商品图片
const getProductImage = (product: any) => {
  if (product.images && product.images.length > 0) {
    return product.images[0]
  }
  return '/default-product.jpg'
}

// 加入购物车
const addToCart = async (product: any) => {
  try {
    cartLoading.value[product.id] = true

    // 获取token
    const token = localStorage.getItem('token')
    if (!token) {
      ElMessage.warning('请先登录')
      router.push('/login')
      return
    }

    const response = await fetch(`/api/cart/items`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        product_id: product.id,
        quantity: 1
      })
    })

    if (response.ok) {
      const cartData = await response.json()
      ElMessage.success('已加入购物车')
      // 更新本地购物车状态
      cart.value = cartData.items || []
    } else {
      const error = await response.json()
      throw new Error(error.detail || '加入购物车失败')
    }
  } catch (error: any) {
    console.error('加入购物车失败:', error)
    ElMessage.error(error.message || '加入购物车失败')
  } finally {
    cartLoading.value[product.id] = false
  }
}

// 立即购买
const buyNow = async (product: any) => {
  try {
    // 先加入购物车
    await addToCart(product)
    // 然后跳转到购物车
    setTimeout(() => {
      router.push('/cart')
    }, 500)
  } catch (error) {
    console.error('立即购买失败:', error)
  }
}

// 查看商品详情
const viewProduct = (productId: number) => {
  router.push(`/simple-products/${productId}`)
}

// 去购物车
const goToCart = () => {
  router.push('/cart')
}

// 加载购物车数据
const loadCart = async () => {
  try {
    const token = localStorage.getItem('token')
    if (!token) {
      // 未登录，不加载购物车
      return
    }

    const response = await fetch('/api/cart/', {
      headers: {
        'Authorization': `Bearer ${token}`
      }
    })

    if (response.ok) {
      const cartData = await response.json()
      cart.value = cartData.items || []
    }
  } catch (error) {
    console.error('加载购物车失败:', error)
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadProducts()
  loadCart()
})
</script>

<style scoped>
.simple-products {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.products-header {
  text-align: center;
  margin-bottom: 40px;
  padding: 40px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.products-header h1 {
  font-size: 2.5rem;
  color: #2d3748;
  margin-bottom: 10px;
  font-weight: 700;
}

.products-header p {
  font-size: 1.2rem;
  color: #718096;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 24px;
  margin-bottom: 40px;
}

.product-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  transition: all 0.3s ease;
  cursor: pointer;
}

.product-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 48px rgba(0,0,0,0.15);
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
  right: 12px;
}

.discount-badge {
  background: linear-gradient(45deg, #ff6b6b, #ee5a24);
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.product-info {
  padding: 20px;
}

.product-name {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 8px;
  line-height: 1.4;
}

.product-description {
  color: #718096;
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 16px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-price {
  margin-bottom: 12px;
}

.current-price {
  font-size: 1.4rem;
  font-weight: 700;
  color: #e53e3e;
}

.original-price {
  font-size: 1rem;
  color: #a0aec0;
  text-decoration: line-through;
  margin-left: 8px;
}

.product-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  font-size: 0.8rem;
  color: #718096;
}

.stock {
  color: #38a169;
  font-weight: 500;
}

.category {
  background: #edf2f7;
  padding: 2px 8px;
  border-radius: 8px;
  font-size: 0.7rem;
}

.product-actions {
  display: flex;
  gap: 8px;
}

.product-actions .el-button {
  flex: 1;
  font-size: 0.9rem;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.cart-fab {
  position: fixed;
  bottom: 30px;
  right: 30px;
  z-index: 1000;
}

.cart-badge {
  cursor: pointer;
}

.cart-badge .el-button {
  width: 60px;
  height: 60px;
  font-size: 1.5rem;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
}

.cart-badge .el-button:hover {
  transform: scale(1.1);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .simple-products {
    padding: 10px;
  }
  
  .products-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 16px;
  }
  
  .products-header {
    padding: 30px 15px;
  }
  
  .products-header h1 {
    font-size: 2rem;
  }
  
  .product-info {
    padding: 15px;
  }
  
  .cart-fab {
    bottom: 20px;
    right: 20px;
  }
}
</style>
