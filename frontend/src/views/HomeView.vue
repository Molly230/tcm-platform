<template>
  <div class="home-view">
    <!-- 主要品牌展示区 -->
    <div class="hero-section">
      <div class="hero-overlay"></div>
      <div class="hero-content">
        <div class="brand-opening">
          <h1 class="brand-title">生活有中医<br/>养生不费力</h1>
          <p class="brand-slogan">
            调理找名医，食养治未病，服务促执行，学习变专家
          </p>
          <p class="brand-description">
            你能成为专业的中医养生专家
          </p>
          <div class="cta-button-wrapper">
            <el-button type="primary" size="large" class="hero-cta-button" @click="$router.push('/solutions')">
              立即体验
            </el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 四大核心板块区域 -->
    <div class="main-content-area">
      <!-- 板块一：「中医入生活」—— 场景化渗透 -->
      <section class="life-scenario-section">
        <div class="section-container">
          <div class="section-title-group">
            <h2 class="main-section-title">中医入生活</h2>
            <p class="main-section-subtitle">加入中医思维，健康如此简单</p>
           </div>

          <div class="scenario-grid">
            <!-- 场景1：一日三餐里的中医 -->
            <div class="scenario-card">
              <div class="scenario-icon">🍚</div>
              <h3 class="scenario-title">一日三餐里的中医</h3>
              <p class="scenario-slogan">只要对症，这些都是你的食疗方</p>
              <div class="scenario-content">
                <div class="recipe-images-grid">
                  <div class="recipe-image-item">
                    <img src="https://images.unsplash.com/photo-1547592166-23ac45744acd?w=400&h=400&fit=crop" alt="生姜小米粥" class="recipe-img">
                    <div class="recipe-overlay">生姜小米粥</div>
                  </div>
                  <div class="recipe-image-item">
                    <img src="https://images.unsplash.com/photo-1559181567-c3190ca9959b?w=400&h=400&fit=crop" alt="百合银耳粥" class="recipe-img">
                    <div class="recipe-overlay">水果</div>
                  </div>
                  <div class="recipe-image-item">
                    <img src="https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=400&fit=crop" alt="赤小豆薏米粥" class="recipe-img">
                    <div class="recipe-overlay">鲜虾鸡蛋面</div>
                  </div>
                  <div class="recipe-image-item">
                    <img src="https://images.unsplash.com/photo-1551024506-0bccd828d307?w=400&h=400&fit=crop" alt="养生汤" class="recipe-img">
                    <div class="recipe-overlay">冷饮和蛋糕</div>
                  </div>
                  <div class="recipe-image-item">
                    <img src="https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=400&fit=crop" alt="赤小豆薏米粥" class="recipe-img">
                    <div class="recipe-overlay">咖啡</div>
                  </div>
                  <div class="recipe-image-item">
                    <img src="https://images.unsplash.com/photo-1569718212165-3a8278d5f624?w=400&h=400&fit=crop" alt="赤小豆薏米粥" class="recipe-img">
                    <div class="recipe-overlay">调料</div>
                  </div>
                </div>
              </div>
              <el-button type="primary" class="scenario-btn" @click="$router.push('/learning-center')">
                查看今日食谱
              </el-button>
            </div>

            <!-- 场景2：节气里的养生细节 -->
            <div class="scenario-card">
              <div class="scenario-icon">📅</div>
              <h3 class="scenario-title">节气里的养生细节</h3>
              <p class="scenario-slogan">跟着节气做，少生病</p>
              <div class="scenario-content">
                <!-- 节气选择器 -->
                <div class="solar-term-selector">
                  <el-select v-model="selectedSolarTerm" placeholder="选择节气" size="large" style="width: 100%;">
                    <el-option-group label="春季">
                      <el-option value="立春" label="立春 - 温补升阳">
                        <span>🌱 立春</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">温补升阳</span>
                      </el-option>
                      <el-option value="雨水" label="雨水 - 健脾祛湿">
                        <span>💧 雨水</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">健脾祛湿</span>
                      </el-option>
                      <el-option value="惊蛰" label="惊蛰 - 疏肝明目">
                        <span>⚡ 惊蛰</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">疏肝明目</span>
                      </el-option>
                      <el-option value="春分" label="春分 - 调和阴阳">
                        <span>🌸 春分</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">调和阴阳</span>
                      </el-option>
                      <el-option value="清明" label="清明 - 清热凉血">
                        <span>🍃 清明</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">清热凉血</span>
                      </el-option>
                      <el-option value="谷雨" label="谷雨 - 清润祛湿">
                        <span>🌾 谷雨</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">清润祛湿</span>
                      </el-option>
                    </el-option-group>
                    <el-option-group label="夏季">
                      <el-option value="立夏" label="立夏 - 清热祛湿">
                        <span>☀️ 立夏</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">清热祛湿</span>
                      </el-option>
                      <el-option value="小满" label="小满 - 健脾祛湿">
                        <span>🌤️ 小满</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">健脾祛湿</span>
                      </el-option>
                      <el-option value="芒种" label="芒种 - 清热解暑">
                        <span>🌾 芒种</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">清热解暑</span>
                      </el-option>
                      <el-option value="夏至" label="夏至 - 养心安神">
                        <span>🔥 夏至</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">养心安神</span>
                      </el-option>
                      <el-option value="小暑" label="小暑 - 消暑祛湿">
                        <span>🌡️ 小暑</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">消暑祛湿</span>
                      </el-option>
                      <el-option value="大暑" label="大暑 - 滋阴清热">
                        <span>🔆 大暑</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">滋阴清热</span>
                      </el-option>
                    </el-option-group>
                    <el-option-group label="秋季">
                      <el-option value="立秋" label="立秋 - 滋阴润燥">
                        <span>🍂 立秋</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">滋阴润燥</span>
                      </el-option>
                      <el-option value="处暑" label="处暑 - 清润祛湿">
                        <span>🌥️ 处暑</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">清润祛湿</span>
                      </el-option>
                      <el-option value="白露" label="白露 - 润肺止咳">
                        <span>💧 白露</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">润肺止咳</span>
                      </el-option>
                      <el-option value="秋分" label="秋分 - 滋阴养肺">
                        <span>🍁 秋分</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">滋阴养肺</span>
                      </el-option>
                      <el-option value="寒露" label="寒露 - 滋阴补肾">
                        <span>🌫️ 寒露</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">滋阴补肾</span>
                      </el-option>
                      <el-option value="霜降" label="霜降 - 润肺化痰">
                        <span>❄️ 霜降</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">润肺化痰</span>
                      </el-option>
                    </el-option-group>
                    <el-option-group label="冬季">
                      <el-option value="立冬" label="立冬 - 温补气血">
                        <span>⛄ 立冬</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">温补气血</span>
                      </el-option>
                      <el-option value="小雪" label="小雪 - 补肾益精">
                        <span>🌨️ 小雪</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">补肾益精</span>
                      </el-option>
                      <el-option value="大雪" label="大雪 - 温补脾肾">
                        <span>❄️ 大雪</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">温补脾肾</span>
                      </el-option>
                      <el-option value="冬至" label="冬至 - 滋阴补肾">
                        <span>🌙 冬至</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">滋阴补肾</span>
                      </el-option>
                      <el-option value="小寒" label="小寒 - 温补阳气">
                        <span>🧊 小寒</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">温补阳气</span>
                      </el-option>
                      <el-option value="大寒" label="大寒 - 温中散寒">
                        <span>🌬️ 大寒</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 10px;">温中散寒</span>
                      </el-option>
                    </el-option-group>
                  </el-select>
                </div>

                <!-- 节气养生方案 -->
                <div class="solar-term-info" v-if="currentSolarTermInfo">
                  <div class="current-term">
                    <strong>{{ selectedSolarTerm }}</strong>
                    <span class="term-theme">{{ currentSolarTermInfo.theme }}</span>
                  </div>
                  <div class="term-tip">{{ currentSolarTermInfo.tip }}</div>

                  <div class="recommend-recipe">
                    <span class="recipe-label">🍲 推荐食疗：</span>
                    <span class="recipe-highlight">{{ currentSolarTermInfo.recipe }}</span>
                  </div>

                  <!-- 经络调理 -->
                  <div class="acupoint-section">
                    <div class="acupoint-title">👆 经络调理</div>
                    <div class="acupoint-list">
                      <div
                        v-for="(point, index) in currentSolarTermInfo.acupoints"
                        :key="index"
                        class="acupoint-item"
                      >
                        <span class="acupoint-name">{{ point.name }}</span>
                        <span class="acupoint-effect">{{ point.effect }}</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
              <el-button type="primary" class="scenario-btn" @click="$router.push('/learning-center')">
                更多定制化方案，找医生调理
              </el-button>
            </div>

            <!-- 场景3：小毛病自己调 -->
            <div class="scenario-card">
              <div class="scenario-icon">🌿</div>
              <h3 class="scenario-title">小毛病自己调</h3>
              <p class="scenario-slogan">头痛、上火？中医的方法千变万化</p>
              <div class="scenario-content">
                <div class="remedy-images-grid">
                  <div class="remedy-image-item">
                    <img src="/images/remedy-press.svg" alt="按压少商穴" class="remedy-img">
                    <div class="remedy-info">
                      <div class="remedy-symptom">🔥 喉咙干痛</div>
                      <div class="remedy-solution">按压少商穴</div>
                    </div>
                  </div>
                  <div class="remedy-image-item">
                    <img src="/images/remedy-hang.svg" alt="倒吊身体" class="remedy-img">
                    <div class="remedy-info">
                      <div class="remedy-symptom">💤 轻微失眠</div>
                      <div class="remedy-solution">倒吊身体</div>
                    </div>
                  </div>
                  <div class="remedy-image-item">
                    <img src="/images/remedy-drink.svg" alt="喝杨梅酒" class="remedy-img">
                    <div class="remedy-info">
                      <div class="remedy-symptom">🤢 轻微腹泻</div>
                      <div class="remedy-solution">喝杨梅酒</div>
                    </div>
                  </div>
                </div>
              </div>
              <el-button type="primary" class="scenario-btn" @click="$router.push('/learning-center')">
                更多小毛病调理
              </el-button>
            </div>
          </div>
        </div>
      </section>

      <!-- 板块二：「养生不费力」—— 工具化赋能 -->
      <section class="easy-wellness-section">
        <div class="section-container">
          <div class="section-title-group">
            <h2 class="main-section-title">养生不费力</h2>
            <p class="main-section-subtitle">用工具帮你快速找到适合自己的调理方式</p>
          </div>

          <div class="tools-grid">
            <!-- 工具1：体质速测 -->
            <div class="tool-card tool-card-primary">
              <div class="tool-header">
                <div class="tool-icon">⚡</div>
                <div class="tool-title-group">
                  <h3 class="tool-title">选择你的健康问题，获得专业调理方案</h3>
                  </div>
              </div>
              <div class="tool-content">
                <div class="tool-feature">
                  <span class="feature-badge">快速</span>
                  <span class="feature-text">5分钟做测评，测完就有方案</span>
                </div>
                <div class="testimonial-quote">
                  "测完才知道，我一直吃错了"
                  <span class="quote-author">—— 用户张女士</span>
                </div>
              </div>
              <el-button type="primary" size="large" class="tool-btn" @click="$router.push('/assessment')">
                立即测试
              </el-button>
              <!-- 失眠测评快速入口 -->
              <el-button type="warning" size="small" class="insomnia-quick-btn" @click="$router.push('/insomnia-assessment')">
                <span class="quick-btn-icon">😴</span>
                失眠测评：睡眠质量差、入睡困难、多梦易醒
              </el-button>
            </div>

            <!-- 工具2：我的食疗计划 -->
            <div class="tool-card tool-card-secondary">
              <div class="tool-header">
                <div class="tool-icon">📋</div>
                <div class="tool-title-group">
                  <h3 class="tool-title">我的食疗计划</h3>
                  <p class="tool-tagline">按体质生成7天菜单，不用想</p>
                </div>
              </div>
              <div class="tool-content">
                <div class="plan-preview">
                  <div class="plan-title">痰湿体质本周计划：</div>
                  <div class="plan-item">周一：赤小豆薏米粥</div>
                  <div class="plan-item">周三：冬瓜排骨汤</div>
                  <div class="plan-item">周五：山楂陈皮茶</div>
                </div>
                <div class="plan-note">食材常见、做法简单</div>
              </div>
              <el-button type="success" size="large" class="tool-btn" @click="$router.push('/solutions')">
                生成我的计划
              </el-button>
            </div>
          </div>
        </div>
      </section>

      

      <!-- 板块三：「执行最重要」—— 从知道到做到 -->
      <section class="execution-section">
        <div class="section-container">
          <div class="section-title-group">
            <h2 class="main-section-title">执行最重要</h2>
            <p class="main-section-subtitle">从"知道"到"做到"，他们这样改变</p>
          </div>

          <!-- 三个真实案例 -->
          <div class="case-studies-grid">
            <!-- 案例1：执行记录 -->
            <div class="case-card">
              <div class="case-image-wrapper">
                <div class="case-image-placeholder">
                  <div class="placeholder-icon">📱</div>
                  <p class="placeholder-text">张女士的小程序<br/>打卡截图</p>
                </div>
              </div>
              <div class="case-content">
                <div class="case-badge">执行记录</div>
                <p class="case-quote">
                  "坚持21天食疗，痰湿体质症状减轻，小程序提醒太管用了"
                </p>
                <div class="case-author">—— 张女士</div>
              </div>
            </div>

            <!-- 案例2：数据变化 -->
            <div class="case-card">
              <div class="case-image-wrapper">
                <div class="case-image-placeholder">
                  <div class="placeholder-icon">📊</div>
                  <p class="placeholder-text">体质复测<br/>报告对比图</p>
                </div>
              </div>
              <div class="case-content">
                <div class="case-badge">数据变化</div>
                <p class="case-quote">
                  "从阳虚质→平和质，感谢方案动态调整"
                </p>
                <div class="case-author">—— 李先生</div>
              </div>
            </div>

            <!-- 案例3：场景化 -->
            <div class="case-card">
              <div class="case-image-wrapper">
                <div class="case-image-placeholder">
                  <div class="placeholder-icon">👨‍👩‍👧‍👦</div>
                  <p class="placeholder-text">全家食疗<br/>打卡墙照片</p>
                </div>
              </div>
              <div class="case-content">
                <div class="case-badge">场景化</div>
                <p class="case-quote">
                  "全家跟着小程序吃，孩子脾胃变好了"
                </p>
                <div class="case-author">—— 王女士</div>
              </div>
            </div>
          </div>

          <!-- 小程序功能亮点 -->
          <div class="miniprogram-features">
            <h3 class="features-title">专业医助陪你一起</h3>
            <div class="features-grid">
              <div class="feature-item">
                <span class="feature-icon">⏰</span>
                <span class="feature-text">每日提醒，永不忘记</span>
              </div>
              <div class="feature-item">
                <span class="feature-icon">✅</span>
                <span class="feature-text">打卡记录，看见进步</span>
              </div>
              <div class="feature-item">
                <span class="feature-icon">📱</span>
                <span class="feature-text">方案随身，随时查看</span>
              </div>
              <div class="feature-item">
                <span class="feature-icon">🔄</span>
                <span class="feature-text">动态调整，精准匹配</span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 板块四：「学习变专家」—— 成长路径 -->
      <section class="growth-path-section">
        <div class="section-container">
          <div class="section-title-group">
            <h2 class="main-section-title">学习变专家</h2>
            <p class="main-section-subtitle">你能成为专业的中医养生专家</p>
          </div>

          <div class="growth-ladder">
            <!-- 阶梯1：入门 -->
            <div class="ladder-step step-1">
              <div class="step-badge">入门</div>
              <h3 class="step-title">建框架<br/>—— 搭建中医基础认知体系</h3>
              <div class="step-content">
                <p class="step-description">快速掌握核心概念</p>
                <p class="step-description">阴阳、寒热、虚实、经络、配伍~~~</p>
              </div>
              <el-button type="primary" class="step-btn" @click="$router.push('/learning-center')">
                开始入门
              </el-button>
            </div>

            <!-- 阶梯2：进阶 -->
            <div class="ladder-step step-2">
              <div class="step-badge">进阶</div>
              <h3 class="step-title">懂原理<br/>—— 吃透中医调理底层逻辑</h3>
              <div class="step-content">
                <p class="step-description">从 "知其然" 到 "知其所以然"</p>
                <p class="step-description">中医调理专家们怎么思考</p>
              </div>
              <el-button type="primary" class="step-btn" @click="$router.push('/courses')">
                持续学习和思考
              </el-button>
            </div>

            <!-- 阶梯3：精通 -->
            <div class="ladder-step step-3">
              <div class="step-badge">精通</div>
              <h3 class="step-title">能调理<br/>—— 从专病应对到全面养护</h3>
              <div class="step-content">
                <p class="step-description">用方如用兵</p>
                <p class="step-description">实现 "专病精准调、全身综合养"</p>
              </div>
              <el-button type="primary" class="step-btn" @click="$router.push('/learning-center')">
                看真实案例
              </el-button>
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
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'

const router = useRouter()
const email = ref('')

// 节气选择
const selectedSolarTerm = ref('立冬')

// 24节气养生数据
const solarTermData: Record<string, {
  theme: string
  tip: string
  recipe: string
  acupoints: Array<{ name: string; effect: string }>
}> = {
  '立春': {
    theme: '温补升阳',
    tip: '立春阳气渐升，温补肝气，助力阳气升发',
    recipe: '韭菜炒鸡蛋',
    acupoints: [
      { name: '太冲穴', effect: '疏肝解郁，缓解烦躁' },
      { name: '行间穴', effect: '增强疏肝效果' }
    ]
  },
  '雨水': {
    theme: '健脾祛湿',
    tip: '雨水湿气重，健脾祛湿，避免春湿困脾',
    recipe: '小米山药粥',
    acupoints: [
      { name: '太冲穴', effect: '疏肝理气' },
      { name: '行间穴', effect: '改善春季失眠' }
    ]
  },
  '惊蛰': {
    theme: '疏肝明目',
    tip: '惊蛰春困来袭，疏肝明目，缓解春困',
    recipe: '菊花枸杞茶',
    acupoints: [
      { name: '太冲穴', effect: '疏肝明目' },
      { name: '行间穴', effect: '缓解头痛眩晕' }
    ]
  },
  '春分': {
    theme: '调和阴阳',
    tip: '春分昼夜等长，调和阴阳，补气养血',
    recipe: '红枣桂圆粥',
    acupoints: [
      { name: '太冲穴', effect: '平衡阴阳' },
      { name: '行间穴', effect: '调节情绪' }
    ]
  },
  '清明': {
    theme: '清热凉血',
    tip: '清明祛湿时节，清热凉血，顺应清明祛湿',
    recipe: '荠菜豆腐汤',
    acupoints: [
      { name: '太冲穴', effect: '清肝火' },
      { name: '行间穴', effect: '凉血止血' }
    ]
  },
  '谷雨': {
    theme: '清润祛湿',
    tip: '谷雨春末燥热，清润祛湿，预防春末燥热',
    recipe: '绿豆百合粥',
    acupoints: [
      { name: '太冲穴', effect: '疏肝润燥' },
      { name: '行间穴', effect: '清热祛湿' }
    ]
  },

  '立夏': {
    theme: '清热祛湿',
    tip: '立夏暑热来临，清热祛湿，预防暑热',
    recipe: '冬瓜海带汤',
    acupoints: [
      { name: '内关穴', effect: '养心安神' },
      { name: '足三里穴', effect: '健脾祛湿' }
    ]
  },
  '小满': {
    theme: '健脾祛湿',
    tip: '小满湿气渐重，健脾祛湿，缓解身体沉重',
    recipe: '赤小豆薏米水',
    acupoints: [
      { name: '阴陵泉穴', effect: '祛湿消肿' },
      { name: '足三里穴', effect: '健脾益气' }
    ]
  },
  '芒种': {
    theme: '清热解暑',
    tip: '芒种炎热多汗，清热解暑，补充水分',
    recipe: '绿豆汤',
    acupoints: [
      { name: '内关穴', effect: '清心除烦' },
      { name: '足三里穴', effect: '补气生津' }
    ]
  },
  '夏至': {
    theme: '养心安神',
    tip: '夏至阳气最盛，养心安神，应对夏至养心',
    recipe: '莲子百合粥',
    acupoints: [
      { name: '内关穴', effect: '养心安神' },
      { name: '神门穴', effect: '宁心助眠' }
    ]
  },
  '小暑': {
    theme: '消暑祛湿',
    tip: '小暑暑湿交蒸，消暑祛湿，改善暑热头晕',
    recipe: '荷叶茶',
    acupoints: [
      { name: '内关穴', effect: '消暑止呕' },
      { name: '阴陵泉穴', effect: '祛暑湿' }
    ]
  },
  '大暑': {
    theme: '滋阴清热',
    tip: '大暑酷热难耐，滋阴清热，避免大暑燥热耗气',
    recipe: '鸭肉冬瓜汤',
    acupoints: [
      { name: '内关穴', effect: '养心阴' },
      { name: '足三里穴', effect: '清热生津' }
    ]
  },

  '立秋': {
    theme: '滋阴润燥',
    tip: '立秋防燥时节，滋阴润燥，应对立秋防燥',
    recipe: '银耳百合汤',
    acupoints: [
      { name: '肺俞穴', effect: '养肺润燥' },
      { name: '太渊穴', effect: '补肺气' }
    ]
  },
  '处暑': {
    theme: '清润祛湿',
    tip: '处暑秋老虎来袭，清润祛湿，缓解秋老虎余温',
    recipe: '冬瓜薏米汤',
    acupoints: [
      { name: '肺俞穴', effect: '润肺清热' },
      { name: '太渊穴', effect: '止咳化痰' }
    ]
  },
  '白露': {
    theme: '润肺止咳',
    tip: '白露昼夜温差大，润肺止咳，预防白露干燥',
    recipe: '雪梨炖川贝',
    acupoints: [
      { name: '肺俞穴', effect: '润肺止咳' },
      { name: '太渊穴', effect: '缓解咽干' }
    ]
  },
  '秋分': {
    theme: '滋阴养肺',
    tip: '秋分阴阳平衡，滋阴养肺，调和阴阳',
    recipe: '山药百合粥',
    acupoints: [
      { name: '肺俞穴', effect: '养肺益气' },
      { name: '太渊穴', effect: '增强肺功能' }
    ]
  },
  '寒露': {
    theme: '滋阴补肾',
    tip: '寒露秋深气凉，滋阴补肾，顺应寒露养阴',
    recipe: '芝麻核桃粥',
    acupoints: [
      { name: '肺俞穴', effect: '滋阴润燥' },
      { name: '太渊穴', effect: '补气养阴' }
    ]
  },
  '霜降': {
    theme: '润肺化痰',
    tip: '霜降初霜降临，润肺化痰，预防霜降寒凉',
    recipe: '白萝卜排骨汤',
    acupoints: [
      { name: '肺俞穴', effect: '润肺化痰' },
      { name: '太渊穴', effect: '止咳平喘' }
    ]
  },

  '立冬': {
    theme: '温补气血',
    tip: '立冬阳气收藏，温补气血，抵御立冬寒凉',
    recipe: '当归生姜羊肉汤',
    acupoints: [
      { name: '肾俞穴', effect: '补肾益精' },
      { name: '涌泉穴', effect: '温补肾阳' }
    ]
  },
  '小雪': {
    theme: '补肾益精',
    tip: '小雪天寒地冻，补肾益精，缓解冬季手脚冰凉',
    recipe: '核桃红枣粥',
    acupoints: [
      { name: '肾俞穴', effect: '补肾纳气' },
      { name: '涌泉穴', effect: '改善手脚冰凉' }
    ]
  },
  '大雪': {
    theme: '温补脾肾',
    tip: '大雪严寒来临，温补脾肾，增强抗寒能力',
    recipe: '栗子炖鸡',
    acupoints: [
      { name: '肾俞穴', effect: '温补脾肾' },
      { name: '关元穴', effect: '温补元气' }
    ]
  },
  '冬至': {
    theme: '滋阴补肾',
    tip: '冬至一阳生，滋阴补肾，顺应冬至养藏',
    recipe: '桂圆枸杞茶',
    acupoints: [
      { name: '肾俞穴', effect: '滋补肾阴' },
      { name: '涌泉穴', effect: '固精纳气' }
    ]
  },
  '小寒': {
    theme: '温补阳气',
    tip: '小寒最冷时节，温补阳气，应对小寒严寒',
    recipe: '鹿茸炖排骨',
    acupoints: [
      { name: '肾俞穴', effect: '温补肾阳' },
      { name: '关元穴', effect: '增强抗寒' }
    ]
  },
  '大寒': {
    theme: '温中散寒',
    tip: '大寒最冷时刻，温中散寒，预防大寒感冒',
    recipe: '姜枣桂圆茶',
    acupoints: [
      { name: '肾俞穴', effect: '温中散寒' },
      { name: '涌泉穴', effect: '驱寒暖身' }
    ]
  }
}

// 计算当前节气信息
const currentSolarTermInfo = computed(() => {
  return solarTermData[selectedSolarTerm.value]
})

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

/* ========== 四大核心板块通用样式 ========== */
.main-content-area {
  background: linear-gradient(180deg, #ffffff 0%, #f8fafc 100%);
}

.section-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
}

.section-title-group {
  text-align: center;
  margin-bottom: 60px;
}

.main-section-title {
  font-size: 2.8rem;
  font-weight: 800;
  color: #2d3748;
  margin-bottom: 15px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.main-section-subtitle {
  font-size: 1.1rem;
  color: #718096;
  line-height: 1.6;
}

/* ========== 板块一：中医入生活 ========== */
.life-scenario-section {
  padding: 100px 0;
  background: linear-gradient(135deg, #fdfbfb 0%, #ebedee 100%);
  position: relative;
}

.scenario-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 35px;
}

.scenario-card {
  background: white;
  border-radius: 20px;
  padding: 40px 30px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}

.scenario-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.scenario-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 50px rgba(102, 126, 234, 0.15);
}

.scenario-card:hover::before {
  transform: scaleX(1);
}

.scenario-icon {
  font-size: 3.5rem;
  margin-bottom: 20px;
  text-align: center;
}

.scenario-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 12px;
  text-align: center;
}

.scenario-slogan {
  font-size: 1rem;
  color: #667eea;
  text-align: center;
  margin-bottom: 25px;
  font-weight: 600;
}

.scenario-content {
  margin-bottom: 25px;
  min-height: 140px;
}

.recipe-images-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 12px;
}

.recipe-image-item {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  aspect-ratio: 1;
  cursor: pointer;
  transition: all 0.3s ease;
}

.recipe-image-item:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.recipe-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

.recipe-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(to top, rgba(0, 0, 0, 0.8), transparent);
  color: white;
  padding: 12px 10px 8px;
  font-size: 0.9rem;
  font-weight: 600;
  text-align: center;
  transform: translateY(100%);
  transition: transform 0.3s ease;
}

.recipe-image-item:hover .recipe-overlay {
  transform: translateY(0);
}

.remedy-images-grid {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.remedy-image-item {
  position: relative;
  border-radius: 12px;
  overflow: hidden;
  background: white;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
}

.remedy-image-item:hover {
  transform: translateX(8px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.2);
}

.remedy-img {
  width: 100%;
  height: 120px;
  object-fit: cover;
  display: block;
}

.remedy-info {
  padding: 12px 15px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.remedy-symptom {
  font-size: 0.95rem;
  font-weight: 700;
  color: #2d3748;
}

.remedy-solution {
  font-size: 0.9rem;
  font-weight: 600;
  color: #667eea;
}

.recipe-item {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  padding: 10px;
  background: #f7fafc;
  border-radius: 8px;
}

.constitution-tag {
  font-size: 0.85rem;
  font-weight: 600;
  padding: 4px 12px;
  border-radius: 12px;
  white-space: nowrap;
}

.constitution-tag.yang-deficiency {
  background: linear-gradient(135deg, #feca57, #ff9ff3);
  color: #2d3748;
}

.constitution-tag.yin-deficiency {
  background: linear-gradient(135deg, #48dbfb, #0abde3);
  color: white;
}

.constitution-tag.phlegm-dampness {
  background: linear-gradient(135deg, #1dd1a1, #55a3ff);
  color: white;
}

.recipe-name {
  font-size: 0.95rem;
  color: #4a5568;
  font-weight: 500;
}

.solar-term-selector {
  margin-bottom: 20px;
}

.solar-term-info {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  padding: 20px;
  border-radius: 12px;
  border-left: 4px solid #667eea;
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.current-term {
  font-size: 1.1rem;
  color: #2d3748;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.current-term strong {
  color: #667eea;
  font-size: 1.3rem;
}

.term-theme {
  display: inline-block;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.term-tip {
  font-size: 0.95rem;
  color: #4a5568;
  margin-bottom: 15px;
  line-height: 1.6;
}

.recommend-recipe {
  display: flex;
  align-items: center;
  gap: 8px;
}

.recipe-label {
  font-size: 0.9rem;
  color: #718096;
}

.recipe-highlight {
  font-size: 1rem;
  color: #764ba2;
  font-weight: 700;
}

.acupoint-section {
  margin-top: 18px;
  padding-top: 18px;
  border-top: 1px dashed #cbd5e0;
}

.acupoint-title {
  font-size: 1rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 12px;
}

.acupoint-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.acupoint-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 12px;
  background: white;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.acupoint-item:hover {
  background: #edf2f7;
  transform: translateX(5px);
}

.acupoint-name {
  font-size: 0.9rem;
  font-weight: 700;
  color: #667eea;
}

.acupoint-effect {
  font-size: 0.85rem;
  color: #718096;
}

.remedy-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  background: #f7fafc;
  border-radius: 8px;
  margin-bottom: 10px;
}

.symptom {
  font-size: 0.95rem;
  color: #2d3748;
  font-weight: 600;
}

.solution {
  font-size: 0.9rem;
  color: #667eea;
  font-weight: 600;
}

.scenario-btn {
  width: 100%;
  border-radius: 20px;
  font-weight: 600;
}

/* ========== 板块二：养生不费力 ========== */
.easy-wellness-section {
  padding: 100px 0;
  background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
}

.tools-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 40px;
}

.tool-card {
  background: white;
  border-radius: 24px;
  padding: 45px 40px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
}

.tool-card::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.05) 0%, transparent 70%);
  transform: scale(0);
  transition: transform 0.6s ease;
}

.tool-card:hover::before {
  transform: scale(1);
}

.tool-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 25px 60px rgba(102, 126, 234, 0.2);
}

.tool-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.tool-icon {
  font-size: 4rem;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea, #764ba2);
  border-radius: 20px;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
  flex-shrink: 0;
}

.tool-card-secondary .tool-icon {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
}

.tool-title-group {
  flex: 1;
}

.tool-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #2d3748;
  margin-bottom: 8px;
}

.tool-tagline {
  font-size: 1rem;
  color: #718096;
  line-height: 1.5;
}

.tool-content {
  margin-bottom: 30px;
  position: relative;
  z-index: 1;
}

.tool-feature {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.feature-badge {
  background: linear-gradient(135deg, #ffd700, #ffed4a);
  color: #2d3748;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 700;
}

.feature-text {
  font-size: 1rem;
  color: #4a5568;
}

.testimonial-quote {
  background: #f7fafc;
  padding: 15px 20px;
  border-radius: 12px;
  border-left: 4px solid #667eea;
  font-size: 1rem;
  color: #2d3748;
  font-style: italic;
  line-height: 1.6;
}

.quote-author {
  display: block;
  margin-top: 8px;
  font-size: 0.85rem;
  color: #718096;
  font-style: normal;
}

.plan-preview {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  padding: 20px;
  border-radius: 12px;
  margin-bottom: 15px;
}

.plan-title {
  font-size: 1.05rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 12px;
}

.plan-item {
  font-size: 0.95rem;
  color: #4a5568;
  padding: 8px 0;
  border-bottom: 1px dashed #cbd5e0;
}

.plan-item:last-child {
  border-bottom: none;
}

.plan-note {
  font-size: 0.9rem;
  color: #43e97b;
  font-weight: 600;
  text-align: center;
}

.tool-btn {
  width: 100%;
  height: 55px;
  font-size: 1.1rem;
  font-weight: 700;
  border-radius: 28px;
  position: relative;
  z-index: 1;
}

/* 失眠测评快速入口按钮 */
.insomnia-quick-btn {
  width: 100%;
  height: 45px;
  font-size: 0.9rem;
  font-weight: 600;
  border-radius: 22px;
  margin-top: 12px;
  position: relative;
  z-index: 1;
  background: linear-gradient(135deg, #fbbf24, #f59e0b) !important;
  border: none !important;
  color: white !important;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(251, 191, 36, 0.3);
}

.insomnia-quick-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(251, 191, 36, 0.5);
}

.quick-btn-icon {
  margin-right: 8px;
  font-size: 1.1rem;
}

/* ========== 健康问题测评板块 ========== */
.health-assessment-section {
  padding: 100px 0;
  background: linear-gradient(135deg, #fff5f5 0%, #ffe3e3 100%);
  position: relative;
}

.assessment-cards-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  margin-bottom: 60px;
}

.assessment-card {
  background: white;
  border-radius: 24px;
  padding: 50px 35px;
  text-align: center;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
  transition: all 0.4s ease;
  position: relative;
  overflow: hidden;
  min-height: 320px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: space-between;
}

.assessment-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 5px;
  background: linear-gradient(90deg, #ff6b6b, #ee5a24);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.4s ease;
}

.assessment-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 25px 60px rgba(255, 107, 107, 0.2);
}

.assessment-card:hover::before {
  transform: scaleX(1);
}

.assessment-icon {
  font-size: 5rem;
  margin-bottom: 25px;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.1));
}

.assessment-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #2d3748;
  margin-bottom: 15px;
}

.assessment-description {
  font-size: 1.05rem;
  color: #718096;
  line-height: 1.8;
  margin-bottom: 30px;
  flex-grow: 1;
}

.assessment-btn {
  width: 100%;
  height: 55px;
  font-size: 1.1rem;
  font-weight: 700;
  border-radius: 28px;
  background: linear-gradient(45deg, #ff6b6b, #ee5a24) !important;
  border: none !important;
  box-shadow: 0 8px 20px rgba(255, 107, 107, 0.3);
  transition: all 0.3s ease;
}

.assessment-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 12px 30px rgba(255, 107, 107, 0.5);
}

/* 开发中状态的卡片 */
.card-developing {
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  opacity: 0.75;
  cursor: not-allowed;
}

.card-developing:hover {
  transform: none;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
}

.card-developing::before {
  background: linear-gradient(90deg, #cbd5e0, #a0aec0);
}

.developing-badge {
  display: inline-block;
  background: linear-gradient(45deg, #ffd700, #ffed4a);
  color: #2d3748;
  padding: 12px 40px;
  border-radius: 28px;
  font-size: 1rem;
  font-weight: 700;
  width: 100%;
  text-align: center;
  box-shadow: 0 4px 12px rgba(255, 215, 0, 0.3);
}

/* 底部提示区域 */
.assessment-footer {
  text-align: center;
  padding: 40px 0 0;
  border-top: 2px dashed #ffd7d7;
}

.assessment-footer-text {
  font-size: 1.4rem;
  color: #4a5568;
  font-weight: 600;
  margin-bottom: 25px;
}

.consult-btn {
  height: 60px;
  padding: 0 60px;
  font-size: 1.2rem;
  font-weight: 700;
  border-radius: 30px;
  background: linear-gradient(45deg, #43e97b, #38f9d7) !important;
  border: none !important;
  box-shadow: 0 10px 30px rgba(67, 233, 123, 0.3);
  transition: all 0.3s ease;
}

.consult-btn:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 15px 40px rgba(67, 233, 123, 0.5);
}

/* 健康测评板块移动端适配 */
@media (max-width: 1200px) {
  .assessment-cards-grid {
    grid-template-columns: 1fr;
    gap: 30px;
  }
}

@media (max-width: 768px) {
  .health-assessment-section {
    padding: 60px 0;
  }

  .assessment-card {
    padding: 40px 30px;
    min-height: 280px;
  }

  .assessment-icon {
    font-size: 4rem;
  }

  .assessment-title {
    font-size: 1.5rem;
  }

  .assessment-description {
    font-size: 1rem;
  }

  .assessment-btn,
  .developing-badge {
    height: 50px;
    font-size: 1rem;
    padding: 12px 30px;
  }

  .assessment-footer-text {
    font-size: 1.2rem;
  }

  .consult-btn {
    height: 50px;
    padding: 0 40px;
    font-size: 1rem;
  }
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

/* ========== 核心服务快捷入口区 ========== */
.service-shortcut-section {
  background: linear-gradient(135deg, #f5f7fa 0%, #e8eef5 100%);
  padding: 80px 0;
  position: relative;
  overflow: hidden;
}

.service-shortcut-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><circle cx="50" cy="50" r="1" fill="rgba(102,126,234,0.05)"/></svg>');
  background-size: 30px 30px;
  opacity: 0.3;
}

.service-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px;
  position: relative;
  z-index: 1;
}

.service-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 40px;
}

.service-card {
  background: white;
  border-radius: 24px;
  padding: 50px 30px;
  text-align: center;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
  position: relative;
  overflow: hidden;
}

.service-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05), rgba(118, 75, 162, 0.05));
  opacity: 0;
  transition: opacity 0.4s ease;
}

.service-card:hover {
  transform: translateY(-12px) scale(1.03);
  box-shadow: 0 20px 50px rgba(102, 126, 234, 0.2);
}

.service-card:hover::before {
  opacity: 1;
}

.service-icon {
  width: 100px;
  height: 100px;
  margin: 0 auto 25px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.4s ease;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
}

.service-card:hover .service-icon {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 12px 30px rgba(102, 126, 234, 0.5);
}

.icon-emoji {
  font-size: 3rem;
  filter: drop-shadow(0 2px 4px rgba(0, 0, 0, 0.2));
}

.service-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 15px;
  position: relative;
  z-index: 1;
}

.service-desc {
  font-size: 1rem;
  color: #718096;
  line-height: 1.6;
  position: relative;
  z-index: 1;
}

/* 不同卡片的渐变色 */
.service-card:nth-child(1) .service-icon {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.service-card:nth-child(2) .service-icon {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
}

.service-card:nth-child(3) .service-icon {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
}

.service-card:nth-child(4) .service-icon {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
}

/* 核心服务区移动端适配 */
@media (max-width: 1200px) {
  .service-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 30px;
  }
}

@media (max-width: 768px) {
  .service-shortcut-section {
    padding: 60px 0;
  }

  .service-container {
    padding: 0 20px;
  }

  .service-grid {
    grid-template-columns: 1fr;
    gap: 25px;
  }

  .service-card {
    padding: 40px 25px;
  }

  .service-icon {
    width: 80px;
    height: 80px;
    margin-bottom: 20px;
  }

  .icon-emoji {
    font-size: 2.5rem;
  }

  .service-title {
    font-size: 1.3rem;
  }

  .service-desc {
    font-size: 0.95rem;
  }
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
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.05) 0%, rgba(255, 255, 255, 0.05) 100%);
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
  font-size: 5rem;
  font-weight: 900;
  margin-bottom: 30px;
  letter-spacing: 3px;
  animation: fadeInUp 1s ease-out;
  line-height: 1.2;
  display: inline-block;
  background: rgba(102, 126, 234, 0.9);
  color: white;
  padding: 15px 35px;
  border-radius: 12px;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.3);
}

.brand-slogan {
  font-size: 2rem;
  margin-top: 25px;
  margin-bottom: 20px;
  font-weight: 600;
  letter-spacing: 1px;
  animation: fadeInUp 1s ease-out 0.2s both;
  display: inline-block;
  background: rgba(255, 215, 0, 0.95);
  color: #2d3748;
  padding: 12px 30px;
  border-radius: 10px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.25);
  line-height: 1.6;
}

.brand-description {
  font-size: 1.6rem;
  margin-top: 20px;
  margin-bottom: 40px;
  font-weight: 600;
  animation: fadeInUp 1s ease-out 0.4s both;
  display: inline-block;
  background: rgba(255, 255, 255, 0.95);
  color: #2d3748;
  padding: 10px 28px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.cta-button-wrapper {
  margin-top: 40px;
  animation: fadeInUp 1s ease-out 0.6s both;
}

.hero-cta-button {
  font-size: 1.4rem;
  font-weight: 700;
  padding: 20px 60px;
  height: auto;
  border-radius: 50px;
  background: linear-gradient(45deg, #ff6b6b, #ee5a24) !important;
  border: none !important;
  color: white !important;
  box-shadow: 0 12px 35px rgba(255, 107, 107, 0.5);
  transition: all 0.4s ease;
  cursor: pointer;
}

.hero-cta-button:hover {
  transform: translateY(-5px) scale(1.05);
  box-shadow: 0 18px 45px rgba(255, 107, 107, 0.7);
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

  .brand-slogan {
    font-size: 1.4rem;
    padding: 10px 24px;
  }

  .brand-description {
    font-size: 1.2rem;
    padding: 8px 20px;
  }

  .cta-button-wrapper {
    margin-top: 30px;
  }

  .hero-cta-button {
    font-size: 1.2rem;
    padding: 16px 40px;
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

/* ========== 板块三：专业支持 ========== */
.professional-support-section {
  padding: 100px 0;
  background: linear-gradient(135deg, #f6f9fc 0%, #e9f0f5 100%);
}

.support-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 40px;
}

.support-card {
  background: white;
  border-radius: 24px;
  padding: 45px 40px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
  transition: all 0.4s ease;
}

.support-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.12);
}

.support-title {
  font-size: 1.8rem;
  font-weight: 800;
  color: #2d3748;
  margin-bottom: 15px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.title-icon {
  font-size: 2rem;
}

.support-slogan {
  font-size: 1.05rem;
  color: #718096;
  margin-bottom: 30px;
  font-weight: 500;
}

.prevention-list,
.expert-list {
  margin-bottom: 30px;
}

.prevention-item {
  padding: 18px;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border-radius: 12px;
  margin-bottom: 15px;
  border-left: 4px solid #43e97b;
  transition: all 0.3s ease;
}

.prevention-item:hover {
  transform: translateX(8px);
  box-shadow: 0 8px 20px rgba(67, 233, 123, 0.15);
}

.crowd-tag {
  font-size: 1rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 8px;
}

.prevention-tip {
  font-size: 0.95rem;
  color: #4a5568;
  line-height: 1.6;
}

.expert-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 18px;
  background: linear-gradient(135deg, #f8f9fa, #e9ecef);
  border-radius: 12px;
  margin-bottom: 15px;
  transition: all 0.3s ease;
}

.expert-item:hover {
  transform: translateX(8px);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
}

.expert-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 700;
  flex-shrink: 0;
}

.expert-info {
  flex: 1;
}

.expert-name {
  font-size: 1.1rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 5px;
}

.expert-skill {
  font-size: 0.9rem;
  color: #718096;
}

.expert-note {
  font-size: 0.9rem;
  color: #667eea;
  font-weight: 600;
  text-align: center;
  margin-bottom: 20px;
}

.support-btn {
  width: 100%;
  height: 50px;
  font-size: 1.05rem;
  font-weight: 700;
  border-radius: 25px;
}

/* ========== 板块四：学习变专家 ========== */
.growth-path-section {
  padding: 100px 0;
  background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
}

.growth-ladder {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 35px;
  margin-bottom: 60px;
}

.ladder-step {
  background: white;
  border-radius: 24px;
  padding: 40px 35px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
  position: relative;
  transition: all 0.4s ease;
}

.ladder-step::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: 24px;
  padding: 3px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-mask: linear-gradient(#fff 0 0) content-box, linear-gradient(#fff 0 0);
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0;
  transition: opacity 0.4s ease;
}

.ladder-step:hover::before {
  opacity: 1;
}

.ladder-step:hover {
  transform: translateY(-10px) scale(1.02);
  box-shadow: 0 20px 50px rgba(102, 126, 234, 0.2);
}

.step-badge {
  display: inline-block;
  background: linear-gradient(135deg, #ffd700, #ffed4a);
  color: #2d3748;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 700;
  margin-bottom: 20px;
}

.step-2 .step-badge {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
}

.step-3 .step-badge {
  background: linear-gradient(135deg, #43e97b, #38f9d7);
  color: white;
}

.step-title {
  font-size: 1.2rem;
  font-weight: 800;
  color: #2d3748;
  margin-bottom: 25px;
  text-align: center;
  line-height: 1.6;
}

.step-content {
  margin-bottom: 25px;
  min-height: 80px;
}

.learning-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px;
  background: #f7fafc;
  border-radius: 10px;
  margin-bottom: 12px;
  transition: all 0.3s ease;
}

.learning-item:hover {
  background: #edf2f7;
  transform: translateX(5px);
}

.item-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.item-name {
  font-size: 0.95rem;
  color: #4a5568;
  line-height: 1.6;
  font-weight: 500;
}

.step-description {
  font-size: 1rem;
  color: #4a5568;
  line-height: 1.8;
  text-align: center;
  padding: 8px 10px;
  margin: 0;
  font-weight: 500;
}

.step-btn {
  width: 100%;
  height: 50px;
  font-size: 1.05rem;
  font-weight: 700;
  border-radius: 25px;
}

.growth-footer {
  text-align: center;
  padding: 50px 40px;
  background: white;
  border-radius: 24px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
}

.footer-slogan {
  font-size: 2.2rem;
  font-weight: 800;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1.5;
}

/* ========== 板块三：执行最重要 ========== */
.execution-section {
  padding: 100px 0;
  background: linear-gradient(135deg, #e0f7fa 0%, #b2ebf2 100%);
}

.case-studies-title {
  text-align: center;
  margin-bottom: 50px;
}

.case-studies-title h3 {
  font-size: 2rem;
  font-weight: 700;
  color: #2d3748;
  position: relative;
  display: inline-block;
}

.case-studies-title h3::after {
  content: '';
  position: absolute;
  bottom: -10px;
  left: 50%;
  transform: translateX(-50%);
  width: 60%;
  height: 3px;
  background: linear-gradient(90deg, #00acc1, #26c6da);
  border-radius: 2px;
}

.case-studies-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 40px;
  margin-bottom: 60px;
}

.case-card {
  background: white;
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: all 0.4s ease;
}

.case-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 20px 50px rgba(0, 188, 212, 0.2);
}

.case-image-wrapper {
  height: 240px;
  background: linear-gradient(135deg, #e0f2f1 0%, #b2dfdb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
}

.case-image-placeholder {
  text-align: center;
  padding: 20px;
}

.placeholder-icon {
  font-size: 4rem;
  margin-bottom: 15px;
  opacity: 0.8;
}

.placeholder-text {
  font-size: 1rem;
  color: #546e7a;
  font-weight: 600;
  line-height: 1.6;
}

.case-content {
  padding: 30px 25px;
}

.case-badge {
  display: inline-block;
  background: linear-gradient(135deg, #00acc1, #26c6da);
  color: white;
  padding: 6px 16px;
  border-radius: 15px;
  font-size: 0.85rem;
  font-weight: 700;
  margin-bottom: 15px;
}

.case-quote {
  font-size: 1.05rem;
  color: #2d3748;
  line-height: 1.7;
  margin-bottom: 15px;
  font-weight: 500;
  font-style: italic;
}

.case-author {
  font-size: 0.9rem;
  color: #718096;
  text-align: right;
  font-weight: 600;
}

/* 小程序功能亮点 */
.miniprogram-features {
  background: white;
  border-radius: 20px;
  padding: 40px;
  margin-bottom: 50px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
}

.features-title {
  font-size: 1.6rem;
  font-weight: 700;
  color: #2d3748;
  text-align: center;
  margin-bottom: 35px;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 30px;
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 25px 20px;
  background: linear-gradient(135deg, #e0f2f1, #b2dfdb);
  border-radius: 16px;
  transition: all 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 25px rgba(0, 188, 212, 0.2);
}

.feature-icon {
  font-size: 2.5rem;
}

.feature-text {
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
  text-align: center;
  line-height: 1.4;
}

/* 扫码引导 */
.miniprogram-cta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: linear-gradient(135deg, #ffffff, #f0f9ff);
  border-radius: 24px;
  padding: 50px 60px;
  box-shadow: 0 15px 40px rgba(0, 0, 0, 0.1);
  gap: 60px;
}

.qr-section {
  text-align: center;
  flex-shrink: 0;
}

.qr-placeholder {
  width: 200px;
  height: 200px;
  background: white;
  border-radius: 16px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
}

.qr-icon {
  font-size: 4rem;
  margin-bottom: 10px;
}

.qr-placeholder p {
  font-size: 0.95rem;
  color: #718096;
  font-weight: 600;
}

.qr-tip {
  font-size: 1rem;
  color: #00acc1;
  font-weight: 700;
}

.cta-text {
  flex: 1;
}

.cta-text h3 {
  font-size: 2rem;
  font-weight: 800;
  color: #2d3748;
  margin-bottom: 15px;
  line-height: 1.4;
}

.cta-text p {
  font-size: 1.1rem;
  color: #4a5568;
  margin-bottom: 30px;
  line-height: 1.6;
}

.execution-cta-btn {
  height: 60px;
  padding: 0 50px;
  font-size: 1.2rem;
  font-weight: 700;
  border-radius: 30px;
  background: linear-gradient(45deg, #00acc1, #26c6da) !important;
  border: none !important;
  box-shadow: 0 10px 30px rgba(0, 172, 193, 0.3);
}

.execution-cta-btn:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(0, 172, 193, 0.4);
}

/* 四大板块移动端适配 */
@media (max-width: 1200px) {
  .scenario-grid {
    grid-template-columns: 1fr;
  }

  .tools-grid {
    grid-template-columns: 1fr;
  }

  .support-grid {
    grid-template-columns: 1fr;
  }

  .growth-ladder {
    grid-template-columns: 1fr;
  }

  .case-studies-grid {
    grid-template-columns: 1fr;
  }

  .features-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .miniprogram-cta {
    flex-direction: column;
    gap: 40px;
  }
}

@media (max-width: 768px) {
  .life-scenario-section,
  .easy-wellness-section,
  .professional-support-section,
  .execution-section,
  .growth-path-section {
    padding: 60px 0;
  }

  .section-container {
    padding: 0 20px;
  }

  .section-title-group {
    margin-bottom: 40px;
  }

  .main-section-title {
    font-size: 2rem;
  }

  .main-section-subtitle {
    font-size: 1rem;
  }

  .scenario-card,
  .tool-card,
  .support-card,
  .ladder-step {
    padding: 30px 25px;
  }

  .scenario-icon {
    font-size: 2.8rem;
  }

  .recipe-images-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
  }

  .recipe-overlay {
    font-size: 0.8rem;
    padding: 10px 8px 6px;
    transform: translateY(0);
  }

  .remedy-images-grid {
    gap: 10px;
  }

  .remedy-img {
    height: 100px;
  }

  .remedy-info {
    padding: 10px 12px;
  }

  .remedy-symptom {
    font-size: 0.85rem;
  }

  .remedy-solution {
    font-size: 0.8rem;
  }

  .solar-term-selector {
    margin-bottom: 15px;
  }

  .current-term {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .term-theme {
    font-size: 0.75rem;
  }

  .acupoint-section {
    margin-top: 15px;
    padding-top: 15px;
  }

  .acupoint-title {
    font-size: 0.9rem;
  }

  .acupoint-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 5px;
    padding: 10px;
  }

  .acupoint-name {
    font-size: 0.85rem;
  }

  .acupoint-effect {
    font-size: 0.75rem;
  }

  .scenario-title,
  .tool-title,
  .support-title,
  .step-title {
    font-size: 1.4rem;
  }

  .tool-header {
    flex-direction: column;
    text-align: center;
  }

  .tool-icon {
    width: 70px;
    height: 70px;
    font-size: 3rem;
  }

  .growth-footer {
    padding: 35px 25px;
  }

  .footer-slogan {
    font-size: 1.6rem;
  }

  /* 执行板块移动端适配 */
  .case-studies-title h3 {
    font-size: 1.5rem;
  }

  .case-image-wrapper {
    height: 200px;
  }

  .placeholder-icon {
    font-size: 3rem;
  }

  .placeholder-text {
    font-size: 0.9rem;
  }

  .case-content {
    padding: 25px 20px;
  }

  .case-quote {
    font-size: 1rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .features-title {
    font-size: 1.3rem;
  }

  .miniprogram-features {
    padding: 30px 20px;
  }

  .miniprogram-cta {
    padding: 35px 25px;
    flex-direction: column;
    text-align: center;
  }

  .qr-placeholder {
    width: 180px;
    height: 180px;
  }

  .qr-icon {
    font-size: 3rem;
  }

  .cta-text h3 {
    font-size: 1.5rem;
  }

  .cta-text p {
    font-size: 1rem;
  }

  .execution-cta-btn {
    height: 50px;
    font-size: 1rem;
    padding: 0 40px;
  }
}
</style>