<template>
  <div id="home-page">
    <!-- 健康平权宣言区 -->
    <section class="values-section">
      <div class="container">
        <!-- 核心标题区域 - 独立显示 -->
        <div class="core-title-area">
          <h1 class="core-title">
            人人都有<br>机会健康
          </h1>
          <div class="title-cta-message">
            <span class="highlight-gold">是时候拿回属于你的健康主导权了</span>
          </div>
        </div>

        <!-- 其他内容区域 -->
        <div class="content-area">
          <div class="awakening-manifesto">
            <div class="manifesto-line">
              <span class="line-text">真正的健康，应该像呼吸一样简单自然</span>
            </div>
            <div class="manifesto-line delay-1">
              <span class="line-text">真正的养生，应该融入每天的柴米油盐</span>
            </div>
            <div class="manifesto-line delay-2">
              <span class="line-text">真正的智慧，应该代代相传</span>
            </div>
          </div>

          <div class="final-call-to-action">
          </div>
        </div>
      </div>
    </section>


    <!-- 第二屏：碎片化 vs 系统性对比 -->
    <section class="comparison-section">
      <div class="container">
        <!-- 认知碎片化引言 -->
        <div class="misconceptions-intro">
          <h2 class="intro-title">
            健康的最大敌人，不是疾病<br>
            <span class="highlight">是认知碎片化</span>
          </h2>
          <p class="intro-subtitle">
            收藏1000篇健康文章，依然一脸茫然<br>
            <strong>缺的不是知识，是认知体系</strong>
          </p>
        </div>
        
        <div class="comparison-grid">
          <div class="comparison-card fragmented">
            <div class="card-header">
              <span class="icon">🧩</span>
              <h3>碎片化健康学习</h3>
              <span class="status error">❌ 混乱状态</span>
            </div>
            <ul class="comparison-list">
              <li>收藏了100篇养生文章</li>
              <li>今天说要多喝水，明天说伤肾</li>
              <li>遇事就搜索，找不到统一答案</li>
              <li>越学越焦虑，无所适从</li>
              <li>症状出现才临时抱佛脚</li>
            </ul>
            <div class="result-tag">结果：信息过载，认知混乱</div>
          </div>

          <div class="comparison-card systematic">
            <div class="card-header">
              <span class="icon">🧠</span>
              <h3>系统性健康认知</h3>
              <span class="status success">✅ 清晰框架</span>
            </div>
            <ul class="comparison-list">
              <li>建立1套完整认知框架</li>
              <li>理解健康的底层逻辑</li>
              <li>遇事有原则，判断有依据</li>
              <li>越用越清晰，持续优化</li>
              <li>预测性管理，防患于未然</li>
            </ul>
            <div class="result-tag">结果：系统思维，精准管理</div>
          </div>
        </div>
      </div>
    </section>


    <!-- 第四屏：权威背书 -->
    <section class="authority-section">
      <div class="container">
        <h2 class="section-title red-title">科学的健康评测系统</h2>
        
        <div class="authority-grid">
          <div class="authority-card">
            <div class="authority-icon">🧬</div>
            <h3>现代科学支撑</h3>
            <p>结合认知科学、系统论、中医理论的跨学科方法</p>
          </div>
          <div class="authority-card">
            <div class="authority-icon">📈</div>
            <h3>数据验证有效</h3>
            <p>{{ userCount.toLocaleString() }}+ 用户实践验证，平均健康满意度提升 68%</p>
          </div>
          <div class="authority-card">
            <div class="authority-icon">👨‍⚕️</div>
            <h3>专业团队开发</h3>
            <p>中医专家 + 认知科学家 + 健康管理师联合研发</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 健康平权宣言区 -->
    <section class="health-rights-section">
      <div class="container">
        <div class="rights-content">
          <div class="core-truth">
            <div class="truth-highlight">
              <span class="truth-main red-text">个性化健康管理方案</span>
            </div>
            <div class="truth-secondary">
              每个人都有权知道真正有效的健康方法
            </div>
          </div>

          <div class="three-pillars">
            <div class="pillar-item">
              <div class="pillar-icon">🍃</div>
              <div class="pillar-title">食疗</div>
              <div class="pillar-desc">药食同源，调理脾胃</div>
            </div>
            
            <div class="pillar-item">
              <div class="pillar-icon">⚡</div>
              <div class="pillar-title">穴位</div>
              <div class="pillar-desc">经络疏通，气血调和</div>
            </div>
            
            <div class="pillar-item">
              <div class="pillar-icon">💪</div>
              <div class="pillar-title">练体</div>
              <div class="pillar-desc">动静结合，强身健体</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 平台介绍 -->
    <section class="action-section">
      <div class="container">
        <div class="action-content">
          <h2>中医健康服务平台</h2>
          <p>传承千年智慧，服务现代健康</p>
          
          <div class="platform-features">
            <div class="feature-row">
              <div class="feature-item">
                <h3>📚 系统化学习</h3>
                <p>从基础理论到实践应用，构建完整的健康知识体系</p>
              </div>
              <div class="feature-item">
                <h3>👨‍⚕️ 专业咨询</h3>
                <p>资深中医专家在线答疑，提供个性化健康指导</p>
              </div>
            </div>
            <div class="feature-row">
              <div class="feature-item">
                <h3>🔬 科学评测</h3>
                <p>结合传统诊断与现代技术，精准分析体质状况</p>
              </div>
              <div class="feature-item">
                <h3>🛒 精选商城</h3>
                <p>严选优质中药材和养生产品，品质有保障</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

// 响应式数据
const userCount = ref(156429) // 用户数量，可以从API获取

// 动态递增用户数量效果
onMounted(() => {
  const increment = () => {
    userCount.value += Math.floor(Math.random() * 5) + 1
    setTimeout(increment, Math.random() * 30000 + 10000) // 10-40秒随机增长
  }
  increment()
})

// 开始觉醒之旅功能
const startJourney = () => {
  // 跳转到咨询或测评页面
  console.log('开始健康认知觉醒之旅')
  router.push('/consultation')
}

// 开始测评功能
const startAssessment = () => {
  // 这里可以跳转到测评页面或者打开测评弹窗
  console.log('开始健康认知测评')
  // router.push('/assessment') // 如果有测评页面
  
  // 暂时跳转到咨询页面
  router.push('/consultation')
}
</script>

<style scoped>
/* 全局重置 */
#home-page {
  margin: 0;
  padding: 0;
  font-family: 'Microsoft YaHei', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  line-height: 1.6;
  color: #333;
  background: #fff;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 健康平权宣言区样式 */
.values-section {
  min-height: 100vh;
  background: url('/images/family-health.png');
  background-size: cover;
  background-position: center center;
  background-attachment: fixed;
  color: #333;
  display: flex;
  align-items: center;
  position: relative;
  padding: 100px 0;
  overflow: hidden;
}


/* 核心标题区域 - 独立居左 */
.core-title-area {
  position: absolute;
  left: 3%;
  top: 40%;
  transform: translateY(-50%);
  z-index: 2;
}

.core-title {
  font-size: 8rem;
  font-weight: 900;
  line-height: 1.2;
  color: white;
  text-shadow: 3px 3px 10px rgba(0, 0, 0, 0.8);
  letter-spacing: 2px;
  margin: 0;
}

.title-cta-message {
  text-align: right;
  margin-top: 2rem;
  padding-right: 1rem;
}

.title-cta-message .highlight-gold {
  font-size: 1.2rem;
  font-weight: 600;
  color: #ffd93d;
  text-shadow: 0 0 25px rgba(255, 217, 61, 0.5);
}

/* 其他内容区域 - 居右显示 */
.content-area {
  position: absolute;
  right: 5%;
  top: 50%;
  transform: translateY(-50%);
  width: 500px;
  background: transparent;
  backdrop-filter: blur(1px);
  border-radius: 25px;
  padding: 3rem 2.5rem;
  color: white;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.5);
  border: none;
  z-index: 1;
}

@keyframes glow {
  from {
    filter: drop-shadow(0 0 20px rgba(255, 217, 61, 0.4));
  }
  to {
    filter: drop-shadow(0 0 40px rgba(255, 107, 107, 0.6));
  }
}


/* 觉醒宣言 */
.awakening-manifesto {
  margin: 4rem 0;
  font-size: 1.1rem;
  font-weight: 400;
  line-height: 1.8;
}

.manifesto-line {
  opacity: 0;
  transform: translateX(-30px);
  animation: slideInLeft 1s ease-out forwards;
  margin: 1rem 0;
}

.manifesto-line.delay-1 {
  animation-delay: 1s;
}

.manifesto-line.delay-2 {
  animation-delay: 1.5s;
}

.line-text {
  display: inline-block;
  padding: 0.5rem 0;
  border-bottom: 2px solid rgba(255, 217, 61, 0.3);
  transition: all 0.3s ease;
}

.line-text:hover {
  border-bottom-color: #ffd93d;
  text-shadow: 0 0 10px rgba(255, 217, 61, 0.5);
}

@keyframes slideInLeft {
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

/* 核心真相 */
.core-truth {
  margin: 5rem 0;
  padding: 3rem;
  background: rgba(255, 107, 107, 0.1);
  border-radius: 25px;
  border: 2px solid rgba(255, 107, 107, 0.3);
  backdrop-filter: blur(15px);
}

.truth-highlight {
  margin-bottom: 1rem;
}

.truth-main {
  font-size: 2.4rem;
  font-weight: 800;
  color: #ff6b6b;
  text-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
  line-height: 1.3;
}

.truth-secondary {
  font-size: 1.4rem;
  color: rgba(255,255,255,0.8);
  font-weight: 300;
}

/* 三大支柱 */
.three-pillars {
  display: flex;
  justify-content: space-between;
  gap: 2rem;
  margin: 5rem 0;
}

.pillar-item {
  flex: 1;
  background: white;
  border-radius: 25px;
  padding: 3rem 1.5rem;
  border: 2px solid #e9ecef;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.pillar-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  transition: left 0.5s ease;
}

.pillar-item:hover {
  transform: translateY(-15px);
  border-color: #ffd93d;
  background: #fff;
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

.pillar-item:hover::before {
  left: 100%;
}

.pillar-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  filter: drop-shadow(0 0 10px rgba(255, 217, 61, 0.3));
}

.pillar-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #ffd93d;
  margin-bottom: 1rem;
  text-shadow: 0 0 15px rgba(255, 217, 61, 0.3);
}

.pillar-desc {
  font-size: 1.1rem;
  color: #636e72;
  font-weight: 300;
}

/* 最终行动召唤 */
.final-call-to-action {
  margin-top: 5rem;
}

.call-message {
  font-size: 1.2rem;
  margin-bottom: 2.5rem;
  font-weight: 600;
}

.highlight-gold {
  color: #ffd93d;
  text-shadow: 0 0 25px rgba(255, 217, 61, 0.5);
  font-weight: 800;
}

.awakening-cta-button {
  background: linear-gradient(135deg, #ff6b6b, #ee5a24, #ffd93d);
  background-size: 200% 200%;
  color: white;
  border: none;
  padding: 25px 60px;
  font-size: 1.6rem;
  font-weight: 800;
  border-radius: 60px;
  cursor: pointer;
  transition: all 0.4s ease;
  box-shadow: 
    0 15px 40px rgba(255, 107, 107, 0.4),
    0 0 30px rgba(255, 217, 61, 0.2);
  letter-spacing: 1px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
  margin-bottom: 2rem;
  animation: gradientShift 3s ease infinite;
  position: relative;
  overflow: hidden;
}

@keyframes gradientShift {
  0%, 100% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
}

.awakening-cta-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.5s ease;
}

.awakening-cta-button:hover {
  transform: translateY(-6px) scale(1.05);
  box-shadow: 
    0 25px 60px rgba(255, 107, 107, 0.6),
    0 0 50px rgba(255, 217, 61, 0.4);
  filter: brightness(1.1);
}

.awakening-cta-button:hover::before {
  left: 100%;
}

.social-proof {
  font-size: 1.1rem;
  opacity: 0.8;
  font-weight: 300;
}

.user-count {
  color: #ffd93d;
  font-weight: 700;
  font-size: 1.2em;
  text-shadow: 0 0 10px rgba(255, 217, 61, 0.3);
}

/* 第一屏：认知冲击 */
.hero-section {
  min-height: 100vh;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: white;
  display: flex;
  align-items: center;
  position: relative;
}

.hero-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
  opacity: 0.3;
}

.hero-content {
  position: relative;
  z-index: 1;
  text-align: center;
  max-width: 900px;
  margin: 0 auto;
}

.hero-title {
  font-size: 4rem;
  font-weight: 800;
  line-height: 1.1;
  margin-bottom: 2.5rem;
  text-shadow: 3px 3px 6px rgba(0,0,0,0.4);
  letter-spacing: -1px;
}

.hero-title .highlight {
  color: #ff6b6b;
  text-shadow: 0 0 30px rgba(255, 107, 107, 0.8);
  font-size: 1.1em;
  font-weight: 900;
}

.hero-subtitle {
  font-size: 1.6rem;
  margin-bottom: 3.5rem;
  opacity: 0.95;
  line-height: 1.5;
  font-weight: 300;
}

.hero-subtitle strong {
  color: #ffd93d;
  font-weight: 700;
  font-size: 1.1em;
  text-shadow: 0 0 15px rgba(255, 217, 61, 0.3);
}


.cta-button {
  background: linear-gradient(135deg, #ff6b6b, #ee5a24);
  color: white;
  border: none;
  padding: 22px 45px;
  font-size: 1.4rem;
  font-weight: 700;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 10px 30px rgba(255, 107, 107, 0.4);
  margin-bottom: 2.5rem;
  letter-spacing: 0.5px;
  text-shadow: 1px 1px 2px rgba(0,0,0,0.2);
}

.cta-button:hover {
  transform: translateY(-4px);
  box-shadow: 0 15px 40px rgba(255, 107, 107, 0.5);
  filter: brightness(1.05);
}

.cta-button.large {
  padding: 25px 50px;
  font-size: 1.5rem;
}

.cta-description {
  font-size: 1.1rem;
  opacity: 0.85;
  font-weight: 300;
}

.user-count {
  color: #ffd93d;
  font-weight: 700;
  font-size: 1.05em;
  text-shadow: 0 0 10px rgba(255, 217, 61, 0.2);
}

/* 第二屏：对比区 */
.comparison-section {
  padding: 100px 0;
  background: #f8f9fa;
}

.section-title {
  text-align: center;
  font-size: 2.8rem;
  font-weight: 700;
  color: #2d3436;
  margin-bottom: 1rem;
}

.section-title.red-title {
  color: #ff6b6b;
}

.truth-main.red-text {
  color: #ff6b6b !important;
}

.section-subtitle {
  text-align: center;
  font-size: 1.2rem;
  color: #636e72;
  margin-bottom: 4rem;
}

/* 健康误区引言 */
.misconceptions-intro {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  border-radius: 15px;
  color: white;
  margin-bottom: 40px;
  position: relative;
  overflow: hidden;
}

.misconceptions-intro::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
  opacity: 0.3;
}

.intro-title {
  position: relative;
  z-index: 1;
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 2rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.intro-title .highlight {
  color: #ff6b6b;
  text-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
  font-weight: 900;
}

.intro-subtitle {
  position: relative;
  z-index: 1;
  font-size: 1.3rem;
  opacity: 0.95;
  line-height: 1.5;
  margin: 0;
  font-weight: 300;
}

.intro-subtitle strong {
  color: #ffd93d;
  font-weight: 700;
  font-size: 1.1em;
  text-shadow: 0 0 15px rgba(255, 217, 61, 0.3);
}

.comparison-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 3rem;
  max-width: 1000px;
  margin: 0 auto;
}

.comparison-card {
  background: white;
  border-radius: 20px;
  padding: 2.5rem;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
  position: relative;
  overflow: hidden;
}

.comparison-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
}

.comparison-card.fragmented::before {
  background: linear-gradient(135deg, #ff7675, #fd79a8);
}

.comparison-card.systematic::before {
  background: linear-gradient(135deg, #00b894, #00cec9);
}

.comparison-card:hover {
  transform: translateY(-5px);
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
}

.card-header .icon {
  font-size: 2rem;
}

.card-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3436;
  margin: 0;
  flex: 1;
  margin-left: 1rem;
}

.status {
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status.error {
  background: #ffe0e0;
  color: #d63031;
}

.status.success {
  background: #e0f7f0;
  color: #00b894;
}

.comparison-list {
  list-style: none;
  padding: 0;
  margin-bottom: 2rem;
}

.comparison-list li {
  padding: 0.8rem 0;
  border-bottom: 1px solid #f1f2f6;
  color: #636e72;
  position: relative;
  padding-left: 2rem;
}

.comparison-list li::before {
  content: '•';
  position: absolute;
  left: 0;
  color: #ddd;
  font-size: 1.5rem;
}

.fragmented .comparison-list li::before {
  color: #ff7675;
}

.systematic .comparison-list li::before {
  color: #00b894;
}

.result-tag {
  background: linear-gradient(135deg, #ddd, #bbb);
  color: white;
  padding: 0.8rem 1.5rem;
  border-radius: 25px;
  text-align: center;
  font-weight: 600;
  font-size: 0.9rem;
}

.fragmented .result-tag {
  background: linear-gradient(135deg, #ff7675, #fd79a8);
}

.systematic .result-tag {
  background: linear-gradient(135deg, #00b894, #00cec9);
}

/* 第三屏：框架展示 */
.framework-section {
  padding: 100px 0;
  background: white;
}

.framework-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 3rem;
}

.framework-card {
  text-align: center;
  padding: 2.5rem;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 20px;
  transition: transform 0.3s ease;
}

.framework-card:hover {
  transform: translateY(-10px);
}

.framework-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
}

.framework-card h3 {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 1rem;
}

.framework-card p {
  opacity: 0.9;
  line-height: 1.6;
}

/* 第四屏：权威背书 */
.authority-section {
  padding: 100px 0;
  background: #f8f9fa;
}

.authority-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
  margin-top: 3rem;
}

.authority-card {
  background: white;
  padding: 2.5rem;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
  transition: transform 0.3s ease;
}

.authority-card:hover {
  transform: translateY(-5px);
}

.authority-icon {
  font-size: 3rem;
  margin-bottom: 1.5rem;
}

.authority-card h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2d3436;
  margin-bottom: 1rem;
}

.authority-card p {
  color: #636e72;
  line-height: 1.6;
}

/* 健康平权宣言区 */
.health-rights-section {
  padding: 100px 0;
  background: white;
  color: #333;
}

.rights-content {
  text-align: center;
  max-width: 1200px;
  margin: 0 auto;
}

.core-truth {
  margin-bottom: 5rem;
  padding: 3rem;
  background: #f8f9fa;
  border-radius: 25px;
  border: 2px solid #e9ecef;
}

.truth-highlight {
  margin-bottom: 1rem;
}

.truth-main {
  font-size: 2.4rem;
  font-weight: 800;
  color: #ffd93d;
  text-shadow: 0 0 20px rgba(255, 217, 61, 0.5);
  line-height: 1.3;
}

.truth-secondary {
  font-size: 1.4rem;
  color: #636e72;
  font-weight: 300;
  line-height: 1.5;
}

.three-pillars {
  display: flex;
  justify-content: space-between;
  gap: 2rem;
  margin: 0;
}

.pillar-item {
  flex: 1;
  background: white;
  border-radius: 25px;
  padding: 3rem 1.5rem;
  border: 2px solid #e9ecef;
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.pillar-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
  transition: left 0.5s ease;
}

.pillar-item:hover {
  transform: translateY(-15px);
  border-color: #ffd93d;
  background: #fff;
  box-shadow: 0 20px 40px rgba(0,0,0,0.15);
}

.pillar-item:hover::before {
  left: 100%;
}

.pillar-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  filter: drop-shadow(0 0 10px rgba(255, 217, 61, 0.3));
}

.pillar-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: #ffd93d;
  margin-bottom: 1rem;
  text-shadow: 0 0 15px rgba(255, 217, 61, 0.3);
}

.pillar-desc {
  font-size: 1.1rem;
  color: #636e72;
  font-weight: 300;
}

/* 第五屏：行动入口 */
.action-section {
  padding: 100px 0;
  background: #f8f9fa;
  color: #333;
  text-align: center;
}

.action-content h2 {
  font-size: 2.5rem;
  font-weight: 700;
  margin-bottom: 1rem;
}

.action-content p {
  font-size: 1.2rem;
  opacity: 0.9;
  margin-bottom: 3rem;
}

.platform-features {
  margin-top: 3rem;
  max-width: 900px;
  margin-left: auto;
  margin-right: auto;
}

.feature-row {
  display: flex;
  gap: 3rem;
  margin-bottom: 2.5rem;
}

.feature-row .feature-item {
  flex: 1;
  text-align: left;
  padding: 2rem;
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
  border: 2px solid #e9ecef;
  transition: transform 0.3s ease;
}

.feature-row .feature-item:hover {
  transform: translateY(-5px);
  border-color: #ff6b6b;
}

.feature-row .feature-item h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2d3436;
  margin-bottom: 1rem;
}

.feature-row .feature-item p {
  font-size: 1rem;
  color: #636e72;
  line-height: 1.6;
  margin: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  /* 健康平权宣言区响应式 */
  .values-section {
    padding: 60px 0;
    background-attachment: scroll;
  }
  
  /* 移动端重新布局为垂直排列 */
  .core-title-area {
    position: relative;
    left: auto;
    top: auto;
    transform: none;
    text-align: center;
    margin-bottom: 3rem;
  }
  
  .core-title {
    font-size: 4rem;
    line-height: 1.1;
    letter-spacing: 1px;
  }
  
  .title-cta-message {
    text-align: center;
    margin-top: 1.5rem;
    padding-right: 0;
  }
  
  .title-cta-message .highlight-gold {
    font-size: 1rem;
  }
  
  .content-area {
    position: relative;
    right: auto;
    top: auto;
    transform: none;
    width: auto;
    margin: 0 1rem;
    padding: 2.5rem 2rem;
  }
  
  
  .awakening-manifesto {
    margin: 3rem 0;
    font-size: 1rem;
    line-height: 1.6;
  }
  
  .core-truth {
    margin: 3rem 0;
    padding: 2rem;
  }
  
  .truth-main {
    font-size: 1.8rem;
    line-height: 1.4;
  }
  
  .truth-secondary {
    font-size: 1.2rem;
  }
  
  .three-pillars {
    flex-direction: column;
    gap: 2rem;
    margin: 3rem 0;
  }
  
  .pillar-item {
    padding: 2.5rem 2rem;
  }
  
  .pillar-icon {
    font-size: 3rem;
    margin-bottom: 1rem;
  }
  
  .pillar-title {
    font-size: 1.5rem;
  }
  
  .pillar-desc {
    font-size: 1rem;
  }
  
  .call-message {
    font-size: 1.1rem;
    margin-bottom: 2rem;
  }
  
  .awakening-cta-button {
    padding: 20px 40px;
    font-size: 1.3rem;
    border-radius: 50px;
  }
  
  .social-proof {
    font-size: 1rem;
  }

  /* 原有内容响应式 */
  .hero-title {
    font-size: 2.8rem;
    line-height: 1.2;
    margin-bottom: 2rem;
  }
  
  .hero-title .highlight {
    font-size: 1.05em;
  }
  
  .hero-subtitle {
    font-size: 1.3rem;
    margin-bottom: 3rem;
    line-height: 1.4;
  }
  
  .hero-subtitle strong {
    font-size: 1.08em;
  }
  
  .cta-button {
    padding: 18px 35px;
    font-size: 1.2rem;
  }
  
  .comparison-grid,
  .framework-grid,
  .authority-grid {
    grid-template-columns: 1fr;
    gap: 2rem;
  }
  
  .section-title {
    font-size: 2.2rem;
  }
  
  .platform-features {
    margin-top: 2rem;
  }
  
  .feature-row {
    flex-direction: column;
    gap: 1.5rem;
    margin-bottom: 1.5rem;
  }
  
  .feature-row .feature-item {
    padding: 1.5rem;
  }
  
  .feature-row .feature-item h3 {
    font-size: 1.2rem;
  }
  
  .feature-row .feature-item p {
    font-size: 0.95rem;
  }
}
</style>