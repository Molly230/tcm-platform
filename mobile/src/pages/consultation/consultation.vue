<template>
  <view class="container">
    <view class="header">
      <text class="title">健康咨询</text>
      <text class="subtitle">请选择您需要的咨询服务类型</text>
    </view>
    
    <view class="service-options">
      <view class="service-card" @click="selectAIConsultation">
        <text class="service-title">AI智能问诊</text>
        <text class="service-desc">基于中医理论的智能问诊系统</text>
        <text class="service-price">¥9.9/次</text>
      </view>
      
      <view class="service-card" @click="selectExpertConsultation">
        <text class="service-title">专家咨询</text>
        <text class="service-desc">与资深中医师一对一交流</text>
        <text class="service-price">¥50-500/次</text>
      </view>
    </view>
    
    <view class="ai-form" v-if="showAIForm">
      <view class="form-group">
        <text class="label">主要症状</text>
        <textarea v-model="symptoms" placeholder="请描述您的主要症状" class="textarea"></textarea>
      </view>
      
      <view class="form-group">
        <text class="label">持续时间</text>
        <input v-model="duration" placeholder="症状持续多长时间了？" class="input" />
      </view>
      
      <view class="form-group">
        <text class="label">既往病史</text>
        <textarea v-model="medicalHistory" placeholder="请描述您的既往病史" class="textarea"></textarea>
      </view>
      
      <button class="primary-btn" @click="submitAIConsultation">提交问诊</button>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      showAIForm: false,
      symptoms: '',
      duration: '',
      medicalHistory: ''
    }
  },
  methods: {
    selectAIConsultation() {
      this.showAIForm = true
    },
    selectExpertConsultation() {
      // 跳转到专家咨询页面
      uni.navigateTo({
        url: '/pages/expert-consultation/expert-consultation'
      })
    },
    submitAIConsultation() {
      console.log('提交AI问诊:', {
        symptoms: this.symptoms,
        duration: this.duration,
        medicalHistory: this.medicalHistory
      })
      // 这里可以调用后端API
      uni.showToast({
        title: '问诊已提交',
        icon: 'success'
      })
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
  margin-bottom: 30px;
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

.service-options {
  margin-bottom: 30px;
}

.service-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 15px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.service-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 5px;
}

.service-desc {
  font-size: 14px;
  color: #666;
  display: block;
  margin-bottom: 10px;
}

.service-price {
  font-size: 16px;
  color: #f56c6c;
  font-weight: bold;
  display: block;
}

.form-group {
  margin-bottom: 20px;
}

.label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
  color: #333;
}

.textarea {
  width: 100%;
  height: 80px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
}

.primary-btn {
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 12px 20px;
  font-size: 16px;
  width: 100%;
}
</style>