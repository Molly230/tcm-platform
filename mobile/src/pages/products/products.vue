<template>
  <view class="products-container">
    <!-- 搜索栏 -->
    <view class="search-bar">
      <input class="search-input" v-model="searchQuery" placeholder="搜索中药材..." @confirm="handleSearch" />
      <button class="search-btn" @click="handleSearch">
        <text>搜索</text>
      </button>
    </view>
    
    <!-- 分类筛选 -->
    <scroll-view class="categories" scroll-x="true">
      <view class="category-item" 
            :class="{ active: selectedCategory === '' }" 
            @click="selectCategory('')">
        <text>全部</text>
      </view>
      <view class="category-item" 
            v-for="category in categories" 
            :key="category.code"
            :class="{ active: selectedCategory === category.code }"
            @click="selectCategory(category.code)">
        <text>{{ category.zh }}</text>
      </view>
    </scroll-view>
    
    <!-- 商品列表 -->
    <scroll-view class="products-list" 
                 scroll-y="true" 
                 @scrolltolower="loadMore" 
                 :refresher-enabled="true"
                 :refresher-triggered="refreshing"
                 @refresherrefresh="handleRefresh">
      
      <view class="product-grid">
        <view class="product-card" 
              v-for="product in products" 
              :key="product.id"
              @click="goToProductDetail(product.id)">
          <image class="product-image" 
                 :src="getProductImage(product)" 
                 mode="aspectFill"
                 :lazy-load="true"></image>
          
          <view class="product-info">
            <text class="product-name">{{ product.name }}</text>
            <text class="product-desc">{{ product.description }}</text>
            
            <view class="price-row">
              <text class="price">¥{{ product.price }}</text>
              <view class="stock-status" :class="{ 'out-of-stock': product.stock_quantity <= 0 }">
                <text v-if="product.stock_quantity > 0">库存: {{ product.stock_quantity }}</text>
                <text v-else>缺货</text>
              </view>
            </view>
            
            <view class="product-tags">
              <text class="tag featured" v-if="product.is_featured">精选</text>
              <text class="tag common" v-if="product.is_common">常用</text>
              <text class="tag prescription" v-if="product.is_prescription_required">处方药</text>
            </view>
          </view>
          
          <button class="add-cart-btn" 
                  @click.stop="addToCart(product)"
                  :disabled="product.stock_quantity <= 0">
            <text v-if="product.stock_quantity > 0">加入购物车</text>
            <text v-else>缺货</text>
          </button>
        </view>
      </view>
      
      <!-- 加载状态 -->
      <view class="loading-status" v-if="loading">
        <text>加载中...</text>
      </view>
      
      <view class="loading-status" v-if="!hasMore && products.length > 0">
        <text>没有更多商品了</text>
      </view>
      
      <view class="empty-state" v-if="!loading && products.length === 0">
        <text>暂无商品</text>
      </view>
    </scroll-view>
    
    <!-- 购物车浮动按钮 -->
    <view class="cart-float" @click="goToCart" v-if="cartCount > 0">
      <text class="cart-count">{{ cartCount }}</text>
      <text>购物车</text>
    </view>
  </view>
</template>

<script>
import { apiRequest } from '@/utils/api.js'

export default {
  data() {
    return {
      products: [],
      categories: [],
      searchQuery: '',
      selectedCategory: '',
      loading: false,
      refreshing: false,
      hasMore: true,
      page: 1,
      pageSize: 20,
      cartCount: 0
    }
  },
  
  onLoad() {
    this.loadCategories()
    this.loadProducts()
    this.updateCartCount()
  },
  
  onShow() {
    this.updateCartCount()
  },
  
  methods: {
    async loadCategories() {
      try {
        // 从枚举接口获取商品分类
        const response = await apiRequest('/api/system/enums/PRODUCT_CATEGORY')
        this.categories = response || []
      } catch (error) {
        console.error('加载分类失败:', error)
        // 设置默认分类
        this.categories = [
          { code: 'HERBS', zh: '中药材' },
          { code: 'WELLNESS', zh: '养生产品' },
          { code: 'HEALTH_FOOD', zh: '保健食品' }
        ]
      }
    },
    
    async loadProducts(reset = false) {
      if (this.loading) return
      
      this.loading = true
      
      try {
        const params = {
          page: reset ? 1 : this.page,
          page_size: this.pageSize,
          status: 'ACTIVE' // 只显示在售商品
        }
        
        if (this.searchQuery) {
          params.search = this.searchQuery
        }
        
        if (this.selectedCategory) {
          params.category = this.selectedCategory
        }
        
        const response = await apiRequest('/api/products/', {
          method: 'GET',
          data: params
        })
        
        if (reset) {
          this.products = response.items || []
          this.page = 1
        } else {
          this.products = [...this.products, ...(response.items || [])]
        }
        
        this.hasMore = response.items && response.items.length === this.pageSize
        this.page++
        
      } catch (error) {
        console.error('加载商品失败:', error)
        uni.showToast({
          title: '加载失败',
          icon: 'none'
        })
      } finally {
        this.loading = false
        this.refreshing = false
      }
    },
    
    handleSearch() {
      this.loadProducts(true)
    },
    
    selectCategory(category) {
      this.selectedCategory = category
      this.loadProducts(true)
    },
    
    handleRefresh() {
      this.refreshing = true
      this.loadProducts(true)
    },
    
    loadMore() {
      if (this.hasMore && !this.loading) {
        this.loadProducts()
      }
    },
    
    getProductImage(product) {
      if (product.images && product.images.length > 0) {
        return product.images[0].startsWith('http') 
          ? product.images[0] 
          : `http://localhost:8001${product.images[0]}`
      }
      return '/static/default-product.png'
    },
    
    async addToCart(product) {
      if (product.stock_quantity <= 0) {
        uni.showToast({
          title: '商品缺货',
          icon: 'none'
        })
        return
      }
      
      try {
        // 获取当前购物车
        let cart = uni.getStorageSync('cart') || []
        
        // 查找商品是否已在购物车中
        const existingIndex = cart.findIndex(item => item.id === product.id)
        
        if (existingIndex >= 0) {
          // 增加数量
          cart[existingIndex].quantity += 1
          if (cart[existingIndex].quantity > product.stock_quantity) {
            cart[existingIndex].quantity = product.stock_quantity
            uni.showToast({
              title: '库存不足',
              icon: 'none'
            })
            return
          }
        } else {
          // 添加新商品
          cart.push({
            id: product.id,
            name: product.name,
            price: product.price,
            image: this.getProductImage(product),
            quantity: 1,
            stock: product.stock_quantity
          })
        }
        
        uni.setStorageSync('cart', cart)
        this.updateCartCount()
        
        uni.showToast({
          title: '已加入购物车',
          icon: 'success'
        })
        
      } catch (error) {
        console.error('添加购物车失败:', error)
        uni.showToast({
          title: '添加失败',
          icon: 'none'
        })
      }
    },
    
    updateCartCount() {
      const cart = uni.getStorageSync('cart') || []
      this.cartCount = cart.reduce((total, item) => total + item.quantity, 0)
    },
    
    goToProductDetail(productId) {
      uni.navigateTo({
        url: `/pages/product-detail/product-detail?id=${productId}`
      })
    },
    
    goToCart() {
      uni.switchTab({
        url: '/pages/cart/cart'
      })
    }
  }
}
</script>

<style scoped>
.products-container {
  background: #f5f5f5;
  min-height: 100vh;
}

.search-bar {
  display: flex;
  align-items: center;
  padding: 20rpx;
  background: white;
}

.search-input {
  flex: 1;
  height: 70rpx;
  border: 1px solid #e0e0e0;
  border-radius: 35rpx;
  padding: 0 30rpx;
  margin-right: 20rpx;
  font-size: 28rpx;
}

.search-btn {
  width: 120rpx;
  height: 70rpx;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 35rpx;
  font-size: 28rpx;
}

.categories {
  background: white;
  white-space: nowrap;
  padding: 20rpx 0;
  border-bottom: 1px solid #f0f0f0;
}

.category-item {
  display: inline-block;
  padding: 15rpx 30rpx;
  margin: 0 10rpx;
  background: #f5f5f5;
  border-radius: 25rpx;
  font-size: 26rpx;
  color: #666;
}

.category-item.active {
  background: #409eff;
  color: white;
}

.products-list {
  height: calc(100vh - 300rpx);
  padding: 20rpx;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20rpx;
}

.product-card {
  background: white;
  border-radius: 15rpx;
  overflow: hidden;
  box-shadow: 0 4rpx 15rpx rgba(0,0,0,0.1);
}

.product-image {
  width: 100%;
  height: 300rpx;
}

.product-info {
  padding: 20rpx;
}

.product-name {
  font-size: 30rpx;
  font-weight: 500;
  color: #333;
  display: block;
  margin-bottom: 10rpx;
}

.product-desc {
  font-size: 24rpx;
  color: #666;
  display: block;
  margin-bottom: 15rpx;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.price-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15rpx;
}

.price {
  font-size: 32rpx;
  font-weight: bold;
  color: #ff4757;
}

.stock-status {
  font-size: 22rpx;
  color: #67c23a;
}

.stock-status.out-of-stock {
  color: #f56c6c;
}

.product-tags {
  margin-bottom: 20rpx;
}

.tag {
  font-size: 20rpx;
  padding: 4rpx 12rpx;
  border-radius: 10rpx;
  margin-right: 10rpx;
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

.add-cart-btn {
  width: 100%;
  height: 70rpx;
  background: #409eff;
  color: white;
  border: none;
  font-size: 26rpx;
}

.add-cart-btn[disabled] {
  background: #c0c4cc;
}

.loading-status, .empty-state {
  text-align: center;
  padding: 40rpx;
  color: #999;
  font-size: 28rpx;
}

.cart-float {
  position: fixed;
  bottom: 100rpx;
  right: 30rpx;
  width: 120rpx;
  height: 120rpx;
  background: #ff4757;
  color: white;
  border-radius: 60rpx;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8rpx 25rpx rgba(255,71,87,0.3);
  font-size: 24rpx;
}

.cart-count {
  position: absolute;
  top: -10rpx;
  right: -10rpx;
  width: 40rpx;
  height: 40rpx;
  background: #ffd700;
  color: #333;
  border-radius: 20rpx;
  font-size: 20rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}
</style>