<template>
  <div class="home-view">
    <!-- 主要品牌展示区 -->
    <div class="hero-section">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="brand-opening">
          <h1 class="brand-title">让中医智慧<br/>融入日常生活</h1>
          <p class="brand-subtitle">探索中医治未病的智慧</p>
          <div class="brand-intro">
            <p class="intro-text">
              通过饮食调理、经络锻炼、情志调节<br/>
              了解自身体质，预防疾病，享受健康生活
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="content-wrapper">
      <!-- 健康认知内容体系 -->
      <section class="content-preview">
        <div class="section-header">
          <span class="section-tag">one</span>
          <h2>核心内容</h2>
          <p class="section-desc">了解健康底层逻辑</p>
        </div>

        <!-- 热门内容精选 -->
        <div class="content-grid">
            <div class="featured-article" @click="handleArticleClick('thinking-wrong')">
              <div class="article-badge mindset">💡 认知颠覆</div>
              <h4>你对健康的理解，可能从根上就错了</h4>
              <p>测一测，你是否了解健康？ <span class="arrow-indicator">→</span></p>
            </div>


            <div class="featured-article" @click="handleArticleClick('body-system')">
              <div class="article-badge framework">🧠 思维框架</div>
              <h4>学会这套思维，你就是自己的健康管家</h4>
              <p>如何像中医一样思考健康问题？</p>
            </div>

            <div class="featured-article" @click="handleArticleClick('constitution-logic')">
              <div class="article-badge method">⚡ 体质测评</div>
              <h4>体质决定一切，但体质到底是什么？</h4>
              <p>找到属于你的独特的体质</p>
           </div>

            <div class="featured-article" @click="handleArticleClick('doctor-vs-health')">
              <div class="article-badge insight">🎯 解决方案</div>
              <h4>医生治病，你管健康，分工要明确</h4>
              <p>健康的解决方案腰自己管理</p>
            </div>

            <div class="featured-article" @click="handleArticleClick('health-misconceptions')">
              <div class="article-badge warning">⚠️ 避坑指南</div>
              <h4>为什么越养生越不健康？思维错了</h4>
              <p>停止这些错误的养生方式</p>
            </div>

            <div class="featured-article" @click="handleArticleClick('harmony-body')">
              <div class="article-badge wisdom">🌟 健康智慧</div>
              <h4>健康的最高境界：把中医融入生活</h4>
              <p>把生活过成诗，让健康变简单</p>
            </div>
        </div>
      </section>

      <!-- 客户见证（精选） -->
      <section class="testimonial-preview">
        <div class="section-header">
          <span class="section-tag">Success Stories</span>
          <h2>会员反馈</h2>
          <p class="section-desc">来自真实用户的改变见证</p>
        </div>
        <div class="testimonial-cards">
          <div class="testimonial-card">
            <div class="testimonial-content">
              <p>"现在我不再盲目养生，而是有针对性地调理，失眠问题彻底改善了。"</p>
            </div>
            <div class="testimonial-author">
              <div class="author-info">
                <h4>李女士</h4>
                <span>健康认知课程学员</span>
              </div>
            </div>
          </div>
          <div class="testimonial-card">
            <div class="testimonial-content">
              <p>"这里让我从一个养生小白变成了家庭健康顾问。现在全家人的健康都由我来管理。"</p>
            </div>
            <div class="testimonial-author">
              <div class="author-info">
                <h4>张先生</h4>
                <span>体质调理学员</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 行动召唤 -->
      <section class="cta-section">
        <div class="cta-content">
          <div class="cta-grid">
            <div class="cta-item">
              <el-button type="primary" size="large" class="primary-cta" @click="$router.push('/insomnia-assessment')">
                <span class="button-icon">🌟</span>
                评估你的体质
              </el-button>
            </div>

            <div class="cta-item">
              <el-button type="success" size="large" class="community-cta" @click="joinHealthCommunity">
                <span class="button-icon">💎</span>
                成为会员
              </el-button>

              <!-- 会员价值说明 -->
              <div class="community-value">
                <div class="benefit-compact">
                  <div>📚 健康认知分享</div>
                  <div>🩺 专业老师答疑</div>
                  <div>🎯 个性化调理指导</div>
                  <div>👨‍👩‍👧‍👦 会员案例交流</div>
                  <div>已有<strong>2850+</strong>会员在群内受益，每天限量50人</div>
                  <div>⏰ 限时免费：价值399元的专业体质评估</div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 网站Footer -->
    <footer class="site-footer">
      <div class="container-footer">
        <div class="footer-content">
          <div class="footer-section">
            <h3>中医健康平台</h3>
            <div class="footer-links">
              <a href="/courses">在线课程</a>
              <a href="/products">健康产品</a>
              <a href="/assessment">体质测评</a>
            </div>
          </div>

          <div class="footer-section">
            <h3>客户服务</h3>
            <div class="footer-links">
              <a href="#">常见问题</a>
              <a href="#">联系我们</a>
              <a href="#">配送政策</a>
              <a href="#">退换货政策</a>
            </div>
          </div>

          <div class="footer-section">
            <h3>法律条款</h3>
            <div class="footer-links">
              <a href="#">服务条款</a>
              <a href="#">隐私政策</a>
              <a href="#">免责声明</a>
              <a href="#">医疗声明</a>
            </div>
          </div>

          <div class="footer-section newsletter">
            <h3>订阅健康资讯</h3>
            <p>获取最新的中医健康知识和优惠信息</p>
            <div class="newsletter-form">
              <el-input
                placeholder="请输入您的邮箱"
                v-model="email"
                class="newsletter-input"
              ></el-input>
              <el-button type="primary" class="newsletter-btn">
                订阅
              </el-button>
            </div>
          </div>
        </div>

        <div class="footer-bottom">
          <div class="copyright">
            <p>© 2025 中医健康平台 版权所有</p>
          </div>
          <div class="social-links">
            <span>关注我们：</span>
            <a href="#" class="social-link">微信</a>
            <a href="#" class="social-link">微博</a>
            <a href="#" class="social-link">抖音</a>
          </div>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const email = ref('')

// 页面交互逻辑
const handleArticleClick = (articleId: string) => {
  // 认知颠覆卡片跳转到健康认知测评
  if (articleId === 'thinking-wrong') {
    router.push('/health-cognition-assessment')
    return
  }
  // 避坑指南卡片跳转到避坑指南页面
  if (articleId === 'health-misconceptions') {
    router.push('/health-misconceptions')
    return
  }
  // 其他文章暂时只打印日志
  console.log('点击文章:', articleId)
  // 后续可以路由到具体文章页面
}

const filterContent = (category: string) => {
  // 内容筛选逻辑
  console.log('筛选内容:', category)
  // 后续可以实现筛选功能
}

const joinHealthCommunity = () => {
  // 弹出会员加入指引
  ElMessageBox.alert(
    `
    <div style="text-align: center; padding: 20px;">
      <h3 style="color: #2d3748; margin-bottom: 15px;">💎 欢迎成为会员</h3>
      <p style="margin-bottom: 20px; line-height: 1.6; color: #4a5568;">
        添加客服微信，回复「<strong style="color: #667eea;">成为会员</strong>」即可获取会员权益
      </p>
      <div style="background: #f7fafc; padding: 15px; border-radius: 12px; margin: 20px 0;">
        <p style="font-weight: 600; color: #2d3748; margin-bottom: 10px;">客服微信：请联系官方客服</p>
        <p style="font-size: 14px; color: #718096;">备注：来自官网-会员申请</p>
      </div>
      <div style="font-size: 14px; color: #e53e3e; line-height: 1.5;">
        ⚡ 每天仅限50个新会员加入<br/>
        📱 建议截图保存微信号
      </div>
    </div>
    `,
    '成为会员',
    {
      dangerouslyUseHTMLString: true,
      confirmButtonText: '我已添加微信',
      confirmButtonClass: 'community-confirm-btn',
      showCancelButton: true,
      cancelButtonText: '稍后添加',
      customClass: 'community-dialog'
    }
  )
}
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

/* 主要内容区域的层次感 */
.content-wrapper {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
}

/* 各个section增加更好的间距和层次 */
.content-wrapper > section {
  margin-bottom: 120px;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 24px;
  padding: 80px 60px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.08);
  backdrop-filter: blur(10px);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.content-wrapper > section:hover {
  transform: translateY(-8px);
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.12);
}

/* Hero区域样式 */
.hero-section {
  position: relative;
  background-image: url('/images/family-health.png');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  color: white;
  padding: 120px 0 80px;
  text-align: left;
  overflow: hidden;
  min-height: 600px;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.35) 0%, rgba(118, 75, 162, 0.35) 100%);
  opacity: 1;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 60px;
}

.brand-opening {
  text-align: left;
  max-width: 700px;
  margin: 0;
}

.brand-title {
  font-size: 4rem;
  font-weight: 800;
  margin-bottom: 20px;
  letter-spacing: 1px;
  animation: fadeInUp 1s ease-out;
  line-height: 1.4;
  display: inline;
  background: rgba(102, 126, 234, 0.85);
  padding: 8px 20px;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.brand-subtitle {
  font-size: 1.8rem;
  margin-top: 30px;
  margin-bottom: 40px;
  font-weight: 300;
  letter-spacing: 2px;
  animation: fadeInUp 1s ease-out 0.2s both;
  display: inline-block;
  background: rgba(255, 215, 0, 0.9);
  color: #2d3748;
  padding: 8px 24px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.brand-intro {
  margin-top: 30px;
  animation: fadeInUp 1s ease-out 0.4s both;
}

.intro-text {
  font-size: 1.3rem;
  line-height: 2;
  font-weight: 500;
  display: inline;
  background: rgba(102, 126, 234, 0.85);
  color: white;
  padding: 6px 18px;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
  border-radius: 6px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}


/* Section通用样式 */
.section-header {
  text-align: center;
  margin-bottom: 80px;
  position: relative;
}

.section-tag {
  display: inline-block;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 12px 32px;
  border-radius: 30px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 32px;
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
  transform: translateY(0);
  transition: all 0.3s ease;
}

.section-tag:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 35px rgba(102, 126, 234, 0.4);
}

.section-header h2 {
  font-size: 3.2rem;
  color: #1a202c;
  margin-bottom: 24px;
  position: relative;
  font-weight: 800;
  line-height: 1.2;
  background: linear-gradient(135deg, #2d3748, #4a5568);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.section-header h2::after {
  content: '';
  position: absolute;
  bottom: -15px;
  left: 50%;
  transform: translateX(-50%);
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 2px;
}

.section-desc {
  color: #64748b;
  font-size: 1.25rem;
  max-width: 700px;
  margin: 32px auto 0;
  line-height: 1.7;
  font-weight: 400;
  opacity: 0.9;
}


/* 健康认知内容样式 */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 30px;
  margin-bottom: 50px;
}

.featured-article {
  background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.9) 100%);
  border-radius: 20px;
  padding: 30px;
  position: relative;
  cursor: pointer;
  transition: all 0.4s ease;
  border: 1px solid rgba(255,255,255,0.8);
  backdrop-filter: blur(10px);
  overflow: hidden;
}

.featured-article:hover {
  transform: translateY(-8px) scale(1.02);
  box-shadow: 0 25px 50px rgba(0,0,0,0.12);
}

.featured-article h4 {
  font-size: 1.3rem;
  color: #2d3748;
  margin-bottom: 10px;
  font-weight: 700;
  line-height: 1.4;
}

.featured-article p {
  color: #4a5568;
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 15px;
  opacity: 0.8;
}

.article-badge {
  display: inline-block;
  padding: 6px 14px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 600;
  margin-bottom: 15px;
  position: relative;
  overflow: hidden;
}

.article-badge.trending {
  background: linear-gradient(45deg, #ff6b6b, #ee5a24);
  color: white;
  animation: pulse-glow 2s ease-in-out infinite;
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

.article-badge.method {
  background: linear-gradient(45deg, #feca57, #48dbfb);
  color: #2d3748;
}

.article-badge.warning {
  background: linear-gradient(45deg, #ff6348, #ff9ff3);
  color: white;
}

.article-badge.wisdom {
  background: linear-gradient(45deg, #a55eea, #26de81);
  color: white;
}

@keyframes pulse-glow {
  0%, 100% {
    transform: scale(1);
    box-shadow: 0 0 15px rgba(255, 107, 107, 0.4);
  }
  50% {
    transform: scale(1.05);
    box-shadow: 0 0 25px rgba(255, 107, 107, 0.6);
  }
}

.arrow-indicator {
  font-weight: 900;
  font-size: 1.2em;
  color: #667eea;
  margin-left: 4px;
}

/* 客户见证预览样式 */
.testimonial-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(450px, 1fr));
  gap: 40px;
}

.testimonial-card {
  background: linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(248,250,252,0.9) 100%);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.05);
  position: relative;
  transition: all 0.4s ease;
  border: 1px solid rgba(255,255,255,0.8);
  backdrop-filter: blur(10px);
}

.testimonial-card:hover {
  transform: translateY(-12px) scale(1.02);
  box-shadow: 0 30px 60px rgba(0,0,0,0.08);
}

.testimonial-card::before {
  content: '"';
  position: absolute;
  top: -10px;
  left: 20px;
  font-size: 6rem;
  color: #667eea;
  opacity: 0.2;
  font-family: serif;
  line-height: 1;
}

.testimonial-content p {
  font-size: 1.1rem;
  line-height: 1.7;
  color: #4a5568;
  margin-bottom: 25px;
  font-style: italic;
}

.testimonial-author {
  display: flex;
  align-items: center;
  gap: 15px;
}

.author-info h4 {
  font-size: 1.1rem;
  color: #2d3748;
  margin-bottom: 5px;
  font-weight: 600;
}

.author-info span {
  font-size: 0.9rem;
  color: #718096;
}

/* CTA区域样式 */
.cta-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 100px 0;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="stars" width="20" height="20" patternUnits="userSpaceOnUse"><circle cx="10" cy="10" r="1" fill="white" opacity="0.1"/></pattern></defs><rect width="100" height="100" fill="url(%23stars)"/></svg>');
  animation: twinkle 3s ease-in-out infinite;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.6; }
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
  padding: 0 20px;
  position: relative;
  z-index: 1;
}

.cta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  margin-bottom: 20px;
  align-items: start;
}

.cta-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
}

.primary-cta, .community-cta {
  min-width: 280px;
  height: 70px;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 35px;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}

.primary-cta {
  background: linear-gradient(45deg, #ffd700, #ffed4a) !important;
  border: none !important;
  color: #2d3748 !important;
  box-shadow: 0 10px 30px rgba(255,215,0,0.4);
  animation: pulse-glow 2s ease-in-out infinite;
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 10px 30px rgba(255,215,0,0.4); }
  50% { box-shadow: 0 15px 40px rgba(255,215,0,0.6); }
}

.primary-cta:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 20px 50px rgba(255,215,0,0.6);
}

.community-cta {
  background: linear-gradient(45deg, #ffd700, #ffed4a) !important;
  border: none !important;
  color: #2d3748 !important;
  box-shadow: 0 10px 30px rgba(255,215,0,0.4);
  animation: pulse-glow 2s ease-in-out infinite;
}

.community-cta:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 20px 50px rgba(255,215,0,0.6);
}

.benefit-compact {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.benefit-compact div {
  font-size: 0.9rem;
  font-weight: 600;
  color: #667eea;
  line-height: 1.6;
}

.button-icon {
  margin-right: 10px;
  font-size: 1.3rem;
}


/* 响应式设计 */
@media (max-width: 768px) {
  .brand-title {
    font-size: 2.8rem;
  }

  .brand-subtitle {
    font-size: 1.4rem;
  }

  .intro-text {
    font-size: 1.1rem;
  }

  .content-wrapper {
    padding: 40px 15px;
  }

  .content-wrapper > section {
    padding: 50px 30px;
    margin-bottom: 80px;
  }


  .content-grid {
    grid-template-columns: 1fr;
  }

  .testimonial-cards {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .cta-grid {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .primary-cta, .community-cta {
    width: 280px;
    min-width: auto;
    font-size: 1rem;
    height: 60px;
  }

  .benefit-compact div {
    font-size: 0.85rem;
  }
}

/* ========== Footer样式 ========== */
.site-footer {
  background: #2d3748;
  color: white;
  padding: 60px 0 20px;
}

.container-footer {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
  margin-bottom: 40px;
}

.footer-section h3 {
  font-size: 1.3rem;
  font-weight: 600;
  margin-bottom: 20px;
  color: #ffd700;
}

.footer-links {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.footer-links a {
  color: #a0aec0;
  text-decoration: none;
  transition: color 0.3s ease;
}

.footer-links a:hover {
  color: #ffd700;
}

.newsletter p {
  color: #a0aec0;
  margin-bottom: 15px;
  line-height: 1.6;
}

.newsletter-form {
  display: flex;
  gap: 10px;
  margin-top: 15px;
}

.newsletter-input {
  flex: 1;
}

.newsletter-btn {
  background: #ffd700 !important;
  border-color: #ffd700 !important;
  color: #2d3748 !important;
}

.newsletter-btn:hover {
  background: #ffed4a !important;
  border-color: #ffed4a !important;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 20px;
  border-top: 1px solid #4a5568;
}

.copyright p {
  margin: 0;
  color: #a0aec0;
}

.social-links {
  display: flex;
  align-items: center;
  gap: 15px;
}

.social-links span {
  color: #a0aec0;
}

.social-link {
  color: #a0aec0;
  text-decoration: none;
  padding: 5px 10px;
  border-radius: 5px;
  transition: all 0.3s ease;
}

.social-link:hover {
  color: #ffd700;
  background: rgba(255, 215, 0, 0.1);
}

/* Footer移动端适配 */
@media (max-width: 768px) {
  .footer-content {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .footer-bottom {
    flex-direction: column;
    gap: 15px;
    text-align: center;
  }

  .newsletter-form {
    flex-direction: column;
  }
}
</style>