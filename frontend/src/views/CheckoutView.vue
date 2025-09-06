<template>
  <div class="checkout-container">
    <el-row :gutter="20">
      <!-- 订单信息 -->
      <el-col :lg="14" :md="24">
        <div class="checkout-section">
          <!-- 收货地址 -->
          <el-card class="address-card" shadow="never">
            <template #header>
              <div class="section-header">
                <el-icon><LocationFilled /></el-icon>
                <span>收货地址</span>
              </div>
            </template>
            
            <div v-if="selectedAddress" class="address-item selected">
              <div class="address-info">
                <div class="address-header">
                  <span class="name">{{ selectedAddress.name }}</span>
                  <span class="phone">{{ selectedAddress.phone }}</span>
                  <el-tag v-if="selectedAddress.isDefault" size="small" type="primary">默认</el-tag>
                </div>
                <div class="address-detail">{{ selectedAddress.address }}</div>
              </div>
              <el-button link @click="showAddressDialog = true">更换地址</el-button>
            </div>
            
            <div v-else class="no-address">
              <el-empty description="暂无收货地址" :image-size="80" />
              <el-button type="primary" @click="showAddressDialog = true">添加收货地址</el-button>
            </div>
          </el-card>

          <!-- 商品清单 -->
          <el-card class="products-card" shadow="never">
            <template #header>
              <div class="section-header">
                <el-icon><ShoppingBag /></el-icon>
                <span>商品清单</span>
              </div>
            </template>
            
            <div v-for="item in orderItems" :key="item.id" class="order-item">
              <el-image 
                :src="item.images?.[0] || 'https://via.placeholder.com/80x80'" 
                class="item-image"
              />
              <div class="item-info">
                <div class="item-name">{{ item.name }}</div>
                <div class="item-specs">{{ item.specifications }}</div>
                <div class="item-price">
                  <span class="price">¥{{ item.price }}</span>
                  <span class="quantity">x{{ item.quantity }}</span>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 支付方式 -->
          <el-card class="payment-card" shadow="never">
            <template #header>
              <div class="section-header">
                <el-icon><CreditCard /></el-icon>
                <span>支付方式</span>
              </div>
            </template>
            
            <el-radio-group v-model="selectedPayment" class="payment-methods">
              <el-radio value="alipay" class="payment-option">
                <div class="payment-info">
                  <el-icon size="24" color="#1677ff"><Wallet /></el-icon>
                  <span>支付宝</span>
                </div>
              </el-radio>
              <el-radio value="wechat" class="payment-option">
                <div class="payment-info">
                  <el-icon size="24" color="#07c160"><ChatDotRound /></el-icon>
                  <span>微信支付</span>
                </div>
              </el-radio>
              <el-radio value="bank" class="payment-option">
                <div class="payment-info">
                  <el-icon size="24" color="#ff6b35"><CreditCard /></el-icon>
                  <span>银行卡</span>
                </div>
              </el-radio>
            </el-radio-group>
          </el-card>

          <!-- 订单备注 -->
          <el-card class="remark-card" shadow="never">
            <template #header>
              <div class="section-header">
                <el-icon><EditPen /></el-icon>
                <span>订单备注</span>
              </div>
            </template>
            
            <el-input 
              v-model="orderRemark"
              type="textarea" 
              :rows="3"
              placeholder="请输入订单备注（可选）"
              maxlength="200"
              show-word-limit
            />
          </el-card>
        </div>
      </el-col>

      <!-- 订单汇总 -->
      <el-col :lg="10" :md="24">
        <div class="order-summary" :class="{ 'sticky-summary': !isMobile }">
          <el-card shadow="never">
            <template #header>
              <div class="summary-header">订单汇总</div>
            </template>

            <div class="summary-item">
              <span>商品总额</span>
              <span>¥{{ subtotal.toFixed(2) }}</span>
            </div>
            <div class="summary-item">
              <span>运费</span>
              <span v-if="shippingFee > 0">¥{{ shippingFee.toFixed(2) }}</span>
              <span v-else class="free-shipping">免运费</span>
            </div>
            <div class="summary-item">
              <span>优惠券</span>
              <span class="coupon-discount">-¥{{ discountAmount.toFixed(2) }}</span>
            </div>
            <el-divider />
            <div class="summary-total">
              <span>实付金额</span>
              <span class="total-price">¥{{ totalAmount.toFixed(2) }}</span>
            </div>

            <el-button 
              type="primary" 
              size="large" 
              class="submit-button"
              :loading="submitting"
              :disabled="!canSubmit"
              @click="submitOrder"
            >
              {{ submitting ? '提交中...' : '提交订单' }}
            </el-button>

            <!-- 优惠券选择 -->
            <div class="coupon-section">
              <el-button link @click="showCouponDialog = true">
                <el-icon><Ticket /></el-icon>
                选择优惠券
              </el-button>
            </div>
          </el-card>
        </div>
      </el-col>
    </el-row>

    <!-- 地址选择对话框 -->
    <el-dialog 
      v-model="showAddressDialog" 
      title="选择收货地址" 
      width="600px"
      :before-close="handleCloseAddressDialog"
    >
      <div class="address-list">
        <div 
          v-for="address in addresses" 
          :key="address.id"
          class="address-option"
          :class="{ selected: selectedAddressId === address.id }"
          @click="selectAddress(address)"
        >
          <el-radio v-model="selectedAddressId" :value="address.id" />
          <div class="address-content">
            <div class="address-header">
              <span class="name">{{ address.name }}</span>
              <span class="phone">{{ address.phone }}</span>
              <el-tag v-if="address.isDefault" size="small" type="primary">默认</el-tag>
            </div>
            <div class="address-detail">{{ address.address }}</div>
          </div>
          <div class="address-actions">
            <el-button link size="small" @click.stop="editAddress(address)">编辑</el-button>
            <el-button link size="small" type="danger" @click.stop="deleteAddress(address.id)">删除</el-button>
          </div>
        </div>
      </div>
      <div class="address-quick-actions">
        <div class="quick-buttons">
          <el-button @click="showAddressTemplates" :loading="loadingTemplates">
            <el-icon><LocationFilled /></el-icon>
            常用地址模板
          </el-button>
          <el-button @click="useCurrentLocation" :loading="gettingLocation">
            <el-icon><Position /></el-icon>
            使用当前位置
          </el-button>
        </div>
      </div>
      <div class="dialog-footer">
        <div class="footer-right">
          <el-button @click="showAddressDialog = false">取消</el-button>
          <el-button type="primary" @click="addNewAddress">新增地址</el-button>
          <el-button type="primary" @click="confirmAddress">确认</el-button>
        </div>
      </div>
    </el-dialog>

    <!-- 优惠券对话框 -->
    <el-dialog v-model="showCouponDialog" title="选择优惠券" width="500px">
      <div class="coupon-list">
        <div 
          v-for="coupon in availableCoupons" 
          :key="coupon.id"
          class="coupon-item"
          :class="{ selected: selectedCouponId === coupon.id }"
          @click="selectCoupon(coupon)"
        >
          <el-radio v-model="selectedCouponId" :value="coupon.id" />
          <div class="coupon-content">
            <div class="coupon-amount">¥{{ coupon.amount }}</div>
            <div class="coupon-info">
              <div class="coupon-name">{{ coupon.name }}</div>
              <div class="coupon-condition">满{{ coupon.minAmount }}元可用</div>
            </div>
          </div>
        </div>
        <div v-if="!availableCoupons.length" class="no-coupon">
          <el-empty description="暂无可用优惠券" :image-size="60" />
        </div>
      </div>
      <template #footer>
        <el-button @click="showCouponDialog = false">取消</el-button>
        <el-button type="primary" @click="confirmCoupon">确认</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { 
  LocationFilled, 
  ShoppingBag, 
  CreditCard, 
  EditPen, 
  Wallet, 
  ChatDotRound, 
  Ticket,
  Position
} from '@element-plus/icons-vue'

interface OrderItem {
  id: number
  name: string
  price: number
  quantity: number
  images?: string[]
  specifications?: string
}

interface Address {
  id: number
  name: string
  phone: string
  address: string
  isDefault: boolean
}

interface Coupon {
  id: number
  name: string
  amount: number
  minAmount: number
}

const router = useRouter()

// 响应式状态
const orderItems = ref<OrderItem[]>([])
const addresses = ref<Address[]>([])
const availableCoupons = ref<Coupon[]>([])
const selectedAddress = ref<Address | null>(null)
const selectedAddressId = ref<number | null>(null)
const selectedPayment = ref('alipay')
const selectedCouponId = ref<number | null>(null)
const orderRemark = ref('')
const submitting = ref(false)
const loadingTemplates = ref(false)
const gettingLocation = ref(false)
const showAddressDialog = ref(false)
const showCouponDialog = ref(false)
const showTemplateDialog = ref(false)
const isMobile = ref(window.innerWidth < 768)

// 计算属性
const subtotal = computed(() => {
  return orderItems.value.reduce((sum, item) => sum + item.price * item.quantity, 0)
})

const shippingFee = computed(() => {
  return subtotal.value >= 99 ? 0 : 10 // 满99免运费
})

const selectedCoupon = computed(() => {
  return availableCoupons.value.find(c => c.id === selectedCouponId.value)
})

const discountAmount = computed(() => {
  if (!selectedCoupon.value) return 0
  if (subtotal.value >= selectedCoupon.value.minAmount) {
    return selectedCoupon.value.amount
  }
  return 0
})

const totalAmount = computed(() => {
  return subtotal.value + shippingFee.value - discountAmount.value
})

const canSubmit = computed(() => {
  return selectedAddress.value && selectedPayment.value && !submitting.value && orderItems.value.length > 0
})

// 方法
const loadOrderData = async () => {
  try {
    // 检查是否有URL参数传递的商品
    const urlParams = new URLSearchParams(window.location.search)
    const itemsParam = urlParams.get('items')
    
    if (itemsParam) {
      // 从URL参数获取商品列表
      const items = JSON.parse(decodeURIComponent(itemsParam))
      console.log('从URL获取的商品:', items)
      
      // 根据product_id获取完整商品信息
      const productsWithDetails = []
      for (const item of items) {
        try {
          const response = await fetch(`/api/products/${item.product_id}`)
          if (response.ok) {
            const product = await response.json()
            productsWithDetails.push({
              id: product.id,
              name: product.name,
              price: product.price,
              quantity: item.quantity,
              images: product.images || [],
              specifications: product.specifications || ''
            })
          }
        } catch (error) {
          console.error(`获取商品${item.product_id}失败:`, error)
        }
      }
      
      orderItems.value = productsWithDetails
    } else {
      // 从购物车获取订单数据（原有逻辑）
      const cartData = JSON.parse(localStorage.getItem('cart') || '[]')
      orderItems.value = cartData.filter((item: any) => item.selected)
    }
    
    if (!orderItems.value.length) {
      ElMessage.warning('请先选择要结算的商品')
      router.push('/cart')
      return
    }
  } catch (error) {
    console.error('加载订单数据失败:', error)
    ElMessage.error('加载订单数据失败')
  }
}

const loadAddresses = () => {
  // 模拟地址数据
  addresses.value = [
    {
      id: 1,
      name: '张三',
      phone: '138****8888',
      address: '北京市朝阳区建国门外大街1号',
      isDefault: true
    },
    {
      id: 2,
      name: '李四',
      phone: '139****9999',
      address: '上海市浦东新区陆家嘴金融中心',
      isDefault: false
    }
  ]
  
  const defaultAddress = addresses.value.find(addr => addr.isDefault)
  if (defaultAddress) {
    selectedAddress.value = defaultAddress
    selectedAddressId.value = defaultAddress.id
  }
}

const loadCoupons = () => {
  // 模拟优惠券数据
  availableCoupons.value = [
    { id: 1, name: '新用户优惠券', amount: 20, minAmount: 100 },
    { id: 2, name: '满减优惠券', amount: 50, minAmount: 300 },
    { id: 3, name: '会员专享', amount: 100, minAmount: 500 }
  ]
}

const selectAddress = (address: Address) => {
  selectedAddressId.value = address.id
}

const confirmAddress = () => {
  const address = addresses.value.find(addr => addr.id === selectedAddressId.value)
  if (address) {
    selectedAddress.value = address
    showAddressDialog.value = false
  }
}

const handleCloseAddressDialog = () => {
  selectedAddressId.value = selectedAddress.value?.id || null
  showAddressDialog.value = false
}

const addNewAddress = () => {
  ElMessage.info('跳转到新增地址页面')
  // 这里可以跳转到地址管理页面
}

const editAddress = (address: Address) => {
  ElMessage.info('编辑地址: ' + address.name)
  // 编辑地址逻辑
}

const deleteAddress = (addressId: number) => {
  ElMessageBox.confirm('确定删除此地址吗？', '提示', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning'
  }).then(() => {
    addresses.value = addresses.value.filter(addr => addr.id !== addressId)
    if (selectedAddress.value?.id === addressId) {
      selectedAddress.value = null
      selectedAddressId.value = null
    }
    ElMessage.success('删除成功')
  }).catch(() => {})
}

// 显示地址模板
const showAddressTemplates = async () => {
  loadingTemplates.value = true
  
  try {
    // 常用城市地址模板
    const templates = [
      { 
        name: '北京用户', 
        phone: '138****8888', 
        address: '北京市朝阳区建国门外大街1号国贸大厦',
        label: '北京-国贸商圈' 
      },
      { 
        name: '上海用户', 
        phone: '139****9999', 
        address: '上海市浦东新区陆家嘴金融中心大厦',
        label: '上海-陆家嘴' 
      },
      { 
        name: '广州用户', 
        phone: '135****5555', 
        address: '广州市天河区珠江新城CBD中心',
        label: '广州-天河区' 
      },
      { 
        name: '深圳用户', 
        phone: '136****6666', 
        address: '深圳市南山区科技园腾讯大厦',
        label: '深圳-南山区' 
      },
      { 
        name: '杭州用户', 
        phone: '137****7777', 
        address: '杭州市西湖区文三路阿里巴巴大厦',
        label: '杭州-西湖区' 
      }
    ]
    
    // 使用confirm方式简化实现
    const options = templates.map((t, i) => `${i + 1}. ${t.label}\n   ${t.name} ${t.phone}\n   ${t.address}`).join('\n\n')
    
    const result = await ElMessageBox.confirm(
      `请选择地址模板：\n\n${options}`,
      '常用地址模板',
      {
        confirmButtonText: '选择第一个',
        cancelButtonText: '取消',
        type: 'info'
      }
    )
    
    // 默认选择第一个模板
    const selectedTemplate = templates[0]
    const newAddress: Address = {
      id: Date.now(),
      name: selectedTemplate.name,
      phone: selectedTemplate.phone,
      address: selectedTemplate.address,
      isDefault: addresses.value.length === 0
    }
    
    addresses.value.unshift(newAddress)
    selectedAddress.value = newAddress
    selectedAddressId.value = newAddress.id
    ElMessage.success(`已添加${selectedTemplate.label}地址模板`)
    
  } catch (error) {
    // 用户取消或出错
  } finally {
    loadingTemplates.value = false
  }
}

// 使用当前位置
const useCurrentLocation = () => {
  gettingLocation.value = true
  
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      (position) => {
        // 这里应该调用逆地理编码API（如高德、百度地图API）将坐标转换为地址
        // 现在模拟地址获取
        const mockAddress: Address = {
          id: Date.now(),
          name: '当前位置用户',
          phone: '请填写手机号',
          address: '根据当前位置获取的地址（需要配置地图API）',
          isDefault: addresses.value.length === 0
        }
        
        addresses.value.unshift(mockAddress)
        selectedAddress.value = mockAddress
        selectedAddressId.value = mockAddress.id
        
        ElMessage.success('已获取当前位置，请完善收货信息')
        gettingLocation.value = false
      },
      (error) => {
        console.error('获取位置失败:', error)
        let message = '获取位置失败'
        
        switch (error.code) {
          case error.PERMISSION_DENIED:
            message = '用户拒绝了位置请求'
            break
          case error.POSITION_UNAVAILABLE:
            message = '位置信息不可用'
            break
          case error.TIMEOUT:
            message = '位置请求超时'
            break
        }
        
        ElMessage.error(message)
        gettingLocation.value = false
      },
      {
        timeout: 10000,
        enableHighAccuracy: true
      }
    )
  } else {
    ElMessage.error('您的浏览器不支持地理位置服务')
    gettingLocation.value = false
  }
}

const selectCoupon = (coupon: Coupon) => {
  selectedCouponId.value = coupon.id
}

const confirmCoupon = () => {
  showCouponDialog.value = false
}

const submitOrder = async () => {
  if (!canSubmit.value) return
  
  submitting.value = true
  
  try {
    // 构建订单数据
    const orderData = {
      items: orderItems.value.map(item => ({
        product_id: item.id,
        quantity: item.quantity,
        price: item.price
      })),
      shipping_address: selectedAddress.value 
        ? `${selectedAddress.value.name} ${selectedAddress.value.phone} ${selectedAddress.value.address}`
        : '',
      payment_method: selectedPayment.value,
      remark: orderRemark.value || '',
      subtotal: subtotal.value,
      shipping_fee: shippingFee.value,
      discount_amount: discountAmount.value,
      total_amount: totalAmount.value
    }

    // 调用API创建订单
    const response = await fetch('/api/orders/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(orderData)
    })

    if (!response.ok) {
      const errorData = await response.text()
      console.error('提交订单失败，响应:', errorData)
      throw new Error(`创建订单失败: ${response.status}`)
    }

    const order = await response.json()
    console.log('订单创建成功:', order)
    
    // 清空购物车中已下单的商品
    const remainingCart = JSON.parse(localStorage.getItem('cart') || '[]')
      .filter((item: any) => !item.selected)
    localStorage.setItem('cart', JSON.stringify(remainingCart))

    ElMessage.success('订单创建成功')
    
    // 跳转到新的简化支付页面
    router.push(`/simple-pay/${order.order_number}`)
    
  } catch (error) {
    console.error('提交订单失败:', error)
    console.error('订单数据:', orderData)
    ElMessage.error('提交订单失败，请重试')
  } finally {
    submitting.value = false
  }
}

// 监听窗口大小变化
const handleResize = () => {
  isMobile.value = window.innerWidth < 768
}

onMounted(() => {
  loadOrderData()
  loadAddresses()
  loadCoupons()
  window.addEventListener('resize', handleResize)
})
</script>

<style scoped>
.checkout-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.checkout-section > .el-card {
  margin-bottom: 20px;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
}

/* 收货地址 */
.address-item {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding: 16px;
  border: 2px solid #e4e7ed;
  border-radius: 8px;
  transition: all 0.3s;
}

.address-item.selected {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.address-info {
  flex: 1;
}

.address-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.address-header .name {
  font-weight: 600;
}

.address-header .phone {
  color: #666;
}

.address-detail {
  color: #666;
  line-height: 1.5;
}

.no-address {
  text-align: center;
  padding: 40px 20px;
}

/* 商品清单 */
.order-item {
  display: flex;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.order-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 80px;
  height: 80px;
  border-radius: 8px;
  margin-right: 16px;
  flex-shrink: 0;
}

.item-info {
  flex: 1;
}

.item-name {
  font-size: 16px;
  font-weight: 500;
  margin-bottom: 8px;
  color: #303133;
}

.item-specs {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
}

.item-price {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.item-price .price {
  font-size: 16px;
  font-weight: 600;
  color: #f56c6c;
}

.item-price .quantity {
  color: #909399;
}

/* 支付方式 */
.payment-methods {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.payment-option {
  width: 100%;
  margin-right: 0;
}

.payment-info {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
}

/* 订单汇总 */
.sticky-summary {
  position: sticky;
  top: 80px;
}

.summary-header {
  font-size: 18px;
  font-weight: 600;
}

.summary-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  color: #606266;
}

.free-shipping {
  color: #67c23a;
}

.coupon-discount {
  color: #f56c6c;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  font-size: 18px;
  font-weight: 600;
}

.total-price {
  color: #f56c6c;
  font-size: 20px;
}

.submit-button {
  width: 100%;
  margin-top: 20px;
  height: 50px;
  font-size: 16px;
}

.coupon-section {
  text-align: center;
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #f0f0f0;
}

/* 对话框 */
.address-list {
  max-height: 400px;
  overflow-y: auto;
}

.address-option {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.address-option:hover {
  border-color: #409eff;
}

.address-option.selected {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.address-content {
  flex: 1;
}

.address-actions {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.address-quick-actions {
  margin: 16px 0;
  padding: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #e9ecef;
}

.quick-buttons {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}

.quick-buttons .el-button {
  flex: 1;
  min-width: 120px;
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
}

.dialog-footer .footer-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 优惠券 */
.coupon-list {
  max-height: 300px;
  overflow-y: auto;
}

.coupon-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px;
  border: 1px solid #e4e7ed;
  border-radius: 8px;
  margin-bottom: 12px;
  cursor: pointer;
  transition: all 0.3s;
}

.coupon-item:hover,
.coupon-item.selected {
  border-color: #409eff;
  background-color: #f0f9ff;
}

.coupon-content {
  display: flex;
  align-items: center;
  gap: 16px;
  flex: 1;
}

.coupon-amount {
  font-size: 20px;
  font-weight: 600;
  color: #f56c6c;
  min-width: 60px;
}

.coupon-info .coupon-name {
  font-weight: 500;
  margin-bottom: 4px;
}

.coupon-info .coupon-condition {
  font-size: 12px;
  color: #909399;
}

.no-coupon {
  text-align: center;
  padding: 40px 20px;
}

/* 移动端适配 */
@media (max-width: 768px) {
  .checkout-container {
    padding: 16px;
  }
  
  .order-summary {
    margin-top: 20px;
  }
  
  .address-item {
    flex-direction: column;
    gap: 12px;
  }
  
  .order-item {
    flex-direction: column;
    text-align: center;
  }
  
  .item-image {
    margin: 0 auto 12px;
  }
  
  .item-price {
    justify-content: center;
    gap: 20px;
  }
  
  .payment-info {
    justify-content: center;
  }
  
  .address-option {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .address-actions {
    flex-direction: row;
    align-self: flex-end;
  }
}
</style>