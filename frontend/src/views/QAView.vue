<template>
  <div class="qa-view">
    <PageContainer>
      <div class="qa-content">
        <!-- 问答页面标题 -->
        <div class="qa-header">
          <h1 class="qa-title">健康认知问答</h1>
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
import { ref, reactive } from 'vue'
import PageContainer from '@/components/PageContainer.vue'
import { ArrowDown, ArrowUp } from '@element-plus/icons-vue'

// 展开状态管理
const expandedItems = reactive<Record<number, boolean>>({})
const showTestModal = ref(false)
const showJoinModal = ref(false)

// 切换展开状态
const toggleExpand = (index: number) => {
  expandedItems[index] = !expandedItems[index]
}

// 30个健康认知问答 - 基于商业策略的视频题目设计
// 对应商业策略文档中的30个热门视频题目
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
  // 思维框架系列（10个）
  {
    question: "学会这套思维，你就是自己的健康管家",
    answer: "8年临床总结出一套人人可学的健康管理思维模式！<br/><strong>健康管家思维框架：</strong><br/><strong>1. 观察思维</strong>：学会看懂身体信号<br/>• 看脸色：苍白、潮红、暗沉代表什么<br/>• 看舌苔：厚薄、颜色反映脾胃状态<br/>• 看精神：疲惫还是亢奋，都有原因<br/><strong>2. 分析思维</strong>：找到症状背后的原因<br/>• 不是头痛医头，而是找到头痛的根源<br/>• 不是止咳，而是分析咳嗽的性质<br/><strong>3. 系统思维</strong>：整体调理而非局部修补<br/>• 一个症状往往涉及多个脏腑<br/>• 调理一个，带动全身<br/><strong>4. 预防思维</strong>：未病先防胜过治病<br/>掌握这套思维，你就是自己最好的健康顾问！"
  },
  {
    question: "中医的整体观念是什么？",
    answer: "整体观念认为人体是一个有机的整体，各脏腑组织器官在生理上相互联系、相互协调，在病理上相互影响。同时，人与自然环境也是一个整体，季节变化、地理环境都会影响人体健康。因此，中医治病不是头痛医头、脚痛医脚，而是统筹兼顾，整体调理。"
  },
  {
    question: "什么是阴阳平衡？为什么重要？",
    answer: "阴阳是中医理论的核心概念，用来概括和说明事物的对立统一关系。在人体中，阴阳的平衡决定了健康状态，阴阳失衡则会导致疾病。阴阳平衡包括：<br/>• 阴阳的相对平衡<br/>• 阴阳的动态调节<br/>• 阴阳的相互转化<br/>维持阴阳平衡是中医养生和治病的根本目标。"
  },
  {
    question: "五脏六腑在中医中是如何相互关联的？",
    answer: "中医的五脏六腑不仅指解剖结构，更是功能系统的概念。五脏（心、肝、脾、肺、肾）为阴，主藏精气；六腑（小肠、胆、胃、大肠、膀胱、三焦）为阳，主传化物质。它们通过经络系统相互联系，形成：<br/>• 脏腑表里关系<br/>• 五行生克关系<br/>• 气血津液的循环<br/>这种关联性使得中医能够通过调理一个脏腑来影响整个机体。"
  },
  {
    question: "什么是气血津液？它们有什么作用？",
    answer: "<strong>气</strong>：推动和调控人体各种生理活动的精微物质<br/><strong>血</strong>：营养和滋润全身的红色液体<br/><strong>津液</strong>：人体内除血液以外的所有正常液体<br/>它们的作用：<br/>• 气：推动、温煦、防御、固摄、气化<br/>• 血：营养、滋润<br/>• 津液：滋润、濡养<br/>三者相互依存、相互转化，共同维持人体的正常生理活动。"
  },
  {
    question: "中医的经络系统是什么？",
    answer: "经络是运行气血、联系脏腑和体表及全身各部的通道，是人体功能的调控系统。包括：<br/>• <strong>经脉</strong>：主要的纵行干线，分为十二正经和奇经八脉<br/>• <strong>络脉</strong>：经脉的分支，遍布全身<br/>• <strong>腧穴</strong>：经络上的特殊点位，可以调节脏腑功能<br/>经络系统是中医针灸、按摩等治疗方法的理论基础。"
  },
  {
    question: "为什么失眠需要辨证论治？",
    answer: "失眠的病因病机复杂多样，不同的人失眠原因不同：<br/>• <strong>心火亢盛型</strong>：心烦不寐、面红目赤<br/>• <strong>痰热扰心型</strong>：胸闷脘痞、恶心嗳气<br/>• <strong>阴虚火旺型</strong>：五心烦热、盗汗<br/>• <strong>心脾两虚型</strong>：多梦易醒、心悸健忘<br/>• <strong>心胆气虚型</strong>：虚烦不寐、善惊易恐<br/>只有准确辨证，才能选择合适的治疗方法和方药。"
  },
  {
    question: "中医如何看待情志对健康的影响？",
    answer: "中医认为情志活动与脏腑功能密切相关，'七情'（喜、怒、忧、思、悲、恐、惊）过度或持续时间过长都会影响脏腑功能：<br/>• 喜伤心：过喜使心气涣散<br/>• 怒伤肝：暴怒使肝气上逆<br/>• 思伤脾：过度思虑损伤脾胃<br/>• 忧悲伤肺：忧愁悲伤耗伤肺气<br/>• 恐伤肾：恐惧使肾气不固<br/>因此，调节情志是养生保健的重要内容。"
  },
  {
    question: "什么是中医的'因时制宜'？",
    answer: "'因时制宜'是指根据不同的时间（季节、昼夜等）特点来调整治疗和养生方法：<br/>• <strong>四季养生</strong>：春养肝、夏养心、长夏养脾、秋养肺、冬养肾<br/>• <strong>昼夜节律</strong>：白天重阳气升发，夜晚重阴精内守<br/>• <strong>月份调理</strong>：根据月相变化调整作息<br/>• <strong>节气养生</strong>：依据二十四节气特点进行调养<br/>这体现了中医'天人合一'的思想。"
  },
  {
    question: "为什么要根据体质选择食物？",
    answer: "不同体质的人对食物的适应性不同，合适的食物能够改善体质，不合适的食物可能加重体质偏颇：<br/>• <strong>气虚质</strong>：宜温补益气食物，如黄芪、山药<br/>• <strong>阳虚质</strong>：宜温阳食物，如羊肉、肉桂<br/>• <strong>阴虚质</strong>：宜滋阴食物，如百合、银耳<br/>• <strong>痰湿质</strong>：宜化痰除湿食物，如薏米、冬瓜<br/>• <strong>湿热质</strong>：宜清热祛湿食物，如绿豆、荷叶<br/>个性化的食疗能够事半功倍。"
  },
  {
    question: "中医的'扶正祛邪'是什么意思？",
    answer: "'扶正祛邪'是中医治疗疾病的基本原则：<br/><strong>扶正</strong>：增强人体正气，提高抗病能力，包括补气、补血、补阴、补阳等<br/><strong>祛邪</strong>：祛除致病因素，包括清热、解毒、化痰、祛湿、活血等<br/>根据正邪的盛衰情况，可以采用：<br/>• 单纯扶正或祛邪<br/>• 先扶正后祛邪<br/>• 先祛邪后扶正<br/>• 扶正祛邪并用<br/>达到恢复健康的目的。"
  },
  {
    question: "什么是中医的'君臣佐使'组方原则？",
    answer: "'君臣佐使'是中医方剂组成的基本原则，体现了用药的主次和配伍关系：<br/>• <strong>君药</strong>：针对主证或主病的主要药物，药力最强<br/>• <strong>臣药</strong>：辅助君药治疗主证，或治疗兼证的药物<br/>• <strong>佐药</strong>：辅助君臣药，或制约君臣药毒性的药物<br/>• <strong>使药</strong>：引经药，引导诸药到达病所，或调和诸药<br/>这种组方原则使得方剂配伍严谨，疗效确切。"
  },
  {
    question: "中医如何理解疾病的发生发展？",
    answer: "中医认为疾病的发生发展遵循一定的规律：<br/><strong>病因</strong>：内因（情志、体质）、外因（六淫）、不内外因（饮食、劳逸、外伤等）<br/><strong>病机</strong>：邪正斗争、阴阳失调、气血失常、津液代谢异常<br/><strong>病理过程</strong>：<br/>• 由表入里<br/>• 由浅入深<br/>• 由轻到重<br/>• 相互传变<br/>了解这些规律有助于早期诊断和及时治疗。"
  },
  {
    question: "为什么要重视'胃气'？",
    answer: "中医认为'胃气'是人体后天之本，代表了脾胃的消化吸收功能：<br/><strong>胃气的重要性</strong>：<br/>• 化生气血的源泉<br/>• 维持生命活动的基础<br/>• 抗病能力的根本<br/><strong>胃气强弱的表现</strong>：<br/>• 胃气足：食欲好、消化佳、精神充沛<br/>• 胃气虚：食欲差、腹胀、乏力<br/><strong>保护胃气的方法</strong>：<br/>• 规律饮食<br/>• 适量进食<br/>• 情志调节<br/>• 合理用药"
  },
  {
    question: "什么是'肾为先天之本'？",
    answer: "'肾为先天之本'是指肾在人体生命活动中的根本地位：<br/><strong>肾的功能</strong>：<br/>• 藏精：储存和调节人体精气<br/>• 主生殖：控制生殖发育功能<br/>• 主骨生髓：主管骨骼和脑髓<br/>• 主水液：调节水液代谢<br/><strong>肾精的作用</strong>：<br/>• 促进生长发育<br/>• 维持生殖功能<br/>• 抗衰防老<br/>• 增强免疫力<br/>因此，养肾护肾是延缓衰老、防治疾病的关键。"
  },
  {
    question: "中医的'同病异治'和'异病同治'是什么意思？",
    answer: "这体现了中医辨证论治的灵活性：<br/><strong>同病异治</strong>：同一种疾病，由于患者的体质、病程、症状等不同，采用不同的治疗方法。如同样是感冒，有风寒感冒用辛温解表，风热感冒用辛凉解表。<br/><strong>异病同治</strong>：不同的疾病，如果病机相同，可以采用相同的治疗方法。如头痛、胁痛、月经不调，如果都属于肝气郁结，都可以用疏肝理气的方法治疗。"
  },
  {
    question: "为什么说'脾胃为后天之本'？",
    answer: "脾胃被称为'后天之本'是因为：<br/><strong>脾胃的功能</strong>：<br/>• 脾主运化：消化吸收水谷精微<br/>• 胃主受纳：接受和腐熟食物<br/>• 生成气血：将食物转化为营养物质<br/><strong>对健康的意义</strong>：<br/>• 营养供应的源泉<br/>• 免疫功能的基础<br/>• 其他脏腑功能的保障<br/><strong>调养方法</strong>：<br/>• 饮食有节<br/>• 细嚼慢咽<br/>• 定时定量<br/>• 避免生冷"
  },
  {
    question: "中医的'三因制宜'具体指什么？",
    answer: "'三因制宜'是中医治疗的基本原则，指：<br/><strong>因人制宜</strong>：根据患者的年龄、性别、体质、职业等特点制定治疗方案<br/><strong>因时制宜</strong>：根据季节、昼夜等时间因素调整治疗方法<br/><strong>因地制宜</strong>：根据地理环境、气候条件等因素选择治疗手段<br/>例如：<br/>• 老人用药宜轻<br/>• 夏天慎用温热药<br/>• 南方多湿用祛湿药<br/>• 北方多燥用润燥药"
  },
  {
    question: "什么是中医的'标本缓急'治则？",
    answer: "'标本缓急'是指在治疗时要分清主次、轻重、缓急：<br/><strong>标与本</strong>：<br/>• 本：疾病的根本原因<br/>• 标：疾病的表面现象<br/><strong>治疗原则</strong>：<br/>• <strong>急则治标</strong>：危急情况先控制症状<br/>• <strong>缓则治本</strong>：病情稳定时治疗根本<br/>• <strong>标本兼治</strong>：同时治疗症状和根因<br/>例如：高热昏迷时先退热（治标），热退后再调理体质（治本）。"
  },
  {
    question: "为什么中医强调'药食同源，寓医于食'？",
    answer: "这一理念体现了中医的预防思想和整体观念：<br/><strong>药食同源的基础</strong>：<br/>• 食物和药物都来源于自然<br/>• 都具有四气五味的属性<br/>• 都能影响人体的阴阳气血<br/><strong>寓医于食的优势</strong>：<br/>• 温和安全，副作用小<br/>• 便于长期调理<br/>• 符合生活习惯<br/>• 预防重于治疗<br/><strong>实际应用</strong>：<br/>• 根据体质选择食物<br/>• 随季节调整饮食<br/>• 药膳食疗配方"
  },
  {
    question: "中医如何看待'治未病'与现代预防医学的关系？",
    answer: "中医'治未病'思想与现代预防医学有相通之处，但各有特色：<br/><strong>共同点</strong>：<br/>• 都强调预防的重要性<br/>• 都注重早期干预<br/>• 都关注生活方式<br/><strong>中医特色</strong>：<br/>• 强调个体差异（体质辨识）<br/>• 注重整体调节（阴阳平衡）<br/>• 融入生活实践（养生保健）<br/>• 天人合一理念（因时因地制宜）<br/><strong>现代价值</strong>：为现代预防医学提供了独特的理论和方法。"
  }
])
</script>

<style scoped>
.qa-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.qa-content {
  max-width: 1000px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 问答页面标题 */
.qa-header {
  text-align: center;
  padding: 60px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  margin: -20px -20px 40px -20px;
  border-radius: 0 0 20px 20px;
}

.qa-title {
  font-size: 3rem;
  font-weight: 700;
  margin-bottom: 20px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.qa-subtitle {
  font-size: 1.2rem;
  opacity: 0.95;
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.6;
}

/* 问答列表 */
.qa-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-bottom: 60px;
}

.qa-item {
  background: white;
  border-radius: 15px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.08);
  overflow: hidden;
  transition: all 0.3s ease;
  cursor: pointer;
}

.qa-item:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.12);
}

.qa-item.expanded {
  box-shadow: 0 10px 30px rgba(102, 126, 234, 0.15);
}

.qa-question {
  display: flex;
  align-items: center;
  padding: 25px 30px;
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}

.qa-item.expanded .qa-question {
  border-bottom-color: #f0f0f0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
}

.question-number {
  min-width: 50px;
  height: 50px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1.1rem;
  margin-right: 20px;
  transition: all 0.3s ease;
}

.qa-item:hover .question-number {
  transform: scale(1.1);
}

.question-text {
  flex: 1;
  font-size: 1.2rem;
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
  padding: 0 30px 30px 100px;
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

/* 响应式设计 */
@media (max-width: 768px) {
  .qa-header {
    padding: 40px 20px;
    margin: -20px -20px 30px -20px;
  }
  
  .qa-title {
    font-size: 2.2rem;
  }
  
  .qa-subtitle {
    font-size: 1rem;
  }
  
  .qa-question {
    padding: 20px;
  }
  
  .question-number {
    min-width: 40px;
    height: 40px;
    font-size: 1rem;
    margin-right: 15px;
  }
  
  .question-text {
    font-size: 1.1rem;
  }
  
  .qa-answer {
    padding: 0 20px 25px 75px;
  }
  
  .answer-content {
    font-size: 0.95rem;
  }
}

@media (max-width: 480px) {
  .qa-header {
    padding: 30px 15px;
  }
  
  .qa-title {
    font-size: 1.8rem;
  }
  
  .qa-question {
    padding: 15px;
  }
  
  .question-number {
    min-width: 35px;
    height: 35px;
    font-size: 0.9rem;
    margin-right: 12px;
  }
  
  .question-text {
    font-size: 1rem;
  }
  
  .qa-answer {
    padding: 0 15px 20px 62px;
  }
  
  .answer-content {
    font-size: 0.9rem;
  }
}

/* CTA引导区域样式 */
.cta-section {
  margin-top: 40px;
  padding-bottom: 40px;
}

.cta-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.15);
  max-width: 600px;
  margin: 0 auto;
}

.cta-content {
  padding: 30px;
  text-align: center;
  color: white;
}

.cta-content h3 {
  font-size: 1.4rem;
  margin-bottom: 0.8rem;
  font-weight: 600;
}

.cta-content p {
  font-size: 1rem;
  margin-bottom: 1.5rem;
  opacity: 0.9;
  line-height: 1.5;
}

.cta-buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-buttons .el-button {
  padding: 10px 20px;
  font-size: 1rem;
  font-weight: 600;
  min-width: 130px;
}

/* 测试弹窗样式 */
.test-modal-content {
  text-align: center;
}

.test-intro p {
  font-size: 1.1rem;
  color: #666;
  margin-bottom: 1.5rem;
}

.test-features {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 2rem;
}

.feature-item {
  font-size: 1rem;
  color: #333;
  text-align: left;
  padding: 5px 0;
}

.qr-placeholder {
  margin: 1.5rem 0;
}

.qr-code {
  width: 150px;
  height: 150px;
  background: #f5f5f5;
  border-radius: 8px;
  margin: 1rem auto;
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
  margin-top: 1.5rem;
}

.join-instructions h4 {
  margin-bottom: 1rem;
  color: #333;
}

.join-instructions ol {
  padding-left: 1.5rem;
}

.join-instructions li {
  margin-bottom: 0.5rem;
  color: #666;
}

/* 移动端响应式 */
@media (max-width: 768px) {
  .cta-content {
    padding: 25px 20px;
  }

  .cta-content h3 {
    font-size: 1.3rem;
  }

  .cta-content p {
    font-size: 0.95rem;
  }

  .cta-buttons {
    flex-direction: column;
    align-items: center;
    gap: 12px;
  }

  .cta-buttons .el-button {
    min-width: 180px;
  }
}
</style>