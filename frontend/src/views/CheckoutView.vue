<template>
  <div class="checkout-page">
    <div class="checkout-container">
      <h1>💳 订单结算</h1>

      <div v-if="loading" class="loading">
        <p>⏳ 正在加载商品信息...</p>
      </div>

      <div v-else-if="isFromCart || product" class="checkout-content">
        <!-- 商品信息 -->
        <div class="product-section">
          <h3>📦 商品信息</h3>

          <!-- 购物车模式：显示多个商品 -->
          <template v-if="isFromCart">
            <div v-for="item in cartStore.items" :key="item.id" class="product-item">
              <img :src="getProductImage(item)" :alt="item.product.name" class="product-image" />
              <div class="product-details">
                <h4>{{ item.product.name }}</h4>
                <p>{{ item.product.description }}</p>
                <div class="quantity-info">
                  <span>数量：{{ item.quantity }}</span>
                </div>
              </div>
              <div class="product-price">
                <div class="unit-price">单价：¥{{ parseFloat(item.product.price).toFixed(2) }}</div>
                <div class="total-price">小计：¥{{ (parseFloat(item.product.price) * item.quantity).toFixed(2) }}</div>
              </div>
            </div>
          </template>

          <!-- 立即购买模式：显示单个商品 -->
          <template v-else>
            <div class="product-item">
              <img :src="getProductImage(product)" :alt="product.name" class="product-image" />
              <div class="product-details">
                <h4>{{ product.name }}</h4>
                <p>{{ product.description }}</p>
                <div class="quantity-info">
                  <span>数量：{{ quantity }}</span>
                </div>
              </div>
              <div class="product-price">
                <div class="unit-price">单价：¥{{ product.price }}</div>
                <div class="total-price">小计：¥{{ (product.price * quantity).toFixed(2) }}</div>
              </div>
            </div>
          </template>
        </div>

        <!-- 收货信息 -->
        <div class="address-section">
          <h3>📍 收货信息</h3>
          <el-form :model="addressForm" label-width="80px">
            <el-row :gutter="20">
              <el-col :span="12">
                <el-form-item label="收货人">
                  <el-input v-model="addressForm.name" placeholder="请输入收货人姓名" />
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="联系电话">
                  <el-input v-model="addressForm.phone" placeholder="请输入联系电话" />
                </el-form-item>
              </el-col>
            </el-row>
            <el-form-item label="收货地址">
              <el-input
                v-model="addressForm.address"
                type="textarea"
                :rows="3"
                placeholder="请输入详细地址"
              />
            </el-form-item>
          </el-form>
        </div>

        <!-- 订单汇总 -->
        <div class="summary-section">
          <h3>📋 订单汇总</h3>
          <div class="summary-content">
            <div class="summary-row total">
              <span>应付金额：</span>
              <span class="final-amount">¥{{ finalAmount.toFixed(2) }}</span>
            </div>
          </div>
        </div>

        <!-- 提交订单 -->
        <div class="submit-section">
          <el-button size="large" @click="goBack">返回</el-button>
          <el-button
            type="primary"
            size="large"
            @click="submitOrder"
            :loading="submitting"
            class="submit-btn"
          >
            提交订单并支付 ¥{{ finalAmount.toFixed(2) }}
          </el-button>
        </div>
      </div>

      <div v-else class="error">
        <p>❌ 商品信息加载失败</p>
        <el-button @click="goBack">返回商品页面</el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useCartStore } from '../stores/cart'

interface Product {
  id: number
  name: string
  description: string
  price: number
  stock_quantity: number
  images: string[]
}

const router = useRouter()
const route = useRoute()
const cartStore = useCartStore()

// 判断是从购物车还是立即购买
const isFromCart = computed(() => route.query.from === 'cart')

// 响应式数据
const loading = ref(false)
const submitting = ref(false)
const product = ref<Product | null>(null)
const quantity = ref(1)

// 表单数据
const addressForm = ref({
  name: '',
  phone: '',
  address: ''
})

// 计算属性
const productTotal = computed(() => {
  if (isFromCart.value) {
    return cartStore.totalPrice
  }
  return product.value ? product.value.price * quantity.value : 0
})

const shippingFee = computed(() => {
  return 0  // 免运费
})

const finalAmount = computed(() => {
  return productTotal.value + shippingFee.value
})

// 方法
const fetchProduct = async (productId: number) => {
  loading.value = true
  try {
    const response = await fetch(`/api/products-simple/?id=${productId}`)
    const data = await response.json()

    if (data && Array.isArray(data) && data.length > 0) {
      product.value = data[0]
    } else {
      throw new Error('商品不存在')
    }
  } catch (error) {
    console.error('获取商品失败:', error)
    ElMessage.error('获取商品信息失败')
    product.value = null
  } finally {
    loading.value = false
  }
}

const getProductImage = (item: any) => {
  // 购物车商品格式：item.product.images
  if (item.product && item.product.images && item.product.images.length > 0) {
    return item.product.images[0]
  }
  // 立即购买商品格式：item.images 或 item.image
  if (item.image) return item.image
  if (item.images && item.images.length > 0) return item.images[0]
  return '/placeholder-product.jpg'
}

const goBack = () => {
  router.go(-1)
}

const submitOrder = async () => {
  // 添加详细的调试信息
  console.log('=== 开始提交订单 ===')
  console.log('是否从购物车:', isFromCart.value)
  console.log('购物车商品:', cartStore.items)
  console.log('购物车totalPrice:', cartStore.totalPrice)
  console.log('product.value:', product.value)
  console.log('quantity.value:', quantity.value)
  console.log('productTotal:', productTotal.value)
  console.log('shippingFee:', shippingFee.value)
  console.log('finalAmount:', finalAmount.value)

  // 详细检查购物车每个商品的价格
  if (isFromCart.value && cartStore.items.length > 0) {
    console.log('=== 购物车商品详情 ===')
    cartStore.items.forEach((item, index) => {
      console.log(`商品${index + 1}:`, {
        name: item.product.name,
        price: item.product.price,
        price_type: typeof item.product.price,
        price_parsed: parseFloat(item.product.price),
        quantity: item.quantity,
        subtotal: parseFloat(item.product.price) * item.quantity
      })
    })
    console.log('====================')
  }
  console.log('===================')

  if (!addressForm.value.name || !addressForm.value.phone || !addressForm.value.address) {
    ElMessage.warning('请填写完整的收货信息')
    return
  }

  // 验证商品信息
  if (isFromCart.value) {
    if (cartStore.items.length === 0) {
      ElMessage.warning('购物车为空')
      return
    }
  } else {
    if (!product.value) {
      ElMessage.warning('商品信息不完整')
      return
    }
  }

  submitting.value = true

  try {
    // 获取token
    const token = localStorage.getItem('user_token') || localStorage.getItem('admin_token')
    if (!token) {
      ElMessage.warning('请先登录')
      router.push('/login')
      return
    }

    // 创建订单数据 - 匹配后端schema（不传price，后端会从数据库读取）
    let orderItems
    let remark

    if (isFromCart.value) {
      // 购物车模式：使用购物车中的所有商品
      orderItems = cartStore.items.map(item => ({
        product_id: item.product.id,
        quantity: item.quantity
      }))
      remark = '购物车结算订单'
    } else {
      // 立即购买模式：使用单个商品
      orderItems = [{
        product_id: product.value.id,
        quantity: quantity.value
      }]
      remark = '立即购买订单'
    }

    const orderData = {
      items: orderItems,
      customer_info: {
        name: addressForm.value.name,
        phone: addressForm.value.phone,
        address: addressForm.value.address
      },
      remark: remark,
      total_amount: finalAmount.value,
      subtotal: productTotal.value,
      shipping_fee: shippingFee.value,
      discount_amount: 0
    }

    console.log('提交订单数据:', orderData)

    // 创建订单
    const orderResponse = await fetch('/api/orders/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify(orderData)
    })

    const orderResult = await orderResponse.json()
    console.log('订单响应:', orderResult)

    if (orderResponse.ok && (orderResult.success || orderResult.order_id)) {
      ElMessage.success('订单创建成功！')

      // ⚠️ 重要：在清空购物车之前保存支付金额
      const paymentAmount = finalAmount.value.toFixed(2)
      console.log('=== 准备跳转支付页面 ===')
      console.log('订单ID:', orderResult.order_id)
      console.log('支付金额 finalAmount.value:', finalAmount.value)
      console.log('支付金额格式化:', paymentAmount)
      console.log('订单号:', orderResult.order_number)
      console.log('===========================')

      // 如果是从购物车结算，清空购物车（在保存金额之后）
      if (isFromCart.value) {
        await cartStore.clearCart()
      }

      // 跳转到二维码支付页面
      router.push({
        path: '/payment/qr',
        query: {
          orderId: orderResult.order_id,
          amount: paymentAmount,
          orderNumber: orderResult.order_number
        }
      })
    } else {
      ElMessage.error(orderResult.message || orderResult.detail || '创建订单失败')
    }
  } catch (error) {
    console.error('提交订单失败:', error)
    ElMessage.error('提交订单失败')
  } finally {
    submitting.value = false
  }
}

// 生命周期
onMounted(() => {
  if (isFromCart.value) {
    // 购物车模式：检查购物车是否为空
    if (cartStore.items.length === 0) {
      ElMessage.error('购物车为空')
      router.push('/cart')
    }
  } else {
    // 立即购买模式：需要 productId
    const productId = route.query.productId
    const queryQuantity = route.query.quantity

    if (productId) {
      quantity.value = Number(queryQuantity) || 1
      fetchProduct(Number(productId))
    } else {
      ElMessage.error('缺少商品信息')
      router.push('/products')
    }
  }
})
</script>

<style scoped>
.checkout-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px;
}

.checkout-container {
  max-width: 800px;
  margin: 0 auto;
}

.checkout-container h1 {
  text-align: center;
  color: #2c3e50;
  margin-bottom: 30px;
}

.loading, .error {
  text-align: center;
  padding: 50px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.checkout-content {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.product-section, .address-section, .summary-section {
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #ebeef5;
}

.product-section h3, .address-section h3, .summary-section h3 {
  color: #2c3e50;
  margin-bottom: 20px;
}

.product-item {
  display: flex;
  align-items: center;
  gap: 20px;
  padding-bottom: 15px;
  margin-bottom: 15px;
  border-bottom: 1px solid #ebeef5;
}

.product-item:last-child {
  border-bottom: none;
  margin-bottom: 0;
  padding-bottom: 0;
}

.product-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  flex-shrink: 0;
}

.product-details {
  flex: 1;
}

.product-details h4 {
  color: #2c3e50;
  margin: 0 0 8px 0;
}

.product-details p {
  color: #7f8c8d;
  margin: 0 0 10px 0;
  font-size: 14px;
}

.quantity-info {
  font-size: 14px;
  color: #666;
}

.product-price {
  text-align: right;
}

.unit-price {
  color: #7f8c8d;
  font-size: 12px;
  margin-bottom: 4px;
}

.total-price {
  color: #e74c3c;
  font-weight: 600;
}

.summary-content {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.summary-row.total {
  border-top: 1px solid #dee2e6;
  padding-top: 10px;
  font-weight: 600;
  font-size: 16px;
}

.final-amount {
  color: #e74c3c;
  font-size: 18px;
}

.submit-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 30px;
}

.submit-btn {
  min-width: 200px;
}
</style>