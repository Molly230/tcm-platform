<template>
  <div class="health-solution-view">
    <!-- 前后对比 -->
    <section class="before-after-comparison">
      <div class="container">
        <h2 class="section-title">专业体质测评，让你告别健康困扰</h2>
        <div class="comparison-wrapper">
          <!-- 测评前 -->
          <div class="before-section">
            <div class="section-header-badge before-badge">
              <span class="badge-icon">❌</span>
              <span class="badge-text">测评前</span>
            </div>
            <div class="comparison-content">
              <div class="comparison-item">
                <div class="item-icon">😵</div>
                <div class="item-content">
                  <h3>盲目养生，越养越差</h3>
                  <p>网上方法千千万，不知道哪个适合自己，跟风尝试却适得其反</p>
                </div>
              </div>
              <div class="comparison-item">
                <div class="item-icon">🤔</div>
                <div class="item-content">
                  <h3>身体信号，看不懂</h3>
                  <p>总感觉身体不舒服，但说不清哪里不对，去医院检查又没问题</p>
                </div>
              </div>
              <div class="comparison-item">
                <div class="item-icon">💸</div>
                <div class="item-content">
                  <h3>花钱无数，效果甚微</h3>
                  <p>买了很多保健品和课程，钱花了不少，身体却没有明显改善</p>
                </div>
              </div>
            </div>
          </div>

          <!-- VS分隔线 -->
          <div class="vs-divider">
            <div class="vs-line"></div>
            <div class="vs-icon">⚡</div>
            <div class="vs-text">专业体质测评</div>
          </div>

          <!-- 测评后 -->
          <div class="after-section">
            <div class="section-header-badge after-badge">
              <span class="badge-icon">✅</span>
              <span class="badge-text">测评后</span>
            </div>
            <div class="comparison-content">
              <div class="comparison-item">
                <div class="item-icon">🎯</div>
                <div class="item-content">
                  <h3>精准识别体质类型</h3>
                  <p>9大体质精准分析，告别盲目调理，每一步都有科学依据</p>
                </div>
              </div>
              <div class="comparison-item">
                <div class="item-icon">📋</div>
                <div class="item-content">
                  <h3>找出健康问题根源</h3>
                  <p>清楚了解身体状况，明确调理方向，健康管理有的放矢</p>
                </div>
              </div>
              <div class="comparison-item">
                <div class="item-icon">💡</div>
                <div class="item-content">
                  <h3>获得个性化方案</h3>
                  <p>量身定制调理计划，预防疾病于未然，投入精准见效快</p>
                </div>
              </div>
            </div>
          </div>
        </div>
        
        <!-- 权威背书 -->
        <div class="authority-footer">
          <div class="authority-item">
            <span class="authority-icon">💼</span>
            <span class="authority-text">基于《中医体质分类与判定》标准</span>
          </div>
          <div class="authority-item">
            <span class="authority-icon">👨‍⚕️</span>
            <span class="authority-text">长年临床经验总结</span>
          </div>
        </div>
      </div>
    </section>


    <!-- 专业体质测评入口 -->
    <section class="assessment-cta">
      <div class="container">
        <div class="cta-content">
          <div class="cta-header">
            <h2>选择你的健康问题，获得专业调理方案</h2>
            <p class="cta-desc">针对不同健康问题，提供个性化的中医调理指导</p>
          </div>
          
          <div class="health-issues">
            <div class="issue-button" @click="goToAssessment('insomnia')">
              <div class="issue-icon">😴</div>
              <div class="issue-content">
                <h3>失眠测评</h3>
                <p>睡眠质量差、入睡困难、多梦易醒</p>
                <div class="issue-tag">5分钟测评</div>
              </div>
            </div>
            
            <div class="issue-button disabled" @click="showComingSoon">
              <div class="issue-icon">🫄</div>
              <div class="issue-content">
                <h3>胃病测评</h3>
                <p>胃痛胃胀、消化不良、食欲不振</p>
                <div class="issue-tag">
                  <span class="coming-soon-text">开发中</span>
                </div>
              </div>
            </div>
            
            <div class="issue-button disabled" @click="showComingSoon">
              <div class="issue-icon">👩‍🦳</div>
              <div class="issue-content">
                <h3>早衰测评</h3>
                <p>疲劳乏力、记忆力下降、皮肤暗沉</p>
                <div class="issue-tag">
                  <span class="coming-soon-text">开发中</span>
                </div>
              </div>
            </div>
          </div>

          <div class="general-assessment">
            <p class="general-text">不确定自己的问题？</p>
            <el-button type="primary" size="large" class="general-btn" @click="showComingSoon" :disabled="true">
              <span class="button-icon">🔍</span>
              综合体质测评
              <span class="coming-soon-badge">开发中</span>
            </el-button>
          </div>
        </div>
      </div>
    </section>

    <!-- 用户见证 -->
    <section class="testimonials-section">
      <div class="container">
        <h2 class="section-title">用户真实反馈</h2>
        <div class="testimonials-grid">
          <div class="testimonial-card">
            <div class="testimonial-content">
              <p>"通过体质测评发现我是湿热体质，按照个性化方案调理3个月，痘痘明显减少，精神状态好了很多。"</p>
            </div>
            <div class="testimonial-author">
              <div class="author-info">
                <h4>小王</h4>
                <span>湿热体质 · 调理3个月</span>
              </div>
            </div>
          </div>
          <div class="testimonial-card">
            <div class="testimonial-content">
              <p>"测评还真有用，以前瞎买保健品，花了很多钱，现在好了，知道什么是我要的。"</p>
            </div>
            <div class="testimonial-author">
              <div class="author-info">
                <h4>李女士</h4>
                <span>气虚体质 · 调养6个月</span>
              </div>
            </div>
          </div>
          <div class="testimonial-card">
            <div class="testimonial-content">
              <p>"在线咨询很方便，专家很专业，给的建议都很有针对性，解决了我长期的睡眠问题。"</p>
            </div>
            <div class="testimonial-author">
              <div class="author-info">
                <h4>张先生</h4>
                <span>阴虚体质 · 咨询8次</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>



    <!-- 网站Footer -->
    <footer class="site-footer">
      <div class="container">
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
import { ElMessage } from 'element-plus'

const router = useRouter()
const email = ref('')

// 导航方法
const goToAssessment = (type = '') => {
  if (type === 'insomnia') {
    router.push('/insomnia-assessment')
  } else if (type) {
    // 其他类型暂时不可用
    ElMessage.warning('该功能正在开发中，敬请期待')
  } else {
    ElMessage.warning('请选择具体的测评类型')
  }
}

const showComingSoon = () => {
  // 开发中提示
}
</script>

<style scoped>
.health-solution-view {
  min-height: 100vh;
}

/* 前后对比区域 */
.before-after-comparison {
  padding: 100px 0 80px;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.comparison-wrapper {
  display: grid;
  grid-template-columns: 1fr auto 1fr;
  gap: 40px;
  align-items: start;
  margin-top: 50px;
}

.before-section, .after-section {
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
  position: relative;
}

.before-section {
  border: 2px solid #ff6b6b;
}

.after-section {
  border: 2px solid #4ade80;
}

.section-header-badge {
  position: absolute;
  top: -15px;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  border-radius: 25px;
  font-size: 1rem;
  font-weight: 600;
  color: white;
}

.before-badge {
  background: linear-gradient(135deg, #ff6b6b, #ff5252);
  box-shadow: 0 5px 15px rgba(255, 107, 107, 0.4);
}

.after-badge {
  background: linear-gradient(135deg, #4ade80, #22c55e);
  box-shadow: 0 5px 15px rgba(74, 222, 128, 0.4);
}

.badge-icon {
  font-size: 1.1rem;
}

.comparison-content {
  padding-top: 25px;
}

.comparison-item {
  display: flex;
  align-items: flex-start;
  gap: 15px;
  margin-bottom: 25px;
  padding: 15px;
  border-radius: 12px;
  transition: transform 0.3s ease;
}

.before-section .comparison-item {
  background: rgba(255, 107, 107, 0.05);
  border-left: 3px solid #ff6b6b;
}

.after-section .comparison-item {
  background: rgba(74, 222, 128, 0.05);
  border-left: 3px solid #4ade80;
}

.comparison-item:hover {
  transform: translateY(-3px);
}

.before-section .comparison-item:hover {
  background: rgba(255, 107, 107, 0.1);
}

.after-section .comparison-item:hover {
  background: rgba(74, 222, 128, 0.1);
}

.item-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
  margin-top: 2px;
}

.item-content h3 {
  font-size: 1.2rem;
  color: #2d3748;
  margin-bottom: 8px;
  font-weight: 600;
}

.item-content p {
  color: #4a5568;
  line-height: 1.6;
  font-size: 0.95rem;
  margin: 0;
}

/* VS 分隔线 */
.vs-divider {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  min-height: 300px;
}

.vs-line {
  width: 2px;
  height: 100px;
  background: linear-gradient(to bottom, #667eea, #764ba2);
  border-radius: 1px;
}

.vs-icon {
  font-size: 2.5rem;
  color: #667eea;
  margin: 15px 0;
  animation: pulse 2s ease-in-out infinite;
}

.vs-text {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  font-size: 1rem;
  font-weight: 600;
  color: #667eea;
  background: white;
  padding: 15px 8px;
  border-radius: 25px;
  box-shadow: 0 5px 15px rgba(102, 126, 234, 0.2);
  border: 2px solid #667eea;
  white-space: nowrap;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); }
  50% { transform: scale(1.1); }
}

/* 权威背书 */
.authority-footer {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-top: 50px;
  padding-top: 40px;
  border-top: 1px solid #e2e8f0;
}

.authority-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 20px;
  background: white;
  border-radius: 25px;
  box-shadow: 0 5px 15px rgba(0,0,0,0.08);
  transition: transform 0.3s ease;
}

.authority-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.12);
}

.authority-icon {
  font-size: 1.2rem;
}

.authority-text {
  font-size: 0.9rem;
  color: #2d3748;
  font-weight: 600;
}

/* 容器样式 */
.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  color: #2d3748;
  margin-bottom: 60px;
  font-weight: 700;
  position: relative;
}

.section-title::after {
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


/* 专业体质测评入口 */
.assessment-cta {
  padding: 80px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  text-align: center;
}

.cta-content {
  max-width: 800px;
  margin: 0 auto;
}

.cta-header h2 {
  font-size: 2.8rem;
  font-weight: 800;
  margin-bottom: 20px;
  text-shadow: 3px 3px 6px rgba(0,0,0,0.3);
}

.cta-desc {
  font-size: 1.2rem;
  opacity: 0.95;
  margin-bottom: 40px;
  line-height: 1.6;
}

.health-issues {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 25px;
  margin-bottom: 50px;
}

.issue-button {
  background: rgba(255,255,255,0.95);
  border-radius: 20px;
  padding: 25px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  color: #2d3748;
  text-align: center;
  position: relative;
  overflow: hidden;
}

.issue-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, #667eea, #764ba2);
  opacity: 0;
  transition: opacity 0.3s ease;
  z-index: 0;
}

.issue-button:hover::before {
  opacity: 1;
}

.issue-button:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
  border-color: #667eea;
  color: white;
}

.issue-button > * {
  position: relative;
  z-index: 1;
}

.issue-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.issue-content h3 {
  font-size: 1.4rem;
  font-weight: 700;
  margin-bottom: 10px;
}

.issue-content p {
  font-size: 1rem;
  line-height: 1.5;
  margin-bottom: 12px;
  opacity: 0.8;
}

.issue-button:hover .issue-content p {
  opacity: 0.95;
}

.issue-tag {
  display: inline-block;
  background: rgba(102, 126, 234, 0.1);
  color: #667eea;
  padding: 6px 15px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.3s ease;
}

.issue-button:hover:not(.disabled) .issue-tag {
  background: rgba(255,255,255,0.2);
  color: white;
}

.issue-button.disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.issue-button.disabled::before {
  opacity: 0;
}

.issue-button.disabled:hover {
  transform: none;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  border-color: transparent;
  color: #2d3748;
}

.coming-soon-text {
  background: rgba(255, 165, 0, 0.8);
  color: white;
  padding: 4px 10px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.general-assessment {
  text-align: center;
  padding-top: 30px;
  border-top: 1px solid rgba(255,255,255,0.2);
}

.general-text {
  font-size: 1.1rem;
  margin-bottom: 20px;
  opacity: 0.9;
}

.general-btn {
  background: rgba(255,255,255,0.1) !important;
  border: 2px solid rgba(255,255,255,0.3) !important;
  color: white !important;
  min-width: 200px;
  height: 60px;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 30px;
  backdrop-filter: blur(10px);
  transition: all 0.3s ease;
}

.general-btn:hover:not(:disabled) {
  background: rgba(255,255,255,0.2) !important;
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0,0,0,0.2);
}

.general-btn:disabled {
  opacity: 0.7 !important;
  cursor: not-allowed !important;
  background: rgba(255,255,255,0.1) !important;
}

.coming-soon-badge {
  margin-left: 8px;
  padding: 2px 8px;
  background: rgba(255, 165, 0, 0.8);
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 500;
  color: white;
}


/* 用户见证 */
.testimonials-section {
  padding: 80px 0;
  background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
}

.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 30px;
}

.testimonial-card {
  background: white;
  border-radius: 15px;
  padding: 35px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.08);
  position: relative;
  transition: transform 0.3s ease;
}

.testimonial-card:hover {
  transform: translateY(-5px);
}

.testimonial-card::before {
  content: '"';
  position: absolute;
  top: -10px;
  left: 20px;
  font-size: 4rem;
  color: #667eea;
  opacity: 0.3;
  font-family: serif;
}

.testimonial-content p {
  font-size: 1.1rem;
  line-height: 1.7;
  color: #4a5568;
  margin-bottom: 20px;
  font-style: italic;
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


/* 响应式设计 */
@media (max-width: 768px) {
  /* 前后对比 - 移动端适配 */
  .comparison-wrapper {
    grid-template-columns: 1fr;
    gap: 30px;
  }

  .vs-divider {
    min-height: auto;
    flex-direction: row;
    padding: 20px 0;
  }

  .vs-line {
    width: 60px;
    height: 2px;
  }

  .vs-text {
    writing-mode: horizontal-tb;
    text-orientation: mixed;
    padding: 8px 15px;
    margin: 0 15px;
  }

  .vs-icon {
    font-size: 2rem;
  }

  .before-section, .after-section {
    padding: 25px 20px;
  }

  .comparison-item {
    padding: 12px;
    gap: 12px;
  }

  .item-icon {
    font-size: 1.3rem;
  }

  .item-content h3 {
    font-size: 1.1rem;
  }

  .item-content p {
    font-size: 0.9rem;
  }

  .authority-footer {
    flex-direction: column;
    align-items: center;
    gap: 20px;
  }

  .authority-item {
    padding: 10px 16px;
  }


  /* 专业体质测评入口 - 移动端适配 */
  .cta-header h2 {
    font-size: 2rem;
  }

  .cta-desc {
    font-size: 1.1rem;
  }

  .health-issues {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .issue-button {
    padding: 20px;
  }

  .issue-icon {
    font-size: 2.5rem;
  }

  .issue-content h3 {
    font-size: 1.2rem;
  }

  .issue-content p {
    font-size: 0.95rem;
  }

  .general-btn {
    min-width: 180px;
    height: 55px;
    font-size: 1rem;
  }

}

@media (max-width: 480px) {
  .container {
    padding: 0 15px;
  }
}


/* Footer样式 */
.site-footer {
  background: #2d3748;
  color: white;
  padding: 60px 0 20px;
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