<template>
  <div class="about-story">
    <!-- 左侧固定导航栏 -->
    <div class="sidebar-nav">
      <div class="sidebar-header">
        <h3>关于芮艾</h3>
      </div>
      <div class="sidebar-menu">
        <div
          v-for="(section, index) in sections"
          :key="index"
          class="menu-item"
          :class="{ active: currentPage === index }"
          @click="goToPage(index)"
        >
          <div class="menu-dot"></div>
          <div class="menu-text">{{ section.name }}</div>
        </div>
      </div>
    </div>

    <!-- 主要内容区域 -->
    <div class="main-content">

    <!-- 页面进度指示器 -->
    <div class="page-indicator">
      <span class="current">{{ currentPage + 1 }}</span>
      <span class="separator">/</span>
      <span class="total">{{ sections.length }}</span>
    </div>

    <!-- 左右切换按钮 -->
    <div class="page-nav-buttons">
      <!-- 上一页按钮 -->
      <button
        class="page-nav-btn prev-btn"
        :class="{ disabled: currentPage === 0 }"
        @click="goToPrevPage"
        :disabled="currentPage === 0"
      >
        <el-icon><ArrowLeft /></el-icon>
      </button>

      <!-- 下一页按钮 -->
      <button
        class="page-nav-btn next-btn"
        :class="{ disabled: currentPage === sections.length - 1 }"
        @click="goToNextPage"
        :disabled="currentPage === sections.length - 1"
      >
        <el-icon><ArrowRight /></el-icon>
      </button>
    </div>

    <!-- 板块容器 - 每次只显示一个 -->
    <div class="pages-container">

      <!-- 板块1: Hero 开篇 -->
      <section v-show="currentPage === 0" class="page-content hero-section">
        <div class="hero-overlay"></div>
        <div class="hero-content">
          <div class="stats-row">
            <div class="stat-item">
              <div class="stat-number">{{ displayStats.unhealthy }}%</div>
              <div class="stat-label">亚健康人群</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ displayStats.chronic }}亿</div>
              <div class="stat-label">慢病人群</div>
            </div>
            <div class="stat-item">
              <div class="stat-number">{{ displayStats.talents }}+</div>
              <div class="stat-label">中医人才</div>
            </div>
          </div>

          <h1 class="hero-title">
            当75%的人被亚健康困扰，3.3亿人需要终身服药<br>
            我们开始思考：中医的千年智慧，如何守护现代人的健康？
          </h1>

          <p class="hero-subtitle">
            用"中医+科技"打造全周期健康管理方案<br>
            让你不用排队挂号，5分钟找到调理方案<br>
            不用依赖药物，从食疗到理疗找到适配方案
          </p>

          <el-button type="success" size="large" class="hero-cta" @click="goToPage(7)">
            <el-icon><Guide /></el-icon>
            立即免费测评
          </el-button>
        </div>
      </section>

      <!-- 板块2: 初心故事 -->
      <section v-show="currentPage === 1" class="page-content story-section origin-story">
        <h2 class="section-title">
          <el-icon><Sunny /></el-icon>
          我们为何踏上中医健康创新路
        </h2>

        <div class="story-content">
          <div class="story-intro">
            <p class="highlight-text">2019年，我们发现一些中医的现实：</p>
          </div>

          <el-row :gutter="40" class="problems-row">
            <el-col :xs="24" :md="12">
              <div class="problem-card">
                <div class="problem-icon">📚</div>
                <h3>困境一：年轻中医群体的困惑</h3>
                <ul>
                  <li>空有理论却难转换成可应用的技术</li>
                  <li>好的中医技术被困在"老师傅经验里"</li>
                  <li>缺乏系统的临床思维培训</li>
                </ul>
              </div>
            </el-col>
            <el-col :xs="24" :md="12">
              <div class="problem-card">
                <div class="problem-icon">😰</div>
                <h3>困境二：普通百姓的无奈</h3>
                <ul>
                  <li>75%的人被亚健康缠上</li>
                  <li>3.3亿慢病人群终身服药</li>
                  <li>看中医依赖个人经验，换医生方案就"断档"</li>
                  <li>买了健康产品没人跟进，体质变了无新方案</li>
                </ul>
              </div>
            </el-col>
          </el-row>

          <div class="decision-card">
            <div class="decision-icon">💡</div>
            <h3>我们的决定</h3>
            <p class="decision-text">
              中医的千年智慧不该是"小众宝藏"，更不该是"不稳定的个人经验"
            </p>
            <div class="solution-flow">
              <div class="flow-item">
                <el-icon><Platform /></el-icon>
                <span>用现代科技系统化</span>
              </div>
              <el-icon class="flow-arrow"><DArrowRight /></el-icon>
              <div class="flow-item">
                <el-icon><Location /></el-icon>
                <span>用连锁服务送到身边</span>
              </div>
              <el-icon class="flow-arrow"><DArrowRight /></el-icon>
              <div class="flow-item">
                <el-icon><User /></el-icon>
                <span>让普通人轻松管好健康</span>
              </div>
            </div>
          </div>

          <div class="first-step-card">
            <h3>
              <el-icon><Trophy /></el-icon>
              第一步：扎根人才培养
            </h3>
            <el-row :gutter="20" class="achievements">
              <el-col :xs="12" :sm="6">
                <div class="achievement-item">
                  <div class="achievement-number">20+</div>
                  <div class="achievement-label">临床培训班</div>
                </div>
              </el-col>
              <el-col :xs="12" :sm="6">
                <div class="achievement-item">
                  <div class="achievement-number">2000+</div>
                  <div class="achievement-label">中医人才</div>
                </div>
              </el-col>
              <el-col :xs="12" :sm="6">
                <div class="achievement-item">
                  <div class="achievement-number">全国</div>
                  <div class="achievement-label">医生特训营</div>
                </div>
              </el-col>
              <el-col :xs="12" :sm="6">
                <div class="achievement-item">
                  <div class="achievement-number">进大学</div>
                  <div class="achievement-label">培训进校园</div>
                </div>
              </el-col>
            </el-row>
            <p class="achievement-desc">
              看着2000多名年轻中医从"会理论"变成"能实战"，能独立用"十字中医辨证""醒髓疗法"帮患者解决问题，我们知道：这条"让中医惠及全民"的路，算走对了第一步。
            </p>
          </div>
        </div>
      </section>

      <!-- 板块3: 服务故事 - 3个真实案例 -->
      <section v-show="currentPage === 2" class="story-section service-stories">
        <h2 class="section-title">
          <el-icon><ChatLineRound /></el-icon>
          我们如何帮用户解决真实健康烦恼
        </h2>

        <el-row :gutter="30" class="cases-row">
          <el-col :xs="24" :md="8" v-for="(caseItem, index) in userCases" :key="index">
            <el-card class="case-card" shadow="hover" @click="showCaseDetail(caseItem)">
              <div class="case-header">
                <div class="case-avatar">{{ caseItem.avatar }}</div>
                <div class="case-user">
                  <div class="user-name">{{ caseItem.name }}</div>
                  <div class="user-age">{{ caseItem.age }}岁 | {{ caseItem.profession }}</div>
                </div>
              </div>

              <div class="case-problem">
                <div class="problem-label">😰 痛点</div>
                <p>{{ caseItem.problem }}</p>
              </div>

              <div class="case-solution">
                <div class="solution-label">💡 方案</div>
                <ul>
                  <li v-for="(item, i) in caseItem.solution" :key="i">{{ item }}</li>
                </ul>
              </div>

              <div class="case-result">
                <div class="result-label">✅ 结果</div>
                <p class="result-text">{{ caseItem.result }}</p>
              </div>

              <div class="case-feedback">
                <div class="feedback-icon">"</div>
                <p class="feedback-text">{{ caseItem.feedback }}</p>
                <div class="feedback-author">—— {{ caseItem.name }}</div>
              </div>

              <el-button text type="primary" class="detail-btn">
                查看完整故事 <el-icon><ArrowRight /></el-icon>
              </el-button>
            </el-card>
          </el-col>
        </el-row>
      </section>

      <!-- 板块4: 差异故事 -->
      <section v-show="currentPage === 3" class="story-section difference-story">
        <div class="question-intro">
          <h2 class="main-question">
            <el-icon><MagicStick /></el-icon>
            我们和中医馆、健康产品公司有啥不一样？
          </h2>
          <p class="answer-intro">其实答案就藏在两个"解决用户痛点"的细节里</p>
        </div>

         <el-row :gutter="40" class="comparison-row">
          <el-col :xs="24" :md="12">
            <div class="pain-point-card">
              <div class="pain-icon">🔬</div>
              <h3>痛点1：中医调理不稳定</h3>
              <div class="traditional-way">
                <div class="label">❌ 传统：</div>
                <p>A医生开安神汤，B医生改疏肝方，不知道该信谁</p>
              </div>
              <div class="ruiai-way">
                <div class="label">✅ 我们：</div>
                <ul>
                  <li>线上智能诊断平台（3年搭建）</li>
                  <li>老中医辨证逻辑 → 标准化专业量表</li>
                  <li>AI算法生成方案 + 专家团队把关</li>
                  <li>统一诊断体系，避免"一人一策"混乱</li>
                </ul>
              </div>
            </div>
          </el-col>

          <el-col :xs="24" :md="12">
            <div class="pain-point-card">
              <div class="pain-icon">🔗</div>
              <h3>痛点2：健康服务断链条</h3>
              <div class="traditional-way">
                <div class="label">❌ 传统：</div>
                <p>吃药为主，没有更完善的整体方案</p>
              </div>
              <div class="ruiai-way">
                <div class="label">✅ 我们：</div>
                <ul>
                  <li>测评 → 动态方案 → 适配产品（中药+食疗+理疗）</li>
                  <li>社区交流 + 实时监测</li>
                  <li>体质变化自动提醒医生更新方案</li>
                  <li>像"健康管家"一样长期陪伴</li>
                </ul>
              </div>
            </div>
          </el-col>
        </el-row>

        <div class="service-flow-card">
          <h3>健康服务闭环</h3>
          <div class="flow-diagram">
            <div class="flow-step" v-for="(step, index) in serviceFlow" :key="index">
              <div class="step-icon">{{ step.icon }}</div>
              <div class="step-title">{{ step.title }}</div>
              <div class="step-desc">{{ step.desc }}</div>
              <el-icon v-if="index < serviceFlow.length - 1" class="step-arrow"><DArrowRight /></el-icon>
            </div>
          </div>
          <p class="flow-summary">
            我们不只是"提供健康服务"，更是"陪用户长期守护健康"
          </p>
        </div>
      </section>

      <!-- 板块5: 信任背书 -->
      <section v-show="currentPage === 4" class="story-section trust-section">
        <h2 class="section-title">
          <el-icon><Medal /></el-icon>
          凭什么相信我们
        </h2>

        <!-- 人才硬实力 -->
        <div class="talent-strength">
          <h3 class="subsection-title">
            <el-icon><User /></el-icon>
            人才硬实力
          </h3>
          <p class="subsection-desc">不止说"有多少人"，更说"人有多专业"</p>

          <div class="strength-stats">
            <div class="strength-stat">
              <div class="stat-num">2000+</div>
              <div class="stat-desc">中医人才输送</div>
            </div>
            <div class="strength-stat">
              <div class="stat-num">20期</div>
              <div class="stat-desc">临床培训班</div>
            </div>
            <div class="strength-stat">
              <div class="stat-num">100%</div>
              <div class="stat-desc">专项培训通过</div>
            </div>
            <div class="strength-stat">
              <div class="stat-num">全国</div>
              <div class="stat-desc">医生特训营</div>
            </div>
          </div>

          <div class="certification-text">
            <p>
              <el-icon><Select /></el-icon>
              所有医生通过"十字中医辨证""醒髓疗法"等专项培训
            </p>
            <p>
              <el-icon><Select /></el-icon>
              临床培训进大学校园，输送优质中医力量
            </p>
          </div>
        </div>

        <!-- 用户真实反馈 -->
        <div class="user-feedback">
          <h3 class="subsection-title">
            <el-icon><ChatDotRound /></el-icon>
            用户真实反馈
          </h3>
          <p class="subsection-desc">细节化评价，避免"空洞好评"</p>

          <div class="feedback-list">
            <div class="feedback-item" v-for="(item, index) in feedbacks" :key="index">
              <div class="feedback-avatar">{{ item.avatar }}</div>
              <div class="feedback-content">
                <div class="feedback-quote">"{{ item.content }}"</div>
                <div class="feedback-meta">
                  <span class="feedback-name">{{ item.name }}</span>
                  <span class="feedback-tag">{{ item.tag }}</span>
                  <el-rate v-model="item.rating" disabled show-score text-color="#ff9900" />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 行业与政策认可 -->
        <div class="policy-recognition">
          <h3 class="subsection-title">
            <el-icon><Document /></el-icon>
            行业与政策认可
          </h3>
          <el-card class="recognition-card" shadow="hover">
            <div class="recognition-content">
              <el-icon class="recognition-icon" :size="60" color="#409EFF"><Flag /></el-icon>
              <div class="recognition-text">
                <h4>响应"健康中国2030"战略</h4>
                <p>聚焦"生命周期健康服务"，中西医结合的方案符合国家大健康发展方向</p>
                <ul>
                  <li>推动中医食养一体化</li>
                  <li>构建全生命周期健康生态</li>
                  <li>探索轻资产连锁健康服务模式</li>
                </ul>
              </div>
            </div>
          </el-card>
        </div>
      </section>

      <!-- 板块6: 发展历程 -->
      <section v-show="currentPage === 5" class="story-section history-section">
        <h2 class="section-title">
          <el-icon><Calendar /></el-icon>
          发展历程
        </h2>

        <div class="timeline-modern">
          <div class="timeline-item-modern" v-for="(item, index) in timeline" :key="index">
            <!-- 左侧：年份+图标 -->
            <div class="timeline-left">
              <div class="timeline-year-box">{{ item.year }}</div>
              <div class="timeline-icon-box">{{ item.icon }}</div>
            </div>

            <!-- 右侧：内容 -->
            <div class="timeline-right">
              <div class="timeline-content-card">
                <h3>{{ item.title }}</h3>
                <p>{{ item.desc }}</p>

                <div class="timeline-tags" v-if="item.tags">
                  <el-tag v-for="(tag, i) in item.tags" :key="i" :type="item.tagType" effect="plain">
                    {{ tag }}
                  </el-tag>
                </div>

                <div class="timeline-stats" v-if="item.stats">
                  <div class="stat" v-for="(stat, i) in item.stats" :key="i">
                    <span class="stat-num">{{ stat.num }}</span>
                    <span class="stat-label">{{ stat.label }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 板块7: 核心价值观 + 愿景 -->
      <section v-show="currentPage === 6" class="story-section values-vision-section">
        <div class="values-part">
          <h2 class="section-title">
            <el-icon><Star /></el-icon>
            核心价值观
          </h2>

          <el-row :gutter="24" class="values-row">
            <el-col :xs="12" :sm="6" v-for="(value, index) in values" :key="index">
              <el-card class="value-card" shadow="hover">
                <div class="value-icon" :style="{color: value.color}">
                  <component :is="value.icon" />
                </div>
                <h3>{{ value.title }}</h3>
                <p>{{ value.desc }}</p>
              </el-card>
            </el-col>
          </el-row>
        </div>

        <div class="vision-part">
          <h2 class="section-title">
            <el-icon><TrendCharts /></el-icon>
            发展愿景
          </h2>

          <el-row :gutter="30" class="vision-row">
            <el-col :xs="24" :md="8" v-for="(item, index) in visions" :key="index">
              <div class="vision-item">
                <div class="vision-icon">
                  <el-icon :size="50" :color="item.color"><component :is="item.icon" /></el-icon>
                </div>
                <div class="vision-content">
                  <h3 class="vision-title">{{ item.title }}</h3>
                  <p class="vision-desc">{{ item.desc }}</p>
                </div>
              </div>
            </el-col>
          </el-row>
        </div>
      </section>

      <!-- 板块8: 行动引导 + 情感结尾 -->
      <section v-show="currentPage === 7" class="story-section action-section">
        <div class="emotional-ending">
          <h2 class="ending-title">健康不是"治好了某病"，而是长期的身心平衡</h2>
          <p class="ending-text">
            我们不想做"你生病时才找的医生"<br>
            想做"陪你每天管健康的伙伴"
          </p>
          <p class="ending-detail">
            无论是社区驿站的一次理疗，还是线上的一份体质报告<br>
            都是我们想让"中医智慧"离你更近一点的努力
          </p>
          <p class="ending-call">
            如果你也认同"健康需要长期管"<br>
            不妨从一次免费测评开始，让我们一起，把健康握在自己手里
          </p>
        </div>

        <div class="action-cards">
          <el-row :gutter="30">
            <el-col :xs="24" :md="8">
              <el-card class="action-card light-action" shadow="hover">
                <div class="action-icon">🎁</div>
                <h3>轻行动</h3>
                <div class="action-buttons">
                  <el-button type="success" plain>领取免费测评</el-button>
                  <el-button type="success" plain>养生小课（10节）</el-button>
                </div>
              </el-card>
            </el-col>

            <el-col :xs="24" :md="8">
              <el-card class="action-card medium-action" shadow="hover">
                <div class="action-icon">🏥</div>
                <h3>中行动</h3>
                <div class="action-buttons">
                  <el-button type="primary" plain>预约体验理疗</el-button>
                  <el-button type="primary" plain>添加健康顾问</el-button>
                </div>
              </el-card>
            </el-col>

            <el-col :xs="24" :md="8">
              <el-card class="action-card high-action" shadow="hover">
                <div class="action-icon">💎</div>
                <h3>高行动</h3>
                <div class="action-buttons">
                  <el-button type="warning" plain>VIP定制方案</el-button>
                  <el-button type="warning" plain>1对1专家咨询</el-button>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>

        <div class="contact-info">
          <h3>联系我们</h3>
          <div class="contact-grid">
            <div class="contact-item">
              <el-icon><Location /></el-icon>
              <span>地址：待补充</span>
            </div>
            <div class="contact-item">
              <el-icon><Phone /></el-icon>
              <span>电话：待补充</span>
            </div>
            <div class="contact-item">
              <el-icon><Message /></el-icon>
              <span>邮箱：待补充</span>
            </div>
          </div>
        </div>
      </section>

    </div><!-- 关闭 pages-container -->

    <!-- 案例详情对话框 -->
    <el-dialog v-model="caseDialogVisible" :title="selectedCase?.name + '的健康故事'" width="800px">
      <div class="case-detail" v-if="selectedCase">
        <div class="detail-section">
          <h4>😰 遇到的问题</h4>
          <p>{{ selectedCase.problem }}</p>
        </div>
        <div class="detail-section">
          <h4>💡 我们的方案</h4>
          <ul>
            <li v-for="(item, i) in selectedCase.solution" :key="i">{{ item }}</li>
          </ul>
        </div>
        <div class="detail-section">
          <h4>✅ 调理结果</h4>
          <p>{{ selectedCase.result }}</p>
        </div>
        <div class="detail-section">
          <h4>💬 用户反馈</h4>
          <blockquote>"{{ selectedCase.feedback }}"</blockquote>
          <p class="author">—— {{ selectedCase.name }}（{{ selectedCase.age }}岁）</p>
        </div>
      </div>
    </el-dialog>
    </div><!-- 关闭 main-content -->
  </div><!-- 关闭 about-story -->
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, reactive } from 'vue'
import {
  Guide, Sunny, Platform, Location, User, Trophy, DArrowRight,
  ChatLineRound, ArrowRight, ArrowLeft, MagicStick, Medal, Select,
  ChatDotRound, Document, Flag, Calendar, Star, TrendCharts,
  Phone, Message, Aim, Connection
} from '@element-plus/icons-vue'

// 导航相关
const currentPage = ref(0)
const sections = ref([
  { name: '首页', id: 'section0' },
  { name: '初心故事', id: 'section1' },
  { name: '服务案例', id: 'section2' },
  { name: '差异对比', id: 'section3' },
  { name: '信任背书', id: 'section4' },
  { name: '发展历程', id: 'section5' },
  { name: '价值愿景', id: 'section6' },
  { name: '联系我们', id: 'section7' }
])

// 切换到指定页面
const goToPage = (index: number) => {
  if (index >= 0 && index < sections.value.length) {
    currentPage.value = index
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}

// 上一页
const goToPrevPage = () => {
  if (currentPage.value > 0) {
    goToPage(currentPage.value - 1)
  }
}

// 下一页
const goToNextPage = () => {
  if (currentPage.value < sections.value.length - 1) {
    goToPage(currentPage.value + 1)
  }
}

// 数字滚动动画
const displayStats = reactive({
  unhealthy: 0,
  chronic: 0,
  talents: 0
})

// 用户案例数据
const userCases = ref([
  {
    avatar: '👩',
    name: '王女士',
    age: 38,
    profession: '失眠患者',
    problem: '靠安眠药助眠2年，睡着易醒，第二天精神差得没法工作，试过不少食疗方，要么没效果，要么坚持不下来',
    solution: [
      '线上智能体质测评（5分钟）→ 肝郁气滞+脾胃虚弱',
      '醒髓安神方案：中药汤剂配送到家',
      '智能食谱：跟着作息调整（红枣黑芝麻粉安神）',
      '社区驿站：每周2次头颈肩松解术',
      '智能手环：实时监测睡眠质量'
    ],
    result: '2个月后不用安眠药也能睡6+小时，早上起来不觉得累了',
    feedback: '现在不用吃安眠药也能睡6个多小时，食谱跟着季节变花样，不像以前那样觉得是"任务"，反而像在慢慢养成健康的习惯'
  },
  {
    avatar: '👨',
    name: '张先生',
    age: 55,
    profession: '三高患者',
    problem: '3年三高病史，每天要吃3种药，血糖、血压还是时高时低。去医院看，医生只说"少吃油盐"，具体该吃什么、怎么吃没个准数',
    solution: [
      '3个月代谢平衡计划',
      '四人服务小组：医生+营养师+理疗师+医助',
      '节气食疗方案（霜降加萝卜汤、冬至用羊肉汤）',
      '中药分包配送，不用自己熬',
      '健康档案实时更新，数据对比'
    ],
    result: '血糖从7.8降到6.5mmol/L，降压药减量30%',
    feedback: '以前觉得三高只能靠药"压着"，现在才知道，中医的调理能帮身体慢慢恢复代谢能力，还有人陪着一起管健康，比自己瞎琢磨靠谱多了'
  },
  {
    avatar: '👧',
    name: '李女士',
    age: 26,
    profession: '上班族',
    problem: '经常加班熬夜，慢慢出现了胸闷、食欲不振的问题。想去看中医，又觉得"没大病没必要"，买了些养生茶喝，喝了半个月也没感觉',
    solution: [
      '小程序免费测评（5分钟）→ 痰湿壅滞体质',
      '社区驿站轻养生：下班顺路做拔罐理疗',
      '食疗配送：谷物果汁送到公司',
      '健康社区：同体质用户分享经验'
    ],
    result: '1个月胸闷改善，有食欲，不用"挤时间"管理健康',
    feedback: '现在胸闷的情况少了，吃饭也有胃口了，最惊喜的是，不用特意抽时间去调理，社区就在小区楼下，食疗配送也省了自己准备的麻烦'
  }
])

// 服务流程
const serviceFlow = ref([
  { icon: '🔍', title: '智能评测', desc: '5分钟读懂体质' },
  { icon: '📋', title: '动态方案', desc: '个性化调理计划' },
  { icon: '📦', title: '适配产品', desc: '中药+食疗+理疗' },
  { icon: '👥', title: '社区陪伴', desc: '实时监测+交流' },
  { icon: '🔄', title: '方案调整', desc: '体质变化跟踪' }
])

// 用户反馈
const feedbacks = ref([
  {
    avatar: '👩',
    name: '王女士',
    tag: '38岁 | 失眠改善',
    content: '食谱跟着季节变花样，不像以前那样觉得是"任务"，反而像在慢慢养成健康的习惯',
    rating: 5
  },
  {
    avatar: '👨',
    name: '张先生',
    tag: '55岁 | 三高控制',
    content: '中医的调理能帮身体慢慢恢复代谢能力，还有人陪着一起管健康，比自己瞎琢磨靠谱多了',
    rating: 5
  },
  {
    avatar: '👧',
    name: '李女士',
    tag: '26岁 | 亚健康调理',
    content: '不用特意抽时间去调理，社区就在小区楼下，食疗配送也省了自己准备的麻烦，像健康养成游戏一样',
    rating: 5
  }
])

// 发展历程
const timeline = ref([
  {
    year: '2019-2021',
    icon: '🎓',
    title: '人才培养',
    desc: '搭建专业人才梯队，输送优质中医力量',
    stats: [
      { num: '20+', label: '培训班' },
      { num: '2000+', label: '人才' }
    ]
  },
  {
    year: '2021-2023',
    icon: '🏥',
    title: '专科深耕',
    desc: '打造特色专科，形成全周期调理方案',
    tags: ['亚健康', '失眠', '三高', '脾胃', '妇科', '抗衰'],
    tagType: 'success'
  },
  {
    year: '2024至今',
    icon: '🌐',
    title: '生态共建',
    desc: '构建健康生态，拓展服务边界',
    tags: ['评测-方案-产品-社区', '线上+线下融合'],
    tagType: 'primary'
  }
])

// 核心价值观
const values = ref([
  { icon: Aim, title: '关爱', desc: '服务动力', color: '#67C23A' },
  { icon: User, title: '专业', desc: '发展根基', color: '#409EFF' },
  { icon: TrendCharts, title: '创新', desc: '效率提升', color: '#E6A23C' },
  { icon: Connection, title: '共赢', desc: '生态链接', color: '#F56C6C' }
])

// 发展愿景
const visions = ref([
  {
    icon: Sunny,
    title: '传承中医文化',
    desc: '让千年中医智慧惠及现代健康生活',
    color: '#67C23A'
  },
  {
    icon: TrendCharts,
    title: '推动中医食养一体化',
    desc: '实现预防与调理的完美结合',
    color: '#409EFF'
  },
  {
    icon: Connection,
    title: '构建全生命周期健康生态',
    desc: '从评测到产品，从方案到社区，全程守护健康',
    color: '#E6A23C'
  }
])

// 案例详情对话框
const caseDialogVisible = ref(false)
const selectedCase = ref(null)
const actionSection = ref(null)

// 数字滚动动画
const animateNumber = (target: number, key: string, suffix = '') => {
  const duration = 2000
  const steps = 60
  const increment = target / steps
  let current = 0

  const timer = setInterval(() => {
    current += increment
    if (current >= target) {
      displayStats[key] = target + suffix
      clearInterval(timer)
    } else {
      displayStats[key] = Math.floor(current) + suffix
    }
  }, duration / steps)
}

const showCaseDetail = (caseItem: any) => {
  selectedCase.value = caseItem
  caseDialogVisible.value = true
}

onMounted(() => {
  // 数字滚动动画
  setTimeout(() => {
    animateNumber(75, 'unhealthy')
    animateNumber(3.3, 'chronic')
    animateNumber(2000, 'talents')
  }, 500)
})

onUnmounted(() => {
  // 清理定时器等资源
})
</script>

<style scoped>
/* ==================== 全局样式 ==================== */
/* 分页模式布局 */
.about-story {
  min-height: 100vh;
  background: linear-gradient(to bottom, #FAF6E8 0%, #FEFEFE 50%, #F5F7FA 100%);
  position: relative;
  display: flex;
}

/* ==================== 左侧固定导航栏 ==================== */
.sidebar-nav {
  position: fixed;
  left: 0;
  top: 0;
  bottom: 0;
  width: 220px;
  background: white;
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.08);
  z-index: 1000;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #EBEEF5;
}

.sidebar-header {
  padding: 30px 20px 20px;
  border-bottom: 2px solid #F0F9FF;
  background: linear-gradient(135deg, #F0F9FF 0%, #FEFEFE 100%);
}

.sidebar-header h3 {
  font-size: 20px;
  font-weight: bold;
  color: #2C3E50;
  margin: 0;
  text-align: center;
  background: linear-gradient(135deg, #67C23A, #409EFF);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.sidebar-menu {
  flex: 1;
  padding: 20px 15px;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.menu-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s;
  position: relative;
}

.menu-item:hover {
  background: #F0F9FF;
  transform: translateX(5px);
}

.menu-item.active {
  background: linear-gradient(135deg, #ECF5FF, #F0F9FF);
  border-left: 4px solid #67C23A;
  box-shadow: 0 2px 12px rgba(103, 194, 58, 0.15);
}

.menu-item.active .menu-dot {
  background: linear-gradient(135deg, #67C23A, #409EFF);
  box-shadow: 0 0 0 4px rgba(103, 194, 58, 0.2);
  transform: scale(1.3);
}

.menu-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #DCDFE6;
  transition: all 0.3s;
  flex-shrink: 0;
}

.menu-text {
  font-size: 15px;
  color: #606266;
  font-weight: 500;
  white-space: nowrap;
  transition: all 0.3s;
}

.menu-item.active .menu-text {
  color: #67C23A;
  font-weight: 600;
}

.menu-item:hover .menu-text {
  color: #409EFF;
}

/* ==================== 主要内容区域 ==================== */
.main-content {
  margin-left: 220px; /* 给侧边栏留出空间 */
  flex: 1;
  min-height: 100vh;
}

/* 手机端导航 */
@media (max-width: 768px) {
  .sidebar-nav {
    width: 180px;
  }

  .main-content {
    margin-left: 180px;
  }

  .sidebar-header h3 {
    font-size: 18px;
  }

  .menu-item {
    padding: 12px 14px;
  }

  .menu-text {
    font-size: 14px;
  }
}

/* 超小屏幕隐藏侧边栏 */
@media (max-width: 576px) {
  .sidebar-nav {
    display: none;
  }

  .main-content {
    margin-left: 0;
  }
}

/* ==================== 页面进度指示器 ==================== */
.page-indicator {
  position: fixed;
  bottom: 40px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 999;
  background: rgba(255, 255, 255, 0.95);
  padding: 12px 24px;
  border-radius: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  font-size: 18px;
  font-weight: bold;
  color: #2C3E50;
  backdrop-filter: blur(10px);
  transition: all 0.3s;
}

.page-indicator:hover {
  transform: translateX(-50%) translateY(-5px);
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
}

.page-indicator .current {
  color: #67C23A;
  font-size: 24px;
  text-shadow: 0 2px 4px rgba(103, 194, 58, 0.3);
}

.page-indicator .separator {
  margin: 0 8px;
  color: #DCDFE6;
}

.page-indicator .total {
  color: #909399;
  font-size: 16px;
}

/* 手机端进度指示器 */
@media (max-width: 768px) {
  .page-indicator {
    bottom: 20px;
    padding: 10px 20px;
    font-size: 16px;
  }

  .page-indicator .current {
    font-size: 20px;
  }

  .page-indicator .total {
    font-size: 14px;
  }
}

/* ==================== 左右切换按钮 ==================== */
.page-nav-buttons {
  position: fixed;
  top: 50%;
  left: 0;
  right: 0;
  transform: translateY(-50%);
  z-index: 998;
  pointer-events: none; /* 容器不拦截点击 */
}

.page-nav-btn {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  color: #67C23A;
  pointer-events: auto; /* 按钮可以点击 */
  backdrop-filter: blur(10px);
}

.page-nav-btn:hover:not(.disabled) {
  background: linear-gradient(135deg, #67C23A, #409EFF);
  color: white;
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 8px 30px rgba(103, 194, 58, 0.4);
}

.page-nav-btn:active:not(.disabled) {
  transform: translateY(-50%) scale(0.95);
}

.page-nav-btn.disabled {
  opacity: 0.3;
  cursor: not-allowed;
  background: rgba(255, 255, 255, 0.5);
}

/* 上一页按钮 - 左侧 */
.prev-btn {
  left: 30px;
}

/* 下一页按钮 - 右侧 */
.next-btn {
  right: 30px;
}

/* 手机端切换按钮 */
@media (max-width: 768px) {
  .page-nav-btn {
    width: 50px;
    height: 50px;
    font-size: 20px;
  }

  .prev-btn {
    left: 15px;
  }

  .next-btn {
    right: 15px;
  }
}

/* ==================== 页面板块容器 ==================== */
.pages-container {
  width: 100%;
  min-height: 100vh;
}

/* ==================== 板块1: Hero开篇 ==================== */
.hero-section {
  position: relative;
  min-height: 100vh;
  background: linear-gradient(135deg, #A8D8B8 0%, #67C23A 100%);
  padding: 80px 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  overflow: hidden;
}

.hero-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><circle cx="50" cy="50" r="40" fill="rgba(255,255,255,0.05)"/></svg>') repeat;
  opacity: 0.3;
}

.hero-content {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  text-align: center;
  color: white;
}

.stats-row {
  display: flex;
  justify-content: center;
  gap: 60px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 48px;
  font-weight: bold;
  color: white;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
  margin-bottom: 8px;
}

.stat-label {
  font-size: 16px;
  color: rgba(255,255,255,0.9);
}

.hero-title {
  font-size: 36px;
  font-weight: bold;
  line-height: 1.6;
  margin-bottom: 24px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.hero-subtitle {
  font-size: 18px;
  line-height: 1.8;
  margin-bottom: 40px;
  opacity: 0.95;
}

.hero-cta {
  font-size: 20px;
  padding: 20px 50px;
  border-radius: 50px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.2);
  transition: all 0.3s;
}

.hero-cta:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.3);
}

/* ==================== 通用板块样式 ==================== */
/* 所有页面板块的基础样式 */
.page-content {
  min-height: 100vh;
  width: 100%;
}

/* 故事板块统一样式 */
.story-section {
  min-height: 100vh;
  padding: 80px 40px;
  display: flex;
  flex-direction: column;
}

.section-title {
  text-align: center;
  font-size: 36px;
  color: #2C3E50;
  margin-bottom: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.section-title .el-icon {
  font-size: 40px;
  color: #67C23A;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .story-section {
    padding: 60px 20px;
  }

  .section-title {
    font-size: 28px;
  }
}

/* ==================== 板块2: 初心故事 ==================== */
.origin-story {
  background: #FAF6E8;
}

.story-content {
  max-width: 1200px;
  margin: 0 auto;
}

.story-intro {
  text-align: center;
  margin-bottom: 40px;
}

.highlight-text {
  font-size: 24px;
  color: #2C3E50;
  font-weight: bold;
}

.problems-row {
  margin-bottom: 60px;
}

.problem-card {
  background: white;
  padding: 40px 30px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: all 0.3s;
  height: 100%;
}

.problem-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 12px 24px rgba(103, 194, 58, 0.2);
}

.problem-icon {
  font-size: 60px;
  text-align: center;
  margin-bottom: 20px;
}

.problem-card h3 {
  font-size: 22px;
  color: #2C3E50;
  margin-bottom: 20px;
  text-align: center;
}

.problem-card ul {
  list-style: none;
  padding: 0;
}

.problem-card li {
  padding: 12px 0;
  color: #606266;
  line-height: 1.6;
  border-bottom: 1px dashed #EBEEF5;
}

.problem-card li:last-child {
  border-bottom: none;
}

.problem-card li::before {
  content: '• ';
  color: #67C23A;
  font-weight: bold;
  margin-right: 8px;
}

.decision-card {
  background: linear-gradient(135deg, #ECF5FF 0%, #FEFEFE 100%);
  padding: 50px 40px;
  border-radius: 20px;
  margin-bottom: 60px;
  border: 2px solid #409EFF;
}

.decision-icon {
  font-size: 60px;
  text-align: center;
  margin-bottom: 20px;
}

.decision-card h3 {
  font-size: 28px;
  color: #2C3E50;
  text-align: center;
  margin-bottom: 20px;
}

.decision-text {
  font-size: 20px;
  color: #606266;
  text-align: center;
  margin-bottom: 40px;
  line-height: 1.8;
}

.solution-flow {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

.flow-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  background: white;
  padding: 24px 32px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: all 0.3s;
}

.flow-item:hover {
  transform: scale(1.05);
  box-shadow: 0 8px 20px rgba(64, 158, 255, 0.2);
}

.flow-item .el-icon {
  font-size: 36px;
  color: #409EFF;
}

.flow-item span {
  font-size: 16px;
  color: #2C3E50;
  font-weight: 500;
}

.flow-arrow {
  font-size: 24px;
  color: #409EFF;
}

.first-step-card {
  background: white;
  padding: 50px 40px;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
}

.first-step-card h3 {
  font-size: 28px;
  color: #2C3E50;
  margin-bottom: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

.achievements {
  margin-bottom: 40px;
}

.achievement-item {
  text-align: center;
  padding: 24px;
  background: linear-gradient(135deg, #F0F9FF 0%, #FEFEFE 100%);
  border-radius: 12px;
  transition: all 0.3s;
}

.achievement-item:hover {
  transform: translateY(-5px);
  background: linear-gradient(135deg, #ECF5FF 0%, #FEFEFE 100%);
}

.achievement-number {
  font-size: 36px;
  font-weight: bold;
  color: #409EFF;
  margin-bottom: 8px;
}

.achievement-label {
  font-size: 14px;
  color: #909399;
}

.achievement-desc {
  font-size: 16px;
  color: #606266;
  line-height: 1.8;
  text-align: center;
}

/* ==================== 板块3: 服务故事 ==================== */
.service-stories {
  background: white;
}

.cases-row {
  max-width: 1400px;
  margin: 0 auto;
}

.case-card {
  height: 100%;
  cursor: pointer;
  transition: all 0.3s;
  border: 2px solid transparent;
}

.case-card:hover {
  transform: translateY(-10px);
  border-color: #67C23A;
  box-shadow: 0 12px 32px rgba(103, 194, 58, 0.2);
}

.case-header {
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 2px solid #EBEEF5;
}

.case-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #A8D8B8, #67C23A);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
}

.user-name {
  font-size: 20px;
  font-weight: bold;
  color: #2C3E50;
}

.user-age {
  font-size: 14px;
  color: #909399;
  margin-top: 4px;
}

.case-problem,
.case-solution,
.case-result {
  margin-bottom: 20px;
}

.problem-label,
.solution-label,
.result-label {
  font-size: 16px;
  font-weight: bold;
  color: #2C3E50;
  margin-bottom: 12px;
}

.case-problem p,
.case-result p {
  color: #606266;
  line-height: 1.6;
}

.case-solution ul {
  list-style: none;
  padding: 0;
}

.case-solution li {
  padding: 8px 0;
  color: #606266;
  line-height: 1.5;
  font-size: 14px;
}

.case-solution li::before {
  content: '✓ ';
  color: #67C23A;
  font-weight: bold;
  margin-right: 6px;
}

.result-text {
  color: #67C23A;
  font-weight: 500;
}

.case-feedback {
  background: #F0F9FF;
  padding: 20px;
  border-radius: 12px;
  border-left: 4px solid #409EFF;
  margin-bottom: 20px;
}

.feedback-icon {
  font-size: 32px;
  color: #409EFF;
  opacity: 0.3;
  line-height: 1;
  margin-bottom: 8px;
}

.feedback-text {
  font-size: 15px;
  color: #606266;
  line-height: 1.6;
  font-style: italic;
  margin-bottom: 12px;
}

.feedback-author {
  text-align: right;
  font-size: 14px;
  color: #909399;
}

.detail-btn {
  width: 100%;
  justify-content: center;
}

/* ==================== 板块4: 差异故事 ==================== */
.difference-story {
  background: #F0F9FF;
}

.question-intro {
  text-align: center;
  margin-bottom: 60px;
}

.main-question {
  font-size: 36px;
  color: #2C3E50;
  font-weight: bold;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  line-height: 1.4;
}

.main-question .el-icon {
  font-size: 40px;
  color: #67C23A;
  flex-shrink: 0;
}

.answer-intro {
  font-size: 18px;
  color: #909399;
  line-height: 1.6;
}

/* 响应式 */
@media (max-width: 768px) {
  .main-question {
    font-size: 26px;
  }

  .main-question .el-icon {
    font-size: 32px;
  }

  .answer-intro {
    font-size: 16px;
  }
}

.comparison-row {
  margin-bottom: 60px;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
}

.pain-point-card {
  background: white;
  padding: 40px 30px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  height: 100%;
  transition: all 0.3s;
}

.pain-point-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(64, 158, 255, 0.2);
}

.pain-icon {
  font-size: 50px;
  text-align: center;
  margin-bottom: 20px;
}

.pain-point-card h3 {
  font-size: 24px;
  color: #2C3E50;
  margin-bottom: 30px;
  text-align: center;
}

.traditional-way,
.ruiai-way {
  margin-bottom: 20px;
}

.label {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 12px;
  display: inline-block;
}

.traditional-way .label {
  color: #909399;
}

.ruiai-way .label {
  color: #67C23A;
}

.traditional-way p {
  color: #909399;
  line-height: 1.6;
  padding-left: 20px;
}

.ruiai-way ul {
  list-style: none;
  padding: 0;
}

.ruiai-way li {
  padding: 10px 0 10px 20px;
  color: #606266;
  line-height: 1.6;
  border-left: 3px solid #67C23A;
  margin-bottom: 8px;
  background: #F0F9FF;
  padding-left: 16px;
  border-radius: 4px;
}

.service-flow-card {
  background: white;
  padding: 50px 40px;
  border-radius: 20px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.1);
  max-width: 1200px;
  margin: 0 auto;
}

.service-flow-card h3 {
  font-size: 28px;
  color: #2C3E50;
  text-align: center;
  margin-bottom: 40px;
}

.flow-diagram {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
  margin-bottom: 40px;
}

.flow-step {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
}

.step-icon {
  font-size: 48px;
  margin-bottom: 12px;
}

.step-title {
  font-size: 18px;
  font-weight: bold;
  color: #2C3E50;
  margin-bottom: 8px;
}

.step-desc {
  font-size: 14px;
  color: #909399;
  text-align: center;
}

.step-arrow {
  font-size: 32px;
  color: #67C23A;
  margin: 0 10px;
}

.flow-summary {
  font-size: 20px;
  color: #606266;
  text-align: center;
  font-weight: 500;
  line-height: 1.8;
}

/* ==================== 板块5: 信任背书 ==================== */
.trust-section {
  background: #FAF6E8;
}

.subsection-title {
  font-size: 28px;
  color: #2C3E50;
  margin-bottom: 16px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.subsection-desc {
  font-size: 16px;
  color: #909399;
  margin-bottom: 40px;
}

.talent-strength {
  margin-bottom: 80px;
}

.strength-stats {
  display: flex;
  justify-content: center;
  gap: 60px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.strength-stat {
  text-align: center;
}

.stat-num {
  font-size: 48px;
  font-weight: bold;
  color: #409EFF;
  display: block;
  margin-bottom: 12px;
}

.stat-desc {
  font-size: 16px;
  color: #606266;
}

.certification-text {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.certification-text p {
  font-size: 18px;
  color: #606266;
  line-height: 2;
  display: flex;
  align-items: center;
  gap: 12px;
}

.certification-text .el-icon {
  color: #67C23A;
  font-size: 20px;
}

.user-feedback {
  margin-bottom: 80px;
}

.feedback-list {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.feedback-item {
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  display: flex;
  gap: 24px;
  transition: all 0.3s;
}

.feedback-item:hover {
  transform: translateX(10px);
  box-shadow: 0 8px 20px rgba(103, 194, 58, 0.15);
}

.feedback-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  background: linear-gradient(135deg, #A8D8B8, #67C23A);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  flex-shrink: 0;
}

.feedback-content {
  flex: 1;
}

.feedback-quote {
  font-size: 16px;
  color: #606266;
  line-height: 1.8;
  margin-bottom: 16px;
  font-style: italic;
}

.feedback-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  flex-wrap: wrap;
}

.feedback-name {
  font-weight: bold;
  color: #2C3E50;
}

.feedback-tag {
  color: #909399;
  font-size: 14px;
}

.recognition-card {
  border: 2px solid #409EFF;
}

.recognition-content {
  display: flex;
  gap: 32px;
  align-items: flex-start;
}

.recognition-icon {
  flex-shrink: 0;
}

.recognition-text h4 {
  font-size: 24px;
  color: #2C3E50;
  margin-bottom: 16px;
}

.recognition-text p {
  font-size: 16px;
  color: #606266;
  line-height: 1.8;
  margin-bottom: 20px;
}

.recognition-text ul {
  list-style: none;
  padding: 0;
}

.recognition-text li {
  padding: 10px 0;
  color: #606266;
  line-height: 1.6;
}

.recognition-text li::before {
  content: '✓ ';
  color: #409EFF;
  font-weight: bold;
  margin-right: 8px;
}

/* ==================== 板块6: 发展历程（左右布局）==================== */
.history-section {
  background: white;
}

/* 新的左右布局 */
.timeline-modern {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.timeline-item-modern {
  display: flex;
  gap: 40px;
  align-items: stretch;
  position: relative;
}

/* 左侧：年份+图标 */
.timeline-left {
  flex-shrink: 0;
  width: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  padding: 30px 20px;
  background: linear-gradient(135deg, #F0F9FF 0%, #ECF5FF 100%);
  border-radius: 16px;
  border: 2px solid #409EFF;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.1);
  transition: all 0.3s;
}

.timeline-left:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(64, 158, 255, 0.2);
  border-color: #67C23A;
}

.timeline-year-box {
  background: linear-gradient(135deg, #67C23A, #409EFF);
  color: white;
  padding: 12px 20px;
  border-radius: 25px;
  font-size: 16px;
  font-weight: bold;
  text-align: center;
  box-shadow: 0 4px 12px rgba(103, 194, 58, 0.3);
  white-space: nowrap;
}

.timeline-icon-box {
  font-size: 64px;
  text-align: center;
  line-height: 1;
}

/* 右侧：内容卡片 */
.timeline-right {
  flex: 1;
  display: flex;
}

.timeline-content-card {
  background: white;
  padding: 40px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  border: 2px solid transparent;
  transition: all 0.3s;
  flex: 1;
  border-left: 4px solid #67C23A;
}

.timeline-content-card:hover {
  transform: translateX(10px);
  box-shadow: 0 12px 32px rgba(103, 194, 58, 0.2);
  border-color: #67C23A;
}

.timeline-content-card h3 {
  font-size: 28px;
  color: #2C3E50;
  margin-bottom: 16px;
  font-weight: bold;
}

.timeline-content-card p {
  font-size: 16px;
  color: #606266;
  line-height: 1.8;
  margin-bottom: 24px;
}

.timeline-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-top: 20px;
}

.timeline-stats {
  display: flex;
  gap: 40px;
  justify-content: flex-start;
  margin-top: 24px;
  padding-top: 24px;
  border-top: 2px dashed #EBEEF5;
}

.timeline-stats .stat {
  text-align: center;
}

.timeline-stats .stat-num {
  font-size: 32px;
  font-weight: bold;
  color: #409EFF;
  display: block;
  margin-bottom: 8px;
}

.timeline-stats .stat-label {
  font-size: 14px;
  color: #909399;
}

/* ==================== 板块7: 价值观+愿景 ==================== */
.values-vision-section {
  background: #F0F9FF;
}

.values-part {
  margin-bottom: 80px;
}

.values-row {
  max-width: 1200px;
  margin: 0 auto;
}

.value-card {
  text-align: center;
  padding: 40px 20px;
  transition: all 0.3s;
  border: 2px solid transparent;
  height: 100%;
}

.value-card:hover {
  transform: translateY(-10px);
  border-color: #67C23A;
  box-shadow: 0 12px 32px rgba(103, 194, 58, 0.2);
}

.value-icon {
  font-size: 50px;
  margin-bottom: 20px;
}

.value-card h3 {
  font-size: 24px;
  color: #2C3E50;
  margin-bottom: 12px;
}

.value-card p {
  font-size: 16px;
  color: #909399;
}

/* 发展愿景样式 */
.vision-row {
  max-width: 1400px;
  margin: 0 auto;
}

.vision-item {
  background: white;
  border-radius: 16px;
  padding: 40px 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  border: 2px solid transparent;
}

.vision-item:hover {
  transform: translateY(-10px);
  box-shadow: 0 12px 32px rgba(103, 194, 58, 0.2);
  border-color: #67C23A;
}

.vision-icon {
  width: 90px;
  height: 90px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #F0F9FF, #ECF5FF);
  border-radius: 50%;
  margin-bottom: 24px;
  transition: all 0.3s;
}

.vision-item:hover .vision-icon {
  transform: rotate(360deg) scale(1.1);
  background: linear-gradient(135deg, #ECF5FF, #E6F7FF);
}

.vision-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
}

.vision-title {
  font-size: 22px;
  color: #2C3E50;
  margin-bottom: 16px;
  font-weight: bold;
  line-height: 1.4;
}

.vision-desc {
  font-size: 15px;
  color: #606266;
  line-height: 1.8;
}

/* 响应式 */
@media (max-width: 768px) {
  .vision-item {
    padding: 30px 20px;
    margin-bottom: 20px;
  }

  .vision-icon {
    width: 70px;
    height: 70px;
  }

  .vision-title {
    font-size: 20px;
  }

  .vision-desc {
    font-size: 14px;
  }
}

/* ==================== 板块8: 行动引导 ==================== */
.action-section {
  background: linear-gradient(135deg, #A8D8B8 0%, #67C23A 50%, #409EFF 100%);
  padding: 80px 20px;
  color: white;
}

.emotional-ending {
  text-align: center;
  max-width: 900px;
  margin: 0 auto 60px;
}

.ending-title {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 24px;
  text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
}

.ending-text {
  font-size: 24px;
  line-height: 1.8;
  margin-bottom: 20px;
}

.ending-detail {
  font-size: 18px;
  line-height: 1.8;
  margin-bottom: 20px;
  opacity: 0.95;
}

.ending-call {
  font-size: 20px;
  line-height: 1.8;
  font-weight: 500;
}

.action-cards {
  max-width: 1200px;
  margin: 0 auto 60px;
}

.action-card {
  background: white;
  padding: 40px 30px;
  text-align: center;
  transition: all 0.3s;
  border: 3px solid transparent;
  height: 100%;
}

.action-card:hover {
  transform: translateY(-10px);
}

.light-action:hover {
  border-color: #67C23A;
  box-shadow: 0 12px 32px rgba(103, 194, 58, 0.3);
}

.medium-action:hover {
  border-color: #409EFF;
  box-shadow: 0 12px 32px rgba(64, 158, 255, 0.3);
}

.high-action:hover {
  border-color: #E6A23C;
  box-shadow: 0 12px 32px rgba(230, 162, 60, 0.3);
}

.action-icon {
  font-size: 60px;
  margin-bottom: 20px;
}

.action-card h3 {
  font-size: 24px;
  color: #2C3E50;
  margin-bottom: 30px;
}

.action-buttons {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.contact-info {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
  background: rgba(255,255,255,0.1);
  padding: 40px;
  border-radius: 20px;
  backdrop-filter: blur(10px);
}

.contact-info h3 {
  font-size: 28px;
  margin-bottom: 30px;
}

.contact-grid {
  display: flex;
  justify-content: center;
  gap: 40px;
  flex-wrap: wrap;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 16px;
}

.contact-item .el-icon {
  font-size: 24px;
}

/* ==================== 案例详情对话框 ==================== */
.case-detail {
  padding: 20px 0;
}

.detail-section {
  margin-bottom: 30px;
}

.detail-section h4 {
  font-size: 20px;
  color: #2C3E50;
  margin-bottom: 16px;
  font-weight: bold;
}

.detail-section p {
  font-size: 16px;
  color: #606266;
  line-height: 1.8;
}

.detail-section ul {
  list-style: none;
  padding: 0;
}

.detail-section li {
  padding: 12px 0;
  color: #606266;
  line-height: 1.6;
  border-bottom: 1px dashed #EBEEF5;
}

.detail-section li::before {
  content: '✓ ';
  color: #67C23A;
  font-weight: bold;
  margin-right: 8px;
}

.detail-section blockquote {
  background: #F0F9FF;
  padding: 20px;
  border-left: 4px solid #409EFF;
  font-style: italic;
  color: #606266;
  margin: 16px 0;
  line-height: 1.8;
}

.detail-section .author {
  text-align: right;
  color: #909399;
  font-size: 14px;
  margin-top: 12px;
}

/* ==================== 响应式设计 ==================== */
@media (max-width: 768px) {
  .hero-title {
    font-size: 24px;
  }

  .hero-subtitle {
    font-size: 16px;
  }

  .stat-number {
    font-size: 36px;
  }

  .stats-row {
    gap: 30px;
  }

  .section-title {
    font-size: 28px;
  }

  .solution-flow {
    flex-direction: column;
  }

  .flow-arrow {
    transform: rotate(90deg);
  }

  .timeline-item-modern {
    flex-direction: column;
    gap: 20px;
  }

  .timeline-left {
    width: 100%;
    flex-direction: row;
    justify-content: center;
    padding: 20px;
  }

  .timeline-year-box {
    font-size: 14px;
    padding: 10px 16px;
  }

  .timeline-icon-box {
    font-size: 48px;
  }

  .timeline-content-card {
    padding: 24px;
  }

  .timeline-content-card h3 {
    font-size: 22px;
  }

  .timeline-stats {
    flex-direction: column;
    gap: 20px;
    align-items: center;
  }

  .flow-diagram {
    flex-direction: column;
  }

  .step-arrow {
    transform: rotate(90deg);
  }

  .recognition-content {
    flex-direction: column;
    text-align: center;
  }

  .ending-title {
    font-size: 24px;
  }

  .ending-text {
    font-size: 18px;
  }

  .vision-item {
    flex-direction: column;
    align-items: center;
    text-align: center;
  }
}
</style>
