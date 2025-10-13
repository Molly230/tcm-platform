<template>
  <view class="container">
    <!-- 品牌展示区 -->
    <view class="hero-section">
      <view class="brand-content">
        <text class="brand-title">巫闪闪</text>
        <text class="brand-subtitle">健康认知导师</text>
        <view class="brand-intro">
          <text class="intro-text">8年临床培训经验，培训2850+医生</text>
          <text class="intro-text">现在，用同样的方法帮助大众成为健康的主人</text>
        </view>

        <view class="hero-stats">
          <view class="stat-item">
            <text class="stat-number">2850+</text>
            <text class="stat-label">培训医生</text>
          </view>
          <view class="stat-item">
            <text class="stat-number">8年</text>
            <text class="stat-label">临床培训经验</text>
          </view>
          <view class="stat-item">
            <text class="stat-number">96.8%</text>
            <text class="stat-label">学员成功率</text>
          </view>
        </view>
      </view>
    </view>

    <!-- 核心理念 -->
    <view class="core-philosophy">
      <view class="section-header">
        <text class="section-tag">Core Philosophy</text>
        <text class="section-title">核心理念</text>
        <text class="section-desc">认知决定健康，让每个人成为健康管理专家</text>
      </view>

      <view class="insight-card">
        <text class="insight-icon">💡</text>
        <text class="insight-title">我发现的真相</text>
        <text class="insight-content">培训了2850多名医生后，我意识到：医生再牛，也只能救治已经生病的人。而真正的健康，应该是让人不生病。</text>
      </view>

      <view class="insight-card">
        <text class="insight-icon">🔬</text>
        <text class="insight-title">巫闪闪独创学习方法论</text>
        <text class="insight-content">用培训医生的专业体系，让普通人掌握健康管理技能</text>
      </view>
    </view>

    <!-- 学习方法4步骤 -->
    <view class="method-steps">
      <text class="steps-title">4步掌握健康管理技能</text>
      <view class="steps-grid">
        <view class="method-step">
          <view class="step-number">1</view>
          <text class="step-title">医生思维导入</text>
          <text class="step-desc">用医生的诊断思维，教你看懂身体信号</text>
        </view>
        <view class="method-step">
          <view class="step-number">2</view>
          <text class="step-title">案例驱动学习</text>
          <text class="step-desc">真实医疗案例教学，深度理解健康原理</text>
        </view>
        <view class="method-step">
          <view class="step-number">3</view>
          <text class="step-title">工具化应用</text>
          <text class="step-desc">把复杂理论转化为简单实用的操作工具</text>
        </view>
        <view class="method-step">
          <view class="step-number">4</view>
          <text class="step-title">个性化指导</text>
          <text class="step-desc">根据个人体质，制定专属健康管理方案</text>
        </view>
      </view>
    </view>

    <!-- 热门健康认知内容 -->
    <view class="featured-content">
      <text class="content-title">🔥 爆款健康认知</text>

      <view class="featured-article main-article" @click="handleArticleClick('health-essence')">
        <view class="article-badge trending">🔥 爆款认知</view>
        <text class="article-title">健康的本质是什么？99%的人想错了</text>
        <text class="article-desc">大多数人认为健康就是没有疾病，这是最大的认知误区...</text>
        <view class="article-meta">
          <text class="read-count">🔥 10万+阅读</text>
          <text class="category">底层认知</text>
        </view>
      </view>

      <view class="content-list">
        <view class="article-item" @click="handleArticleClick('thinking-wrong')">
          <view class="article-badge mindset">💡 认知颠覆</view>
          <text class="item-title">你对健康的理解，可能从根上就错了</text>
          <text class="read-count">8.5万阅读</text>
        </view>

        <view class="article-item" @click="handleArticleClick('doctor-vs-health')">
          <view class="article-badge insight">🎯 核心洞察</view>
          <text class="item-title">医生治病，你管健康，分工要明确</text>
          <text class="read-count">7.2万阅读</text>
        </view>

        <view class="article-item" @click="handleArticleClick('body-system')">
          <view class="article-badge framework">🧠 思维框架</view>
          <text class="item-title">学会这套思维，你就是自己的健康管家</text>
          <text class="read-count">6.8万阅读</text>
        </view>
      </view>

      <view class="more-content-btn" @click="goToHealthInsights">
        <text>📚 探索更多健康认知内容</text>
      </view>
    </view>

    <!-- 学员反馈 -->
    <view class="testimonials">
      <text class="testimonial-title">学员真实反馈</text>

      <view class="testimonial-card">
        <text class="testimonial-text">"跟着巫老师学习了3个月，终于理解了什么叫'认知决定健康'。现在我不再盲目养生，而是有针对性地调理，失眠问题彻底改善了。"</text>
        <view class="testimonial-author">
          <text class="author-name">李女士</text>
          <text class="author-role">健康认知课程学员</text>
        </view>
      </view>

      <view class="testimonial-card">
        <text class="testimonial-text">"巫老师用培训医生的方式教我们，让我从一个养生小白变成了家庭健康顾问。现在全家人的健康都由我来管理。"</text>
        <view class="testimonial-author">
          <text class="author-name">张先生</text>
          <text class="author-role">体质调理学员</text>
        </view>
      </view>
    </view>

    <!-- 行动召唤 -->
    <view class="cta-section">
      <text class="cta-title">开始你的健康认知之旅</text>
      <text class="cta-subtitle">让我用培训医生的方法，教会你管理健康</text>
      <text class="value-text">从被动治病到主动健康，从此你就是自己的健康专家</text>

      <view class="cta-buttons">
        <view class="primary-btn" @click="goToAssessment">
          <text class="btn-icon">🌟</text>
          <text>免费评估你的体质</text>
        </view>
        <view class="community-btn" @click="showJoinModal">
          <text class="btn-icon">👥</text>
          <text>加入健康学习群</text>
        </view>
      </view>

      <view class="community-benefits">
        <view class="benefit-item">
          <text class="benefit-icon">📚</text>
          <text>每日健康认知分享</text>
        </view>
        <view class="benefit-item">
          <text class="benefit-icon">🩺</text>
          <text>巫闪闪亲自答疑</text>
        </view>
        <view class="benefit-item">
          <text class="benefit-icon">👨‍👩‍👧‍👦</text>
          <text>学员案例交流</text>
        </view>
      </view>

      <text class="urgency-text">⏰ 限时免费：价值399元的专业体质评估</text>
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
    handleArticleClick(articleId) {
      console.log('点击文章:', articleId)
      // 可以跳转到问答页面
      uni.navigateTo({
        url: '/pages/health-insights/health-insights'
      })
    },
    goToHealthInsights() {
      // 跳转到健康认知内容页面（可以是问答页面）
      uni.switchTab({
        url: '/pages/consultation/consultation'
      })
    },
    goToAssessment() {
      uni.navigateTo({
        url: '/pages/assessment/assessment'
      })
    },
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
  background-color: #f5f7fa;
  min-height: 100vh;
}

/* 品牌展示区 */
.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 60px 20px 40px;
  text-align: center;
}

.brand-content {
  max-width: 600px;
  margin: 0 auto;
}

.brand-title {
  font-size: 48px;
  font-weight: bold;
  display: block;
  margin-bottom: 15px;
  color: white;
}

.brand-subtitle {
  font-size: 20px;
  display: block;
  margin-bottom: 30px;
  color: #ffd700;
  font-weight: 600;
}

.brand-intro {
  margin-bottom: 40px;
}

.intro-text {
  display: block;
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 8px;
  opacity: 0.9;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 30px;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
  flex: 1;
  min-width: 80px;
}

.stat-number {
  font-size: 32px;
  font-weight: bold;
  color: #ffd700;
  display: block;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 12px;
  opacity: 0.9;
  display: block;
}

/* 核心理念区域 */
.core-philosophy {
  padding: 50px 20px;
  background: white;
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
}

.section-tag {
  display: inline-block;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 12px;
  font-weight: bold;
  text-transform: uppercase;
  margin-bottom: 15px;
}

.section-title {
  font-size: 28px;
  color: #2d3748;
  font-weight: bold;
  display: block;
  margin-bottom: 15px;
}

.section-desc {
  font-size: 16px;
  color: #64748b;
  line-height: 1.6;
  display: block;
}

.insight-card {
  background: #f8f9fa;
  border-radius: 16px;
  padding: 30px 20px;
  margin-bottom: 20px;
  text-align: center;
}

.insight-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 15px;
}

.insight-title {
  font-size: 18px;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 15px;
}

.insight-content {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
  display: block;
}

/* 方法步骤 */
.method-steps {
  padding: 50px 20px;
  background: #f8f9fa;
}

.steps-title {
  font-size: 24px;
  font-weight: bold;
  color: #FF6B35;
  text-align: center;
  display: block;
  margin-bottom: 30px;
}

.steps-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
}

.method-step {
  flex: 1;
  min-width: 150px;
  background: white;
  border-radius: 12px;
  padding: 25px 15px;
  text-align: center;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.step-number {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  font-size: 18px;
  margin: 0 auto 15px;
}

.step-title {
  font-size: 16px;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin-bottom: 10px;
}

.step-desc {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.5;
  display: block;
}

/* 热门内容区域 */
.featured-content {
  padding: 50px 20px;
  background: white;
}

.content-title {
  font-size: 24px;
  font-weight: bold;
  color: #2d3748;
  text-align: center;
  display: block;
  margin-bottom: 30px;
}

.main-article {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 16px;
  padding: 25px 20px;
  margin-bottom: 25px;
}

.article-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: bold;
  margin-bottom: 12px;
}

.article-badge.trending {
  background: linear-gradient(45deg, #ff6b6b, #ee5a24);
  color: white;
}

.article-badge.mindset {
  background: linear-gradient(45deg, #feca57, #ff9ff3);
  color: #2d3748;
}

.article-badge.insight {
  background: linear-gradient(45deg, #48dbfb, #0abde3);
  color: white;
}

.article-badge.framework {
  background: linear-gradient(45deg, #1dd1a1, #55a3ff);
  color: white;
}

.article-title {
  font-size: 18px;
  font-weight: bold;
  display: block;
  margin-bottom: 12px;
  line-height: 1.4;
}

.article-desc {
  font-size: 14px;
  opacity: 0.9;
  display: block;
  margin-bottom: 15px;
  line-height: 1.5;
}

.article-meta {
  display: flex;
  align-items: center;
  gap: 15px;
}

.read-count {
  font-size: 12px;
  font-weight: 500;
}

.category {
  background: rgba(255,255,255,0.2);
  padding: 4px 10px;
  border-radius: 8px;
  font-size: 11px;
}

.content-list {
  margin-bottom: 30px;
}

.article-item {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px 15px;
  margin-bottom: 15px;
}

.item-title {
  font-size: 16px;
  font-weight: bold;
  color: #2d3748;
  display: block;
  margin: 10px 0;
  line-height: 1.4;
}

.more-content-btn {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 15px 25px;
  border-radius: 25px;
  text-align: center;
  font-size: 16px;
  font-weight: 600;
}

/* 学员反馈 */
.testimonials {
  padding: 50px 20px;
  background: #f8f9fa;
}

.testimonial-title {
  font-size: 24px;
  font-weight: bold;
  color: #2d3748;
  text-align: center;
  display: block;
  margin-bottom: 30px;
}

.testimonial-card {
  background: white;
  border-radius: 16px;
  padding: 25px 20px;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.testimonial-text {
  font-size: 14px;
  color: #4a5568;
  line-height: 1.6;
  display: block;
  margin-bottom: 15px;
  font-style: italic;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 10px;
}

.author-name {
  font-size: 16px;
  font-weight: bold;
  color: #2d3748;
}

.author-role {
  font-size: 12px;
  color: #718096;
}

/* 行动召唤 */
.cta-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 50px 20px;
  text-align: center;
}

.cta-title {
  font-size: 28px;
  font-weight: bold;
  display: block;
  margin-bottom: 15px;
}

.cta-subtitle {
  font-size: 18px;
  display: block;
  margin-bottom: 20px;
  opacity: 0.95;
}

.value-text {
  font-size: 16px;
  color: #ffd700;
  font-weight: bold;
  display: block;
  margin-bottom: 30px;
}

.cta-buttons {
  margin-bottom: 30px;
}

.primary-btn, .community-btn {
  background: #ffd700;
  color: #2d3748;
  padding: 15px 25px;
  border-radius: 25px;
  margin-bottom: 15px;
  font-weight: 600;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.community-btn {
  background: #26de81;
  color: white;
}

.btn-icon {
  font-size: 18px;
}

.community-benefits {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.benefit-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 15px;
  background: rgba(255,255,255,0.15);
  border-radius: 15px;
}

.benefit-icon {
  font-size: 14px;
}

.urgency-text {
  font-size: 14px;
  color: #ffd700;
  font-weight: bold;
  display: block;
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

.step {
  display: block;
  font-size: 14px;
  color: #666;
  margin-bottom: 8px;
  padding-left: 10px;
}
</style>