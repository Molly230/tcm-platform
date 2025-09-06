<template>
  <el-header class="header">
    <div class="header-content">
      <h1 class="logo" @click="$router.push('/')">中医健康服务平台</h1>
      <nav class="nav">
        <el-button link @click="$router.push('/')">首页</el-button>
        <el-button link @click="$router.push('/courses')">课程</el-button>
        <el-button link @click="$router.push('/assessment')">系统诊断</el-button>
        <el-button link @click="$router.push('/products')">商城</el-button>
        <el-button link @click="$router.push('/consultation')">咨询</el-button>
        <el-button link @click="$router.push('/my')">我的</el-button>
      </nav>
      <div class="user-actions">
        <el-popover
          placement="bottom-end"
          width="320"
          trigger="hover"
          :show-after="200"
          :hide-after="100"
        >
          <template #reference>
            <el-button link @click="$router.push('/cart')" class="cart-button">
              <el-badge :value="cartItemCount" :hidden="cartItemCount === 0" :max="99">
                <el-icon><ShoppingCart /></el-icon>
              </el-badge>
              购物车
            </el-button>
          </template>
          
          <!-- 购物车悬浮预览 -->
          <div class="cart-preview">
            <div class="cart-preview-header">
              <h4>购物车 ({{ cartItemCount }}件)</h4>
            </div>
            
            <div v-if="cartItems.length === 0" class="cart-empty">
              购物车为空
            </div>
            
            <div v-else class="cart-preview-content">
              <div v-for="item in cartItems.slice(0, 3)" :key="item.id" class="cart-preview-item">
                <img :src="item.images?.[0] || '/default-product.jpg'" :alt="item.name" class="item-image">
                <div class="item-info">
                  <div class="item-name">{{ item.name }}</div>
                  <div class="item-price">¥{{ item.price }} × {{ item.quantity }}</div>
                </div>
              </div>
              
              <div v-if="cartItems.length > 3" class="more-items">
                还有 {{ cartItems.length - 3 }} 件商品...
              </div>
              
              <div class="cart-preview-footer">
                <div class="total-price">合计: ¥{{ cartTotalPrice.toFixed(2) }}</div>
                <el-button type="primary" size="small" @click="$router.push('/cart')">
                  去购物车结算
                </el-button>
              </div>
            </div>
          </div>
        </el-popover>
        
        <!-- 未登录状态 -->
        <template v-if="!isLoggedIn">
          <el-button type="primary" @click="$router.push('/login')">登录 / 注册</el-button>
        </template>
        
        <!-- 已登录状态 -->
        <template v-else>
          <el-dropdown @command="handleUserAction">
            <el-button type="text" class="user-dropdown">
              <el-icon><User /></el-icon>
              {{ userData?.username || userData?.full_name || '用户' }}
              <el-icon class="el-icon--right"><ArrowDown /></el-icon>
            </el-button>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile">个人资料</el-dropdown-item>
                <el-dropdown-item command="orders">我的订单</el-dropdown-item>
                <el-dropdown-item command="courses">我的课程</el-dropdown-item>
                <el-dropdown-item divided command="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </template>
      </div>
    </div>
  </el-header>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { ShoppingCart, User, ArrowDown } from '@element-plus/icons-vue'

interface UserData {
  id: number
  email: string
  username: string
  full_name?: string
  avatar?: string
  role: string
  status: string
}

const router = useRouter()
const isLoggedIn = ref(false)
const userData = ref<UserData | null>(null)

// 购物车相关
const cartItems = ref<any[]>([])

const cartItemCount = computed(() => {
  return cartItems.value.reduce((total, item) => total + item.quantity, 0)
})

const cartTotalPrice = computed(() => {
  return cartItems.value.reduce((total, item) => total + (item.price * item.quantity), 0)
})

const loadCartItems = () => {
  try {
    const cartData = localStorage.getItem('cart')
    if (cartData) {
      cartItems.value = JSON.parse(cartData)
    } else {
      cartItems.value = []
    }
  } catch (error) {
    console.error('加载购物车数据失败:', error)
    cartItems.value = []
  }
}

const updateCartDisplay = () => {
  loadCartItems()
}

const checkLoginStatus = () => {
  const token = localStorage.getItem('user_token')
  const userDataStr = localStorage.getItem('user_data')
  
  if (token && userDataStr) {
    try {
      userData.value = JSON.parse(userDataStr)
      isLoggedIn.value = true
    } catch (error) {
      console.error('解析用户数据失败:', error)
      localStorage.removeItem('user_token')
      localStorage.removeItem('user_data')
      isLoggedIn.value = false
      userData.value = null
    }
  } else {
    isLoggedIn.value = false
    userData.value = null
  }
}

const handleUserAction = (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'orders':
      router.push('/my/orders')
      break
    case 'courses':
      router.push('/my/courses')
      break
    case 'logout':
      handleLogout()
      break
  }
}

const handleLogout = () => {
  localStorage.removeItem('user_token')
  localStorage.removeItem('user_data')
  isLoggedIn.value = false
  userData.value = null
  ElMessage.success('已退出登录')
  router.push('/')
}


onMounted(() => {
  checkLoginStatus()
  loadCartItems()
  
  // 监听localStorage变化（用于跨标签页同步登录状态和购物车）
  window.addEventListener('storage', (e) => {
    if (e.key === 'user_token' || e.key === 'user_data') {
      checkLoginStatus()
    }
    if (e.key === 'cart') {
      loadCartItems()
    }
  })
  
  // 监听自定义购物车更新事件
  window.addEventListener('cartUpdated', updateCartDisplay)
})

// 暴露方法供外部调用
defineExpose({
  checkLoginStatus,
  updateCartDisplay
})
</script>

<style scoped>
.header {
  background-color: white;
  box-shadow: 0 2px 4px rgba(0,0,0,.1);
  padding: 0;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.logo {
  color: #409eff;
  margin: 0;
  font-size: 24px;
  cursor: pointer;
}

.nav .el-button {
  margin: 0 10px;
  font-size: 16px;
}

.user-actions .el-button {
  margin-left: 10px;
}

.cart-button {
  display: flex;
  align-items: center;
  gap: 4px;
}

.user-dropdown {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #303133;
  font-size: 14px;
}

.user-dropdown:hover {
  color: #409eff;
}

/* 购物车预览样式 */
.cart-preview {
  padding: 0;
}

.cart-preview-header {
  padding: 12px 16px;
  border-bottom: 1px solid #ebeef5;
  margin: 0;
}

.cart-preview-header h4 {
  margin: 0;
  font-size: 14px;
  color: #303133;
}

.cart-empty {
  padding: 20px 16px;
  text-align: center;
  color: #909399;
  font-size: 14px;
}

.cart-preview-content {
  max-height: 300px;
  overflow-y: auto;
}

.cart-preview-item {
  display: flex;
  align-items: center;
  padding: 12px 16px;
  border-bottom: 1px solid #f5f7fa;
  gap: 10px;
}

.cart-preview-item:last-child {
  border-bottom: none;
}

.item-image {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 4px;
  flex-shrink: 0;
}

.item-info {
  flex: 1;
  min-width: 0;
}

.item-name {
  font-size: 14px;
  color: #303133;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.item-price {
  font-size: 12px;
  color: #f56c6c;
  font-weight: 600;
}

.more-items {
  padding: 8px 16px;
  font-size: 12px;
  color: #909399;
  text-align: center;
  background: #f5f7fa;
}

.cart-preview-footer {
  padding: 12px 16px;
  border-top: 1px solid #ebeef5;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: #fafafa;
}

.total-price {
  font-size: 14px;
  font-weight: 600;
  color: #f56c6c;
}
</style>