<template>
  <div class="simple-payment">
    <div class="payment-header">
      <h1>💳 支付订单</h1>
      <p>订单号: {{ orderNumber }}</p>
    </div>

    <div class="payment-content">
      <!-- 订单信息 -->
      <div class="order-info">
        <h3>订单信息</h3>
        <div class="info-card">
          <div class="info-row">
            <span>订单号：</span>
            <span>{{ orderNumber }}</span>
          </div>
          <div class="info-row">
            <span>订单金额：</span>
            <span class="amount">¥{{ orderAmount.toFixed(2) }}</span>
          </div>
          <div class="info-row">
            <span>订单状态：</span>
            <span :class="orderStatusClass">{{ orderStatusText }}</span>
          </div>
        </div>
      </div>

      <!-- 支付方式选择 -->
      <div class="payment-methods" v-if="orderStatus === 'pending'">
        <h3>选择支付方式</h3>
        <div class="methods-grid">
          <div 
            class="method-card"
            :class="{ active: selectedMethod === 'alipay_qr' }"
            @click="selectMethod('alipay_qr')"
          >
            <div class="method-icon">🅰️</div>
            <div class="method-name">支付宝扫码</div>
            <div class="method-desc">使用支付宝扫描二维码支付</div>
          </div>
          
          <div 
            class="method-card"
            :class="{ active: selectedMethod === 'wechat_qr' }"
            @click="selectMethod('wechat_qr')"
          >
            <div class="method-icon">💚</div>
            <div class="method-name">微信扫码</div>
            <div class="method-desc">使用微信扫描二维码支付</div>
          </div>
        </div>
      </div>

      <!-- 支付二维码 -->
      <div class="payment-qr" v-if="paymentUrl && orderStatus === 'pending'">
        <h3>扫码支付</h3>
        <div class="qr-container">
          <div class="qr-code">
            <div class="qr-placeholder">
              <div class="qr-icon">📱</div>
              <div class="qr-text">支付二维码</div>
              <div class="qr-url">{{ paymentUrl }}</div>
            </div>
          </div>
          <div class="qr-instructions">
            <p>请使用{{ selectedMethod === 'alipay_qr' ? '支付宝' : '微信' }}扫描上方二维码完成支付</p>
            <p class="countdown">支付倒计时: {{ countdown }}秒</p>
          </div>
        </div>
      </div>

      <!-- 支付状态 -->
      <div class="payment-status" v-if="orderStatus !== 'pending'">
        <div class="status-icon" :class="orderStatusClass">
          {{ orderStatus === 'paid' ? '✅' : '❌' }}
        </div>
        <div class="status-text">{{ orderStatusText }}</div>
        <div class="status-actions">
          <el-button @click="$router.push('/simple-products')">继续购物</el-button>
          <el-button type="primary" @click="viewOrder">查看订单</el-button>
        </div>
      </div>

      <!-- 支付按钮 -->
      <div class="payment-actions" v-if="orderStatus === 'pending'">
        <el-button @click="$router.push('/simple-cart')">返回购物车</el-button>
        <el-button 
          type="primary" 
          size="large"
          @click="processPayment"
          :loading="processing"
          :disabled="!selectedMethod"
        >
          确认支付
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()
const route = useRoute()

// 响应式数据
const orderNumber = ref('')
const orderAmount = ref(0)
const orderStatus = ref('pending')
const selectedMethod = ref('')
const paymentUrl = ref('')
const processing = ref(false)
const countdown = ref(300) // 5分钟倒计时
let countdownTimer: any = null

// 计算属性
const orderStatusText = computed(() => {
  switch (orderStatus.value) {
    case 'pending':
      return '待支付'
    case 'paid':
      return '已支付'
    case 'cancelled':
      return '已取消'
    default:
      return '未知状态'
  }
})

const orderStatusClass = computed(() => {
  switch (orderStatus.value) {
    case 'pending':
      return 'status-pending'
    case 'paid':
      return 'status-paid'
    case 'cancelled':
      return 'status-cancelled'
    default:
      return 'status-unknown'
  }
})

// 选择支付方式
const selectMethod = (method: string) => {
  selectedMethod.value = method
}

// 处理支付
const processPayment = async () => {
  if (!selectedMethod.value) {
    ElMessage.warning('请选择支付方式')
    return
  }

  processing.value = true
  
  try {
    const response = await fetch('/api/simple/payment/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        order_id: orderNumber.value,
        amount: orderAmount.value,
        subject: '中医健康平台订单',
        payment_method: selectedMethod.value
      })
    })
    
    if (response.ok) {
      const result = await response.json()
      if (result.success) {
        paymentUrl.value = result.payment_url
        ElMessage.success('支付订单创建成功，请扫码支付')
        startCountdown()
      } else {
        ElMessage.error(result.message || '创建支付失败')
      }
    } else {
      const error = await response.json()
      ElMessage.error(error.detail || '创建支付失败')
    }
  } catch (error) {
    console.error('支付处理失败:', error)
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    processing.value = false
  }
}

// 开始倒计时
const startCountdown = () => {
  countdown.value = 300
  countdownTimer = setInterval(() => {
    countdown.value--
    if (countdown.value <= 0) {
      clearInterval(countdownTimer)
      ElMessage.warning('支付超时，请重新支付')
    }
  }, 1000)
}

// 检查支付状态
const checkPaymentStatus = async () => {
  try {
    const response = await fetch(`/api/simple/payment/status/${orderNumber.value}`)
    if (response.ok) {
      const result = await response.json()
      if (result.payment_status === 'success') {
        orderStatus.value = 'paid'
        ElMessage.success('支付成功！')
        if (countdownTimer) {
          clearInterval(countdownTimer)
        }
      }
    }
  } catch (error) {
    console.error('检查支付状态失败:', error)
  }
}

// 查看订单
const viewOrder = () => {
  router.push('/simple-orders')
}

// 加载订单信息
const loadOrderInfo = async () => {
  const orderId = route.params.id
  if (!orderId) {
    ElMessage.error('订单ID不存在')
    router.push('/simple-products')
    return
  }

  try {
    // 模拟订单信息（实际应该从API获取）
    orderNumber.value = `ORD${Date.now()}`
    orderAmount.value = 299.00
    orderStatus.value = 'pending'
  } catch (error) {
    console.error('加载订单信息失败:', error)
    ElMessage.error('加载订单信息失败')
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadOrderInfo()
  
  // 定期检查支付状态
  const statusInterval = setInterval(checkPaymentStatus, 3000)
  
  onUnmounted(() => {
    clearInterval(statusInterval)
    if (countdownTimer) {
      clearInterval(countdownTimer)
    }
  })
})
</script>

<style scoped>
.simple-payment {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.payment-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 30px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.payment-header h1 {
  font-size: 2.2rem;
  color: #2d3748;
  margin-bottom: 10px;
  font-weight: 700;
}

.payment-header p {
  font-size: 1.1rem;
  color: #718096;
}

.payment-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  overflow: hidden;
}

.order-info,
.payment-methods,
.payment-qr,
.payment-status {
  padding: 30px;
  border-bottom: 1px solid #f0f0f0;
}

.order-info h3,
.payment-methods h3,
.payment-qr h3 {
  margin: 0 0 20px 0;
  color: #2d3748;
  font-size: 1.3rem;
  font-weight: 600;
}

.info-card {
  background: #f8f9fa;
  padding: 20px;
  border-radius: 8px;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  font-size: 1rem;
}

.amount {
  color: #e53e3e;
  font-weight: 600;
  font-size: 1.2rem;
}

.status-pending {
  color: #f6ad55;
}

.status-paid {
  color: #38a169;
}

.status-cancelled {
  color: #e53e3e;
}

.methods-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
}

.method-card {
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.method-card:hover {
  border-color: #4299e1;
  transform: translateY(-2px);
}

.method-card.active {
  border-color: #4299e1;
  background: #ebf8ff;
}

.method-icon {
  font-size: 2rem;
  margin-bottom: 10px;
}

.method-name {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2d3748;
  margin-bottom: 5px;
}

.method-desc {
  font-size: 0.9rem;
  color: #718096;
}

.qr-container {
  text-align: center;
}

.qr-code {
  display: inline-block;
  margin-bottom: 20px;
}

.qr-placeholder {
  width: 200px;
  height: 200px;
  border: 2px dashed #cbd5e0;
  border-radius: 12px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background: #f8f9fa;
}

.qr-icon {
  font-size: 3rem;
  margin-bottom: 10px;
}

.qr-text {
  font-size: 1rem;
  color: #718096;
  margin-bottom: 5px;
}

.qr-url {
  font-size: 0.8rem;
  color: #a0aec0;
  word-break: break-all;
  max-width: 180px;
}

.qr-instructions {
  color: #718096;
}

.countdown {
  color: #e53e3e;
  font-weight: 600;
}

.payment-status {
  text-align: center;
}

.status-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.status-text {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 30px;
}

.status-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.payment-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px;
}

.payment-actions .el-button {
  min-width: 120px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .simple-payment {
    padding: 10px;
  }
  
  .methods-grid {
    grid-template-columns: 1fr;
  }
  
  .status-actions {
    flex-direction: column;
    align-items: center;
  }
  
  .payment-actions {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
}
</style>
