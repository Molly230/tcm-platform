// 小程序API调用工具
const BASE_URL = 'http://localhost:8001'

// 统一API请求方法
export function apiRequest(url, options = {}) {
  return new Promise((resolve, reject) => {
    // 获取token
    const token = uni.getStorageSync('token')
    
    // 设置请求头
    const header = {
      'Content-Type': 'application/json',
      ...options.header
    }
    
    if (token) {
      header['Authorization'] = `Bearer ${token}`
    }
    
    // 发起请求
    uni.request({
      url: BASE_URL + url,
      method: options.method || 'GET',
      data: options.data,
      header: header,
      success: (res) => {
        console.log('API Response:', res)
        
        if (res.statusCode === 200) {
          resolve(res.data)
        } else if (res.statusCode === 401) {
          // token过期，清除本地数据并跳转登录
          uni.removeStorageSync('token')
          uni.removeStorageSync('user')
          uni.showModal({
            title: '登录过期',
            content: '请重新登录',
            showCancel: false,
            success: () => {
              uni.navigateTo({
                url: '/pages/login/login'
              })
            }
          })
          reject(new Error('登录过期'))
        } else {
          reject(new Error(res.data?.detail || `请求失败 ${res.statusCode}`))
        }
      },
      fail: (error) => {
        console.error('API Error:', error)
        reject(new Error('网络请求失败'))
      }
    })
  })
}

// 上传文件
export function uploadFile(filePath, url, data = {}) {
  return new Promise((resolve, reject) => {
    const token = uni.getStorageSync('token')
    
    const header = {}
    if (token) {
      header['Authorization'] = `Bearer ${token}`
    }
    
    uni.uploadFile({
      url: BASE_URL + url,
      filePath: filePath,
      name: 'file',
      formData: data,
      header: header,
      success: (res) => {
        if (res.statusCode === 200) {
          try {
            const data = JSON.parse(res.data)
            resolve(data)
          } catch (e) {
            resolve(res.data)
          }
        } else {
          reject(new Error('上传失败'))
        }
      },
      fail: (error) => {
        reject(error)
      }
    })
  })
}

// 获取用户信息
export function getCurrentUser() {
  return uni.getStorageSync('user')
}

// 检查是否登录
export function isLoggedIn() {
  const token = uni.getStorageSync('token')
  const user = uni.getStorageSync('user')
  return !!(token && user)
}

// 登出
export function logout() {
  uni.removeStorageSync('token')
  uni.removeStorageSync('user')
  uni.removeStorageSync('cart') // 清除购物车
  
  uni.showToast({
    title: '已退出登录',
    icon: 'success'
  })
  
  setTimeout(() => {
    uni.switchTab({
      url: '/pages/index/index'
    })
  }, 1500)
}