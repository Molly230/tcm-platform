import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'
import router from '../router'

// 权限检查工具
export const checkAuth = (requiredAuth: boolean = true, requiredAdmin: boolean = false): boolean => {
  const userStore = useUserStore()
  
  // 检查是否需要登录
  if (requiredAuth && !userStore.isLoggedIn) {
    ElMessage.warning('请先登录')
    router.push('/login')
    return false
  }
  
  // 检查是否需要管理员权限
  if (requiredAdmin && !userStore.isAdmin()) {
    ElMessage.error('权限不足，需要管理员权限')
    router.push('/')
    return false
  }
  
  return true
}

// API请求权限验证拦截器
export const getAuthHeaders = (): Record<string, string> => {
  const userStore = useUserStore()
  const headers: Record<string, string> = {
    'Content-Type': 'application/json'
  }
  
  if (userStore.token) {
    headers.Authorization = `Bearer ${userStore.token}`
  }
  
  return headers
}

// 统一的API请求方法
export const authFetch = async (
  url: string, 
  options: RequestInit = {},
  showErrorMessage: boolean = true
): Promise<Response> => {
  const userStore = useUserStore()
  
  // 设置认证头
  const headers = {
    ...getAuthHeaders(),
    ...(options.headers || {})
  }
  
  const response = await fetch(url, {
    ...options,
    headers
  })
  
  // 处理401未授权
  if (response.status === 401) {
    ElMessage.error('登录已过期，请重新登录')
    userStore.clearUser()
    router.push('/login')
    throw new Error('Unauthorized')
  }
  
  // 处理403禁止访问
  if (response.status === 403) {
    ElMessage.error('权限不足')
    throw new Error('Forbidden')
  }
  
  // 处理其他错误
  if (!response.ok && showErrorMessage) {
    try {
      const errorData = await response.clone().json()
      ElMessage.error(errorData.detail || errorData.message || '请求失败')
    } catch {
      ElMessage.error('网络请求失败')
    }
  }
  
  return response
}