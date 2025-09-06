<template>
  <view class="container">
    <view class="header">
      <text class="title">关于我们</text>
    </view>
    
    <view class="content">
      <text class="description">
        中医健康服务平台致力于传承和发扬中医文化，为用户提供专业的中医健康服务。
      </text>
      
      <view class="section">
        <text class="section-title">我们的使命</text>
        <text class="section-content">
          让每一位用户都能享受到专业、便捷、科学的中医健康服务，提升全民健康素养。
        </text>
      </view>
      
      <view class="section">
        <text class="section-title">我们的愿景</text>
        <text class="section-content">
          成为国内领先的中医健康服务平台，推动中医文化的现代化传播。
        </text>
      </view>
      
      <view class="section">
        <text class="section-title">核心价值观</text>
        <view class="values">
          <view class="value-item">
            <text class="value-title">专业</text>
            <text class="value-desc">汇聚资深中医专家，提供权威健康指导</text>
          </view>
          <view class="value-item">
            <text class="value-title">科学</text>
            <text class="value-desc">结合现代医学，提供科学的健康方案</text>
          </view>
          <view class="value-item">
            <text class="value-title">诚信</text>
            <text class="value-desc">以用户健康为本，提供真诚服务</text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {}
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

.description {
  font-size: 16px;
  color: #666;
  display: block;
  margin-bottom: 30px;
  line-height: 1.6;
}

.section {
  margin-bottom: 30px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
  display: block;
  margin-bottom: 10px;
}

.section-content {
  font-size: 16px;
  color: #666;
  display: block;
  line-height: 1.6;
}

.values {
  margin-top: 15px;
}

.value-item {
  background: #f5f5f5;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
}

.value-title {
  font-size: 16px;
  font-weight: bold;
  color: #409eff;
  display: block;
  margin-bottom: 5px;
}

.value-desc {
  font-size: 14px;
  color: #666;
  display: block;
  line-height: 1.5;
}
</style>