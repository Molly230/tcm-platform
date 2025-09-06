<template>
  <div class="payment-success-container">
    <div class="success-content">
      <!-- 成功图标 -->
      <div class="success-icon">
        <el-icon size="80" color="#67c23a">
          <SuccessFilled />
        </el-icon>
      </div>
      
      <!-- 成功信息 -->
      <div class="success-info">
        <h2>支付成功！</h2>
        <p class="success-message">恭喜您，订单支付已完成</p>
        <p class="order-number">订单号：{{ orderNumber }}</p>
      </div>
      
      <!-- 操作按钮 -->
      <div class="success-actions">
        <el-button size="large" @click="continueShopping">继续购物</el-button>
        <el-button type="primary" size="large" @click="viewOrders">查看订单</el-button>
      </div>
      
      <!-- 温馨提示 -->
      <div class="success-notice">
        <el-alert
          title="温馨提示"
          type="info"
          :closable="false"
          show-icon
        >
          <template #default>
            <p>• 我们将在1-2个工作日内为您安排发货</p>
            <p>• 您可以在"我的订单"中查看物流信息</p>
            <p>• 如有疑问，请联系客服：400-888-8888</p>
          </template>
        </el-alert>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { SuccessFilled } from '@element-plus/icons-vue'

const route = useRoute()
const router = useRouter()

const orderNumber = ref<string>('')

onMounted(() => {
  // 从URL参数获取订单号
  orderNumber.value = (route.query.out_trade_no as string) || 
                     (route.query.order_number as string) || 
                     '未知订单号'
})

// 继续购物
const continueShopping = () => {
  router.push('/products')
}

// 查看订单
const viewOrders = () => {
  router.push('/profile/orders')
}
</script>

<style scoped>
.payment-success-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
  padding: 20px;
}

.success-content {
  background: white;
  border-radius: 16px;
  padding: 60px 40px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  text-align: center;
  max-width: 500px;
  width: 100%;
}

.success-icon {
  margin-bottom: 24px;
}

.success-info h2 {
  color: #303133;
  font-size: 28px;
  margin: 0 0 16px;
  font-weight: 600;
}

.success-message {
  color: #606266;
  font-size: 16px;
  margin: 0 0 12px;
  line-height: 1.6;
}

.order-number {
  color: #909399;
  font-size: 14px;
  margin: 0 0 32px;
}

.success-actions {
  display: flex;
  gap: 16px;
  justify-content: center;
  margin-bottom: 32px;
}

.success-actions .el-button {
  min-width: 120px;
  height: 44px;
}

.success-notice {
  text-align: left;
}

.success-notice :deep(.el-alert__content) {
  padding-left: 8px;
}

.success-notice p {
  margin: 4px 0;
  line-height: 1.6;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .success-content {
    padding: 40px 24px;
    margin: 16px;
  }
  
  .success-info h2 {
    font-size: 24px;
  }
  
  .success-actions {
    flex-direction: column;
  }
  
  .success-actions .el-button {
    width: 100%;
  }
}
</style>