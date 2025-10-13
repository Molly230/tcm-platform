/**
 * 统一的API请求封装
 * 简单、直接、易用
 */

interface ApiResponse<T = any> {
  success: boolean
  message: string
  data?: T
  code?: number
}

interface PaginatedResponse<T = any> {
  items: T[]
  pagination: {
    total: number
    page: number
    size: number
    pages: number
  }
}

class ApiClient {
  private baseUrl = import.meta.env.VITE_API_URL || '/api'
  private token: string | null = null

  constructor() {
    // 从localStorage加载token
    this.token = localStorage.getItem('admin_token')
  }

  /**
   * 设置认证token
   */
  setToken(token: string) {
    this.token = token
    localStorage.setItem('admin_token', token)
  }

  /**
   * 清除token
   */
  clearToken() {
    this.token = null
    localStorage.removeItem('admin_token')
  }

  /**
   * 基础请求方法
   */
  private async request<T = any>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    const url = `${this.baseUrl}${endpoint}`
    
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...options.headers
    }

    // 添加认证头
    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers
      })

      const data: ApiResponse<T> = await response.json()

      // 如果是认证错误，清除token
      if (!data.success && (data.code === 401 || data.code === 403)) {
        this.clearToken()
        // 可以在这里触发登录跳转
        window.location.href = '/admin/login'
      }

      return data
    } catch (error) {
      console.error('API请求失败:', error)
      return {
        success: false,
        message: '网络请求失败，请检查连接'
      }
    }
  }

  /**
   * GET请求
   */
  async get<T = any>(endpoint: string, params?: Record<string, any>): Promise<ApiResponse<T>> {
    let url = endpoint
    if (params) {
      const queryString = new URLSearchParams(params).toString()
      url += `?${queryString}`
    }

    return this.request<T>(url, { method: 'GET' })
  }

  /**
   * POST请求
   */
  async post<T = any>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  /**
   * PUT请求
   */
  async put<T = any>(endpoint: string, data?: any): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: data ? JSON.stringify(data) : undefined
    })
  }

  /**
   * DELETE请求
   */
  async delete<T = any>(endpoint: string): Promise<ApiResponse<T>> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }

  /**
   * 管理员API请求
   */
  async adminRequest<T = any>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    return this.request<T>(`/admin${endpoint}`, options)
  }

  /**
   * 文件上传
   */
  async upload<T = any>(endpoint: string, file: File): Promise<ApiResponse<T>> {
    const formData = new FormData()
    formData.append('file', file)

    return this.request<T>(endpoint, {
      method: 'POST',
      body: formData,
      headers: {
        // 不设置Content-Type，让浏览器自动设置multipart/form-data
        ...(this.token && { 'Authorization': `Bearer ${this.token}` })
      }
    })
  }
}

// 导出全局实例
export const api = new ApiClient()

// 认证相关API
export const authApi = {
  /**
   * 登录
   */
  login: async (credentials: { username: string; password: string }) => {
    const result = await api.post<{
      token: string
      user: {
        id: number
        email: string
        username: string
        role: string
        is_admin: boolean
      }
    }>('/auth/simple-login', credentials)
    
    // 登录成功后设置token
    if (result.success && result.data?.token) {
      api.setToken(result.data.token)
    }
    
    return result
  },

  /**
   * 获取当前用户信息
   */
  getCurrentUser: () => api.get('/auth/me'),

  /**
   * 登出
   */
  logout: () => {
    api.clearToken()
    return Promise.resolve({ success: true, message: '已登出' })
  }
}

// 管理员API
export const adminApi = {
  /**
   * 测试接口
   */
  test: () => api.post('/admin/test'),

  /**
   * 获取统计数据
   */
  getStats: () => api.get('/admin/stats'),

  /**
   * 用户管理
   */
  users: {
    list: (params?: { page?: number; size?: number }) =>
      api.get<PaginatedResponse>('/admin/users', params),
    create: (data: any) => api.post('/admin/users', data),
    update: (id: number, data: any) => api.put(`/admin/users/${id}`, data),
    delete: (id: number) => api.delete(`/admin/users/${id}`)
  },

  /**
   * 专家管理
   */
  experts: {
    list: (params?: any) => api.get<PaginatedResponse>('/admin/experts', params),
    create: (data: any) => api.post('/admin/experts', data),
    update: (id: number, data: any) => api.put(`/admin/experts/${id}`, data),
    delete: (id: number) => api.delete(`/admin/experts/${id}`)
  },

  /**
   * 课程管理
   */
  courses: {
    list: (params?: any) => api.get<PaginatedResponse>('/admin/courses', params),
    create: (data: any) => api.post('/admin/courses', data),
    update: (id: number, data: any) => api.put(`/admin/courses/${id}`, data),
    delete: (id: number) => api.delete(`/admin/courses/${id}`)
  },

  /**
   * 商品管理
   */
  products: {
    list: (params?: any) => api.get<PaginatedResponse>('/admin/products', params),
    create: (data: any) => api.post('/admin/products', data),
    update: (id: number, data: any) => api.put(`/admin/products/${id}`, data),
    delete: (id: number) => api.delete(`/admin/products/${id}`)
  },

  /**
   * 文件上传
   */
  upload: {
    image: (file: File) => api.upload('/admin/upload/image', file),
    video: (file: File) => api.upload('/admin/upload/video', file),
    document: (file: File) => api.upload('/admin/upload/document', file)
  },

  /**
   * 审核管理
   */
  audit: {
    // 获取待审核列表
    getPending: (entityType?: string) => 
      api.get('/admin/audit/pending', entityType ? { entity_type: entityType } : {}),
    
    // 执行审核操作
    performAudit: (entityType: string, entityId: number, action: string, reason?: string, notes?: string) =>
      api.post(`/admin/audit/${entityType}/${entityId}`, { action, reason, notes }),
    
    // 获取审核历史
    getHistory: (entityType: string, entityId: number) =>
      api.get(`/admin/audit/logs/${entityType}/${entityId}`),
    
    // 获取审核统计
    getStats: () => api.get('/admin/audit/stats')
  }
}

export default api