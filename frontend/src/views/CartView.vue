<template>
  <div class="cart">
    <PageContainer>
      <div class="cart-content" v-loading="loading">
        <div class="cart-header">
          <h2>购物车</h2>
          <div class="cart-summary" v-if="cartItems.length > 0">
            <span>共 {{ totalItems }} 件商品</span>
          </div>
        </div>

        <!-- 购物车商品列表 -->
        <div class="cart-main" v-if="cartItems.length > 0">
          <div class="cart-table">
            <!-- 表头 -->
            <div class="cart-header-row">
              <div class="cart-col-select">
                <el-checkbox 
                  v-model="selectAll" 
                  :indeterminate="indeterminate"
                  @change="handleSelectAll"
                >
                  全选
                </el-checkbox>
              </div>
              <div class="cart-col-product">商品信息</div>
              <div class="cart-col-price">单价</div>
              <div class="cart-col-quantity">数量</div>
              <div class="cart-col-total">小计</div>
              <div class="cart-col-action">操作</div>
            </div>

            <!-- 商品列表 -->
            <div class="cart-items">
              <div 
                v-for="item in cartItems" 
                :key="item.id"
                class="cart-item"
                :class="{ 'out-of-stock': item.product.stock_quantity === 0 }"
              >
                <div class="cart-col-select">
                  <el-checkbox 
                    v-model="item.selected"
                    @change="updateSelection"
                    :disabled="item.product.stock_quantity === 0"
                  />
                </div>
                
                <div class="cart-col-product">
                  <div class="product-info">
                    <div class="product-image">
                      <img :src="getProductImage(item.product)" :alt="item.product.name">
                    </div>
                    <div class="product-details">
                      <h3 class="product-name" @click="viewProduct(item.product.id)">
                        {{ item.product.name }}
                      </h3>
                      <p class="product-category">{{ item.product.category }}</p>
                      <div class="product-specs" v-if="item.product.specifications">
                        <span v-if="item.product.specifications.weight">
                          {{ item.product.specifications.weight }}
                        </span>
                        <span v-if="item.product.specifications.origin">
                          {{ item.product.specifications.origin }}
                        </span>
                      </div>
                      <div class="product-features" v-if="item.product.features">
                        <el-tag 
                          v-for="feature in item.product.features.slice(0, 2)" 
                          :key="feature"
                          size="small"
                          type="success"
                          effect="plain"
                        >
                          {{ feature }}
                        </el-tag>
                      </div>
                      <!-- 缺货提示 -->
                      <div v-if="item.product.stock_quantity === 0" class="out-of-stock-notice">
                        <el-tag type="danger" size="small">商品缺货</el-tag>
                      </div>
                      <!-- 库存不足提示 -->
                      <div v-else-if="item.quantity > item.product.stock_quantity" class="stock-warning">
                        <el-tag type="warning" size="small">
                          库存不足，仅剩{{ item.product.stock_quantity }}件
                        </el-tag>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="cart-col-price">
                  <div class="price-info">
                    <span class="current-price">¥{{ item.product.price }}</span>
                    <span 
                      v-if="item.product.original_price && item.product.original_price > item.product.price"
                      class="original-price"
                    >
                      ¥{{ item.product.original_price }}
                    </span>
                  </div>
                </div>

                <div class="cart-col-quantity">
                  <el-input-number
                    v-model="item.quantity"
                    :min="1"
                    :max="Math.min(item.product.stock_quantity, 99)"
                    :disabled="item.product.stock_quantity === 0"
                    @change="updateQuantity(item.id, item.quantity)"
                    size="small"
                    controls-position="right"
                  />
                </div>

                <div class="cart-col-total">
                  <span class="item-total">¥{{ ((parseFloat(item.product.price) || 0) * (parseInt(item.quantity) || 0)).toFixed(2) }}</span>
                </div>

                <div class="cart-col-action">
                  <el-button 
                    type="danger" 
                    link 
                    @click="removeItem(item.id)"
                    :loading="removeLoading[item.id]"
                  >
                    删除
                  </el-button>
                </div>
              </div>
            </div>
          </div>

          <!-- 购物车底部操作栏 -->
          <div class="cart-footer">
            <div class="cart-footer-left">
              <el-checkbox 
                v-model="selectAll" 
                :indeterminate="indeterminate"
                @change="handleSelectAll"
              >
                全选
              </el-checkbox>
              <el-button 
                type="danger" 
                link 
                @click="clearSelected"
                :disabled="selectedItems.length === 0"
              >
                删除选中商品
              </el-button>
            </div>

            <div class="cart-footer-right">
              <div class="total-info">
                <div class="selected-count">
                  已选择 {{ selectedItems.length }} 件商品
                </div>
                <div class="total-price">
                  <span class="total-label">合计：</span>
                  <span class="total-amount">¥{{ totalAmount.toFixed(2) }}</span>
                </div>
                <div class="saved-amount" v-if="savedAmount > 0">
                  已为您节省：¥{{ savedAmount.toFixed(2) }}
                </div>
              </div>
              <el-button 
                type="primary" 
                size="large"
                @click="checkout"
                :disabled="selectedItems.length === 0"
                :loading="checkoutLoading"
              >
                结算({{ selectedItems.length }})
              </el-button>
            </div>
          </div>
        </div>

        <!-- 空购物车状态 -->
        <div class="empty-cart" v-else>
          <el-empty description="购物车还是空的">
            <el-button type="primary" @click="$router.push('/products')">
              去逛逛
            </el-button>
          </el-empty>
        </div>

        <!-- 推荐商品 -->
        <div class="recommended-products" v-if="recommendedProducts.length > 0">
          <h3>为您推荐</h3>
          <div class="products-grid">
            <el-card 
              v-for="product in recommendedProducts" 
              :key="product.id"
              class="product-card"
              shadow="hover"
              @click="viewProduct(product.id)"
            >
              <div class="product-image">
                <img :src="getProductImage(product)" :alt="product.name">
              </div>
              <div class="product-info">
                <h4>{{ product.name }}</h4>
                <div class="product-price">
                  <span class="current-price">¥{{ product.price }}</span>
                </div>
                <el-button 
                  type="primary" 
                  size="small"
                  @click.stop="quickAddToCart(product)"
                  :loading="quickAddLoading[product.id]"
                >
                  加入购物车
                </el-button>
              </div>
            </el-card>
          </div>
        </div>
      </div>
    </PageContainer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import PageContainer from '../components/PageContainer.vue'

const router = useRouter()

// 响应式数据
const loading = ref(true)
const cartItems = ref<any[]>([])
const recommendedProducts = ref<any[]>([])
const removeLoading = ref<Record<number, boolean>>({})
const quickAddLoading = ref<Record<number, boolean>>({})
const checkoutLoading = ref(false)

// 计算属性
const totalItems = computed(() => {
  return cartItems.value.reduce((total, item) => total + item.quantity, 0)
})

const selectedItems = computed(() => {
  return cartItems.value.filter(item => item.selected && item.product.stock_quantity > 0)
})

const totalAmount = computed(() => {
  return selectedItems.value.reduce((total, item) => {
    const price = parseFloat(item.product.price) || 0
    const quantity = parseInt(item.quantity) || 0
    return total + (price * quantity)
  }, 0)
})

const savedAmount = computed(() => {
  return selectedItems.value.reduce((total, item) => {
    const originalPrice = parseFloat(item.product.original_price) || 0
    const currentPrice = parseFloat(item.product.price) || 0
    const quantity = parseInt(item.quantity) || 0
    
    if (originalPrice > currentPrice) {
      return total + ((originalPrice - currentPrice) * quantity)
    }
    return total
  }, 0)
})

const selectAll = computed({
  get() {
    const availableItems = cartItems.value.filter(item => item.product.stock_quantity > 0)
    return availableItems.length > 0 && availableItems.every(item => item.selected)
  },
  set(value) {
    cartItems.value.forEach(item => {
      if (item.product.stock_quantity > 0) {
        item.selected = value
      }
    })
  }
})

const indeterminate = computed(() => {
  const availableItems = cartItems.value.filter(item => item.product.stock_quantity > 0)
  const selectedCount = availableItems.filter(item => item.selected).length
  return selectedCount > 0 && selectedCount < availableItems.length
})

// 获取购物车数据
const fetchCartItems = async () => {
  try {
    loading.value = true
    
    // 从localStorage获取购物车数据
    const cartData = localStorage.getItem('cart')
    if (cartData) {
      const items = JSON.parse(cartData)
      cartItems.value = items.map((item: any) => ({
        ...item,
        selected: item.selected !== false && item.product.stock_quantity > 0 // 保持原有选择状态，缺货商品不选中
      }))
    } else {
      // 如果购物车为空，添加一些测试数据
      const testItems = [
        {
          id: 1,
          product: {
            id: 1,
            name: '灵芝孢子粉胶囊',
            price: 299,
            original_price: 399,
            category: '保健品',
            stock_quantity: 50,
            images: ['https://via.placeholder.com/150x150/4CAF50/FFFFFF?text=灵芝孢子粉'],
            specifications: {
              weight: '60粒/瓶',
              origin: '长白山'
            },
            features: ['增强免疫力', '改善睡眠']
          },
          quantity: 2,
          selected: true
        },
        {
          id: 2,
          product: {
            id: 2,
            name: '人参蜂王浆',
            price: 188,
            original_price: 228,
            category: '滋补品',
            stock_quantity: 30,
            images: ['https://via.placeholder.com/150x150/FF9800/FFFFFF?text=人参蜂王浆'],
            specifications: {
              weight: '10ml*20支',
              origin: '东北'
            },
            features: ['滋补养颜', '提高免疫']
          },
          quantity: 1,
          selected: true
        }
      ]
      
      cartItems.value = testItems
      // 同时保存到localStorage
      localStorage.setItem('cart', JSON.stringify(testItems))
    }
  } catch (error) {
    console.error('获取购物车失败:', error)
    cartItems.value = []
  } finally {
    loading.value = false
  }
}

// 获取推荐商品
const fetchRecommendedProducts = async () => {
  try {
    const response = await fetch('/api/products/?featured_only=true&limit=4')
    if (response.ok) {
      recommendedProducts.value = await response.json()
    }
  } catch (error) {
    console.error('获取推荐商品失败:', error)
  }
}

// 获取商品图片
const getProductImage = (product: any) => {
  if (product.images && product.images.length > 0) {
    return product.images[0]
  }
  return `https://via.placeholder.com/150x150/4CAF50/FFFFFF?text=${encodeURIComponent(product.name)}`
}

// 更新商品数量
const updateQuantity = async (itemId: number, quantity: number) => {
  try {
    // 更新本地购物车数据
    const cartData = JSON.parse(localStorage.getItem('cart') || '[]')
    const itemIndex = cartData.findIndex((item: any) => item.id === itemId)
    
    if (itemIndex > -1) {
      if (quantity <= 0) {
        // 如果数量为0或负数，删除商品
        cartData.splice(itemIndex, 1)
      } else {
        cartData[itemIndex].quantity = quantity
      }
      
      // 保存到localStorage
      localStorage.setItem('cart', JSON.stringify(cartData))
      
      // 更新当前显示的数据
      fetchCartItems()
    }
  } catch (error) {
    console.error('更新数量失败:', error)
    ElMessage.error('更新数量失败')
    // 刷新购物车数据
    fetchCartItems()
  }
}

// 删除商品
const removeItem = async (itemId: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个商品吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    removeLoading.value[itemId] = true
    
    // 从localStorage删除商品
    const cartData = JSON.parse(localStorage.getItem('cart') || '[]')
    const filteredData = cartData.filter((item: any) => item.id !== itemId)
    localStorage.setItem('cart', JSON.stringify(filteredData))
    
    // 更新显示
    cartItems.value = cartItems.value.filter(item => item.id !== itemId)
    ElMessage.success('已删除')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  } finally {
    removeLoading.value[itemId] = false
  }
}

// 删除选中商品
const clearSelected = async () => {
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedItems.value.length} 个商品吗？`,
      '批量删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    const deletePromises = selectedItems.value.map(item => 
      fetch(`/api/products/cart/remove/${item.id}`, { method: 'DELETE' })
    )

    await Promise.all(deletePromises)
    
    // 重新获取购物车数据
    await fetchCartItems()
    ElMessage.success('已删除选中商品')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('批量删除失败:', error)
      ElMessage.error('批量删除失败')
    }
  }
}

// 更新选择状态
const updateSelection = () => {
  // 选择状态通过 v-model 自动更新，同时保存到localStorage
  const cartData = cartItems.value.map(item => ({
    id: item.id,
    product: item.product,
    quantity: item.quantity,
    selected: item.selected
  }))
  localStorage.setItem('cart', JSON.stringify(cartData))
}

// 全选/取消全选
const handleSelectAll = (checked: boolean) => {
  cartItems.value.forEach(item => {
    if (item.product.stock_quantity > 0) {
      item.selected = checked
    }
  })
  // 保存到localStorage
  updateSelection()
}

// 查看商品详情
const viewProduct = (productId: number) => {
  router.push(`/products/${productId}`)
}

// 快速添加到购物车
const quickAddToCart = async (product: any) => {
  try {
    quickAddLoading.value[product.id] = true
    
    const response = await fetch('/api/products/cart/add', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        product_id: product.id,
        quantity: 1
      })
    })
    
    if (response.ok) {
      ElMessage.success('已加入购物车')
      // 刷新购物车数据
      fetchCartItems()
    } else {
      const error = await response.json()
      ElMessage.error(error.detail || '加入购物车失败')
    }
  } catch (error) {
    console.error('加入购物车失败:', error)
    ElMessage.error('加入购物车失败')
  } finally {
    quickAddLoading.value[product.id] = false
  }
}

// 结算
const checkout = () => {
  if (selectedItems.value.length === 0) {
    ElMessage.warning('请先选择要购买的商品')
    return
  }

  checkoutLoading.value = true
  
  try {
    // 构建结算数据
    const checkoutItems = selectedItems.value.map(item => ({
      product_id: item.product.id,
      quantity: item.quantity,
      name: item.product.name,
      price: item.product.price
    }))
    
    console.log('准备结算商品:', checkoutItems)
    
    // 跳转到结算页面，携带商品信息
    const queryParams = new URLSearchParams()
    queryParams.append('items', JSON.stringify(checkoutItems))
    queryParams.append('from', 'cart')
    queryParams.append('total', totalAmount.value.toString())
    
    const checkoutUrl = `/checkout?${queryParams.toString()}`
    console.log('跳转到结算页面:', checkoutUrl)
    
    router.push(checkoutUrl)
  } catch (error) {
    console.error('结算跳转失败:', error)
    ElMessage.error('跳转到结算页面失败')
    checkoutLoading.value = false
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchCartItems()
  fetchRecommendedProducts()
})
</script>

<style scoped>
.cart {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.cart-content {
  max-width: 1200px;
  margin: 0 auto;
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  overflow: hidden;
}

.cart-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 30px;
  border-bottom: 1px solid #eee;
}

.cart-header h2 {
  margin: 0;
  color: #333;
}

.cart-summary {
  color: #666;
  font-size: 14px;
}

.cart-main {
  padding: 0 30px 20px;
}

.cart-table {
  margin: 20px 0;
}

.cart-header-row {
  display: flex;
  align-items: center;
  padding: 15px 0;
  border-bottom: 2px solid #f0f0f0;
  font-weight: 600;
  color: #333;
}

.cart-col-select { flex: 0 0 80px; }
.cart-col-product { flex: 1; }
.cart-col-price { flex: 0 0 120px; text-align: center; }
.cart-col-quantity { flex: 0 0 150px; text-align: center; }
.cart-col-total { flex: 0 0 120px; text-align: center; }
.cart-col-action { flex: 0 0 80px; text-align: center; }

.cart-item {
  display: flex;
  align-items: center;
  padding: 20px 0;
  border-bottom: 1px solid #f0f0f0;
  transition: background-color 0.3s;
}

.cart-item:hover {
  background-color: #fafafa;
}

.cart-item.out-of-stock {
  opacity: 0.6;
  background-color: #f9f9f9;
}

.product-info {
  display: flex;
  gap: 15px;
  width: 100%;
}

.product-image {
  flex: 0 0 80px;
  height: 80px;
  border-radius: 6px;
  overflow: hidden;
}

.product-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.product-details {
  flex: 1;
}

.product-name {
  font-size: 16px;
  color: #333;
  margin: 0 0 5px 0;
  cursor: pointer;
  transition: color 0.3s;
}

.product-name:hover {
  color: #409eff;
}

.product-category {
  font-size: 12px;
  color: #999;
  margin: 0 0 5px 0;
}

.product-specs {
  font-size: 12px;
  color: #666;
  margin-bottom: 5px;
}

.product-specs span {
  margin-right: 15px;
}

.product-features {
  display: flex;
  gap: 5px;
  flex-wrap: wrap;
  margin-bottom: 5px;
}

.out-of-stock-notice,
.stock-warning {
  margin-top: 5px;
}

.price-info {
  text-align: center;
}

.current-price {
  font-size: 16px;
  font-weight: 600;
  color: #f56c6c;
  display: block;
}

.original-price {
  font-size: 12px;
  color: #999;
  text-decoration: line-through;
  margin-top: 2px;
}

.item-total {
  font-size: 16px;
  font-weight: 600;
  color: #f56c6c;
}

.cart-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 0;
  border-top: 2px solid #f0f0f0;
  background-color: #fafafa;
  margin: 0 -30px;
  padding-left: 30px;
  padding-right: 30px;
}

.cart-footer-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.cart-footer-right {
  display: flex;
  align-items: center;
  gap: 20px;
}

.total-info {
  text-align: right;
}

.selected-count {
  font-size: 14px;
  color: #666;
  margin-bottom: 5px;
}

.total-price {
  margin-bottom: 5px;
}

.total-label {
  font-size: 16px;
  color: #333;
}

.total-amount {
  font-size: 24px;
  font-weight: 700;
  color: #f56c6c;
  margin-left: 5px;
}

.saved-amount {
  font-size: 12px;
  color: #67c23a;
}

.empty-cart {
  padding: 80px 30px;
  text-align: center;
}

.recommended-products {
  margin-top: 40px;
  padding: 30px;
  border-top: 1px solid #eee;
  background-color: #fafafa;
}

.recommended-products h3 {
  margin: 0 0 20px 0;
  color: #333;
  font-size: 18px;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 15px;
}

.product-card {
  cursor: pointer;
  transition: transform 0.3s;
}

.product-card:hover {
  transform: translateY(-2px);
}

.product-card .product-image {
  height: 120px;
  margin-bottom: 10px;
}

.product-card .product-info h4 {
  font-size: 14px;
  margin: 0 0 8px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.product-card .product-price {
  margin-bottom: 10px;
}

.product-card .current-price {
  font-size: 14px;
  color: #f56c6c;
  font-weight: 600;
}

@media (max-width: 768px) {
  .cart-main {
    padding: 0 15px 20px;
  }
  
  .cart-header {
    padding: 15px 20px;
  }
  
  .cart-footer {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
    padding: 20px;
    margin: 0 -15px;
  }
  
  .cart-footer-right {
    justify-content: space-between;
  }
  
  .cart-header-row {
    display: none; /* 移动端隐藏表头 */
  }
  
  .cart-item {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
    padding: 15px;
    border: 1px solid #eee;
    border-radius: 8px;
    margin-bottom: 10px;
  }
  
  .cart-col-select,
  .cart-col-product,
  .cart-col-price,
  .cart-col-quantity,
  .cart-col-total,
  .cart-col-action {
    flex: none;
    width: 100%;
    text-align: left;
  }
  
  .products-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>