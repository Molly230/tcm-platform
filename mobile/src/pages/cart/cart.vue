<template>
  <view class="cart-container">
    <view v-if="cartItems.length === 0" class="empty-cart">
      <image class="empty-icon" src="/static/empty-cart.png" mode="aspectFit"></image>
      <text class="empty-text">购物车是空的</text>
      <button class="go-shopping-btn" @click="goShopping">去购物</button>
    </view>
    
    <view v-else class="cart-content">
      <!-- 购物车商品列表 -->
      <scroll-view class="cart-list" scroll-y="true">
        <view class="cart-item" v-for="(item, index) in cartItems" :key="item.id">
          <view class="item-select">
            <checkbox :checked="item.selected" @click="toggleSelect(index)" />
          </view>
          
          <image class="item-image" :src="item.image" mode="aspectFill"></image>
          
          <view class="item-info">
            <text class="item-name">{{ item.name }}</text>
            <text class="item-price">¥{{ item.price }}</text>
            <text class="item-stock">库存: {{ item.stock }}</text>
          </view>
          
          <view class="item-controls">
            <view class="quantity-controls">
              <button class="qty-btn" @click="decreaseQuantity(index)" :disabled="item.quantity <= 1">-</button>
              <text class="quantity">{{ item.quantity }}</text>
              <button class="qty-btn" @click="increaseQuantity(index)" :disabled="item.quantity >= item.stock">+</button>
            </view>
            
            <button class="remove-btn" @click="removeItem(index)">删除</button>
          </view>
        </view>
      </scroll-view>
      
      <!-- 底部结算栏 -->
      <view class="checkout-bar">
        <view class="select-all">
          <checkbox :checked="allSelected" @click="toggleSelectAll" />
          <text>全选</text>
        </view>
        
        <view class="total-info">
          <text class="total-text">合计: </text>
          <text class="total-price">¥{{ totalPrice.toFixed(2) }}</text>
        </view>
        
        <button class="checkout-btn" 
                @click="goCheckout" 
                :disabled="selectedItems.length === 0">
          结算({{ selectedItems.length }})
        </button>
      </view>
    </view>
  </view>
</template>

<script>
import { isLoggedIn } from '@/utils/api.js'

export default {
  data() {
    return {
      cartItems: []
    }
  },
  
  computed: {
    selectedItems() {
      return this.cartItems.filter(item => item.selected)
    },
    
    allSelected() {
      return this.cartItems.length > 0 && this.cartItems.every(item => item.selected)
    },
    
    totalPrice() {
      return this.selectedItems.reduce((total, item) => total + (item.price * item.quantity), 0)
    }
  },
  
  onShow() {
    this.loadCartData()
  },
  
  methods: {
    loadCartData() {
      const cart = uni.getStorageSync('cart') || []
      // 为每个商品添加选中状态
      this.cartItems = cart.map(item => ({
        ...item,
        selected: item.selected !== undefined ? item.selected : true
      }))
    },
    
    saveCartData() {
      uni.setStorageSync('cart', this.cartItems)
    },
    
    toggleSelect(index) {
      this.cartItems[index].selected = !this.cartItems[index].selected
      this.saveCartData()
    },
    
    toggleSelectAll() {
      const newState = !this.allSelected
      this.cartItems.forEach(item => {
        item.selected = newState
      })
      this.saveCartData()
    },
    
    increaseQuantity(index) {
      const item = this.cartItems[index]
      if (item.quantity < item.stock) {
        item.quantity++
        this.saveCartData()
      } else {
        uni.showToast({
          title: '库存不足',
          icon: 'none'
        })
      }
    },
    
    decreaseQuantity(index) {
      const item = this.cartItems[index]
      if (item.quantity > 1) {
        item.quantity--
        this.saveCartData()
      }
    },
    
    removeItem(index) {
      uni.showModal({
        title: '确认删除',
        content: '确定要从购物车移除这件商品吗？',
        success: (res) => {
          if (res.confirm) {
            this.cartItems.splice(index, 1)
            this.saveCartData()
            
            uni.showToast({
              title: '已移除',
              icon: 'success'
            })
          }
        }
      })
    },
    
    goShopping() {
      uni.switchTab({
        url: '/pages/products/products'
      })
    },
    
    goCheckout() {
      if (this.selectedItems.length === 0) {
        uni.showToast({
          title: '请选择要结算的商品',
          icon: 'none'
        })
        return
      }
      
      // 检查登录状态
      if (!isLoggedIn()) {
        uni.showModal({
          title: '需要登录',
          content: '请先登录后再结算',
          success: (res) => {
            if (res.confirm) {
              uni.navigateTo({
                url: '/pages/login/login'
              })
            }
          }
        })
        return
      }
      
      // 将选中的商品传递给结算页面
      const selectedData = JSON.stringify(this.selectedItems)
      uni.navigateTo({
        url: `/pages/checkout/checkout?items=${encodeURIComponent(selectedData)}`
      })
    }
  }
}
</script>

<style scoped>
.cart-container {
  background: #f5f5f5;
  min-height: 100vh;
}

.empty-cart {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 200rpx 60rpx;
  text-align: center;
}

.empty-icon {
  width: 200rpx;
  height: 200rpx;
  margin-bottom: 40rpx;
  opacity: 0.6;
}

.empty-text {
  font-size: 32rpx;
  color: #999;
  margin-bottom: 60rpx;
}

.go-shopping-btn {
  width: 300rpx;
  height: 80rpx;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 40rpx;
  font-size: 30rpx;
}

.cart-content {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.cart-list {
  flex: 1;
  padding: 20rpx;
}

.cart-item {
  display: flex;
  align-items: center;
  background: white;
  border-radius: 15rpx;
  padding: 20rpx;
  margin-bottom: 20rpx;
  box-shadow: 0 4rpx 15rpx rgba(0,0,0,0.08);
}

.item-select {
  margin-right: 20rpx;
}

.item-image {
  width: 120rpx;
  height: 120rpx;
  border-radius: 10rpx;
  margin-right: 20rpx;
}

.item-info {
  flex: 1;
}

.item-name {
  font-size: 30rpx;
  color: #333;
  font-weight: 500;
  display: block;
  margin-bottom: 10rpx;
}

.item-price {
  font-size: 28rpx;
  color: #ff4757;
  font-weight: bold;
  display: block;
  margin-bottom: 5rpx;
}

.item-stock {
  font-size: 22rpx;
  color: #999;
  display: block;
}

.item-controls {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.quantity-controls {
  display: flex;
  align-items: center;
  margin-bottom: 20rpx;
}

.qty-btn {
  width: 60rpx;
  height: 60rpx;
  background: #f0f0f0;
  border: none;
  border-radius: 30rpx;
  font-size: 32rpx;
  color: #333;
  display: flex;
  align-items: center;
  justify-content: center;
}

.qty-btn[disabled] {
  background: #e0e0e0;
  color: #999;
}

.quantity {
  margin: 0 20rpx;
  font-size: 30rpx;
  font-weight: 500;
  min-width: 60rpx;
  text-align: center;
}

.remove-btn {
  font-size: 24rpx;
  color: #f56c6c;
  background: none;
  border: 1px solid #f56c6c;
  border-radius: 15rpx;
  padding: 10rpx 20rpx;
}

.checkout-bar {
  display: flex;
  align-items: center;
  background: white;
  padding: 20rpx 30rpx;
  border-top: 1px solid #f0f0f0;
  box-shadow: 0 -4rpx 15rpx rgba(0,0,0,0.08);
}

.select-all {
  display: flex;
  align-items: center;
  font-size: 28rpx;
  color: #333;
}

.select-all text {
  margin-left: 10rpx;
}

.total-info {
  flex: 1;
  text-align: right;
  margin-right: 30rpx;
}

.total-text {
  font-size: 28rpx;
  color: #333;
}

.total-price {
  font-size: 36rpx;
  font-weight: bold;
  color: #ff4757;
}

.checkout-btn {
  width: 200rpx;
  height: 80rpx;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 40rpx;
  font-size: 30rpx;
}

.checkout-btn[disabled] {
  background: #c0c4cc;
}
</style>