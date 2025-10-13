<template>
  <view class="product-detail">
    <view v-if="loading" class="loading">
      <text>加载中...</text>
    </view>
    
    <view v-else-if="product" class="product-content">
      <!-- 商品图片轮播 -->
      <swiper class="product-swiper" indicator-dots="true" autoplay="true">
        <swiper-item v-for="(image, index) in product.images" :key="index">
          <image class="product-image" :src="getImageUrl(image)" mode="aspectFill" />
        </swiper-item>
      </swiper>
      
      <!-- 商品基本信息 -->
      <view class="product-info">
        <text class="product-name">{{ product.name }}</text>
        <text class="product-price">¥{{ product.price }}</text>
        <text class="product-stock">库存: {{ product.stock_quantity }}</text>
        
        <view class="product-tags">
          <text class="tag featured" v-if="product.is_featured">精选</text>
          <text class="tag common" v-if="product.is_common">常用</text>
          <text class="tag prescription" v-if="product.is_prescription_required">处方药</text>
        </view>
      </view>
      
      <!-- 商品详情 -->
      <view class="product-details">
        <text class="section-title">商品详情</text>
        <text class="product-description">{{ product.description }}</text>
        
        <view v-if="product.usage_instructions" class="usage-section">
          <text class="section-title">使用说明</text>
          <text class="usage-text">{{ product.usage_instructions }}</text>
        </view>
      </view>
    </view>
    
    <!-- 底部操作栏 -->
    <view class="bottom-actions" v-if="product">
      <button class="cart-btn" @click="goToCart">
        <text>购物车</text>
        <text v-if="cartCount > 0" class="cart-badge">{{ cartCount }}</text>
      </button>
      <button class="add-cart-btn" @click="addToCart" :disabled="product.stock_quantity <= 0">
        <text v-if="product.stock_quantity > 0">加入购物车</text>
        <text v-else>缺货</text>
      </button>
      <button class="buy-now-btn" @click="buyNow" :disabled="product.stock_quantity <= 0">
        <text>立即购买</text>
      </button>
    </view>
  </view>
</template>

<script>
import { apiRequest, isLoggedIn } from '@/utils/api.js'

export default {
  data() {
    return {
      productId: null,
      product: null,
      loading: true,
      cartCount: 0
    }
  },
  
  onLoad(options) {
    this.productId = options.id
    this.loadProductDetail()
    this.updateCartCount()
  },
  
  onShow() {
    this.updateCartCount()
  },
  
  methods: {
    async loadProductDetail() {
      this.loading = true
      
      try {
        const response = await apiRequest(`/api/products/${this.productId}`)
        this.product = response
      } catch (error) {
        console.error('加载商品详情失败:', error)
        uni.showToast({
          title: '加载失败',
          icon: 'none'
        })
        setTimeout(() => {
          uni.navigateBack()
        }, 1500)
      } finally {
        this.loading = false
      }
    },
    
    getImageUrl(image) {
      if (image && image.startsWith('http')) {
        return image
      }
      return image ? `http://localhost:8001${image}` : '/static/default-product.png'
    },
    
    addToCart() {
      if (!this.product || this.product.stock_quantity <= 0) return
      
      try {
        let cart = uni.getStorageSync('cart') || []
        const existingIndex = cart.findIndex(item => item.id === this.product.id)
        
        if (existingIndex >= 0) {
          cart[existingIndex].quantity += 1
          if (cart[existingIndex].quantity > this.product.stock_quantity) {
            cart[existingIndex].quantity = this.product.stock_quantity
            uni.showToast({
              title: '库存不足',
              icon: 'none'
            })
            return
          }
        } else {
          cart.push({
            id: this.product.id,
            name: this.product.name,
            price: this.product.price,
            image: this.getImageUrl(this.product.images?.[0]),
            quantity: 1,
            stock: this.product.stock_quantity
          })
        }
        
        uni.setStorageSync('cart', cart)
        this.updateCartCount()
        
        uni.showToast({
          title: '已加入购物车',
          icon: 'success'
        })
      } catch (error) {
        uni.showToast({
          title: '添加失败',
          icon: 'none'
        })
      }
    },
    
    buyNow() {
      if (!isLoggedIn()) {
        uni.showModal({
          title: '需要登录',
          content: '请先登录后再购买',
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
      
      // 直接购买逻辑
      const buyItem = {
        id: this.product.id,
        name: this.product.name,
        price: this.product.price,
        image: this.getImageUrl(this.product.images?.[0]),
        quantity: 1,
        stock: this.product.stock_quantity
      }
      
      const buyData = JSON.stringify([buyItem])
      uni.navigateTo({
        url: `/pages/checkout/checkout?items=${encodeURIComponent(buyData)}`
      })
    },
    
    goToCart() {
      uni.switchTab({
        url: '/pages/cart/cart'
      })
    },
    
    updateCartCount() {
      const cart = uni.getStorageSync('cart') || []
      this.cartCount = cart.reduce((total, item) => total + item.quantity, 0)
    }
  }
}
</script>

<style scoped>
.product-detail {
  background: #f5f5f5;
  min-height: 100vh;
  padding-bottom: 120rpx;
}

.loading {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 400rpx;
  font-size: 28rpx;
  color: #999;
}

.product-swiper {
  width: 100%;
  height: 600rpx;
}

.product-image {
  width: 100%;
  height: 100%;
}

.product-info {
  background: white;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.product-name {
  font-size: 36rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 20rpx;
}

.product-price {
  font-size: 42rpx;
  font-weight: bold;
  color: #ff4757;
  display: block;
  margin-bottom: 15rpx;
}

.product-stock {
  font-size: 28rpx;
  color: #67c23a;
  display: block;
  margin-bottom: 20rpx;
}

.product-tags {
  display: flex;
  gap: 15rpx;
}

.tag {
  font-size: 22rpx;
  padding: 8rpx 16rpx;
  border-radius: 12rpx;
}

.tag.featured {
  background: #ffd700;
  color: #333;
}

.tag.common {
  background: #67c23a;
  color: white;
}

.tag.prescription {
  background: #f56c6c;
  color: white;
}

.product-details {
  background: white;
  padding: 30rpx;
  margin-bottom: 20rpx;
}

.section-title {
  font-size: 32rpx;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 20rpx;
}

.product-description {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  display: block;
}

.usage-section {
  margin-top: 40rpx;
}

.usage-text {
  font-size: 28rpx;
  color: #666;
  line-height: 1.6;
  display: block;
}

.bottom-actions {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: white;
  padding: 20rpx;
  display: flex;
  gap: 20rpx;
  box-shadow: 0 -4rpx 15rpx rgba(0,0,0,0.1);
}

.cart-btn {
  flex: 1;
  height: 80rpx;
  background: #f5f5f5;
  color: #333;
  border: 1px solid #e0e0e0;
  border-radius: 40rpx;
  font-size: 28rpx;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
}

.cart-badge {
  position: absolute;
  top: -10rpx;
  right: 20rpx;
  background: #ff4757;
  color: white;
  font-size: 20rpx;
  padding: 4rpx 12rpx;
  border-radius: 12rpx;
  min-width: 24rpx;
  text-align: center;
}

.add-cart-btn {
  flex: 1.5;
  height: 80rpx;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 40rpx;
  font-size: 28rpx;
}

.buy-now-btn {
  flex: 1.5;
  height: 80rpx;
  background: #ff4757;
  color: white;
  border: none;
  border-radius: 40rpx;
  font-size: 28rpx;
}

.add-cart-btn[disabled],
.buy-now-btn[disabled] {
  background: #c0c4cc;
}
</style>