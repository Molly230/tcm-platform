<template>
  <div class="cart-page">
    <div class="cart-container">
      <div class="cart-header">
        <h1>🛒 购物车</h1>
        <p v-if="cartStore.totalItems > 0">共 {{ cartStore.totalItems }} 件商品</p>
      </div>

      <!-- 空购物车状态 -->
      <div v-if="cartStore.items.length === 0" class="empty-cart">
        <div class="empty-icon">🛒</div>
        <h3>购物车为空</h3>
        <p>快去选购您喜欢的商品吧！</p>
        <el-button type="primary" @click="$router.push('/products')">去购物</el-button>
      </div>

      <!-- 购物车商品列表 -->
      <div v-else class="cart-content">
        <div class="cart-items">
          <div
            v-for="item in cartStore.items"
            :key="item.id"
            class="cart-item"
          >
            <div class="item-image">
              <img :src="getProductImage(item)" :alt="item.product.name">
            </div>

            <div class="item-info">
              <h3 class="item-name">{{ item.product.name }}</h3>
              <div class="item-price">¥{{ parseFloat(item.product.price).toFixed(2) }}</div>
              <div class="item-stock">库存: {{ item.product.stock_quantity }}</div>
            </div>

            <div class="item-quantity">
              <label>数量:</label>
              <el-input-number
                v-model="item.quantity"
                :min="1"
                :max="item.product.stock_quantity"
                size="small"
                @change="updateQuantity(item.id, item.quantity)"
              />
            </div>

            <div class="item-total">
              <div class="total-price">¥{{ (parseFloat(item.product.price) * item.quantity).toFixed(2) }}</div>
            </div>

            <div class="item-actions">
              <el-button
                type="danger"
                size="small"
                @click="removeItem(item.id)"
                :icon="Delete"
              >
                删除
              </el-button>
            </div>
          </div>
        </div>

        <!-- 购物车汇总 -->
        <div class="cart-summary">
          <div class="summary-content">
            <div class="summary-row total">
              <span>总计:</span>
              <span class="total-amount">¥{{ finalAmount.toFixed(2) }}</span>
            </div>
          </div>

          <div class="summary-actions">
            <el-button size="large" @click="$router.push('/products')">继续购物</el-button>
            <el-button
              type="primary"
              size="large"
              @click="goToCheckout"
              :disabled="cartStore.items.length === 0"
            >
              去结算
            </el-button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Delete } from '@element-plus/icons-vue'
import { useCartStore } from '../stores/cart'

const router = useRouter()
const cartStore = useCartStore()

// 计算运费
const shippingFee = computed(() => {
  return 0  // 免运费
})

// 计算最终金额
const finalAmount = computed(() => {
  return cartStore.totalPrice + shippingFee.value
})

// 获取商品图片
const getProductImage = (item: any) => {
  if (item.product && item.product.images && item.product.images.length > 0) {
    return item.product.images[0]
  }
  return '/placeholder-product.jpg'
}

// 更新商品数量
const updateQuantity = async (itemId: number, quantity: number) => {
  try {
    await cartStore.updateQuantity(itemId, quantity)
    ElMessage.success('数量已更新')
  } catch (error) {
    ElMessage.error((error as Error).message)
  }
}

// 删除商品
const removeItem = async (itemId: number) => {
  await cartStore.removeFromCart(itemId)
}

// 去结算
const goToCheckout = () => {
  console.log('点击去结算，购物车商品数量:', cartStore.items.length)
  console.log('购物车商品:', cartStore.items)

  if (cartStore.items.length === 0) {
    ElMessage.warning('购物车为空，请先添加商品')
    return
  }

  try {
    console.log('准备跳转到结算页面...')
    // 使用购物车数据进行结算
    router.push({
      path: '/checkout',
      query: { from: 'cart' }
    })
    console.log('跳转命令已发送')
  } catch (error) {
    console.error('跳转失败:', error)
    ElMessage.error('跳转失败: ' + error.message)
  }
}
</script>

<style scoped>
.cart-page {
  min-height: 100vh;
  background: #f5f7fa;
  padding: 20px;
}

.cart-container {
  max-width: 1200px;
  margin: 0 auto;
}

.cart-header {
  text-align: center;
  margin-bottom: 30px;
}

.cart-header h1 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.cart-header p {
  color: #7f8c8d;
  font-size: 16px;
}

/* 空购物车样式 */
.empty-cart {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 80px;
  margin-bottom: 20px;
}

.empty-cart h3 {
  color: #2c3e50;
  margin-bottom: 10px;
}

.empty-cart p {
  color: #7f8c8d;
  margin-bottom: 30px;
}

/* 购物车内容样式 */
.cart-content {
  display: flex;
  gap: 30px;
  align-items: flex-start;
}

.cart-items {
  flex: 1;
  background: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.cart-item {
  display: flex;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #ebeef5;
  gap: 20px;
}

.cart-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 80px;
  height: 80px;
  flex-shrink: 0;
}

.item-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 8px;
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-size: 16px;
  color: #2c3e50;
  margin: 0 0 8px 0;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-price {
  font-size: 14px;
  color: #e74c3c;
  font-weight: 600;
  margin-bottom: 4px;
}

.item-stock {
  font-size: 12px;
  color: #7f8c8d;
}

.item-quantity {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.item-quantity label {
  font-size: 12px;
  color: #7f8c8d;
}

.item-total {
  width: 100px;
  text-align: right;
}

.total-price {
  font-size: 16px;
  color: #e74c3c;
  font-weight: 600;
}

.item-actions {
  width: 80px;
  text-align: center;
}

/* 购物车汇总样式 */
.cart-summary {
  width: 350px;
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  height: fit-content;
  position: sticky;
  top: 20px;
}

.summary-content {
  margin-bottom: 20px;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 12px;
  font-size: 14px;
}

.summary-row.total {
  border-top: 1px solid #ebeef5;
  padding-top: 12px;
  font-size: 16px;
  font-weight: 600;
}

.total-amount {
  color: #e74c3c;
  font-size: 18px;
}

.summary-actions {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.summary-actions .el-button {
  width: 100%;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .cart-content {
    flex-direction: column;
  }

  .cart-summary {
    width: 100%;
    position: static;
  }

  .cart-item {
    flex-wrap: wrap;
    gap: 15px;
  }

  .item-quantity,
  .item-total,
  .item-actions {
    width: auto;
  }
}
</style>