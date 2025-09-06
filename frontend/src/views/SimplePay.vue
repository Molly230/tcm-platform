<template>
  <div class="simple-pay-container">
    <el-card class="pay-card" shadow="hover">
      <!-- 支付头部 -->
      <div class="pay-header">
        <el-icon size="48" color="#67c23a"><Wallet /></el-icon>
        <h2>支付订单</h2>
        <p class="order-number">订单号：{{ orderId }}</p>
      </div>

      <!-- 支付信息 -->
      <div class="pay-info" v-if="orderData">
        <div class="amount-section">
          <div class="amount-label">支付金额</div>
          <div class="amount-value">¥{{ orderData.amount }}</div>
        </div>
        
        <div class="order-details">
          <p><strong>商品：</strong>中医健康平台商品</p>
          <p><strong>订单：</strong>{{ orderId }}</p>
        </div>
      </div>

      <!-- 订单加载失败提示 -->
      <div class="error-info" v-else>
        <el-alert
          title="订单信息加载中..."
          type="info"
          :closable="false"
          show-icon
        />
      </div>

      <!-- 支付方式选择 -->
      <div class="pay-methods">
        <h3>支付方式</h3>
        <div class="single-method">
          <div class="method-content">
            <el-icon size="24" color="#1677ff"><Phone /></el-icon>
            <div class="method-info">
              <div class="method-name">扫码支付</div>
              <div class="method-desc">支付宝扫码支付</div>
            </div>
          </div>
        </div>
      </div>

      <!-- 支付按钮 -->
      <div class="pay-actions">
        <el-button size="large" @click="$router.back()">返回</el-button>
        <el-button 
          type="primary" 
          size="large" 
          :loading="paying"
          @click="startPay"
          :disabled="!orderData"
        >
          {{ paying ? '处理中...' : '立即支付' }}
        </el-button>
      </div>
    </el-card>

    <!-- 二维码支付对话框 -->
    <el-dialog 
      v-model="showQR" 
      title="扫码支付" 
      width="400px"
      :close-on-click-modal="false"
    >
      <div class="qr-section">
        <div class="qr-info">
          <p>请使用支付宝扫描下方二维码完成支付</p>
          <p class="amount-tip">支付金额：¥{{ orderData?.amount }}</p>
        </div>
        
        <div class="qr-code" v-if="qrCodeUrl">
          <el-image :src="qrCodeUrl" alt="支付二维码" />
        </div>
        
        <div class="qr-placeholder" v-else>
          <el-icon size="80" color="#ddd"><Grid /></el-icon>
          <p>二维码生成中...</p>
        </div>

        <div class="qr-status">
          <el-alert
            title="请在10分钟内完成支付"
            type="warning"
            :closable="false"
            show-icon
          />
        </div>
      </div>
      
      <template #footer>
        <el-button @click="showQR = false">取消支付</el-button>
        <el-button type="primary" @click="checkPaymentStatus">检查支付状态</el-button>
      </template>
    </el-dialog>

    <!-- 支付成功对话框 -->
    <el-dialog 
      v-model="showSuccess" 
      title="支付成功"
      width="350px"
      :show-close="false"
      :close-on-click-modal="false"
    >
      <div class="success-content">
        <el-icon size="64" color="#67c23a"><CircleCheckFilled /></el-icon>
        <h3>支付成功！</h3>
        <p>您的订单已支付完成</p>
      </div>
      
      <template #footer>
        <el-button type="primary" @click="goToOrders">查看订单</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Wallet, 
  Phone, 
  Grid, 
  CircleCheckFilled 
} from '@element-plus/icons-vue'

interface OrderData {
  order_id: string
  amount: number
  order_status: string
  payment_status: string
}

const route = useRoute()
const router = useRouter()

// 响应式数据
const orderId = ref('')
const orderData = ref<OrderData | null>(null)
const paying = ref(false)
const showQR = ref(false)
const showSuccess = ref(false)
const qrCodeUrl = ref('')

// 获取订单信息
const loadOrderData = async () => {
  try {
    orderId.value = route.params.orderId as string
    if (!orderId.value) {
      ElMessage.error('订单ID不存在')
      router.push('/')
      return
    }

    // 调用后端API获取订单状态
    const response = await fetch(`/api/reliable-pay/status/${orderId.value}`)
    if (!response.ok) {
      throw new Error('获取订单信息失败')
    }

    const responseData = await response.json()
    
    // 将后端数据映射为前端期望的格式
    orderData.value = {
      order_id: responseData.order_id,
      amount: responseData.amount,
      order_status: responseData.order_status,
      payment_status: responseData.payment_status
    }
    
    // 检查订单状态
    if (responseData.order_status === 'paid') {
      ElMessage.info('订单已支付')
      showSuccess.value = true
      return
    }

  } catch (error) {
    console.error('加载订单数据失败:', error)
    ElMessage.error('订单信息加载失败，请重试')
    // 返回首页，不要显示虚假的订单信息
    router.push('/')
    return
  }
}

// 开始支付
const startPay = async () => {
  if (!orderData.value) {
    ElMessage.error('订单信息加载失败')
    return
  }

  paying.value = true

  try {
    // 调用支付API
    const response = await fetch('/api/reliable-pay/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        order_id: orderData.value.order_id,
        payment_method: 'alipay_qr'
      })
    })

    const result = await response.json()
    console.log('支付响应:', result)

    if (!response.ok) {
      // 显示服务器返回的具体错误信息
      const errorMsg = result.detail || result.message || `支付请求失败: ${response.status}`
      ElMessage.error(errorMsg)
      return
    }

    if (result.success) {
      // 二维码支付
      await handleQRPayment(result.payment_url)
    } else {
      ElMessage.error(result.message || '支付创建失败')
    }

  } catch (error) {
    console.error('支付失败:', error)
    ElMessage.error('支付请求失败，请重试')
  } finally {
    paying.value = false
  }
}

// 处理二维码支付
const handleQRPayment = async (qrContent: string) => {
  try {
    // 生成二维码图片
    qrCodeUrl.value = await generateQRCode(qrContent)
    showQR.value = true
    
    // 开始轮询支付状态
    startPaymentPolling()
    
    ElMessage.success('二维码已生成，请扫码支付')
  } catch (error) {
    console.error('二维码处理失败:', error)
    ElMessage.error('二维码生成失败')
  }
}


// 生成二维码
const generateQRCode = async (content: string): Promise<string> => {
  // 这里可以使用 qrcode 库生成二维码
  // 为了简化，返回一个模拟的二维码图片
  return `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${encodeURIComponent(content)}`
}

// 轮询支付状态
const startPaymentPolling = () => {
  const pollInterval = setInterval(async () => {
    try {
      const success = await checkPaymentStatus()
      if (success) {
        clearInterval(pollInterval)
      }
    } catch (error) {
      console.error('轮询支付状态失败:', error)
    }
  }, 3000) // 每3秒检查一次

  // 10分钟后停止轮询
  setTimeout(() => {
    clearInterval(pollInterval)
  }, 10 * 60 * 1000)
}

// 检查支付状态
const checkPaymentStatus = async (): Promise<boolean> => {
  try {
    const response = await fetch(`/api/reliable-pay/status/${orderId.value}`)
    if (!response.ok) return false

    const status = await response.json()
    
    if (status.order_status === 'paid' || status.payment_status === 'success') {
      // 支付成功
      showQR.value = false
      showSuccess.value = true
      ElMessage.success('支付成功！')
      return true
    }
    
    return false
  } catch (error) {
    console.error('检查支付状态失败:', error)
    return false
  }
}

// 跳转到首页
const goToOrders = () => {
  router.push('/')
}

onMounted(() => {
  loadOrderData()
})
</script>

<style scoped>
.simple-pay-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.pay-card {
  width: 100%;
  max-width: 500px;
  border-radius: 16px;
  overflow: hidden;
}

/* 支付头部 */
.pay-header {
  text-align: center;
  padding: 32px 24px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin: -20px -20px 20px -20px;
}

.pay-header h2 {
  margin: 16px 0 8px;
  font-size: 24px;
  font-weight: 600;
}

.order-number {
  margin: 0;
  opacity: 0.9;
  font-size: 14px;
}

/* 支付信息 */
.pay-info {
  margin-bottom: 24px;
}

.error-info {
  margin-bottom: 24px;
}

.amount-section {
  text-align: center;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  margin-bottom: 16px;
}

.amount-label {
  color: #666;
  font-size: 14px;
  margin-bottom: 8px;
}

.amount-value {
  color: #f56c6c;
  font-size: 32px;
  font-weight: 700;
}

.order-details {
  padding: 16px;
  background: #fff;
  border-left: 4px solid #409eff;
  border-radius: 0 8px 8px 0;
}

.order-details p {
  margin: 8px 0;
  color: #666;
}

/* 支付方式 */
.pay-methods {
  margin: 24px 0;
}

.pay-methods h3 {
  margin-bottom: 16px;
  color: #333;
}

.single-method {
  width: 100%;
}

.method-content {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border: 2px solid #409eff;
  border-radius: 8px;
  background: #f8f9ff;
}

.method-info {
  flex: 1;
}

.method-name {
  font-weight: 600;
  margin-bottom: 4px;
}

.method-desc {
  color: #666;
  font-size: 12px;
}

/* 支付按钮 */
.pay-actions {
  display: flex;
  gap: 16px;
  margin-top: 32px;
}

.pay-actions .el-button {
  flex: 1;
  height: 48px;
  font-size: 16px;
}

/* 二维码对话框 */
.qr-section {
  text-align: center;
  padding: 20px;
}

.qr-info {
  margin-bottom: 20px;
}

.amount-tip {
  color: #f56c6c;
  font-weight: 600;
  font-size: 18px;
}

.qr-code {
  margin: 20px 0;
  padding: 20px;
  background: #f8f9fa;
  border-radius: 12px;
  display: inline-block;
}

.qr-placeholder {
  margin: 20px 0;
  padding: 40px;
  background: #f8f9fa;
  border-radius: 12px;
  color: #999;
}

.qr-status {
  margin-top: 20px;
}

/* 支付成功对话框 */
.success-content {
  text-align: center;
  padding: 20px;
}

.success-content h3 {
  margin: 16px 0 8px;
  color: #67c23a;
}

.success-content p {
  color: #666;
  margin: 0;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .simple-pay-container {
    padding: 16px;
  }
  
  .pay-header {
    padding: 24px 16px;
  }
  
  .pay-header h2 {
    font-size: 20px;
  }
  
  .amount-value {
    font-size: 28px;
  }
  
  .method-content {
    padding: 12px;
  }
  
  .pay-actions .el-button {
    height: 44px;
    font-size: 14px;
  }
}
</style>