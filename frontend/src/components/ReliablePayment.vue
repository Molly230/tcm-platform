<template>
  <div class="reliable-payment">
    <el-card class="payment-card" shadow="hover">
      <template #header>
        <div class="card-header">
          <h3>安全支付</h3>
          <el-tag type="success">可靠支付系统</el-tag>
        </div>
      </template>
      
      <!-- 订单信息 -->
      <div class="order-info">
        <h4>订单信息</h4>
        <p><strong>订单号：</strong>{{ orderId }}</p>
        <p><strong>支付金额：</strong><span class="amount">¥{{ amount }}</span></p>
      </div>
      
      <!-- 支付方式选择 -->
      <div class="payment-methods">
        <h4>选择支付方式</h4>
        <el-radio-group v-model="paymentMethod" @change="handleMethodChange">
          <el-radio label="alipay_qr" class="payment-option">
            <div class="method-info">
              <i class="icon-alipay"></i>
              <span>支付宝扫码</span>
            </div>
          </el-radio>
          <el-radio label="alipay" class="payment-option">
            <div class="method-info">
              <i class="icon-alipay"></i>
              <span>支付宝网页</span>
            </div>
          </el-radio>
          <el-radio label="wechat" class="payment-option">
            <div class="method-info">
              <i class="icon-wechat"></i>
              <span>微信支付</span>
            </div>
          </el-radio>
        </el-radio-group>
      </div>
      
      <!-- 支付按钮 -->
      <div class="payment-actions">
        <el-button 
          type="primary" 
          size="large" 
          :loading="loading" 
          @click="createPayment"
          class="pay-button"
        >
          {{ loading ? '正在创建支付...' : '立即支付' }}
        </el-button>
      </div>
      
      <!-- 二维码展示 -->
      <div v-if="qrCodeUrl" class="qr-code-section">
        <h4>请扫码支付</h4>
        <div class="qr-code">
          <img :src="`https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(qrCodeUrl)}`" 
               alt="支付二维码" />
        </div>
        <p class="qr-tip">请使用{{ getPaymentMethodName() }}扫描上方二维码完成支付</p>
        
        <!-- 支付状态检查 -->
        <div class="status-check">
          <el-button @click="checkPaymentStatus" :loading="checking">
            检查支付状态
          </el-button>
        </div>
      </div>
      
      <!-- 支付结果 -->
      <div v-if="paymentResult" class="payment-result">
        <el-result
          :icon="paymentResult.success ? 'success' : 'error'"
          :title="paymentResult.success ? '支付成功！' : '支付失败'"
          :sub-title="paymentResult.message"
        >
          <template #extra>
            <el-button v-if="paymentResult.success" type="primary" @click="goToOrder">
              查看订单
            </el-button>
            <el-button v-else @click="retryPayment">重试支付</el-button>
          </template>
        </el-result>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { ElMessage } from 'element-plus'
import { useRouter } from 'vue-router'
import axios from 'axios'

interface Props {
  orderId: string
  amount: number
}

const props = defineProps<Props>()
const router = useRouter()

// 响应式数据
const paymentMethod = ref('alipay_qr')
const loading = ref(false)
const checking = ref(false)
const qrCodeUrl = ref('')
const paymentResult = ref<{success: boolean, message: string} | null>(null)
const chargeId = ref('')

// 定时器
let statusTimer: number | null = null

// 创建支付
const createPayment = async () => {
  loading.value = true
  paymentResult.value = null
  qrCodeUrl.value = ''

  try {
    let response

    // 根据支付方式选择不同的API
    if (paymentMethod.value === 'wechat') {
      // 使用真实的微信支付API
      response = await axios.post('/api/wechat-pay/native', {
        order_id: parseInt(props.orderId)
      }, {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('token')}`
        }
      })

      if (response.data.success) {
        const paymentData = response.data.data
        qrCodeUrl.value = paymentData.qr_code_url
        chargeId.value = paymentData.prepay_id
        ElMessage.success('微信支付二维码已生成')
        startStatusPolling()
      } else {
        ElMessage.error(response.data.message || '创建支付失败')
      }
    } else {
      // 其他支付方式使用原来的接口
      response = await axios.post('/api/reliable-pay/create', {
        order_id: props.orderId,
        payment_method: paymentMethod.value
      })

      if (response.data.success) {
        qrCodeUrl.value = response.data.payment_url
        chargeId.value = response.data.charge_id
        ElMessage.success('支付订单创建成功')

        if (paymentMethod.value.includes('qr')) {
          startStatusPolling()
        }
      } else {
        ElMessage.error(response.data.message || '创建支付失败')
      }
    }
  } catch (error: any) {
    console.error('创建支付失败:', error)
    ElMessage.error(error.response?.data?.detail || '网络错误')
  } finally {
    loading.value = false
  }
}

// 检查支付状态
const checkPaymentStatus = async () => {
  checking.value = true
  
  try {
    const response = await axios.get(`/api/reliable-pay/status/${props.orderId}`)
    const status = response.data
    
    if (status.order_status === 'paid' || status.payment_status === 'success') {
      // 支付成功
      paymentResult.value = {
        success: true,
        message: '订单支付完成，感谢您的购买！'
      }
      stopStatusPolling()
      ElMessage.success('支付成功！')
    } else if (status.payment_status === 'failed') {
      // 支付失败
      paymentResult.value = {
        success: false,
        message: '支付失败，请重试'
      }
      stopStatusPolling()
    } else {
      // 还在等待支付
      ElMessage.info('订单还未支付，请继续扫码')
    }
  } catch (error: any) {
    console.error('查询状态失败:', error)
    ElMessage.error('查询状态失败')
  } finally {
    checking.value = false
  }
}

// 开始状态轮询
const startStatusPolling = () => {
  statusTimer = setInterval(() => {
    checkPaymentStatus()
  }, 3000) // 每3秒查询一次
}

// 停止状态轮询
const stopStatusPolling = () => {
  if (statusTimer) {
    clearInterval(statusTimer)
    statusTimer = null
  }
}

// 支付方式改变
const handleMethodChange = () => {
  qrCodeUrl.value = ''
  paymentResult.value = null
  stopStatusPolling()
}

// 获取支付方式名称
const getPaymentMethodName = () => {
  const names = {
    'alipay_qr': '支付宝',
    'alipay': '支付宝',
    'wechat': '微信'
  }
  return names[paymentMethod.value as keyof typeof names] || '支付宝'
}

// 跳转到订单页面
const goToOrder = () => {
  router.push('/orders')
}

// 重试支付
const retryPayment = () => {
  paymentResult.value = null
  qrCodeUrl.value = ''
  createPayment()
}

// 组件销毁时清理定时器
onUnmounted(() => {
  stopStatusPolling()
})
</script>

<style scoped>
.reliable-payment {
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
}

.payment-card {
  border-radius: 12px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.order-info {
  margin-bottom: 24px;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
}

.order-info h4 {
  margin: 0 0 12px 0;
  color: #333;
}

.amount {
  font-size: 24px;
  font-weight: bold;
  color: #e74c3c;
}

.payment-methods {
  margin-bottom: 24px;
}

.payment-methods h4 {
  margin: 0 0 16px 0;
  color: #333;
}

.payment-option {
  display: block;
  margin-bottom: 12px;
  padding: 12px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  transition: all 0.3s;
}

.payment-option:hover {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.method-info {
  display: flex;
  align-items: center;
  gap: 8px;
}

.icon-alipay::before {
  content: "💰";
}

.icon-wechat::before {
  content: "💬";
}

.pay-button {
  width: 100%;
  height: 48px;
  font-size: 18px;
  border-radius: 8px;
}

.qr-code-section {
  text-align: center;
  margin-top: 24px;
  padding: 24px;
  border: 2px dashed #409eff;
  border-radius: 12px;
  background-color: #f0f9ff;
}

.qr-code {
  margin: 16px 0;
}

.qr-code img {
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0,0,0,0.1);
}

.qr-tip {
  color: #666;
  margin: 16px 0;
}

.status-check {
  margin-top: 16px;
}

.payment-result {
  margin-top: 24px;
}
</style>