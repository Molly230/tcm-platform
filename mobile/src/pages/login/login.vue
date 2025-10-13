<template>
  <view class="login-container">
    <view class="header">
      <image class="logo" src="/static/logo.png" mode="aspectFit"></image>
      <text class="title">中医健康平台</text>
      <text class="subtitle">传承中医文化，守护您的健康</text>
    </view>
    
    <view class="form-container">
      <view class="form-item">
        <text class="label">手机号/邮箱</text>
        <input class="input" v-model="form.username" placeholder="请输入手机号或邮箱" />
      </view>
      
      <view class="form-item">
        <text class="label">密码</text>
        <input class="input" v-model="form.password" type="password" placeholder="请输入密码" />
      </view>
      
      <button class="login-btn" @click="handleLogin" :disabled="loading">
        <text v-if="loading">登录中...</text>
        <text v-else>登录</text>
      </button>
      
      <view class="quick-login">
        <text class="quick-title">快速登录</text>
        <button class="wechat-login-btn" @click="handleWechatLogin">
          <text>微信登录</text>
        </button>
      </view>
      
      <view class="register-link">
        <text>还没有账号？</text>
        <text class="link" @click="goToRegister">立即注册</text>
      </view>
    </view>
  </view>
</template>

<script>
import { apiRequest } from '@/utils/api.js'

export default {
  data() {
    return {
      form: {
        username: '',
        password: ''
      },
      loading: false
    }
  },
  methods: {
    async handleLogin() {
      if (!this.form.username || !this.form.password) {
        uni.showToast({
          title: '请填写完整信息',
          icon: 'none'
        })
        return
      }
      
      this.loading = true
      
      try {
        const response = await apiRequest('/api/auth/login', {
          method: 'POST',
          data: {
            username: this.form.username,
            password: this.form.password
          }
        })
        
        if (response.access_token) {
          // 存储用户信息
          uni.setStorageSync('token', response.access_token)
          uni.setStorageSync('user', response.user)
          
          uni.showToast({
            title: '登录成功',
            icon: 'success'
          })
          
          // 跳转回首页
          setTimeout(() => {
            uni.switchTab({
              url: '/pages/index/index'
            })
          }, 1500)
        }
      } catch (error) {
        uni.showToast({
          title: error.message || '登录失败',
          icon: 'none'
        })
      } finally {
        this.loading = false
      }
    },
    
    async handleWechatLogin() {
      try {
        const res = await uni.login({
          provider: 'weixin'
        })
        
        if (res.code) {
          // 发送code到后端进行微信登录
          const response = await apiRequest('/api/auth/wechat-login', {
            method: 'POST',
            data: {
              code: res.code
            }
          })
          
          if (response.access_token) {
            uni.setStorageSync('token', response.access_token)
            uni.setStorageSync('user', response.user)
            
            uni.showToast({
              title: '登录成功',
              icon: 'success'
            })
            
            setTimeout(() => {
              uni.switchTab({
                url: '/pages/index/index'
              })
            }, 1500)
          }
        }
      } catch (error) {
        uni.showToast({
          title: '微信登录失败',
          icon: 'none'
        })
      }
    },
    
    goToRegister() {
      // 这里可以跳转到注册页面或者弹出注册表单
      uni.showModal({
        title: '注册功能',
        content: '请通过网页版注册账号，或联系客服开通账户',
        showCancel: false
      })
    }
  }
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40rpx 60rpx;
}

.header {
  text-align: center;
  margin-bottom: 80rpx;
  margin-top: 100rpx;
}

.logo {
  width: 120rpx;
  height: 120rpx;
  margin-bottom: 30rpx;
}

.title {
  display: block;
  font-size: 48rpx;
  font-weight: bold;
  color: #333;
  margin-bottom: 20rpx;
}

.subtitle {
  display: block;
  font-size: 28rpx;
  color: #666;
}

.form-container {
  background: white;
  border-radius: 20rpx;
  padding: 60rpx 40rpx;
  box-shadow: 0 10rpx 40rpx rgba(0,0,0,0.1);
}

.form-item {
  margin-bottom: 40rpx;
}

.label {
  display: block;
  font-size: 28rpx;
  color: #333;
  margin-bottom: 20rpx;
  font-weight: 500;
}

.input {
  width: 100%;
  height: 80rpx;
  border: 1px solid #e0e0e0;
  border-radius: 10rpx;
  padding: 0 30rpx;
  font-size: 30rpx;
  background: #fafafa;
}

.login-btn {
  width: 100%;
  height: 90rpx;
  background: #409eff;
  color: white;
  border: none;
  border-radius: 45rpx;
  font-size: 32rpx;
  font-weight: 500;
  margin-top: 40rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-btn[disabled] {
  background: #c0c4cc;
}

.quick-login {
  margin-top: 60rpx;
  text-align: center;
}

.quick-title {
  display: block;
  font-size: 24rpx;
  color: #999;
  margin-bottom: 30rpx;
}

.wechat-login-btn {
  width: 100%;
  height: 80rpx;
  background: #07c160;
  color: white;
  border: none;
  border-radius: 40rpx;
  font-size: 30rpx;
  display: flex;
  align-items: center;
  justify-content: center;
}

.register-link {
  text-align: center;
  margin-top: 40rpx;
  font-size: 28rpx;
  color: #666;
}

.link {
  color: #409eff;
  text-decoration: underline;
}
</style>