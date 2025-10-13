import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { useUserStore } from './user'

export interface CartItem {
  id: number
  product_id: number
  quantity: number
  price_snapshot: string
  product: {
    id: number
    name: string
    description: string
    price: string
    images: string[]
    stock_quantity: number
    category: string
  }
}

// 获取认证token
const getAuthToken = () => {
  // 按优先级获取token
  return localStorage.getItem('user_token') ||
         localStorage.getItem('admin_token') ||
         localStorage.getItem('token')
}

// 检查是否已登录
const isAuthenticated = () => {
  return !!getAuthToken()
}

export const useCartStore = defineStore('cart', () => {
  const items = ref<CartItem[]>([])
  const loading = ref(false)
  const cartId = ref<number | null>(null)
  const userStore = useUserStore()

  // 计算总数量
  const totalItems = computed(() => {
    return items.value.reduce((total, item) => total + item.quantity, 0)
  })

  // 计算总价格
  const totalPrice = computed(() => {
    const total = items.value.reduce((total, item) => {
      const price = parseFloat(item.product.price) || 0
      console.log('计算购物车价格:', {
        product: item.product.name,
        price_raw: item.product.price,
        price_parsed: price,
        quantity: item.quantity,
        subtotal: price * item.quantity
      })
      return total + (price * item.quantity)
    }, 0)
    console.log('购物车总价格:', total)
    return total
  })

  // 从后端加载购物车
  const loadCart = async () => {
    if (!isAuthenticated()) {
      items.value = []
      return
    }

    try {
      loading.value = true
      const response = await fetch('/api/cart/', {
        headers: {
          'Authorization': `Bearer ${getAuthToken()}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        cartId.value = data.id
        items.value = data.items || []
      } else if (response.status === 401) {
        // Token无效，同步清除localStorage和userStore状态
        userStore.clearUser()
        items.value = []
      } else {
        console.error('加载购物车失败:', response.statusText)
        items.value = []
      }
    } catch (error) {
      console.error('加载购物车失败:', error)
      items.value = []
    } finally {
      loading.value = false
    }
  }

  // 添加商品到购物车
  const addToCart = async (product: any, quantity: number = 1) => {
    if (!isAuthenticated()) {
      ElMessage.warning('请先登录')
      return false
    }

    try {
      loading.value = true
      const response = await fetch('/api/cart/items', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getAuthToken()}`
        },
        body: JSON.stringify({
          product_id: product.id,
          quantity: quantity
        })
      })

      if (response.ok) {
        const data = await response.json()
        cartId.value = data.id
        items.value = data.items || []
        ElMessage.success('已加入购物车')
        return true
      } else {
        const error = await response.json()
        ElMessage.error(error.detail || '加入购物车失败')
        return false
      }
    } catch (error: any) {
      console.error('加入购物车失败:', error)
      ElMessage.error(error.message || '加入购物车失败')
      return false
    } finally {
      loading.value = false
    }
  }

  // 更新商品数量
  const updateQuantity = async (itemId: number, quantity: number) => {
    if (!isAuthenticated()) {
      ElMessage.warning('请先登录')
      return
    }

    try {
      loading.value = true
      const response = await fetch(`/api/cart/items/${itemId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${getAuthToken()}`
        },
        body: JSON.stringify({
          quantity: quantity
        })
      })

      if (response.ok) {
        const data = await response.json()
        items.value = data.items || []
      } else {
        const error = await response.json()
        throw new Error(error.detail || '更新数量失败')
      }
    } catch (error: any) {
      console.error('更新数量失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  // 从购物车移除商品
  const removeFromCart = async (itemId: number) => {
    if (!isAuthenticated()) {
      ElMessage.warning('请先登录')
      return
    }

    try {
      loading.value = true
      const response = await fetch(`/api/cart/items/${itemId}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${getAuthToken()}`
        }
      })

      if (response.ok) {
        const data = await response.json()
        items.value = data.items || []
      } else {
        const error = await response.json()
        ElMessage.error(error.detail || '删除失败')
      }
    } catch (error: any) {
      console.error('删除失败:', error)
      ElMessage.error(error.message || '删除失败')
    } finally {
      loading.value = false
    }
  }

  // 清空购物车
  const clearCart = async () => {
    if (!isAuthenticated()) {
      return
    }

    try {
      loading.value = true
      const response = await fetch('/api/cart/clear', {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${getAuthToken()}`
        }
      })

      if (response.ok) {
        items.value = []
        ElMessage.success('购物车已清空')
      } else {
        const error = await response.json()
        ElMessage.error(error.detail || '清空购物车失败')
      }
    } catch (error: any) {
      console.error('清空购物车失败:', error)
      ElMessage.error(error.message || '清空购物车失败')
    } finally {
      loading.value = false
    }
  }

  // 获取购物车商品（用于结算）
  const getCartForCheckout = () => {
    return {
      items: items.value.map(item => ({
        product_id: item.product.id,
        quantity: item.quantity,
        price: parseFloat(item.product.price)
      })),
      total_amount: totalPrice.value,
      subtotal: totalPrice.value,
      shipping_fee: 0,
      discount_amount: 0
    }
  }

  // 初始化 - 从后端加载购物车
  loadCart()

  return {
    items,
    loading,
    totalItems,
    totalPrice,
    loadCart,
    addToCart,
    updateQuantity,
    removeFromCart,
    clearCart,
    getCartForCheckout
  }
})
