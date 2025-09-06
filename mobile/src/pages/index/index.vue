<template>
  <view class="container">
    <view class="header">
      <text class="title">中医健康服务平台</text>
      <text class="subtitle">传承中医文化，守护您的健康</text>
    </view>
    
    <view class="features">
      <view class="feature-card" @click="goToConsultation">
        <text class="feature-title">AI智能问诊</text>
        <text class="feature-desc">基于中医理论的智能问诊系统</text>
      </view>
      
      <view class="feature-card" @click="goToExperts">
        <text class="feature-title">专家咨询</text>
        <text class="feature-desc">与资深中医师一对一交流</text>
      </view>
      
      <view class="feature-card" @click="goToCourses">
        <text class="feature-title">健康课程</text>
        <text class="feature-desc">系统性中医养生课程</text>
      </view>
    </view>
    
    <view class="actions">
      <button class="primary-btn" @click="startConsultation">开始健康咨询</button>
      <button class="secondary-btn" @click="viewCourses">了解课程</button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {}
  },
  methods: {
    goToConsultation() {
      // 跳转到健康咨询页面
      uni.navigateTo({
        url: '/pages/consultation/consultation'
      })
    },
    goToExperts() {
      // 跳转到专家服务页面
      uni.navigateTo({
        url: '/pages/experts/experts'
      })
    },
    goToCourses() {
      // 跳转到课程中心页面
      uni.navigateTo({
        url: '/pages/courses/courses'
      })
    },
    startConsultation() {
      this.goToConsultation()
    },
    viewCourses() {
      this.goToCourses()
    }
  }
}
</script>

<style>
.container {
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 16px;
  color: #666;
  display: block;
}

.features {
  margin-bottom: 40px;
}

.feature-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.feature-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 5px;
}

.feature-desc {
  font-size: 14px;
  color: #666;
  display: block;
}

.actions {
  text-align: center;
}

.primary-btn {
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 12px 20px;
  font-size: 16px;
  margin-bottom: 15px;
  width: 100%;
}

.secondary-btn {
  background: #fff;
  color: #409eff;
  border: 1px solid #409eff;
  border-radius: 4px;
  padding: 12px 20px;
  font-size: 16px;
  width: 100%;
}
</style>