<template>
  <div class="learning-center">
    <PageContainer>
      <!-- 核心板块 - 书签式横向布局 -->
      <section class="core-tabs-section">
        <div class="section-header">
          <h2>学习中心</h2>
          <p class="section-desc">系统学中医，自用 / 从业皆可</p>
        </div>

        <!-- 四个书签式卡片 -->
        <div class="tab-cards-grid">
          <!-- 1. 认知颠覆 -->
          <div class="tab-card" @click="activeTab = 'cognition'">
            <div class="tab-card-icon">💡</div>
            <h3 class="tab-card-title">认知颠覆</h3>
            <p class="tab-card-desc">你对健康的理解，可能从根上就错了</p>
            <div class="tab-card-arrow">→</div>
          </div>

          <!-- 2. 避坑指南 -->
          <div class="tab-card" @click="activeTab = 'misconceptions'">
            <div class="tab-card-icon">⚠️</div>
            <h3 class="tab-card-title">避坑指南</h3>
            <p class="tab-card-desc">为什么越养生越不健康？思维错了</p>
            <div class="tab-card-arrow">→</div>
          </div>

          <!-- 3. 知识问答 -->
          <div class="tab-card" @click="activeTab = 'qa'">
            <div class="tab-card-icon">❓</div>
            <h3 class="tab-card-title">知识问答</h3>
            <p class="tab-card-desc">30个健康认知问答，颠覆你的健康观</p>
            <div class="tab-card-arrow">→</div>
          </div>

          <!-- 4. 课程学习 -->
          <div class="tab-card" @click="activeTab = 'courses'">
            <div class="tab-card-icon">📚</div>
            <h3 class="tab-card-title">课程学习</h3>
            <p class="tab-card-desc">三层递进学习体系，系统化掌握中医</p>
            <div class="tab-card-arrow">→</div>
          </div>
        </div>
      </section>

      <!-- Tab切换区域 - 隐藏Tab标签栏，只显示内容 -->
      <div class="tabs-container" v-if="activeTab">
        <el-tabs v-model="activeTab" class="learning-tabs hidden-tabs" @tab-change="handleTabChange">
          <!-- 认知颠覆Tab -->
          <el-tab-pane label="💡 认知颠覆" name="cognition">
            <div class="cognition-content">
              <div class="content-section">
                <div class="insight-card">
                  <h3>🔥 健康认知的三大误区</h3>
                  <div class="insight-list">
                    <div class="insight-item">
                      <div class="insight-number">1</div>
                      <div class="insight-text">
                        <h4>误区一：没病就是健康</h4>
                        <p>大多数人认为体检正常就是健康，但这只是"没病"状态。真正的健康是身体有强大的自愈能力和内在平衡。</p>
                      </div>
                    </div>
                    <div class="insight-item">
                      <div class="insight-number">2</div>
                      <div class="insight-text">
                        <h4>误区二：症状是敌人</h4>
                        <p>发烧、咳嗽、腹泻都是身体的自我保护机制，不是要消灭的敌人，而是要理解和配合的信号。</p>
                      </div>
                    </div>
                    <div class="insight-item">
                      <div class="insight-number">3</div>
                      <div class="insight-text">
                        <h4>误区三：治病不治人</h4>
                        <p>西医看病，中医看人。同样的病在不同人身上，调理方法可能完全不同。体质决定一切！</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="insight-card">
                  <h3>✨ 中医智慧的底层逻辑</h3>
                  <div class="wisdom-grid">
                    <div class="wisdom-item">
                      <div class="wisdom-icon">🌱</div>
                      <h4>正气存内，邪不可干</h4>
                      <p>养好自己的免疫力和自愈力，才是健康的根本</p>
                    </div>
                    <div class="wisdom-item">
                      <div class="wisdom-icon">⚖️</div>
                      <h4>阴阳平衡</h4>
                      <p>健康不是追求完美，而是维持动态平衡</p>
                    </div>
                    <div class="wisdom-item">
                      <div class="wisdom-icon">🔄</div>
                      <h4>整体观念</h4>
                      <p>身体是一个系统，局部问题往往是整体失调</p>
                    </div>
                    <div class="wisdom-item">
                      <div class="wisdom-icon">👤</div>
                      <h4>因人而异</h4>
                      <p>没有万能的方法，只有适合你的方法</p>
                    </div>
                  </div>
                </div>

                <div class="cta-section">
                  <div class="cta-card">
                    <div class="cta-content">
                      <h3>🎯 想深入了解中医健康智慧？</h3>
                      <p>点击下方按钮，查看更多内容，或参加免费体质测试</p>
                      <div class="cta-buttons">
                        <el-button type="primary" size="large" @click="activeTab = 'qa'">
                          查看知识问答
                        </el-button>
                        <el-button type="success" size="large" @click="activeTab = 'courses'">
                          学习课程体系
                        </el-button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>

          <!-- 避坑指南Tab -->
          <el-tab-pane label="⚠️ 避坑指南" name="misconceptions">
            <div class="misconceptions-content">
              <div class="content-section">
                <div class="warning-card">
                  <h3>🚫 常见养生误区</h3>
                  <div class="warning-list">
                    <div class="warning-item">
                      <div class="warning-icon">❌</div>
                      <div class="warning-content">
                        <h4>盲目进补</h4>
                        <p><strong>错误做法：</strong>看到人参、阿胶就买，听说什么好就吃什么</p>
                        <p><strong>正确做法：</strong>根据自己的体质选择补品，虚不受补的人反而会上火</p>
                      </div>
                    </div>
                    <div class="warning-item">
                      <div class="warning-icon">❌</div>
                      <div class="warning-content">
                        <h4>过度养生</h4>
                        <p><strong>错误做法：</strong>天天泡脚、艾灸、刮痧，恨不得把所有养生方法都用上</p>
                        <p><strong>正确做法：</strong>养生要适度，过犹不及，身体需要休息和自我调节</p>
                      </div>
                    </div>
                    <div class="warning-item">
                      <div class="warning-icon">❌</div>
                      <div class="warning-content">
                        <h4>盲目跟风</h4>
                        <p><strong>错误做法：</strong>看到网红养生法就照搬，别人说好就跟着做</p>
                        <p><strong>正确做法：</strong>了解自己的体质和需求，选择适合自己的方法</p>
                      </div>
                    </div>
                    <div class="warning-item">
                      <div class="warning-icon">❌</div>
                      <div class="warning-content">
                        <h4>忽视基础</h4>
                        <p><strong>错误做法：</strong>熬夜、暴饮暴食，却想通过保健品来补救</p>
                        <p><strong>正确做法：</strong>规律作息、均衡饮食、适量运动才是健康的基础</p>
                      </div>
                    </div>
                  </div>
                </div>

                <div class="principle-card">
                  <h3>✅ 科学养生原则</h3>
                  <div class="principle-grid">
                    <div class="principle-item">
                      <div class="principle-number">1</div>
                      <h4>了解体质</h4>
                      <p>先做体质测试，了解自己是什么体质，才能对症调理</p>
                    </div>
                    <div class="principle-item">
                      <div class="principle-number">2</div>
                      <h4>循序渐进</h4>
                      <p>养生不是一蹴而就，要慢慢调理，给身体适应的时间</p>
                    </div>
                    <div class="principle-item">
                      <div class="principle-number">3</div>
                      <h4>辨证施养</h4>
                      <p>根据季节、年龄、体质的不同，选择不同的养生方法</p>
                    </div>
                    <div class="principle-item">
                      <div class="principle-number">4</div>
                      <h4>持之以恒</h4>
                      <p>养生是长期的生活方式，不是短期的突击行为</p>
                    </div>
                  </div>
                </div>

                <div class="cta-section">
                  <div class="cta-card">
                    <div class="cta-content">
                      <h3>🎯 想学习科学的养生方法？</h3>
                      <p>系统学习中医养生，从入门到精通，避免养生误区</p>
                      <div class="cta-buttons">
                        <el-button type="primary" size="large" @click="activeTab = 'courses'">
                          开始学习课程
                        </el-button>
                        <el-button type="success" size="large" @click="showTestModal = true">
                          免费体质测试
                        </el-button>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>

          <!-- 课程学习Tab -->
          <el-tab-pane label="📚 课程学习" name="courses">
            <div class="courses-content">
              <!-- 3层递进结构详细展示 -->
              <div class="three-layer-system">
                <div class="layer-progression">
                  <!-- 第一层：入门阶段 -->
                  <div class="layer">
                    <div class="layer-header">
                      <div class="layer-number">1</div>
                      <div class="layer-title">入门阶段</div>
                      <div class="layer-subtitle">建框架 —— 搭建中医基础认知体系</div>
                    </div>
                    <div class="layer-content">
                      <div class="layer-goal">
                        <strong>核心目标：</strong>让中医小白快速掌握核心概念，建立 "体质 - 症状 - 调理" 的基本逻辑框架
                      </div>

                      <div class="course-item">
                        <div class="course-icon">📖</div>
                        <div class="course-title">搞懂阴阳五行与五脏对应</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">🔍</div>
                        <div class="course-title">3 分钟认清自己的体质类型</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">🌿</div>
                        <div class="course-title">中医养生核心原则：天人相应与辨证施养</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">🍜</div>
                        <div class="course-title">药食同源基础课：食材的 "寒、热、平" 怎么分</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">📚</div>
                        <div class="course-title">中医常用术语拆解：告别 "经络""气血" 盲区</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">🏠</div>
                        <div class="course-title">家庭中医工具包：必学的 3 个基础调理思路</div>
                      </div>
                    </div>
                  </div>

                  <!-- 第二层：进阶阶段 -->
                  <div class="layer">
                    <div class="layer-header">
                      <div class="layer-number">2</div>
                      <div class="layer-title">进阶阶段</div>
                      <div class="layer-subtitle">懂原理 —— 吃透中医调理底层逻辑</div>
                    </div>
                    <div class="layer-content">
                      <div class="layer-goal">
                        <strong>核心目标：</strong>从 "知其然" 到 "知其所以然"，理解调理背后的中医机理
                      </div>

                      <div class="course-item">
                        <div class="course-icon">🧬</div>
                        <div class="course-title">体质形成密码：为什么你是痰湿 / 阴虚体质？</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">🫀</div>
                        <div class="course-title">脏腑调理原理：肝、心、脾、肺、肾的养生逻辑</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">🎯</div>
                        <div class="course-title">经络与穴位入门：12 条正经与 10 个常用穴位功效</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">🥘</div>
                        <div class="course-title">食疗配伍智慧：食材搭配的 "相生相克" 原理</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">🌤️</div>
                        <div class="course-title">节气养生底层逻辑：跟着时节调体质的科学依据</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">🔬</div>
                        <div class="course-title">常见症状辨证课：上火、失眠、疲劳的中医根源分析</div>
                      </div>
                    </div>
                  </div>

                  <!-- 第三层：精通阶段 -->
                  <div class="layer">
                    <div class="layer-header">
                      <div class="layer-number">3</div>
                      <div class="layer-title">精通阶段</div>
                      <div class="layer-subtitle">能调理 —— 从专病应对到全面养护</div>
                    </div>
                    <div class="layer-content">
                      <div class="layer-goal">
                        <strong>核心目标：</strong>掌握具体调理方法，实现 "专病精准调、全身综合养"
                      </div>

                      <!-- 专病调理系列 -->
                      <div class="course-category">
                        <div class="category-title">📋 专病调理系列</div>
                        <div class="category-desc">聚焦常见问题，精准突破</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">🎯</div>
                        <div class="course-title">失眠、脾胃、妇科、三高、抗衰、亚健康等专病调理</div>
                      </div>

                      <!-- 全面养护系列 -->
                      <div class="course-category">
                        <div class="category-title">🌟 全面养护系列</div>
                        <div class="category-desc">打通全身调理，综合提升</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">👨‍👩‍👧‍👦</div>
                        <div class="course-title">全家体质管理：不同人群（老人/儿童/孕妇）的差异化调理</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">🍂</div>
                        <div class="course-title">四季综合养生：按节气定制全身养护方案</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">🛡️</div>
                        <div class="course-title">中医防未病：从 "治已病" 到 "治未病" 的全面防护</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">💆</div>
                        <div class="course-title">经络综合调理：3 套全家适用的经络按摩流程</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">📈</div>
                        <div class="course-title">体质优化方案：从偏颇体质到平和体质的进阶之路</div>
                      </div>

                      <div class="course-item">
                        <div class="course-icon">🚑</div>
                        <div class="course-title">家庭中医应急手册：突发小毛病的即时调理技巧</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </el-tab-pane>

        <!-- 知识问答Tab -->
        <el-tab-pane label="💡 知识问答" name="qa">
          <div class="qa-content">
            <!-- 问答列表 -->
            <div class="qa-list">
              <div
                v-for="(qa, index) in qaData"
                :key="index"
                class="qa-item"
                :class="{ expanded: expandedItems[index] }"
                @click="toggleExpand(index)"
              >
                <div class="qa-question">
                  <div class="question-number">{{ String(index + 1).padStart(2, '0') }}</div>
                  <div class="question-text">{{ qa.question }}</div>
                  <div class="expand-icon">
                    <el-icon>
                      <ArrowDown v-if="!expandedItems[index]" />
                      <ArrowUp v-else />
                    </el-icon>
                  </div>
                </div>
                <div class="qa-answer" v-show="expandedItems[index]">
                  <div class="answer-content" v-html="qa.answer"></div>
                </div>
              </div>
            </div>

            <!-- 体质测试引导 -->
            <div class="cta-section">
              <div class="cta-card">
                <div class="cta-content">
                  <h3>🎯 想了解自己的体质类型？</h3>
                  <p>每个人的体质不同，调理方法也不同。通过专业体质测试，获取个性化健康建议。</p>
                  <div class="cta-buttons">
                    <el-button type="primary" size="large" @click="showTestModal = true">
                      免费体质测试
                    </el-button>
                    <el-button type="success" size="large" @click="showJoinModal = true">
                      加入学习群
                    </el-button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </div>
    </PageContainer>

    <!-- 体质测试弹窗 -->
    <el-dialog v-model="showTestModal" title="免费体质测试" width="400px">
      <div class="test-modal-content">
        <div class="test-intro">
          <p>专业的中医体质辨识，为您提供个性化健康建议</p>
          <div class="test-features">
            <div class="feature-item">✅ 9大体质专业分析</div>
            <div class="feature-item">✅ 个性化调理建议</div>
            <div class="feature-item">✅ 食疗方案推荐</div>
            <div class="feature-item">✅ 巫医生亲自解读</div>
          </div>
        </div>
        <div class="qr-placeholder">
          <div class="qr-code">
            <p>扫码开始测试</p>
            <small>微信扫码即可开始</small>
          </div>
        </div>
      </div>
    </el-dialog>

    <!-- 学习群弹窗 -->
    <el-dialog v-model="showJoinModal" title="加入健康学习群" width="400px">
      <div class="join-modal-content">
        <div class="qr-placeholder">
          <p>扫码添加助手微信</p>
          <div class="qr-code">
            <p>微信二维码</p>
            <small>请截图保存后在微信中扫码</small>
          </div>
        </div>
        <div class="join-instructions">
          <h4>加群步骤：</h4>
          <ol>
            <li>添加助手微信</li>
            <li>发送"学习群"</li>
            <li>等待邀请入群</li>
          </ol>
        </div>
      </div>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { ArrowDown, ArrowUp } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { ElMessageBox } from 'element-plus'
import PageContainer from '@/components/PageContainer.vue'

const router = useRouter()

// Tab切换 - 初始状态为空，点击卡片后才显示内容
const activeTab = ref('')

// 问答相关数据
const expandedItems = reactive<Record<number, boolean>>({})
const showTestModal = ref(false)
const showJoinModal = ref(false)

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

// Tab切换事件
const handleTabChange = (tabName: string) => {
  console.log('切换到Tab:', tabName)
}

// 切换三层体系详情显示
const toggleDetail = (event: Event) => {
  const element = event.currentTarget as HTMLElement
  const detail = element.querySelector('.skill-detail') as HTMLElement
  if (detail.style.display === 'none' || !detail.style.display) {
    detail.style.display = 'block'
    element.style.backgroundColor = '#fff'
  } else {
    detail.style.display = 'none'
    element.style.backgroundColor = ''
  }
}

// 切换问答展开状态
const toggleExpand = (index: number) => {
  expandedItems[index] = !expandedItems[index]
}

// 30个健康认知问答数据
const qaData = ref([
  // 底层认知系列（10个）
  {
    question: "健康的本质是什么？99%的人想错了",
    answer: "大多数人认为健康就是'没病'，这是最大的误区！<br/><strong>真正的健康是什么？</strong><br/>• 不是没有症状，而是身体的<strong>自愈能力强大</strong><br/>• 不是依赖药物，而是拥有<strong>内在平衡</strong><br/>• 不是害怕疾病，而是与身体<strong>和谐相处</strong><br/><strong>8年临床发现：</strong>那些真正健康的人，不是从不生病，而是病了能快速恢复。他们的共同点是：懂得倾听身体，及时调整，让身体保持在最佳的自我修复状态。<br/><strong>关键认知转换：</strong>从'治病'思维转向'养正气'思维。"
  },
  {
    question: "为什么治标不治本？因为你不懂这个底层逻辑",
    answer: "现代医学总是在'灭火'，中医要教你'防火'！<br/><strong>治标不治本的根源：</strong><br/>• 只关注症状，不关注<strong>症状产生的土壤</strong><br/>• 只想快速缓解，不愿<strong>改变生活模式</strong><br/>• 只依赖外力，不相信<strong>身体自愈能力</strong><br/><strong>底层逻辑是什么？</strong><br/>疾病不是敌人，是身体发出的<strong>预警信号</strong>。胃痛不是胃有问题，是你的生活方式在伤胃；失眠不是神经有问题，是你的压力没有疏解渠道。<br/><strong>治本的方法：</strong>找到疾病的'根'，改变产生疾病的'土壤'，让身体重新回到平衡状态。"
  },
  {
    question: "疾病只是结果，真正的原因在这里",
    answer: "8年临床让我明白一个真相：<strong>所有的疾病都是生活方式的结果</strong>！<br/><strong>疾病的真正原因：</strong><br/>• <strong>情志因素</strong>：长期压抑、焦虑、愤怒<br/>• <strong>饮食习惯</strong>：不规律、偏食、暴饮暴食<br/>• <strong>作息混乱</strong>：熬夜、缺乏运动、劳逸失调<br/>• <strong>环境毒素</strong>：空气污染、化学添加剂<br/><strong>临床案例：</strong>90%的胃病患者都有情绪压抑史；80%的失眠患者都有思虑过度的习惯。<br/><strong>核心认知：</strong>改变原因，疾病自然消失。不改变原因，治好了还会复发。"
  },
  {
    question: "身体是个完整系统，别再头痛医头了",
    answer: "这是现代人最大的健康误区！身体不是机器，不能拆分维修。<br/><strong>整体系统思维：</strong><br/>• <strong>五脏六腑相互依存</strong>：心火太旺会伤肾水<br/>• <strong>情绪影响脏腑</strong>：生气伤肝，忧思伤脾<br/>• <strong>局部反映整体</strong>：舌苔看脾胃，脸色看气血<br/><strong>实际应用：</strong><br/>• 颈椎痛要调肝肾（筋骨同源）<br/>• 皮肤问题要看脾胃（脾主肌肉）<br/>• 月经不调要疏肝理气（肝主疏泄）<br/><strong>巫医生提醒：</strong>学会从整体看问题，一个症状背后往往是整个系统的失调。"
  },
  {
    question: "什么叫'正气存内，邪不可干'？",
    answer: "这是中医最重要的健康法则，也是我8年行医的核心体会！<br/><strong>正气是什么？</strong><br/>• 不是什么神秘能量，而是你的<strong>免疫力、自愈力、适应力</strong><br/>• 包括：精神状态、消化能力、睡眠质量、情绪调节<br/><strong>邪气是什么？</strong><br/>• 外邪：病毒、细菌、环境毒素<br/>• 内邪：负面情绪、不良习惯、内生毒素<br/><strong>如何养正气？</strong><br/>• <strong>情志调养</strong>：保持心态平和<br/>• <strong>饮食有节</strong>：营养均衡，不伤脾胃<br/>• <strong>起居有常</strong>：作息规律，顺应自然<br/>• <strong>运动适度</strong>：气血流通，体质强健<br/><strong>记住：</strong>正气足的人，病毒进不来；正气不足的人，喝凉水都塞牙！"
  },
  {
    question: "症状是身体的语言，你会听吗？",
    answer: "大部分人都在'消灭'症状，却不知道症状是身体在'求救'！<br/><strong>学会解读身体语言：</strong><br/>• <strong>发烧</strong>：身体在清理毒素，不要急着退烧<br/>• <strong>咳嗽</strong>：肺在排出异物，要助其排出<br/>• <strong>腹泻</strong>：肠胃在清理垃圾，要支持而非止泻<br/>• <strong>失眠</strong>：心神不安，要安神而非强制入睡<br/><strong>常见误区：</strong><br/>头痛就吃止痛药 → 应该找头痛的原因<br/>便秘就吃泻药 → 应该调理脾胃功能<br/>焦虑就吃安定 → 应该疏解情志根源<br/><strong>正确做法：</strong>倾听症状想告诉你什么，配合身体的自愈过程，而不是对抗它。"
  },
  {
    question: "为什么同样的病，每个人调理方法不同？",
    answer: "这就是中医的精髓所在！同病异治，因人而异。<br/><strong>个体差异决定治疗方案：</strong><br/>• <strong>体质不同</strong>：阳虚体质用温补，阴虚体质用滋阴<br/>• <strong>年龄不同</strong>：老人宜补，年轻人宜泻<br/>• <strong>季节不同</strong>：春夏养阳，秋冬养阴<br/>• <strong>地域不同</strong>：南方多湿，北方多燥<br/><strong>实际案例：</strong><br/>同样是失眠：<br/>• A患者：心火旺 → 用黄连清心<br/>• B患者：肾阴虚 → 用六味地黄丸<br/>• C患者：脾胃弱 → 用归脾汤<br/><strong>关键认知：</strong>没有万能的方法，只有适合的方法。学会辨识自己的体质，才能找到专属的调理方案。"
  },
  {
    question: "体质决定一切，但体质到底是什么？",
    answer: "体质是你的健康基础设施，决定了你容易得什么病，适合什么调理方法！<br/><strong>体质的真相：</strong><br/>不是迷信，而是你身体的<strong>'操作系统'</strong>——决定了你对食物、药物、环境的反应模式<br/><strong>9大体质简化理解：</strong><br/>• <strong>平和质</strong>：身体的'优等生'<br/>• <strong>气虚质</strong>：能量不足，像'低电量手机'<br/>• <strong>阳虚质</strong>：怕冷一族，需要'充电'<br/>• <strong>阴虚质</strong>：内热体质，需要'降温'<br/>• <strong>痰湿质</strong>：身体'下水道堵塞'<br/>• <strong>湿热质</strong>：又湿又热，需要'除湿清热'<br/><strong>体质决定什么？</strong><br/>• 你为什么总感冒，别人不感冒<br/>• 为什么同样的减肥方法，你没效果<br/>• 为什么别人能熬夜，你熬夜就生病<br/><strong>掌握了体质，就掌握了健康主动权！</strong>"
  },
  {
    question: "健康不是没有症状，而是这个状态",
    answer: "颠覆认知：真正的健康不是'没病'，而是拥有强大的自愈力！<br/><strong>健康的真正标志：</strong><br/>• <strong>精神饱满</strong>：不是兴奋，而是内心安定的活力<br/>• <strong>睡眠香甜</strong>：能快速入睡，醒来精神充沛<br/>• <strong>消化有力</strong>：吃什么都消化得了，不胀不痛<br/>• <strong>情绪稳定</strong>：遇事不焦虑，有韧性和弹性<br/>• <strong>恢复能力强</strong>：累了休息一下就满血复活<br/><strong>8年临床观察：</strong><br/>最健康的人不是从不生病，而是：<br/>• 生病了恢复得快<br/>• 压力大了调节得好<br/>• 疲劳了休息后能满血复活<br/>• 情绪低落时能自我修复<br/><strong>目标：</strong>不是追求'完美无缺'，而是培养'动态平衡'的能力。"
  },
  {
    question: "中医为什么说'治未病'？核心逻辑在这",
    answer: "'治未病'是中医最高明的地方，也是现代人最需要的健康智慧！<br/><strong>三个层次的'治未病'：</strong><br/>• <strong>未病先防</strong>：还没生病时就开始养生保健<br/>• <strong>既病防变</strong>：有了小毛病及时调理，不让它发展成大病<br/>• <strong>瘥后防复</strong>：病好了之后继续调理，防止复发<br/><strong>核心逻辑：</strong><br/>疾病不是突然出现的，都有一个发展过程：<br/>健康 → 亚健康 → 功能异常 → 器质性病变<br/><strong>实际应用：</strong><br/>• 感觉疲劳时就开始调理，不等到过劳死<br/>• 情绪不好时就疏解，不等到抑郁症<br/>• 消化不良时就调脾胃，不等到胃溃疡<br/><strong>巫医生的建议：</strong>把钱花在预防上，比花在治疗上划算100倍！"
  },
  // 体质与调理系列（11-20题）
  {
    question: "气虚、阳虚、阴虚，到底有什么区别？",
    answer: "这是最容易混淆的三种体质！搞清楚它们，调理才不会南辕北辙。<br/><strong>气虚质 - 能量不足型：</strong><br/>• 表现：说话没力气，容易累，一动就出汗<br/>• 比喻：手机电量不足，但还能用<br/>• 调理：补气，像给手机充电<br/><strong>阳虚质 - 怕冷型：</strong><br/>• 表现：手脚冰凉，怕冷，喜欢热饮<br/>• 比喻：暖气不足，房间冷<br/>• 调理：温阳，像开暖气<br/><strong>阴虚质 - 内热型：</strong><br/>• 表现：手心热，口干，盗汗，心烦<br/>• 比喻：水箱缺水，发动机过热<br/>• 调理：滋阴，像给水箱加水<br/><strong>关键：</strong>搞反了会出大问题！阳虚的人吃滋阴药，会越来越冷；阴虚的人吃温阳药，会上火更严重。"
  },
  {
    question: "痰湿体质为什么这么难调？",
    answer: "痰湿体质是现代人最常见、最难缠的体质！因为它是'生活方式病'。<br/><strong>痰湿是怎么来的？</strong><br/>• <strong>吃出来的</strong>：爱吃甜食、油腻、冷饮<br/>• <strong>坐出来的</strong>：久坐不动，气血不通<br/>• <strong>熬出来的</strong>：熬夜伤脾，脾虚生湿<br/><strong>痰湿的表现：</strong><br/>• 身体沉重，像背了个麻袋<br/>• 舌苔厚腻，像刷不干净<br/>• 容易水肿，喝水都长胖<br/>• 脸上爱出油，毛孔粗大<br/><strong>为什么难调？</strong><br/>因为痰湿不是一天形成的，也不可能一天消除。需要：<br/>• 改变饮食习惯（最重要！）<br/>• 增加运动出汗<br/>• 规律作息<br/>• 配合中药调理<br/><strong>记住：</strong>痰湿不是病，是生活方式的'垃圾堆积'！"
  },
  {
    question: "为什么中医总说'脾胃是后天之本'？",
    answer: "脾胃就是你的'能量转化站'，吃进去的食物能不能变成气血，全看脾胃！<br/><strong>脾胃到底有多重要？</strong><br/>• <strong>造血工厂</strong>：食物 → 脾胃运化 → 气血<br/>• <strong>免疫卫士</strong>：脾胃好，正气足，不易生病<br/>• <strong>情绪调节器</strong>：脾胃不好，容易焦虑多思<br/><strong>脾胃虚弱的表现：</strong><br/>• 吃一点就胀，不想吃饭<br/>• 大便不成形，容易腹泻<br/>• 脸色发黄，没有光泽<br/>• 四肢无力，容易疲劳<br/><strong>伤脾胃的行为：</strong><br/>• 暴饮暴食，饥一顿饱一顿<br/>• 吃太多生冷食物<br/>• 边吃饭边生气、边工作<br/>• 思虑过度，压力太大<br/><strong>养脾胃的方法：</strong><br/>• 规律饮食，七分饱<br/>• 细嚼慢咽，专心吃饭<br/>• 温热饮食，少吃寒凉<br/>• 保持心情愉悦"
  },
  {
    question: "熬夜到底伤的是什么？",
    answer: "熬夜不只是'缺觉'那么简单，它在透支你的生命能量！<br/><strong>中医角度看熬夜：</strong><br/>• <strong>伤肝血</strong>：晚上11点-凌晨3点是肝胆排毒时间，熬夜=毒素排不出<br/>• <strong>伤肾精</strong>：肾主藏精，熬夜=掏空肾的储蓄罐<br/>• <strong>伤脾胃</strong>：深夜进食，脾胃得不到休息<br/>• <strong>伤心神</strong>：该睡不睡，心神不宁，容易焦虑<br/><strong>熬夜的连锁反应：</strong><br/>肝血不足 → 眼睛干涩、脱发<br/>肾精亏虚 → 腰酸、记忆力下降<br/>脾胃虚弱 → 食欲不振、消化不良<br/>心神不安 → 失眠、焦虑、抑郁<br/><strong>熬夜后如何补救？</strong><br/>• 补充睡眠（但补不回来！）<br/>• 喝养肝茶（枸杞、菊花）<br/>• 吃补肾食物（黑芝麻、核桃）<br/>• 调理脾胃（小米粥、山药）<br/><strong>最好的方法：</strong>别熬夜！"
  },
  {
    question: "为什么老中医都说'虚不受补'？",
    answer: "很多人觉得身体虚就要补，结果越补越虚，甚至上火！为什么？<br/><strong>'虚不受补'的真相：</strong><br/>• 不是你的身体不需要补<br/>• 而是你的<strong>脾胃太虚弱</strong>，补药消化不了<br/>• 就像发动机坏了，再好的汽油也烧不了<br/><strong>虚不受补的表现：</strong><br/>• 吃补药就上火（口腔溃疡、便秘）<br/>• 吃补药就不消化（腹胀、打嗝）<br/>• 吃补药就头晕（气血上涌）<br/><strong>正确的补法：</strong><br/>1. <strong>先调脾胃</strong>：把消化功能修复好<br/>2. <strong>再慢慢补</strong>：从小剂量开始<br/>3. <strong>补中有泻</strong>：补的同时要疏通<br/>4. <strong>辨证施补</strong>：根据体质选补品<br/><strong>巫医生提醒：</strong><br/>气虚补气（人参、黄芪）<br/>血虚补血（阿胶、当归）<br/>阴虚滋阴（枸杞、麦冬）<br/>阳虚温阳（肉桂、附子）<br/>不能乱补！"
  },
  {
    question: "舌头真的能看出身体问题吗？",
    answer: "舌头是身体的'晴雨表'，中医看舌头，一眼就能判断你的体质和健康状态！<br/><strong>舌诊的秘密：</strong><br/>• <strong>舌质</strong>（舌头的颜色）：反映气血状态<br/>• <strong>舌苔</strong>（舌头上的苔）：反映脾胃和湿气<br/>• <strong>舌形</strong>（舌头的形状）：反映体质类型<br/><strong>常见舌象解读：</strong><br/><strong>1. 舌苔厚腻（白色或黄色）</strong><br/>→ 脾胃有湿，消化不良<br/><strong>2. 舌质淡白</strong><br/>→ 气血不足，阳虚体质<br/><strong>3. 舌质红、少苔</strong><br/>→ 阴虚内热，容易上火<br/><strong>4. 舌头胖大有齿痕</strong><br/>→ 脾虚湿重，身体水肿<br/><strong>5. 舌尖红、有红点</strong><br/>→ 心火旺，容易失眠焦虑<br/><strong>自查方法：</strong><br/>每天早上起床，对着镜子伸舌头看看，观察舌质、舌苔的变化。<br/><strong>注意：</strong>刚吃完有色食物（如咖啡、水果）不准确！"
  },
  {
    question: "经络穴位真的有用吗？还是玄学？",
    answer: "经络穴位不是玄学，是中医几千年临床经验的总结！<br/><strong>经络是什么？</strong><br/>• 不是血管，也不是神经<br/>• 是一种<strong>能量通道</strong>，气血运行的路径<br/>• 像高速公路，连接身体各个部位<br/><strong>穴位是什么？</strong><br/>• 经络上的<strong>交通枢纽</strong><br/>• 按压穴位 = 疏通堵塞，调节气血<br/><strong>常用穴位及功效：</strong><br/><strong>1. 足三里</strong>（膝盖下三寸）<br/>→ 健脾胃，增强体质<br/><strong>2. 三阴交</strong>（内踝上三寸）<br/>→ 调月经，养血安神<br/><strong>3. 合谷穴</strong>（虎口）<br/>→ 止痛，治头痛牙痛<br/><strong>4. 太冲穴</strong>（脚背大脚趾和二趾之间）<br/>→ 疏肝解郁，降肝火<br/><strong>5. 内关穴</strong>（手腕内侧两寸）<br/>→ 止呕，调心律，治失眠<br/><strong>如何使用？</strong><br/>• 每天按揉3-5分钟<br/>• 有酸麻胀的感觉最好<br/>• 坚持才有效果"
  },
  // 实用调理系列（21-30题）
  {
    question: "感冒了，中医怎么处理？",
    answer: "中医治感冒，要分清是'风寒'还是'风热'，治法完全相反！<br/><strong>风寒感冒 - 怕冷型：</strong><br/>• 症状：怕冷、流清鼻涕、打喷嚏、不发热或低热<br/>• 舌苔：白色<br/>• 治法：<strong>发汗散寒</strong><br/>• 食疗：生姜红糖水、葱白汤<br/>• 错误：吃寒凉的药，会加重病情<br/><strong>风热感冒 - 上火型：</strong><br/>• 症状：发热、喉咙痛、流黄鼻涕、口渴<br/>• 舌苔：黄色<br/>• 治法：<strong>清热解毒</strong><br/>• 食疗：菊花茶、绿豆汤、梨水<br/>• 错误：喝姜汤，会火上浇油<br/><strong>感冒的正确处理：</strong><br/>1. 多休息，别硬撑<br/>2. 多喝温水，帮助排毒<br/>3. 饮食清淡，减轻脾胃负担<br/>4. 适度出汗，但别大汗淋漓<br/><strong>预防感冒：</strong><br/>增强正气才是关键！规律作息、均衡饮食、适度运动。"
  },
  {
    question: "失眠怎么办？安眠药不是办法",
    answer: "失眠是现代人的通病！中医调失眠，要找到失眠的根本原因。<br/><strong>中医看失眠的类型：</strong><br/><strong>1. 心火旺型</strong><br/>• 表现：入睡困难，心烦，口舌生疮<br/>• 原因：压力大，思虑过度<br/>• 调理：清心火（莲子心泡水）<br/><strong>2. 肝郁化火型</strong><br/>• 表现：睡不安稳，多梦，易怒<br/>• 原因：情绪压抑，生闷气<br/>• 调理：疏肝解郁（玫瑰花茶）<br/><strong>3. 脾胃不和型</strong><br/>• 表现：睡不实，胃胀，消化不良<br/>• 原因：晚饭吃太多太晚<br/>• 调理：调理脾胃（晚饭早吃少吃）<br/><strong>4. 心脾两虚型</strong><br/>• 表现：难入睡，多梦易醒，心悸<br/>• 原因：思虑过度，气血不足<br/>• 调理：补气养血（桂圆红枣）<br/><strong>助眠妙招：</strong><br/>• 睡前泡脚（水温40度左右）<br/>• 按揉安眠穴、神门穴<br/>• 听舒缓音乐<br/>• 睡前别看手机！"
  },
  {
    question: "便秘就吃泻药？大错特错！",
    answer: "长期吃泻药，肠道会越来越懒！中医调便秘，要分清类型对症调理。<br/><strong>便秘的中医分型：</strong><br/><strong>1. 热秘 - 肠道有热</strong><br/>• 表现：大便干硬、口臭、脸上长痘<br/>• 原因：吃太多辛辣油炸食物<br/>• 调理：清热润肠（多吃蔬菜水果）<br/><strong>2. 气秘 - 气机不畅</strong><br/>• 表现：想拉拉不出，肚子胀<br/>• 原因：久坐不动，缺乏运动<br/>• 调理：运动促进肠蠕动（散步、按摩腹部）<br/><strong>3. 虚秘 - 气血不足</strong><br/>• 表现：有便意但无力排出，脸色苍白<br/>• 原因：气血不足，肠道动力不足<br/>• 调理：补气血（黄芪、当归）<br/><strong>4. 冷秘 - 阳虚寒凝</strong><br/>• 表现：大便不干但难排，怕冷<br/>• 原因：阳虚体质，肠道寒凝<br/>• 调理：温阳通便（肉苁蓉）<br/><strong>通用方法：</strong><br/>• 每天喝足够的水<br/>• 多吃富含纤维的食物<br/>• 养成定时排便习惯<br/>• 顺时针按摩腹部"
  },
  {
    question: "脱发、白发，中医怎么看？",
    answer: "头发是'血之余'，发质好坏反映气血状态！<br/><strong>脱发的中医原因：</strong><br/><strong>1. 肝肾阴虚型</strong><br/>• 表现：头发干枯易断，腰酸耳鸣<br/>• 原因：熬夜伤肾，肝血不足<br/>• 调理：滋补肝肾（黑芝麻、何首乌）<br/><strong>2. 气血两虚型</strong><br/>• 表现：头发稀疏，脸色苍白，疲乏无力<br/>• 原因：营养不良，气血不足<br/>• 调理：补气养血（红枣、桂圆）<br/><strong>3. 湿热上蒸型</strong><br/>• 表现：头发油腻，头皮痒，脱发<br/>• 原因：饮食油腻，湿热内生<br/>• 调理：清热祛湿（薏米、绿豆）<br/><strong>白发的原因：</strong><br/>• <strong>少年白</strong>：肾精不足，遗传因素<br/>• <strong>前额白</strong>：脾胃虚弱<br/>• <strong>两鬓白</strong>：肝胆火旺<br/>• <strong>后脑白</strong>：肾气不足<br/><strong>养发妙招：</strong><br/>• 保证充足睡眠（晚上11点前睡）<br/>• 多吃黑色食物（黑豆、黑芝麻）<br/>• 按摩头皮，促进血液循环<br/>• 减少染发烫发"
  },
  {
    question: "痛经能根治吗？不是忍忍就过去",
    answer: "痛经不是小事！中医认为'不通则痛'，调理得当是可以根治的！<br/><strong>痛经的中医分型：</strong><br/><strong>1. 气滞血瘀型</strong><br/>• 表现：经前或经期小腹胀痛，血块多<br/>• 原因：情绪压抑，肝气不舒<br/>• 调理：疏肝理气活血（玫瑰花茶、益母草）<br/><strong>2. 寒凝血瘀型</strong><br/>• 表现：小腹冷痛，热敷后缓解<br/>• 原因：贪凉、宫寒<br/>• 调理：温经散寒（红糖姜茶、艾灸）<br/><strong>3. 气血虚弱型</strong><br/>• 表现：经后小腹隐痛，月经量少<br/>• 原因：气血不足，子宫失养<br/>• 调理：补气养血（当归、阿胶）<br/><strong>4. 湿热下注型</strong><br/>• 表现：小腹灼痛，月经颜色深红<br/>• 原因：湿热内蕴<br/>• 调理：清热利湿（红豆薏米）<br/><strong>日常调理：</strong><br/>• 经期避免生冷食物<br/>• 保持腹部温暖<br/>• 适度运动，不要剧烈<br/>• 情绪保持愉悦<br/>• 按揉三阴交穴"
  },
  {
    question: "上火了怎么办？别急着喝凉茶",
    answer: "很多人一上火就喝凉茶，小心越喝越虚！上火也分'真火'和'虚火'！<br/><strong>真火（实火） - 真的热：</strong><br/>• 表现：口舌生疮、便秘、尿黄、脾气暴躁<br/>• 原因：吃太多辛辣油炸、熬夜<br/>• 舌象：舌质红，舌苔黄厚<br/>• 调理：可以喝凉茶、吃苦瓜、菊花茶<br/><strong>虚火（阴虚火旺） - 假的热：</strong><br/>• 表现：手心热、盗汗、口干但不想喝水<br/>• 原因：阴虚，水不足，相对显热<br/>• 舌象：舌质红，舌苔少<br/>• 调理：<strong>不能喝凉茶！</strong>要滋阴（麦冬、枸杞）<br/><strong>不同部位上火：</strong><br/><strong>心火</strong>：口舌生疮、失眠 → 莲子心泡水<br/><strong>肝火</strong>：眼睛红、易怒 → 菊花茶<br/><strong>胃火</strong>：口臭、牙龈肿痛 → 绿豆汤<br/><strong>肺火</strong>：咽喉痛、咳嗽 → 雪梨水<br/><strong>关键：</strong>分清虚实，对症降火！虚火用凉茶，会越来越虚！"
  },
  {
    question: "湿气重有哪些表现？如何祛湿？",
    answer: "湿气是'万恶之邪'，现代人十个有九个湿气重！<br/><strong>湿气重的表现：</strong><br/><strong>看舌头：</strong><br/>• 舌苔厚腻，白色或黄色<br/>• 舌头胖大，边缘有齿痕<br/><strong>看身体：</strong><br/>• 身体沉重，像背了个麻袋<br/>• 头重如裹，昏昏沉沉<br/>• 关节酸痛，活动不利<br/><strong>看排泄：</strong><br/>• 大便黏腻，冲不干净<br/>• 小便浑浊，不清亮<br/><strong>看皮肤：</strong><br/>• 脸上油腻，毛孔粗大<br/>• 容易长痘、湿疹<br/><strong>湿气的来源：</strong><br/>• <strong>外湿</strong>：环境潮湿，淋雨受凉<br/>• <strong>内湿</strong>：脾虚，饮食不当<br/><strong>祛湿方法：</strong><br/>1. <strong>健脾</strong>：脾虚生湿，健脾才能祛湿（山药、薏米）<br/>2. <strong>运动出汗</strong>：让湿气从汗液排出<br/>3. <strong>艾灸</strong>：温阳祛湿（灸足三里、阴陵泉）<br/>4. <strong>拔罐刮痧</strong>：排出体表湿气<br/>5. <strong>食疗</strong>：红豆薏米水、冬瓜汤<br/><strong>避免：</strong>生冷食物、甜食、油腻食物"
  },
  {
    question: "什么是'冬病夏治'？三伏贴真的有用吗？",
    answer: "'冬病夏治'是中医的智慧精华，利用夏天阳气旺盛调理冬天易发的病！<br/><strong>冬病夏治的原理：</strong><br/>• <strong>冬病</strong>：冬天容易发作或加重的疾病（哮喘、慢性支气管炎、关节炎等）<br/>• <strong>夏治</strong>：夏天阳气最旺，是调理阳虚寒证的最佳时机<br/>• <strong>机理</strong>：借助自然界的阳气，温补人体阳气，驱除寒邪<br/><strong>三伏贴的作用：</strong><br/>• 在三伏天（一年中最热的时候）贴敷穴位<br/>• 药物渗透皮肤，温通经络<br/>• 增强免疫力，减少冬季发病<br/><strong>适用疾病：</strong><br/>• 呼吸系统：哮喘、慢性支气管炎、反复感冒<br/>• 消化系统：慢性腹泻、胃寒<br/>• 骨关节：风湿、类风湿关节炎<br/>• 妇科：痛经、宫寒<br/><strong>注意事项：</strong><br/>• 孕妇、皮肤破损者不宜<br/>• 贴敷时间2-4小时<br/>• 贴后皮肤可能发红发痒，正常反应<br/>• 贴敷期间避免生冷食物<br/><strong>除了三伏贴：</strong><br/>夏天多晒太阳、适度运动出汗，都是冬病夏治的好方法！"
  },
  {
    question: "小孩子能吃中药吗？如何调理小儿体质？",
    answer: "小孩子可以吃中药，但要'轻清灵动'，用药更要谨慎！<br/><strong>小儿体质特点：</strong><br/>• <strong>脏腑娇嫩</strong>：发育不完全，容易生病也容易好<br/>• <strong>脾常不足</strong>：消化功能弱，容易积食<br/>• <strong>肺常不足</strong>：抵抗力弱，容易感冒<br/>• <strong>阳气旺盛</strong>：生长发育快，热证多见<br/><strong>小儿常见问题及调理：</strong><br/><strong>1. 反复感冒</strong><br/>• 原因：正气不足，外邪易侵<br/>• 调理：健脾补肺（山药、大枣）<br/>• 推拿：捏脊、按揉足三里<br/><strong>2. 积食</strong><br/>• 表现：不想吃饭、口臭、大便臭<br/>• 原因：吃太多，脾胃运化不了<br/>• 调理：消食导滞（山楂、麦芽）<br/>• 推拿：顺时针摩腹<br/><strong>3. 盗汗</strong><br/>• 原因：阴虚或气虚<br/>• 调理：滋阴敛汗（浮小麦、牡蛎）<br/><strong>4. 过敏体质</strong><br/>• 原因：脾肺不足，卫气不固<br/>• 调理：健脾补肺益气<br/><strong>小儿养护原则：</strong><br/>• 饮食有节，不要喂太饱<br/>• 穿衣适度，不要捂太热<br/>• 适度运动，增强体质<br/>• 推拿按摩，胜过吃药<br/>• 用药宜轻，不可过重"
  },
  {
    question: "老年人如何养生？重点在哪里？",
    answer: "老年人养生的关键：补而不滞，动而不过，养而有度！<br/><strong>老年人体质特点：</strong><br/>• <strong>气血渐衰</strong>：五脏功能减退<br/>• <strong>阳气不足</strong>：怕冷，代谢慢<br/>• <strong>脾胃虚弱</strong>：消化能力下降<br/>• <strong>肾气亏虚</strong>：骨骼、听力、记忆力下降<br/><strong>老年人养生五大重点：</strong><br/><strong>1. 养脾胃</strong><br/>• 饮食清淡易消化<br/>• 少量多餐，细嚼慢咽<br/>• 温热饮食，少吃生冷<br/><strong>2. 补肾气</strong><br/>• 黑色食物：黑豆、黑芝麻、黑木耳<br/>• 按摩涌泉穴、腰部<br/>• 适度房事，节制欲望<br/><strong>3. 养气血</strong><br/>• 补气：黄芪、党参<br/>• 养血：红枣、桂圆<br/>• 避免过度劳累<br/><strong>4. 疏通经络</strong><br/>• 每天散步30分钟<br/>• 太极拳、八段锦<br/>• 按摩穴位，拍打经络<br/><strong>5. 调畅情志</strong><br/>• 保持心情愉悦<br/>• 多参加社交活动<br/>• 培养兴趣爱好<br/><strong>老年人用药原则：</strong><br/>• 宜补不宜泻<br/>• 缓补为主，不可急攻<br/>• 注意药物相互作用<br/>• 定期体检，监测指标"
  },
  {
    question: "中医养生，从什么时候开始最好？",
    answer: "养生永远不嫌早，也永远不嫌晚！但最佳时机有讲究。<br/><strong>不同年龄段的养生重点：</strong><br/><strong>20-30岁 - 养肝护脾期：</strong><br/>• 重点：规律作息，别熬夜<br/>• 这个年龄最容易熬夜伤肝、饮食不规律伤脾<br/>• 养生方式：早睡早起，规律饮食，适度运动<br/><strong>30-40岁 - 养心补肾期：</strong><br/>• 重点：减压、养心神<br/>• 这个年龄工作压力大，容易焦虑失眠<br/>• 养生方式：学会放松，冥想打坐，补肾气<br/><strong>40-50岁 - 防未病期：</strong><br/>• 重点：预防慢性病<br/>• 这个年龄是慢性病高发期<br/>• 养生方式：定期体检，控制三高，调理体质<br/><strong>50岁以上 - 养正气期：</strong><br/>• 重点：补养气血，疏通经络<br/>• 这个年龄气血渐衰，要补而不滞<br/>• 养生方式：补益脾肾，适度运动，保持心态<br/><strong>最佳养生时机：</strong><br/>• <strong>从现在开始！</strong>无论多大年纪<br/>• 年轻时养生 = 投资健康<br/>• 年老时养生 = 延缓衰老<br/><strong>记住：</strong>养生不是为了长生不老，而是为了<strong>健康地活着</strong>，<strong>有质量地老去</strong>！"
  }
])

// 页面加载（无需额外操作）
onMounted(() => {
  // 页面初始化完成
})
</script>

<style scoped>
/* ========== 设计系统变量 ========== */
/* 统一的颜色、间距、圆角、阴影等设计规范 */

.learning-center {
  min-height: 100vh;
  background-color: #f5f7fa;
}

/* Section通用样式 */
.section-header {
  text-align: center;
  margin-bottom: 60px;
  position: relative;
}

.section-tag {
  display: inline-block;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 12px 32px;
  border-radius: 24px;
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 24px;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.25);
  transform: translateY(0);
  transition: all 0.3s ease;
}

.section-tag:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 32px rgba(102, 126, 234, 0.35);
}

.section-header h2 {
  font-size: 2.5rem;
  color: #2d3748;
  margin-bottom: 20px;
  position: relative;
  font-weight: 800;
  line-height: 1.2;
}

.section-header h2::after {
  content: '';
  position: absolute;
  bottom: -12px;
  left: 50%;
  transform: translateX(-50%);
  width: 60px;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  border-radius: 2px;
}

.section-desc {
  color: #64748b;
  font-size: 1.125rem;
  max-width: 700px;
  margin: 24px auto 0;
  line-height: 1.6;
  font-weight: 400;
  opacity: 0.9;
}

/* ========== 书签式卡片横向布局 ========== */
.core-tabs-section {
  max-width: 1400px;
  margin: 0 auto 60px;
  padding: 60px 40px;
  background: white;
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.tab-cards-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 24px;
}

.tab-card {
  position: relative;
  background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
  border-radius: 16px;
  padding: 32px 24px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  border: 2px solid transparent;
  overflow: hidden;
}

.tab-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #667eea, #764ba2);
  transform: scaleX(0);
  transform-origin: left;
  transition: transform 0.3s ease;
}

.tab-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 40px rgba(102, 126, 234, 0.2);
  border-color: #667eea;
}

.tab-card:hover::before {
  transform: scaleX(1);
}

.tab-card-icon {
  font-size: 3rem;
  text-align: center;
  margin-bottom: 16px;
  line-height: 1;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
  transition: transform 0.3s ease;
}

.tab-card:hover .tab-card-icon {
  transform: scale(1.1);
}

.tab-card-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d3748;
  text-align: center;
  margin-bottom: 12px;
  line-height: 1.3;
}

.tab-card-desc {
  font-size: 0.95rem;
  color: #64748b;
  text-align: center;
  line-height: 1.5;
  margin-bottom: 16px;
  opacity: 0.9;
}

.tab-card-arrow {
  font-size: 1.5rem;
  font-weight: 700;
  color: #667eea;
  text-align: center;
  opacity: 0;
  transform: translateX(-10px);
  transition: all 0.3s ease;
}

.tab-card:hover .tab-card-arrow {
  opacity: 1;
  transform: translateX(0);
}

/* 为不同卡片添加独特的渐变色 */
.tab-card:nth-child(1):hover {
  background: linear-gradient(135deg, #fef3c7 0%, #fef9e7 100%);
}

.tab-card:nth-child(2):hover {
  background: linear-gradient(135deg, #fee2e2 0%, #fef2f2 100%);
}

.tab-card:nth-child(3):hover {
  background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
}

.tab-card:nth-child(4):hover {
  background: linear-gradient(135deg, #d1fae5 0%, #f0fdf4 100%);
}

/* 响应式设计 - 书签式卡片 */
@media (max-width: 1200px) {
  .tab-cards-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 20px;
  }

  .core-tabs-section {
    padding: 50px 32px;
  }

  .layer-progression {
    flex-direction: column;
    align-items: center;
  }

  .layer {
    max-width: 600px;
    margin-bottom: 32px;
  }

  .layer:last-child {
    margin-bottom: 0;
  }
}

@media (max-width: 768px) {
  /* Section标题 */
  .section-header h2 {
    font-size: 2rem;
  }

  .section-desc {
    font-size: 1rem;
  }

  /* 核心板块 */
  .core-tabs-section {
    padding: 40px 24px;
    margin-bottom: 40px;
  }

  .tab-cards-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .tab-card {
    padding: 24px 20px;
  }

  .tab-card-icon {
    font-size: 2.5rem;
  }

  .tab-card-title {
    font-size: 1.25rem;
  }

  .tab-card-desc {
    font-size: 0.9rem;
  }

  /* 三层体系 */
  .three-layer-system {
    padding: 32px 20px;
  }

  .layer {
    max-width: 100%;
    padding: 24px 20px;
    margin-bottom: 24px;
  }

  .layer-number {
    width: 64px;
    height: 64px;
    font-size: 1.75rem;
  }

  .layer-title {
    font-size: 1.25rem;
  }

  .layer-subtitle {
    font-size: 0.95rem;
  }

  /* 问答区域 */
  .qa-header {
    padding: 32px 20px;
  }

  .qa-title {
    font-size: 1.75rem;
  }

  .qa-question {
    padding: 16px 20px;
  }

  .question-number {
    min-width: 40px;
    height: 40px;
    font-size: 0.875rem;
    margin-right: 12px;
  }

  .question-text {
    font-size: 0.95rem;
  }

  .qa-answer {
    padding: 0 20px 20px 72px;
  }

  .answer-content {
    font-size: 0.9rem;
  }

  /* CTA区域 */
  .cta-content {
    padding: 24px 20px;
  }

  .cta-content h3 {
    font-size: 1.25rem;
  }
}

/* 健康认知内容样式 */
.content-preview {
  margin-bottom: 80px;
  padding: 60px 20px;
  background: white;
  border-radius: 24px;
}

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

.arrow-indicator {
  font-weight: 900;
  font-size: 1.2em;
  color: #667eea;
  margin-left: 4px;
}

/* 客户见证预览样式 */
.testimonial-preview {
  margin-bottom: 80px;
  padding: 60px 20px;
  background: white;
  border-radius: 24px;
}

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
  padding: 100px 20px;
  text-align: center;
  position: relative;
  overflow: hidden;
  margin-bottom: 80px;
  border-radius: 24px;
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

/* Tab容器 */
.tabs-container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0;
}

.learning-tabs {
  background: transparent;
  padding: 0;
}

/* 隐藏Tab标签栏 - 只通过书签卡片切换 */
.learning-tabs.hidden-tabs :deep(.el-tabs__header) {
  display: none;
}

/* Tab标签样式 */
.learning-tabs :deep(.el-tabs__header) {
  margin-bottom: 30px;
}

.learning-tabs :deep(.el-tabs__item) {
  font-size: 1.1rem;
  font-weight: 600;
  padding: 0 30px;
  height: 50px;
  line-height: 50px;
}

.learning-tabs :deep(.el-tabs__item.is-active) {
  color: #667eea;
}

.learning-tabs :deep(.el-tabs__active-bar) {
  background-color: #667eea;
}

/* 课程内容样式 */
.courses-content {
  padding: 0;
}

/* 3层递进结构样式 */
.three-layer-system {
  max-width: 1400px;
  margin: 20px auto 0;
  padding: 40px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.08);
}

.layer-progression {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 24px;
}

.layer {
  flex: 1;
  max-width: 420px;
  background: white;
  border-radius: 16px;
  padding: 32px 24px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.layer:hover {
  transform: translateY(-8px);
  box-shadow: 0 16px 40px rgba(102, 126, 234, 0.15);
  border-color: #667eea;
}

.layer-header {
  text-align: center;
  margin-bottom: 24px;
  padding-bottom: 20px;
  border-bottom: 2px solid #f0f0f0;
}

.layer-number {
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  width: 80px;
  height: 80px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 700;
  margin: 0 auto 16px;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.25);
}

.layer-title {
  font-size: 1.5rem;
  color: #2d3748;
  font-weight: 700;
  margin-bottom: 8px;
  line-height: 1.3;
}

.layer-subtitle {
  color: #64748b;
  font-size: 1rem;
  line-height: 1.5;
}

.layer-content {
  background: transparent;
  padding: 0;
}

/* 课程目标样式 */
.layer-goal {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.08) 0%, rgba(118, 75, 162, 0.08) 100%);
  padding: 16px 20px;
  border-radius: 12px;
  margin-bottom: 20px;
  border-left: 4px solid #667eea;
  font-size: 0.95rem;
  color: #2d3748;
  line-height: 1.6;
}

.layer-goal strong {
  color: #667eea;
  font-weight: 700;
}

/* 课程项样式 */
.course-item {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #f8f9fa;
  margin-bottom: 12px;
  padding: 16px;
  border-radius: 12px;
  border-left: 4px solid #667eea;
  transition: all 0.3s ease;
  cursor: pointer;
}

.course-item:hover {
  transform: translateX(8px);
  background: #fff;
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  border-left-color: #764ba2;
}

.course-item:last-child {
  margin-bottom: 0;
}

/* 课程图标 */
.course-icon {
  font-size: 1.5rem;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

.course-item:hover .course-icon {
  transform: scale(1.1);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

/* 课程标题 */
.course-title {
  flex: 1;
  font-weight: 600;
  color: #2d3748;
  font-size: 0.95rem;
  line-height: 1.5;
}

/* 课程分类样式（第三层） */
.course-category {
  margin-top: 24px;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e9ecef;
}

.course-category:first-child {
  margin-top: 0;
}

.category-title {
  font-size: 1.25rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 6px;
  display: flex;
  align-items: center;
  gap: 8px;
  line-height: 1.3;
}

.category-desc {
  font-size: 0.875rem;
  color: #64748b;
  font-style: italic;
  margin-left: 32px;
  line-height: 1.5;
}

.skill-item {
  background: #f8f9fa;
  margin-bottom: 15px;
  padding: 20px;
  border-radius: 12px;
  border-left: 4px solid #FF6B35;
  transition: all 0.3s ease;
  cursor: pointer;
}

.skill-item:hover {
  transform: translateX(10px);
  background: #fff;
  box-shadow: 0 5px 15px rgba(0,0,0,0.1);
}

.skill-item:last-child {
  margin-bottom: 0;
}

.skill-title {
  font-weight: bold;
  color: #333;
  margin-bottom: 8px;
  font-size: 1.05em;
}

.skill-desc {
  color: #666;
  font-size: 0.9em;
}

.skill-detail {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #e0e0e0;
  display: none;
  color: #555;
  line-height: 1.6;
}

/* 问答内容样式 */
.qa-content {
  padding: 20px 0 0 0;
}

.qa-header {
  text-align: center;
  padding: 40px 32px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  margin-bottom: 24px;
  border-radius: 16px;
}

.qa-title {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #2d3748;
  line-height: 1.2;
}

.qa-subtitle {
  font-size: 1rem;
  color: #64748b;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.5;
}

/* 问答列表 */
.qa-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding-bottom: 40px;
}

.qa-item {
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.qa-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.qa-item.expanded {
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.15);
}

.qa-question {
  display: flex;
  align-items: center;
  padding: 20px 24px;
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}

.qa-item.expanded .qa-question {
  border-bottom-color: #f0f0f0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
}

.question-number {
  min-width: 44px;
  height: 44px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.95rem;
  margin-right: 16px;
  transition: all 0.3s ease;
}

.qa-item:hover .question-number {
  transform: scale(1.05);
}

.question-text {
  flex: 1;
  font-size: 1rem;
  font-weight: 600;
  color: #2d3748;
  line-height: 1.5;
}

.expand-icon {
  color: #667eea;
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.qa-item.expanded .expand-icon {
  transform: rotate(180deg);
}

.qa-answer {
  padding: 0 24px 24px 84px;
  animation: slideDown 0.3s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    max-height: 0;
  }
  to {
    opacity: 1;
    max-height: 1000px;
  }
}

.answer-content {
  color: #4a5568;
  line-height: 1.6;
  font-size: 0.95rem;
}

.answer-content :deep(strong) {
  color: #2d3748;
  font-weight: 600;
}

.answer-content :deep(br) {
  margin-bottom: 8px;
}

/* CTA引导区域样式 */
.cta-section {
  margin-top: 24px;
}

.cta-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
}

.cta-content {
  padding: 32px;
  text-align: center;
  color: white;
}

.cta-content h3 {
  font-size: 1.5rem;
  margin-bottom: 12px;
  font-weight: 700;
  line-height: 1.3;
}

.cta-content p {
  font-size: 1rem;
  margin-bottom: 20px;
  opacity: 0.95;
  line-height: 1.5;
}

.cta-buttons {
  display: flex;
  gap: 12px;
  justify-content: center;
  flex-wrap: wrap;
}

/* 测试弹窗样式 */
.test-modal-content {
  text-align: center;
}

.test-intro p {
  font-size: 1rem;
  color: #64748b;
  margin-bottom: 20px;
  line-height: 1.5;
}

.test-features {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.feature-item {
  font-size: 0.95rem;
  color: #2d3748;
  text-align: left;
  line-height: 1.5;
}

.qr-placeholder {
  margin: 20px 0;
}

.qr-code {
  width: 150px;
  height: 150px;
  background: #f5f7fa;
  border-radius: 12px;
  margin: 16px auto;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border: 2px dashed #ddd;
}

.join-modal-content {
  text-align: center;
}

.join-instructions {
  text-align: left;
  margin-top: 20px;
}

.join-instructions h4 {
  margin-bottom: 12px;
  color: #2d3748;
  font-size: 1.125rem;
  font-weight: 700;
}

.join-instructions ol {
  padding-left: 20px;
}

.join-instructions li {
  margin-bottom: 8px;
  color: #64748b;
  line-height: 1.5;
}

/* ========== 认知颠覆内容样式 ========== */
.cognition-content,
.misconceptions-content {
  padding: 0;
}

.content-section {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 20px;
}

/* 洞察卡片 */
.insight-card,
.warning-card,
.principle-card {
  background: white;
  border-radius: 16px;
  padding: 32px;
  margin-bottom: 32px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.insight-card h3,
.warning-card h3,
.principle-card h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 24px;
  line-height: 1.3;
}

/* 洞察列表 */
.insight-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.insight-item {
  display: flex;
  gap: 20px;
  padding: 20px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  border-radius: 12px;
  border-left: 4px solid #667eea;
  transition: all 0.3s ease;
}

.insight-item:hover {
  transform: translateX(8px);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
}

.insight-number {
  min-width: 48px;
  height: 48px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  font-weight: 700;
  flex-shrink: 0;
}

.insight-text h4 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 8px;
  line-height: 1.4;
}

.insight-text p {
  font-size: 0.95rem;
  color: #4a5568;
  line-height: 1.6;
  margin: 0;
}

/* 智慧网格 */
.wisdom-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.wisdom-item {
  padding: 24px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 12px;
  text-align: center;
  transition: all 0.3s ease;
}

.wisdom-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
}

.wisdom-icon {
  font-size: 3rem;
  margin-bottom: 12px;
  filter: drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1));
}

.wisdom-item h4 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 8px;
  line-height: 1.3;
}

.wisdom-item p {
  font-size: 0.95rem;
  color: #64748b;
  line-height: 1.5;
  margin: 0;
}

/* ========== 避坑指南内容样式 ========== */
.warning-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.warning-item {
  display: flex;
  gap: 20px;
  padding: 20px;
  background: linear-gradient(135deg, rgba(239, 68, 68, 0.05) 0%, rgba(220, 38, 38, 0.05) 100%);
  border-radius: 12px;
  border-left: 4px solid #ef4444;
  transition: all 0.3s ease;
}

.warning-item:hover {
  transform: translateX(8px);
  box-shadow: 0 4px 12px rgba(239, 68, 68, 0.15);
}

.warning-icon {
  font-size: 2rem;
  flex-shrink: 0;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 50%;
  box-shadow: 0 2px 8px rgba(239, 68, 68, 0.2);
}

.warning-content h4 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 12px;
  line-height: 1.4;
}

.warning-content p {
  font-size: 0.95rem;
  color: #4a5568;
  line-height: 1.6;
  margin-bottom: 8px;
}

.warning-content p:last-child {
  margin-bottom: 0;
}

.warning-content strong {
  color: #2d3748;
  font-weight: 700;
}

/* 原则网格 */
.principle-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 20px;
}

.principle-item {
  padding: 24px;
  background: linear-gradient(135deg, rgba(16, 185, 129, 0.05) 0%, rgba(5, 150, 105, 0.05) 100%);
  border-radius: 12px;
  border-left: 4px solid #10b981;
  transition: all 0.3s ease;
}

.principle-item:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 12px rgba(16, 185, 129, 0.15);
}

.principle-number {
  width: 40px;
  height: 40px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.125rem;
  font-weight: 700;
  margin-bottom: 12px;
}

.principle-item h4 {
  font-size: 1.125rem;
  font-weight: 700;
  color: #2d3748;
  margin-bottom: 8px;
  line-height: 1.4;
}

.principle-item p {
  font-size: 0.95rem;
  color: #4a5568;
  line-height: 1.5;
  margin: 0;
}

/* 响应式设计 - 新增内容 */
@media (max-width: 768px) {
  .wisdom-grid,
  .principle-grid {
    grid-template-columns: 1fr;
    gap: 16px;
  }

  .insight-item,
  .warning-item {
    flex-direction: column;
    padding: 16px;
  }

  .insight-number,
  .warning-icon {
    align-self: flex-start;
  }

  .insight-card,
  .warning-card,
  .principle-card {
    padding: 24px 20px;
    margin-bottom: 24px;
  }
}
</style>
