<template>
  <view class="container">
    <!-- 价值主张 -->
    <view class="value-proposition">
      <text class="main-title">不教你治病，教你不生病的认知</text>
      <text class="subtitle">掌握正确的健康认知，让你成为全家人的健康守护者</text>
    </view>

    <!-- 社群入口 -->
    <view class="community-section">
      <view class="community-box" @click="showJoinModal">
        <text class="community-title">💬 加入健康学习群，与巫医生和同学们一起学习交流</text>
        <view class="join-btn">立即加入学习群</view>
      </view>
    </view>

    <!-- 三层学习体系 -->
    <view class="learning-system">
      <text class="system-title">📚 三层递进学习体系</text>

      <view class="layer-card">
        <view class="layer-header">
          <view class="layer-number">1</view>
          <view class="layer-info">
            <text class="layer-title">健康常识层</text>
            <text class="layer-desc">先搞懂什么是健康</text>
          </view>
        </view>
        <view class="layer-content">
          <text class="content-item">• 健康本质理解：从"有病找医生"到"健康触手可及"的认知转变</text>
          <text class="content-item">• 身体运行规律：用大白话讲清楚身体怎么工作</text>
          <text class="content-item">• 身体在"说话"：身体不舒服时会给你信号，学会听懂</text>
          <text class="content-item">• 预防思维建立：从被动治疗转向主动预防</text>
        </view>
      </view>

      <view class="layer-card">
        <view class="layer-header">
          <view class="layer-number">2</view>
          <view class="layer-info">
            <text class="layer-title">实用工具层</text>
            <text class="layer-desc">掌握具体操作方法</text>
          </view>
        </view>
        <view class="layer-content">
          <text class="content-item">• 常见病症解析：把常见问题掰开了揉碎了讲明白</text>
          <text class="content-item">• 身体类型判断：同样的病，不同的人，调理方法完全不同</text>
          <text class="content-item">• 食疗配方库：把厨房变成你的私人药房</text>
          <text class="content-item">• 运动养生方案：不同身体状况，运动方式差别很大</text>
        </view>
      </view>

      <view class="layer-card">
        <view class="layer-header">
          <view class="layer-number">3</view>
          <view class="layer-info">
            <text class="layer-title">实践应用层</text>
            <text class="layer-desc">形成可持续健康习惯</text>
          </view>
        </view>
        <view class="layer-content">
          <text class="content-item">• 健康记录本：记录自己身体变化，越来越了解自己</text>
          <text class="content-item">• 家庭健康管理：一人学习全家受益</text>
          <text class="content-item">• 什么时候该看医生：自己能解决和必须找医生，界限要分清</text>
          <text class="content-item">• 慢性病不可怕：学会和慢性病和平共处，生活质量一样高</text>
        </view>
      </view>
    </view>

    <!-- 个人签名 -->
    <view class="signature">
      <text class="signature-text">💫 我是巫闪闪，让健康触手可及，让生命闪闪发光</text>
      <text class="signature-sub">人人都有机会健康 ✨</text>
    </view>

    <!-- 加入群弹窗 -->
    <view class="modal" v-if="showModal" @click="closeModal">
      <view class="modal-content" @click.stop>
        <view class="modal-header">
          <text class="modal-title">加入健康学习群</text>
          <text class="close-btn" @click="closeModal">×</text>
        </view>
        <view class="modal-body">
          <view class="qr-placeholder">
            <text>扫码添加助手微信</text>
            <view class="qr-code">
              <text>微信二维码</text>
              <text class="qr-tip">请截图保存后在微信中扫码</text>
            </view>
          </view>
          <view class="join-steps">
            <text class="steps-title">加群步骤：</text>
            <text class="step">1. 添加助手微信</text>
            <text class="step">2. 发送"学习群"</text>
            <text class="step">3. 等待邀请入群</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      showModal: false
    }
  },
  methods: {
    showJoinModal() {
      this.showModal = true
    },
    closeModal() {
      this.showModal = false
    }
  }
}
</script>

<style>
.container {
  background-color: #f5f5f5;
  min-height: 100vh;
}

/* 价值主张 */
.value-proposition {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  padding: 40px 20px;
  text-align: center;
}

.main-title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 15px;
  line-height: 1.4;
}

.subtitle {
  font-size: 16px;
  color: #666;
  display: block;
  line-height: 1.5;
}

/* 社群入口 */
.community-section {
  padding: 30px 20px;
}

.community-box {
  background: #f8f9fa;
  border: 2px solid #4CAF50;
  border-radius: 12px;
  padding: 25px;
  text-align: center;
}

.community-title {
  font-size: 16px;
  color: #333;
  font-weight: 600;
  display: block;
  margin-bottom: 20px;
  line-height: 1.4;
}

.join-btn {
  background: #409EFF;
  color: white;
  padding: 12px 25px;
  border-radius: 25px;
  font-size: 14px;
  font-weight: 600;
  display: inline-block;
}

/* 学习体系 */
.learning-system {
  padding: 0 20px 40px;
}

.system-title {
  font-size: 20px;
  color: #FF6B35;
  font-weight: bold;
  text-align: center;
  display: block;
  margin-bottom: 30px;
}

.layer-card {
  background: white;
  border-radius: 12px;
  margin-bottom: 20px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.layer-header {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #f8f9fa;
  border-bottom: 1px solid #eee;
}

.layer-number {
  width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #FF6B35, #F9D949);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: bold;
  margin-right: 15px;
}

.layer-info {
  flex: 1;
}

.layer-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 5px;
}

.layer-desc {
  font-size: 14px;
  color: #666;
  display: block;
}

.layer-content {
  padding: 20px;
}

.content-item {
  display: block;
  font-size: 14px;
  color: #555;
  line-height: 1.6;
  margin-bottom: 12px;
}

/* 个人签名 */
.signature {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 25px 20px;
  text-align: center;
}

.signature-text {
  font-size: 16px;
  font-weight: bold;
  display: block;
  margin-bottom: 10px;
}

.signature-sub {
  font-size: 14px;
  display: block;
  opacity: 0.9;
}

/* 弹窗样式 */
.modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  border-radius: 12px;
  margin: 20px;
  max-width: 350px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 20px 0;
}

.modal-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
}

.close-btn {
  font-size: 24px;
  color: #999;
  padding: 0 5px;
}

.modal-body {
  padding: 20px;
}

.qr-placeholder {
  text-align: center;
  margin-bottom: 20px;
}

.qr-code {
  width: 150px;
  height: 150px;
  background: #f5f5f5;
  border: 2px dashed #ddd;
  border-radius: 8px;
  margin: 15px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.qr-tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
  display: block;
}

.join-steps {
  text-align: left;
}

.steps-title {
  font-size: 16px;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 10px;
}

.step {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
  padding-left: 10px;
}
</style>