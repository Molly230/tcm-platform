<template>
  <div class="payment-qr-page">
    <div class="payment-container">
      <div v-if="loading" class="loading">
        <p>⏳ 正在生成支付二维码...</p>
      </div>

      <div v-else class="payment-content">
        <!-- 订单金额 -->
        <div class="amount-display">
          <div class="amount-label">支付金额</div>
          <div class="amount-value">¥{{ amount }}</div>
        </div>

        <!-- 二维码 -->
        <div class="qr-section">
          <div v-if="qrCodeUrl" class="qr-code">
            <img :src="qrCodeUrl" alt="微信支付二维码" />
          </div>
          <div v-else class="qr-placeholder">
            <p>正在加载二维码...</p>
          </div>
        </div>

        <!-- 提示文字 -->
        <div class="payment-tip">
          <p>请使用微信扫描二维码完成支付</p>
        </div>

        <!-- 支付状态 -->
        <div class="payment-status">
          <el-icon class="rotating" v-if="checking"><Loading /></el-icon>
          <span>{{ checkingText }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Loading } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

// 响应式数据
const loading = ref(false)
const checking = ref(false)
const qrCodeUrl = ref('')
const orderId = ref('')
const amount = ref('')
const orderNumber = ref('')
const checkingText = ref('等待支付中...')
const statusCheckTimer = ref<NodeJS.Timeout | null>(null)


// 生命周期
onMounted(() => {
  // 从URL获取订单信息
  orderId.value = route.query.orderId as string
  amount.value = route.query.amount as string
  orderNumber.value = route.query.orderNumber as string

  console.log('=== 支付页面调试信息 ===')
  console.log('1. route.query 完整对象:', route.query)
  console.log('2. orderId:', orderId.value, 'type:', typeof orderId.value)
  console.log('3. amount:', amount.value, 'type:', typeof amount.value)
  console.log('4. orderNumber:', orderNumber.value, 'type:', typeof orderNumber.value)
  console.log('5. amount是否为空字符串:', amount.value === '')
  console.log('6. amount是否为undefined:', amount.value === undefined)
  console.log('========================')

  if (!orderId.value || !amount.value) {
    ElMessage.error('订单信息不完整')
    console.error('订单信息不完整，准备跳转...')
    router.push('/products')
    return
  }

  // 生成微信支付二维码
  generateQRCode()

  // 启动自动检查支付状态
  startStatusCheck()
})

onUnmounted(() => {
  stopStatusCheck()
})

// 生成微信支付二维码
const generateQRCode = async () => {
  try {
    loading.value = true

    // 调用微信支付API
    const token = localStorage.getItem('user_token') || localStorage.getItem('admin_token')
    const response = await fetch('/api/wechat-pay/native', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        order_id: parseInt(orderId.value)
      })
    })

    const result = await response.json()
    console.log('微信支付响应:', result)

    if (result.success && result.data) {
      // 使用在线二维码生成服务生成二维码图片
      const qrUrl = result.data.qr_code_url
      if (qrUrl) {
        qrCodeUrl.value = `https://api.qrserver.com/v1/create-qr-code/?size=250x250&data=${encodeURIComponent(qrUrl)}`
      } else {
        ElMessage.error('二维码URL为空')
        console.error('二维码URL为空:', result.data)
      }
    } else {
      ElMessage.error(result.message || result.error || '生成二维码失败')
      console.error('生成失败详情:', result)
    }
  } catch (error) {
    console.error('生成二维码失败:', error)
    ElMessage.error('生成二维码失败: ' + error.message)
  } finally {
    loading.value = false
  }
}

const checkPaymentStatus = async () => {
  if (!orderNumber.value) return

  checking.value = true

  try {
    const token = localStorage.getItem('user_token') || localStorage.getItem('admin_token')
    // 调用微信支付查询接口
    const response = await fetch('/api/wechat-pay/query', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        order_number: orderNumber.value
      })
    })
    const result = await response.json()

    if (response.ok && result.success && result.data) {
      const tradeState = result.data.trade_state
      if (tradeState === 'SUCCESS') {
        checkingText.value = '支付成功！'
        stopStatusCheck()

        // 跳转到成功页面
        setTimeout(() => {
          router.push('/payment/success')
        }, 1000)
        return
      } else {
        checkingText.value = '等待支付中...'
      }
    }
  } catch (error) {
    console.error('检查支付状态失败:', error)
  } finally {
    checking.value = false
  }
}

const startStatusCheck = () => {
  // 每5秒自动检查一次支付状态
  statusCheckTimer.value = setInterval(() => {
    if (!checking.value) {
      checkPaymentStatus()
    }
  }, 5000)
}

const stopStatusCheck = () => {
  if (statusCheckTimer.value) {
    clearInterval(statusCheckTimer.value)
    statusCheckTimer.value = null
  }
}
</script>

<style scoped>
.payment-qr-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #07c160 0%, #06ad56 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 20px;
}

.payment-container {
  width: 100%;
  max-width: 420px;
}

.loading {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  font-size: 16px;
  color: #666;
}

.payment-content {
  background: white;
  border-radius: 16px;
  padding: 40px 30px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.15);
  text-align: center;
}

.amount-display {
  margin-bottom: 30px;
}

.amount-label {
  font-size: 14px;
  color: #999;
  margin-bottom: 8px;
}

.amount-value {
  font-size: 42px;
  font-weight: 600;
  color: #07c160;
}

.qr-section {
  margin-bottom: 20px;
}

.qr-code {
  display: inline-block;
  padding: 15px;
  background: white;
  border: 3px solid #07c160;
  border-radius: 12px;
}

.qr-code img {
  width: 250px;
  height: 250px;
  display: block;
}

.qr-placeholder {
  padding: 80px 20px;
  color: #999;
  font-size: 14px;
}

.payment-tip {
  margin-bottom: 20px;
  color: #666;
  font-size: 15px;
}

.payment-tip p {
  margin: 0;
}

.payment-status {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding-top: 20px;
  border-top: 1px solid #f0f0f0;
  font-size: 14px;
  color: #999;
  min-height: 40px;
}

.rotating {
  animation: rotate 1s linear infinite;
  color: #07c160;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* 响应式设计 */
@media (max-width: 768px) {
  .payment-content {
    padding: 30px 20px;
  }

  .amount-value {
    font-size: 36px;
  }

  .qr-code img {
    width: 220px;
    height: 220px;
  }
}
</style>