<template>
  <div class="payment-container">
    <div class="payment-content" v-loading="loading">
      <!-- 支付头部 -->
      <div class="payment-header">
        <el-icon size="48" color="#67c23a"><SuccessFilled /></el-icon>
        <h2>订单已创建，请完成支付</h2>
        <p class="order-info">订单号：{{ orderInfo.order_number }}</p>
      </div>

      <!-- 订单信息 -->
      <el-card class="order-summary-card" shadow="never">
        <template #header>
          <div class="card-header">
            <el-icon><Document /></el-icon>
            <span>订单信息</span>
          </div>
        </template>

        <div class="order-details">
          <div class="detail-row">
            <span class="label">订单金额：</span>
            <span class="value amount">¥{{ orderInfo.total_amount }}</span>
          </div>
          <div class="detail-row">
            <span class="label">创建时间：</span>
            <span class="value">{{ formatTime(orderInfo.created_at) }}</span>
          </div>
          <div class="detail-row">
            <span class="label">收货地址：</span>
            <span class="value">{{ formatAddress(orderInfo.shipping_address) }}</span>
          </div>
        </div>

        <!-- 商品列表摘要 -->
        <div class="products-summary">
          <div class="summary-title">商品清单（{{ orderInfo.order_items?.length || 0 }}件）</div>
          <div class="product-list">
            <div 
              v-for="item in orderInfo.order_items" 
              :key="item.id"
              class="product-item"
            >
              <el-image 
                :src="item.product_image || PLACEHOLDER_IMAGES.product" 
                class="product-image"
              />
              <div class="product-info">
                <div class="product-name">{{ item.product_name }}</div>
                <div class="product-detail">
                  <span class="quantity">x{{ item.quantity }}</span>
                  <span class="price">¥{{ item.unit_price }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 支付方式选择 -->
      <el-card class="payment-method-card" shadow="never">
        <template #header>
          <div class="card-header">
            <el-icon><CreditCard /></el-icon>
            <span>选择支付方式</span>
          </div>
        </template>

        <div class="payment-methods">
          <div 
            v-for="method in paymentMethods" 
            :key="method.value"
            class="payment-option"
            :class="{ active: selectedMethod === method.value }"
            @click="selectedMethod = method.value"
          >
            <el-radio v-model="selectedMethod" :value="method.value" />
            <div class="method-info">
              <el-icon :size="32" :color="method.color">
                <component :is="method.icon" />
              </el-icon>
              <div class="method-details">
                <div class="method-name">{{ method.name }}</div>
                <div class="method-desc">{{ method.description }}</div>
              </div>
            </div>
            <div class="method-status">
              <el-tag v-if="method.recommended" type="success" size="small">推荐</el-tag>
            </div>
          </div>
        </div>
      </el-card>

      <!-- 支付操作 -->
      <div class="payment-actions">
        <div class="payment-amount">
          <span class="amount-label">需支付：</span>
          <span class="amount-value">¥{{ orderInfo.total_amount }}</span>
        </div>
        <div class="action-buttons">
          <el-button size="large" @click="cancelPayment">取消支付</el-button>
          <el-button 
            type="primary" 
            size="large" 
            :loading="paying"
            @click="processPay"
          >
            {{ paying ? '支付中...' : '立即支付' }}
          </el-button>
        </div>
      </div>
    </div>

    <!-- 支付结果对话框 -->
    <el-dialog 
      v-model="showPaymentResult" 
      :title="paymentSuccess ? '支付成功' : '支付失败'"
      width="400px"
      :show-close="false"
      :close-on-click-modal="false"
      :close-on-press-escape="false"
    >
      <div class="payment-result">
        <div class="result-icon">
          <el-icon v-if="paymentSuccess" size="64" color="#67c23a">
            <SuccessFilled />
          </el-icon>
          <el-icon v-else size="64" color="#f56c6c">
            <CircleCloseFilled />
          </el-icon>
        </div>
        <div class="result-message">
          <h3>{{ paymentSuccess ? '支付成功！' : '支付失败' }}</h3>
          <p v-if="paymentSuccess">您的订单已支付成功，我们将尽快为您安排发货。</p>
          <p v-else>{{ paymentError || '支付过程中出现问题，请重试或联系客服。' }}</p>
        </div>
      </div>
      <template #footer>
        <div class="result-actions">
          <el-button v-if="!paymentSuccess" @click="showPaymentResult = false">重试支付</el-button>
          <el-button v-if="paymentSuccess" type="primary" @click="viewOrder">查看订单</el-button>
          <el-button v-if="paymentSuccess" @click="continueShopping">继续购物</el-button>
        </div>
      </template>
    </el-dialog>

    <!-- 倒计时提示 -->
    <div v-if="countdown > 0" class="countdown-notice">
      <el-alert
        :title="`请在 ${formatCountdown(countdown)} 内完成支付，超时订单将自动取消`"
        type="warning"
        :closable="false"
        show-icon
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { PLACEHOLDER_IMAGES } from '@/utils/placeholder'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  SuccessFilled, 
  CircleCloseFilled,
  Document,
  CreditCard,
  Wallet,
  ChatDotRound,
  Money
} from '@element-plus/icons-vue'

interface OrderInfo {
  id: number
  order_number: string
  total_amount: number
  created_at: string
  shipping_address: string
  status: string
  order_items?: Array<{
    id: number
    product_id: number
    product_name: string
    product_image?: string
    quantity: number
    unit_price: number
    total_price: number
  }>
}

interface PaymentMethod {
  value: string
  name: string
  description: string
  icon: any
  color: string
  recommended?: boolean
}

const route = useRoute()
const router = useRouter()

// 状态管理
const loading = ref(true)
const paying = ref(false)
const orderInfo = ref<OrderInfo>({
  id: 0,
  order_number: '',
  total_amount: 0,
  created_at: '',
  shipping_address: '',
  status: ''
})
const selectedMethod = ref('alipay_qr')
const showPaymentResult = ref(false)
const paymentSuccess = ref(false)
const paymentError = ref('')
const countdown = ref(30 * 60) // 30分钟倒计时
let countdownTimer: NodeJS.Timeout | null = null

// 支付方式配置
const paymentMethods: PaymentMethod[] = [
  {
    value: 'alipay_qr',
    name: '支付宝扫码',
    description: '使用支付宝扫描二维码支付',
    icon: Wallet,
    color: '#1677ff',
    recommended: true
  },
  {
    value: 'alipay',
    name: '支付宝网页',
    description: '跳转支付宝网页支付',
    icon: Wallet,
    color: '#1677ff'
  },
  {
    value: 'wechat',
    name: '微信支付',
    description: '使用微信钱包快捷支付',
    icon: ChatDotRound,
    color: '#07c160'
  }
]

// 获取订单信息
const loadOrderInfo = async () => {
  try {
    const orderId = route.params.orderId
    if (!orderId) {
      ElMessage.error('订单信息获取失败')
      router.push('/cart')
      return
    }

    // API调用
    const response = await fetch(`/api/orders/${orderId}`)
    if (!response.ok) {
      throw new Error('获取订单信息失败')
    }

    orderInfo.value = await response.json()
    
    // 如果订单已支付，直接跳转
    if (orderInfo.value.status === 'paid' || orderInfo.value.status === 'PAID') {
      ElMessage.info('订单已支付')
      router.push(`/order/${orderId}`)
      return
    }
    
    // 启动倒计时
    startCountdown()
    
  } catch (error) {
    console.error('获取订单信息失败:', error)
    
    // 模拟订单数据用于演示
    orderInfo.value = {
      id: parseInt(route.params.orderId as string) || 1,
      order_number: 'TCM' + Date.now(),
      total_amount: 299.80,
      created_at: new Date().toISOString(),
      shipping_address: '北京市朝阳区建国门外大街1号',
      status: 'pending_payment',
      order_items: [
        {
          id: 1,
          product_id: 1,
          product_name: '灵芝孢子粉胶囊',
          product_image: PLACEHOLDER_IMAGES.product,
          quantity: 2,
          unit_price: 149.90,
          total_price: 299.80
        }
      ]
    }
    startCountdown()
  } finally {
    loading.value = false
  }
}

// 启动倒计时
const startCountdown = () => {
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer!)
      handleTimeout()
    }
  }, 1000)
}

// 处理超时
const handleTimeout = () => {
  ElMessageBox.confirm(
    '支付超时，订单已自动取消。是否重新创建订单？',
    '支付超时',
    {
      confirmButtonText: '重新下单',
      cancelButtonText: '返回购物车',
      type: 'warning'
    }
  ).then(() => {
    router.push('/checkout')
  }).catch(() => {
    router.push('/cart')
  })
}

// 格式化倒计时
const formatCountdown = (seconds: number) => {
  const minutes = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

// 格式化时间
const formatTime = (dateString: string) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleString()
}

// 格式化地址
const formatAddress = (address: any) => {
  if (typeof address === 'string') return address
  if (!address || typeof address !== 'object') return ''
  
  const { province = '', city = '', district = '', address: detail = '' } = address
  return `${province}${city}${district}${detail}`
}

// 处理支付
const processPay = async () => {
  if (!selectedMethod.value) {
    ElMessage.warning('请选择支付方式')
    return
  }

  paying.value = true
  
  try {
    // 调用后端支付API
    const response = await fetch(`/api/reliable-pay/create`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        order_id: orderInfo.value.order_number,
        payment_method: selectedMethod.value
      })
    })
    
    if (!response.ok) {
      throw new Error(`支付请求失败: ${response.status}`)
    }
    
    const result = await response.json()
    console.log('支付结果:', result)
    
    if (result.success && result.payment_url) {
      // 清除倒计时
      if (countdownTimer) {
        clearInterval(countdownTimer)
        countdownTimer = null
      }
      
      if (selectedMethod.value === 'alipay_qr' || selectedMethod.value === 'wechat') {
        // 二维码支付：显示二维码
        ElMessage.success('支付二维码生成成功！请扫描二维码完成支付')
        console.log('二维码内容:', result.payment_url)
        
        // 这里应该显示二维码，暂时先在控制台显示
        // 可以用 qrcode.js 库生成二维码显示
        
      } else if (selectedMethod.value === 'alipay') {
        // 网页跳转支付
        if (result.payment_url.startsWith('http')) {
          window.open(result.payment_url, '_blank')
          ElMessage.info('正在跳转到支付页面...')
        } else {
          // 如果是HTML表单，插入页面并提交
          const tempDiv = document.createElement('div')
          tempDiv.innerHTML = result.payment_url
          document.body.appendChild(tempDiv)
          ElMessage.info('正在跳转到支付宝支付页面...')
        }
        
      } else {
        // 其他支付方式
        ElMessage.info('支付方式处理中...')
      }
      
    } else {
      // 支付失败
      paymentSuccess.value = false
      paymentError.value = result.message || result.error || '支付失败，请重试'
      showPaymentResult.value = true
      ElMessage.error(result.message || result.error || '支付失败')
    }
    
  } catch (error) {
    console.error('支付失败:', error)
    paymentSuccess.value = false
    paymentError.value = '网络错误，请检查网络连接后重试'
    showPaymentResult.value = true
  } finally {
    paying.value = false
  }
}

// 取消支付
const cancelPayment = () => {
  ElMessageBox.confirm(
    '确定要取消支付吗？订单将被取消。',
    '取消支付',
    {
      confirmButtonText: '确定取消',
      cancelButtonText: '继续支付',
      type: 'warning'
    }
  ).then(() => {
    if (countdownTimer) {
      clearInterval(countdownTimer)
    }
    router.push('/cart')
  }).catch(() => {})
}

// 查看订单
const viewOrder = () => {
  router.push(`/order/${orderInfo.value.id}`)
}

// 继续购物
const continueShopping = () => {
  router.push('/products')
}

onMounted(() => {
  loadOrderInfo()
})

onUnmounted(() => {
  if (countdownTimer) {
    clearInterval(countdownTimer)
  }
})
</script>

<style scoped>
.payment-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.payment-content {
  background: white;
  border-radius: 8px;
  overflow: hidden;
}

/* 支付头部 */
.payment-header {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  border-bottom: 1px solid #e4e7ed;
}

.payment-header h2 {
  margin: 16px 0 8px;
  color: #303133;
  font-size: 24px;
  font-weight: 600;
}

.order-info {
  color: #909399;
  margin: 0;
  font-size: 16px;
}

/* 卡片 */
.order-summary-card,
.payment-method-card {
  margin: 20px 0;
}

.card-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 16px;
  font-weight: 600;
}

/* 订单详情 */
.order-details {
  margin-bottom: 24px;
}

.detail-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  padding: 8px 0;
}

.detail-row .label {
  color: #606266;
  font-weight: 500;
}

.detail-row .value {
  color: #303133;
}

.detail-row .amount {
  color: #f56c6c;
  font-size: 18px;
  font-weight: 600;
}

/* 商品摘要 */
.products-summary {
  border-top: 1px solid #f0f0f0;
  padding-top: 20px;
}

.summary-title {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 16px;
  color: #303133;
}

.product-list {
  max-height: 200px;
  overflow-y: auto;
}

.product-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  border-bottom: 1px solid #f8f9fa;
}

.product-item:last-child {
  border-bottom: none;
}

.product-image {
  width: 60px;
  height: 60px;
  border-radius: 6px;
  flex-shrink: 0;
}

.product-info {
  flex: 1;
}

.product-name {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
}

.product-detail {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.quantity {
  color: #909399;
  font-size: 14px;
}

.price {
  color: #f56c6c;
  font-weight: 600;
}

/* 支付方式 */
.payment-methods {
  display: grid;
  gap: 16px;
}

.payment-option {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
  border: 2px solid #f0f0f0;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.payment-option:hover {
  border-color: #409eff;
  background-color: #f8f9ff;
}

.payment-option.active {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.method-info {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.method-details .method-name {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 4px;
}

.method-details .method-desc {
  font-size: 14px;
  color: #909399;
}

/* 支付操作 */
.payment-actions {
  position: sticky;
  bottom: 0;
  background: white;
  border-top: 2px solid #f0f0f0;
  padding: 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 20px;
}

.payment-amount {
  display: flex;
  align-items: center;
  gap: 8px;
}

.amount-label {
  font-size: 16px;
  color: #606266;
}

.amount-value {
  font-size: 24px;
  font-weight: 600;
  color: #f56c6c;
}

.action-buttons {
  display: flex;
  gap: 16px;
}

.action-buttons .el-button {
  min-width: 120px;
  height: 44px;
}

/* 支付结果对话框 */
.payment-result {
  text-align: center;
  padding: 20px;
}

.result-icon {
  margin-bottom: 20px;
}

.result-message h3 {
  margin: 0 0 12px;
  color: #303133;
}

.result-message p {
  margin: 0;
  color: #606266;
  line-height: 1.6;
}

.result-actions {
  display: flex;
  justify-content: center;
  gap: 12px;
}

/* 倒计时通知 */
.countdown-notice {
  position: fixed;
  top: 80px;
  left: 50%;
  transform: translateX(-50%);
  width: 90%;
  max-width: 600px;
  z-index: 2000;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* 移动端适配 */
@media (max-width: 768px) {
  .payment-container {
    padding: 16px;
  }
  
  .payment-header {
    padding: 32px 16px;
  }
  
  .payment-header h2 {
    font-size: 20px;
  }
  
  .payment-actions {
    flex-direction: column;
    gap: 16px;
    text-align: center;
  }
  
  .action-buttons {
    width: 100%;
  }
  
  .action-buttons .el-button {
    flex: 1;
  }
  
  .payment-option {
    padding: 16px;
  }
  
  .method-info {
    gap: 12px;
  }
  
  .countdown-notice {
    width: 95%;
  }
}
</style>