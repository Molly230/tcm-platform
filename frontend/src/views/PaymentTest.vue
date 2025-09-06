<template>
  <div style="padding: 20px;">
    <h2>支付测试页面</h2>
    <el-form>
      <el-form-item label="订单号">
        <el-input v-model="orderNumber" placeholder="输入一个存在的订单号"></el-input>
      </el-form-item>
      <el-form-item label="支付方式">
        <el-select v-model="paymentMethod">
          <el-option label="支付宝扫码" value="alipay_qr"></el-option>
          <el-option label="支付宝网页" value="alipay"></el-option>
          <el-option label="微信扫码" value="wx_qr"></el-option>
        </el-select>
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="testPayment" :loading="loading">测试支付</el-button>
      </el-form-item>
    </el-form>
    
    <div v-if="result" style="margin-top: 20px; padding: 10px; background: #f5f5f5;">
      <h3>测试结果：</h3>
      <pre>{{ JSON.stringify(result, null, 2) }}</pre>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'

const orderNumber = ref('TCM20250905095000A1B2C3D4')
const paymentMethod = ref('alipay_qr')
const loading = ref(false)
const result = ref(null)

const testPayment = async () => {
  loading.value = true
  result.value = null
  
  try {
    console.log('发送支付请求:', {
      order_number: orderNumber.value,
      payment_method: paymentMethod.value
    })
    
    const response = await fetch('/api/payment/create', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        order_number: orderNumber.value,
        payment_method: paymentMethod.value
      })
    })
    
    const data = await response.json()
    
    if (response.ok) {
      result.value = { success: true, data }
      ElMessage.success('支付API调用成功！')
    } else {
      result.value = { success: false, error: data }
      ElMessage.error(`支付API调用失败: ${data.detail || '未知错误'}`)
    }
  } catch (error) {
    console.error('支付测试失败:', error)
    result.value = { success: false, error: error.message }
    ElMessage.error(`请求失败: ${error.message}`)
  } finally {
    loading.value = false
  }
}
</script>