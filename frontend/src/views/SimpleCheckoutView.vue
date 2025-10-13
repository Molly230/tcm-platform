<template>
  <div class="simple-checkout">
    <div class="checkout-header">
      <h1>💳 确认订单</h1>
      <p>请填写收货信息并确认订单</p>
    </div>

    <div class="checkout-content">
      <!-- 商品清单 -->
      <div class="order-items">
        <h3>商品清单</h3>
        <div class="items-list">
          <div 
            v-for="item in orderItems" 
            :key="item.product_id"
            class="order-item"
          >
            <div class="item-image">
              <img :src="getProductImage(item)" :alt="item.product_name">
            </div>
            <div class="item-info">
              <h4 class="item-name">{{ item.product_name }}</h4>
              <div class="item-price">¥{{ item.product_price.toFixed(2) }}</div>
            </div>
            <div class="item-quantity">数量: {{ item.quantity }}</div>
            <div class="item-total">¥{{ (item.product_price * item.quantity).toFixed(2) }}</div>
          </div>
        </div>
      </div>

      <!-- 收货信息表单 -->
      <div class="shipping-form">
        <h3>收货信息</h3>
        <el-form :model="shippingForm" label-width="100px">
          <el-form-item label="收货人" required>
            <el-input v-model="shippingForm.name" placeholder="请输入收货人姓名" />
          </el-form-item>
          <el-form-item label="联系电话" required>
            <el-input v-model="shippingForm.phone" placeholder="请输入联系电话" />
          </el-form-item>
          <el-form-item label="收货地址" required>
            <el-input
              type="textarea"
              v-model="shippingForm.address"
              placeholder="请输入详细收货地址"
              :rows="3"
            />
          </el-form-item>
          <el-form-item label="备注">
            <el-input
              type="textarea"
              v-model="shippingForm.note"
              placeholder="如有特殊需求请备注"
              :rows="2"
            />
          </el-form-item>
        </el-form>
      </div>

      <!-- 订单汇总 -->
      <div class="order-summary">
        <h3>订单汇总</h3>
        <div class="summary-details">
          <div class="summary-row">
            <span>商品总额：</span>
            <span>¥{{ totalAmount.toFixed(2) }}</span>
          </div>
          <div class="summary-row">
            <span>运费：</span>
            <span>¥0.00</span>
          </div>
          <div class="summary-row total">
            <span>应付金额：</span>
            <span class="total-amount">¥{{ totalAmount.toFixed(2) }}</span>
          </div>
        </div>
      </div>

      <!-- 提交按钮 -->
      <div class="submit-actions">
        <el-button @click="$router.push('/simple-cart')">返回购物车</el-button>
        <el-button 
          type="primary" 
          size="large"
          @click="submitOrder"
          :loading="submitting"
          :disabled="!canSubmit"
        >
          提交订单
        </el-button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 响应式数据
const orderItems = ref<any[]>([])
const submitting = ref(false)

// 收货表单
const shippingForm = ref({
  name: '',
  phone: '',
  address: '',
  note: ''
})

// 计算属性
const totalAmount = computed(() => {
  return orderItems.value.reduce((total, item) => {
    return total + (item.product_price * item.quantity)
  }, 0)
})

const canSubmit = computed(() => {
  return shippingForm.value.name && 
         shippingForm.value.phone && 
         shippingForm.value.address &&
         !submitting.value
})

// 获取商品图片
const getProductImage = (item: any) => {
  return '/default-product.jpg'
}

// 加载订单数据
const loadOrderData = () => {
  try {
    const cartData = sessionStorage.getItem('checkout_cart')
    if (cartData) {
      const data = JSON.parse(cartData)
      orderItems.value = data.items || []
    } else {
      ElMessage.error('购物车数据不存在')
      router.push('/simple-cart')
    }
  } catch (error) {
    console.error('加载订单数据失败:', error)
    ElMessage.error('加载订单数据失败')
    router.push('/simple-cart')
  }
}

// 提交订单
const submitOrder = async () => {
  if (!canSubmit.value) {
    return
  }

  submitting.value = true
  
  try {
    const userId = 1 // 模拟用户ID
    
    const orderData = {
      shipping_name: shippingForm.value.name,
      shipping_phone: shippingForm.value.phone,
      shipping_address: shippingForm.value.address,
      items: orderItems.value
    }
    
    const response = await fetch(`/api/simple/orders/${userId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(orderData)
    })
    
    if (response.ok) {
      const result = await response.json()
      ElMessage.success('订单创建成功')
      
      // 清除购物车数据
      sessionStorage.removeItem('checkout_cart')
      
      // 跳转到支付页面
      router.push(`/simple-payment/${result.order_id}`)
    } else {
      const error = await response.json()
      ElMessage.error(error.detail || '创建订单失败')
    }
  } catch (error) {
    console.error('提交订单失败:', error)
    ElMessage.error('网络错误，请稍后重试')
  } finally {
    submitting.value = false
  }
}

// 组件挂载时加载数据
onMounted(() => {
  loadOrderData()
})
</script>

<style scoped>
.simple-checkout {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.checkout-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 30px 20px;
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
}

.checkout-header h1 {
  font-size: 2.2rem;
  color: #2d3748;
  margin-bottom: 10px;
  font-weight: 700;
}

.checkout-header p {
  font-size: 1.1rem;
  color: #718096;
}

.checkout-content {
  background: white;
  border-radius: 16px;
  box-shadow: 0 8px 32px rgba(0,0,0,0.1);
  overflow: hidden;
}

.order-items,
.shipping-form,
.order-summary {
  padding: 30px;
  border-bottom: 1px solid #f0f0f0;
}

.order-items h3,
.shipping-form h3,
.order-summary h3 {
  margin: 0 0 20px 0;
  color: #2d3748;
  font-size: 1.3rem;
  font-weight: 600;
}

.items-list {
  border: 1px solid #e2e8f0;
  border-radius: 8px;
  overflow: hidden;
}

.order-item {
  display: flex;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #f0f0f0;
  gap: 20px;
}

.order-item:last-child {
  border-bottom: none;
}

.item-image {
  flex: 0 0 60px;
  height: 60px;
  border-radius: 6px;
  overflow: hidden;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.item-info {
  flex: 1;
}

.item-name {
  margin: 0 0 8px 0;
  font-size: 1.1rem;
  color: #2d3748;
  font-weight: 500;
}

.item-price {
  font-size: 1rem;
  color: #e53e3e;
  font-weight: 600;
}

.item-quantity {
  flex: 0 0 80px;
  text-align: center;
  color: #718096;
}

.item-total {
  flex: 0 0 100px;
  text-align: right;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2d3748;
}

.shipping-form {
  background: #f8f9fa;
}

.order-summary {
  background: #f8f9fa;
}

.summary-details {
  max-width: 300px;
  margin-left: auto;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  font-size: 1rem;
}

.summary-row.total {
  border-top: 2px solid #e2e8f0;
  margin-top: 12px;
  padding-top: 16px;
  font-size: 1.2rem;
  font-weight: 600;
}

.total-amount {
  color: #e53e3e;
  font-size: 1.4rem;
}

.submit-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 30px;
}

.submit-actions .el-button {
  min-width: 120px;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .simple-checkout {
    padding: 10px;
  }
  
  .order-item {
    flex-direction: column;
    align-items: stretch;
    gap: 15px;
    padding: 15px;
  }
  
  .item-image {
    flex: none;
    align-self: center;
  }
  
  .item-quantity,
  .item-total {
    flex: none;
    text-align: left;
  }
  
  .submit-actions {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }
}
</style>
