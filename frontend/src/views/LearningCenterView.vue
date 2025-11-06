<template>
  <div class="learning-center">
    <PageContainer>
      <!-- Tab切换区域 -->
      <div class="tabs-container">
        <el-tabs v-model="activeTab" class="learning-tabs" @tab-change="handleTabChange">
          <!-- 课程学习Tab -->
          <el-tab-pane label="📚 课程学习" name="courses">
            <div class="courses-content">
              <!-- 页面标题 -->
              <div class="page-title">
                <h1>📚 三层递进学习体系</h1>
                <p class="subtitle">用培训医生的专业体系，让普通人掌握健康管理技能</p>
              </div>

              <!-- 3层递进结构详细展示 -->
              <div class="three-layer-system">
                <div class="layer-progression">
                  <div class="layer">
                    <div class="layer-header">
                      <div class="layer-number">1</div>
                      <div class="layer-title">健康常识层</div>
                      <div class="layer-subtitle">先搞懂什么是健康</div>
                    </div>
                    <div class="layer-content">
                      <div class="skill-item" @click="toggleDetail($event)">
                        <div class="skill-title">健康本质理解</div>
                        <div class="skill-desc">从"有病找医生"到"健康触手可及"的认知转变</div>
                        <div class="skill-detail">
                          <strong>具体内容：</strong><br>
                          • 健康不等于没有症状，而是身心平衡状态<br>
                          • 疾病是身体的预警信号，需要倾听和理解<br>
                          • 预防重于治疗，投资健康认知比治病更划算<br>
                          • 每个人都是自己健康的第一责任人
                        </div>
                      </div>

                      <div class="skill-item" @click="toggleDetail($event)">
                        <div class="skill-title">身体运行规律</div>
                        <div class="skill-desc">用大白话讲清楚身体怎么工作</div>
                        <div class="skill-detail">
                          <strong>身体就像一家公司：</strong><br>
                          • 内脏器官 = 各个部门，各司其职<br>
                          • 血液循环 = 物流系统，运送营养和垃圾<br>
                          • 身体通道 = 信息网络，传递指令和反馈<br>
                          • 身心平衡 = 公司运营稳定，不出乱子
                        </div>
                      </div>

                      <div class="skill-item" @click="toggleDetail($event)">
                        <div class="skill-title">身体在"说话"</div>
                        <div class="skill-desc">身体不舒服时会给你信号，学会听懂</div>
                        <div class="skill-detail">
                          <strong>身体的求救信号：</strong><br>
                          • 脸色不好：说明身体内部有问题<br>
                          • 舌头变化：显示身体是上火还是受寒<br>
                          • 心情不好：会影响身体各器官工作<br>
                          • 睡不好觉：是身心健康的晴雨表
                        </div>
                      </div>

                      <div class="skill-item" @click="toggleDetail($event)">
                        <div class="skill-title">预防思维建立</div>
                        <div class="skill-desc">从被动治疗转向主动预防</div>
                        <div class="skill-detail">
                          <strong>思维转换：</strong><br>
                          • 未病先防：健康时就开始养生<br>
                          • 既病防变：有症状时防止加重<br>
                          • 瘥后防复：康复后防止复发<br>
                          • 因时制宜：根据季节调整方案<br>
                          • 投资思维：把健康当作最重要的资产管理
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="layer">
                    <div class="layer-header">
                      <div class="layer-number">2</div>
                      <div class="layer-title">实用工具层</div>
                      <div class="layer-subtitle">掌握具体操作方法</div>
                    </div>
                    <div class="layer-content">
                      <div class="skill-item" @click="toggleDetail($event)">
                        <div class="skill-title">常见病症解析</div>
                        <div class="skill-desc">把常见问题掰开了揉碎了讲明白</div>
                        <div class="skill-detail">
                          <strong>精讲病症：</strong><br>
                          • 消化系统：胃痛、腹泻、便秘<br>
                          • 呼吸系统：咳嗽、哮喘、感冒<br>
                          • 心血管系统：高血压、心悸<br>
                          • 妇科疾病：月经不调、更年期
                        </div>
                      </div>

                      <div class="skill-item" @click="toggleDetail($event)">
                        <div class="skill-title">身体类型判断</div>
                        <div class="skill-desc">同样的病，不同的人，调理方法完全不同</div>
                        <div class="skill-detail">
                          <strong>疾病体质分型：</strong><br>
                          • 胃病：寒胃型、热胃型、虚胃型、郁胃型<br>
                          • 失眠：心火型、肝郁型、脾虚型、肾虚型<br>
                          • 咳嗽：风寒型、风热型、痰湿型、肺虚型<br>
                          • 月经不调：气滞型、血瘀型、气血虚型、肾虚型<br>
                          • 高血压：肝阳型、痰湿型、肾虚型、血瘀型<br>
                          • 等等...
                        </div>
                      </div>

                      <div class="skill-item" @click="toggleDetail($event)">
                        <div class="skill-title">食疗配方库</div>
                        <div class="skill-desc">把厨房变成你的私人药房</div>
                        <div class="skill-detail">
                          <strong>精准食疗方案：</strong><br>
                          • 胃痛喝错汤只会越来越痛，教你分清寒热虚实<br>
                          • 失眠别再喝牛奶了，根据不同原因选对食材<br>
                          • 咳嗽分风寒风热，梨和姜可不能乱用<br>
                          • 大姨妈不调？红糖水不是万能的<br>
                          • 降压药膳，比单纯忌口更有效<br>
                          • 300+实用食疗方，每道都有具体制作方法
                        </div>
                      </div>

                      <div class="skill-item" @click="toggleDetail($event)">
                        <div class="skill-title">运动养生方案</div>
                        <div class="skill-desc">不同身体状况，运动方式差别很大</div>
                        <div class="skill-detail">
                          <strong>个性化运动指导：</strong><br>
                          • 气虚体质：太极拳、八段锦等柔和运动<br>
                          • 阳虚体质：慢跑、游泳等有氧运动<br>
                          • 痰湿体质：快走、爬山等强度运动<br>
                          • 血瘀体质：舞蹈、球类等活动性运动<br>
                          • 疾病康复期的运动禁忌和注意事项<br>
                          • 不同年龄段的运动强度调整
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="layer">
                    <div class="layer-header">
                      <div class="layer-number">3</div>
                      <div class="layer-title">实践应用层</div>
                      <div class="layer-subtitle">形成可持续健康习惯</div>
                    </div>
                    <div class="layer-content">
                      <div class="skill-item" @click="toggleDetail($event)">
                        <div class="skill-title">健康记录本</div>
                        <div class="skill-desc">记录自己身体变化，越来越了解自己</div>
                        <div class="skill-detail">
                          <strong>档案内容：</strong><br>
                          • 基础信息：年龄、性别、职业、家族史<br>
                          • 体质评估：九大体质测试结果<br>
                          • 症状记录：不适症状及变化趋势<br>
                          • 调理方案：个性化养生方案记录
                        </div>
                      </div>

                      <div class="skill-item" @click="toggleDetail($event)">
                        <div class="skill-title">家庭健康管理</div>
                        <div class="skill-desc">一人学习全家受益</div>
                        <div class="skill-detail">
                          <strong>管理体系：</strong><br>
                          • 家庭成员体质档案建立<br>
                          • 不同年龄段养生重点<br>
                          • 常见疾病家庭应对方案<br>
                          • 家庭药材储备清单
                        </div>
                      </div>

                      <div class="skill-item" @click="toggleDetail($event)">
                        <div class="skill-title">什么时候该看医生</div>
                        <div class="skill-desc">自己能解决和必须找医生，界限要分清</div>
                        <div class="skill-detail">
                          <strong>决策标准：</strong><br>
                          • 绿灯：可自我调理的症状<br>
                          • 黄灯：需要观察的症状<br>
                          • 红灯：必须就医的症状<br>
                          • 急诊指征：危及生命的症状
                        </div>
                      </div>

                      <div class="skill-item" @click="toggleDetail($event)">
                        <div class="skill-title">慢性病不可怕</div>
                        <div class="skill-desc">学会和慢性病和平共处，生活质量一样高</div>
                        <div class="skill-detail">
                          <strong>慢病管理策略：</strong><br>
                          • 高血压：不只是吃药，生活方式更重要<br>
                          • 糖尿病：血糖控制的中医智慧<br>
                          • 失眠症：找到根源，告别安眠药依赖<br>
                          • 慢性胃炎：养胃护胃的正确打开方式<br>
                          • 建立个人慢病管理档案和追踪系统
                        </div>
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
            <!-- 问答页面标题 -->
            <div class="qa-header">
              <h2 class="qa-title">健康认知问答</h2>
              <p class="qa-subtitle">颠覆错误健康观念，掌握不生病的底层逻辑</p>
            </div>

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
import PageContainer from '@/components/PageContainer.vue'

// Tab切换
const activeTab = ref('courses')

// 问答相关数据
const expandedItems = reactive<Record<number, boolean>>({})
const showTestModal = ref(false)
const showJoinModal = ref(false)

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
  }
  // 这里省略了其他20个问答，完整版本应包含所有30个问答
])

// 页面加载（无需额外操作）
onMounted(() => {
  // 页面初始化完成
})
</script>

<style scoped>
.learning-center {
  min-height: 100vh;
  background-color: #f5f5f5;
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

/* 页面标题 */
.page-title {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin: -20px -20px 40px -20px;
  border-radius: 12px;
}

.page-title h1 {
  font-size: 2.5rem;
  margin-bottom: 15px;
  font-weight: 700;
}

.page-title .subtitle {
  font-size: 1.2rem;
  opacity: 0.9;
  margin: 0;
}

/* 3层递进结构样式 */
.three-layer-system {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 20px;
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  border-radius: 24px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.08);
}

.layer-progression {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 30px;
}

.layer {
  flex: 1;
  max-width: 420px;
  background: white;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 15px 35px rgba(0, 0, 0, 0.1);
  transition: all 0.4s ease;
  border: 2px solid transparent;
}

.layer:hover {
  transform: translateY(-12px);
  box-shadow: 0 25px 50px rgba(255, 107, 53, 0.15);
  border-color: #FF6B35;
}

.layer-header {
  text-align: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 3px solid #f0f0f0;
}

.layer-number {
  background: linear-gradient(135deg, #FF6B35, #F9D949);
  color: white;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5em;
  font-weight: bold;
  margin: 0 auto 20px;
  box-shadow: 0 10px 25px rgba(255, 107, 53, 0.3);
}

.layer-title {
  font-size: 1.8em;
  color: #333;
  font-weight: bold;
  margin-bottom: 10px;
}

.layer-subtitle {
  color: #666;
  font-size: 1.1em;
}

.layer-content {
  background: transparent;
  padding: 0;
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
  padding: 0;
}

.qa-header {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  margin-bottom: 30px;
  border-radius: 12px;
}

.qa-title {
  font-size: 2.2rem;
  font-weight: 700;
  margin-bottom: 15px;
  color: #2d3748;
}

.qa-subtitle {
  font-size: 1.1rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* 问答列表 */
.qa-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
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
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.12);
}

.qa-item.expanded {
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.15);
}

.qa-question {
  display: flex;
  align-items: center;
  padding: 20px 25px;
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}

.qa-item.expanded .qa-question {
  border-bottom-color: #f0f0f0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
}

.question-number {
  min-width: 45px;
  height: 45px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  margin-right: 20px;
  transition: all 0.3s ease;
}

.qa-item:hover .question-number {
  transform: scale(1.1);
}

.question-text {
  flex: 1;
  font-size: 1.1rem;
  font-weight: 600;
  color: #2d3748;
  line-height: 1.4;
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
  padding: 0 25px 25px 90px;
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
  line-height: 1.7;
  font-size: 1rem;
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
  margin-top: 30px;
}

.cta-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
}

.cta-content {
  padding: 30px;
  text-align: center;
  color: white;
}

.cta-content h3 {
  font-size: 1.4rem;
  margin-bottom: 15px;
  font-weight: 600;
}

.cta-content p {
  font-size: 1rem;
  margin-bottom: 20px;
  opacity: 0.9;
  line-height: 1.5;
}

.cta-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

/* 测试弹窗样式 */
.test-modal-content {
  text-align: center;
}

.test-intro p {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 20px;
}

.test-features {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.feature-item {
  font-size: 1rem;
  color: #333;
  text-align: left;
}

.qr-placeholder {
  margin: 20px 0;
}

.qr-code {
  width: 150px;
  height: 150px;
  background: #f5f5f5;
  border-radius: 8px;
  margin: 15px auto;
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
  margin-bottom: 15px;
  color: #333;
}

.join-instructions ol {
  padding-left: 20px;
}

.join-instructions li {
  margin-bottom: 8px;
  color: #666;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .layer-progression {
    flex-direction: column;
    align-items: center;
  }

  .layer {
    max-width: 600px;
    margin-bottom: 40px;
  }
}

@media (max-width: 768px) {
  .page-title h1 {
    font-size: 2rem;
  }

  .page-title .subtitle {
    font-size: 1rem;
  }

  .three-layer-system {
    padding: 40px 20px;
  }

  .layer {
    max-width: 100%;
    padding: 25px 20px;
    margin-bottom: 25px;
  }

  .layer:last-child {
    margin-bottom: 0;
  }

  .layer-number {
    width: 80px;
    height: 80px;
    font-size: 2em;
  }

  .layer-title {
    font-size: 1.5em;
  }

  .layer-subtitle {
    font-size: 1em;
  }

  .skill-item {
    padding: 15px;
  }

  .qa-header {
    padding: 30px 15px;
  }

  .qa-title {
    font-size: 1.8rem;
  }

  .qa-question {
    padding: 15px 20px;
  }

  .question-number {
    min-width: 40px;
    height: 40px;
    font-size: 0.9rem;
    margin-right: 15px;
  }

  .question-text {
    font-size: 1rem;
  }

  .qa-answer {
    padding: 0 20px 20px 75px;
  }

  .cta-content {
    padding: 25px 20px;
  }
}
</style>
