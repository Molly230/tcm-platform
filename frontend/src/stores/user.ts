import { defineStore } from 'pinia'
import { ref } from 'vue'

interface User {
  id: number
  username: string
  email: string
  full_name?: string
  phone?: string
  is_active: boolean
  is_admin?: boolean
  is_super_admin?: boolean
}

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(null)
  const isLoggedIn = ref(false)

  // 从localStorage初始化用户状态
  const initFromStorage = () => {
    const storedToken = localStorage.getItem('user_token')
    const storedUser = localStorage.getItem('user_data')
    
    if (storedToken && storedUser) {
      try {
        token.value = storedToken
        user.value = JSON.parse(storedUser)
        isLoggedIn.value = true
      } catch (error) {
        console.error('Failed to parse user data:', error)
        clearUser()
      }
    }
  }

  // 设置用户信息
  const setUser = (userData: User, userToken: string) => {
    user.value = userData
    token.value = userToken
    isLoggedIn.value = true
    
    localStorage.setItem('user_token', userToken)
    localStorage.setItem('user_data', JSON.stringify(userData))
  }

  // 清除用户信息
  const clearUser = () => {
    user.value = null
    token.value = null
    isLoggedIn.value = false
    
    localStorage.removeItem('user_token')
    localStorage.removeItem('user_data')
  }

  // 获取用户ID
  const getUserId = (): number | null => {
    return user.value?.id || null
  }

  // 获取用户ID字符串
  const getUserIdString = (): string => {
    const id = getUserId()
    return id ? `user_${id}` : ''
  }

  // 检查是否为管理员
  const isAdmin = (): boolean => {
    return user.value?.is_admin || user.value?.is_super_admin || false
  }

  // 初始化
  initFromStorage()

  return {
    user,
    token,
    isLoggedIn,
    setUser,
    clearUser,
    getUserId,
    getUserIdString,
    isAdmin,
    initFromStorage
  }
})