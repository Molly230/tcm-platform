<template>
  <view class="profile-container">
    <!-- 用户信息头部 -->
    <view class="user-header">
      <view v-if="!isUserLoggedIn" class="login-prompt">
        <image class="avatar" src="/static/default-avatar.png" mode="aspectFill"></image>
        <text class="login-text">点击登录</text>
        <button class="login-btn" @click="goToLogin">立即登录</button>
      </view>
      
      <view v-else class="user-info">
        <image class="avatar" :src="user.avatar || '/static/default-avatar.png'" mode="aspectFill"></image>
        <view class="user-details">
          <text class="username">{{ user.username || user.email }}</text>
          <text class="user-role">{{ getRoleText(user.role) }}</text>
        </view>
      </view>
    </view>
    
    <!-- 功能菜单 -->
    <view class="menu-section">
      <view class="menu-group">
        <text class="group-title">我的订单</text>
        <view class="menu-item" @click="goToOrders">
          <text class="menu-icon">📋</text>
          <text class="menu-text">我的订单</text>
          <text class="menu-arrow">></text>
        </view>
        <view class="menu-item" @click="goToCourses">
          <text class="menu-icon">📚</text>
          <text class="menu-text">我的课程</text>
          <text class="menu-arrow">></text>
        </view>
      </view>
      
      <view class="menu-group">
        <text class="group-title">健康服务</text>
        <view class="menu-item" @click="goToConsultation">
          <text class="menu-icon">💊</text>
          <text class="menu-text">健康咨询</text>
          <text class="menu-arrow">></text>
        </view>
        <view class="menu-item" @click="goToAssessment">
          <text class="menu-icon">📊</text>
          <text class="menu-text">健康评估</text>
          <text class="menu-arrow">></text>
        </view>
      </view>
      
      <view class="menu-group">
        <text class="group-title">其他</text>
        <view class="menu-item" @click="goToAbout">
          <text class="menu-icon">ℹ️</text>
          <text class="menu-text">关于我们</text>
          <text class="menu-arrow">></text>
        </view>
        <view class="menu-item" @click="contactService">
          <text class="menu-icon">📞</text>
          <text class="menu-text">联系客服</text>
          <text class="menu-arrow">></text>
        </view>
      </view>
      
      <view class="menu-group" v-if="isUserLoggedIn">
        <view class="menu-item danger" @click="handleLogout">
          <text class="menu-icon">🚪</text>
          <text class="menu-text">退出登录</text>
          <text class="menu-arrow">></text>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
import { getCurrentUser, isLoggedIn, logout } from '@/utils/api.js'

export default {
  data() {
    return {
      user: null
    }
  },
  
  computed: {
    isUserLoggedIn() {
      return isLoggedIn() && this.user
    }
  },
  
  onShow() {
    this.loadUserInfo()
  },
  
  methods: {
    loadUserInfo() {
      if (isLoggedIn()) {
        this.user = getCurrentUser()
      } else {
        this.user = null
      }
    },
    
    getRoleText(role) {
      const roleMap = {
        'USER': '普通用户',
        'VIP': 'VIP用户', 
        'EXPERT': '专家',
        'ADMIN': '管理员',
        'SUPER_ADMIN': '超级管理员'
      }
      return roleMap[role] || '用户'
    },
    
    goToLogin() {
      uni.navigateTo({
        url: '/pages/login/login'
      })
    },
    
    goToOrders() {
      if (!this.checkLogin()) return
      uni.navigateTo({
        url: '/pages/my-orders/my-orders'
      })
    },
    
    goToCourses() {
      if (!this.checkLogin()) return
      uni.navigateTo({
        url: '/pages/my-courses/my-courses'
      })
    },
    
    goToConsultation() {
      uni.switchTab({
        url: '/pages/consultation/consultation'
      })
    },
    
    goToAssessment() {
      uni.navigateTo({
        url: '/pages/assessment/assessment'
      })
    },
    
    goToAbout() {
      uni.navigateTo({
        url: '/pages/about/about'
      })
    },
    
    contactService() {
      uni.showModal({
        title: '联系客服',
        content: '客服热线：400-123-4567\n工作时间：9:00-18:00',
        showCancel: false
      })
    },
    
    checkLogin() {
      if (!this.isUserLoggedIn) {
        uni.showModal({
          title: '需要登录',
          content: '请先登录后再使用此功能',
          success: (res) => {
            if (res.confirm) {
              this.goToLogin()
            }
          }
        })
        return false
      }
      return true
    },
    
    handleLogout() {
      uni.showModal({
        title: '确认退出',
        content: '确定要退出登录吗？',
        success: (res) => {
          if (res.confirm) {
            logout()
            this.loadUserInfo()
          }
        }
      })
    }
  }
}
</script>

<style scoped>
.profile-container {
  background: #f5f5f5;
  min-height: 100vh;
}

.user-header {
  background: linear-gradient(135deg, #409eff, #67c23a);
  padding: 60rpx 40rpx 40rpx;
  color: white;
}

.login-prompt {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
}

.avatar {
  width: 120rpx;
  height: 120rpx;
  border-radius: 60rpx;
  border: 4rpx solid rgba(255,255,255,0.3);
  margin-right: 30rpx;
}

.login-prompt .avatar {
  margin-right: 0;
  margin-bottom: 20rpx;
  opacity: 0.8;
}

.user-details {
  flex: 1;
}

.username {
  font-size: 36rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 10rpx;
}

.user-role {
  font-size: 24rpx;
  opacity: 0.9;
  display: block;
}

.login-text {
  font-size: 28rpx;
  margin-bottom: 30rpx;
  opacity: 0.9;
}

.login-btn {
  background: rgba(255,255,255,0.2);
  color: white;
  border: 2rpx solid rgba(255,255,255,0.5);
  border-radius: 50rpx;
  padding: 20rpx 60rpx;
  font-size: 28rpx;
}

.menu-section {
  padding: 20rpx;
}

.menu-group {
  background: white;
  border-radius: 15rpx;
  margin-bottom: 30rpx;
  overflow: hidden;
}

.group-title {
  font-size: 24rpx;
  color: #999;
  padding: 30rpx 30rpx 10rpx;
  display: block;
}

.menu-item {
  display: flex;
  align-items: center;
  padding: 30rpx;
  border-bottom: 1rpx solid #f5f5f5;
}

.menu-item:last-child {
  border-bottom: none;
}

.menu-item.danger .menu-text {
  color: #f56c6c;
}

.menu-icon {
  font-size: 32rpx;
  margin-right: 20rpx;
  width: 40rpx;
  text-align: center;
}

.menu-text {
  flex: 1;
  font-size: 30rpx;
  color: #333;
}

.menu-arrow {
  font-size: 28rpx;
  color: #c0c4cc;
}
</style>