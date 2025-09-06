<template>
  <div class="assessment">
    <PageContainer>
      <div class="assessment-content">
        <!-- 体质测评标题区域 -->
        <div class="assessment-header">
          <h1 class="assessment-title">体质测评</h1>
          <p class="assessment-subtitle">用整体性视角分析身体信号和健康状态</p>
        </div>

        <!-- 疾病选择界面 -->
        <div class="disease-selection" v-if="!selectedDisease">
          <div class="selection-header">
            <h2>选择测评类型</h2>
            <p>请选择您想要进行的专业测评，我们将为您提供个性化的健康分析</p>
          </div>
          
          <div class="disease-cards">
            <div 
              v-for="disease in diseases" 
              :key="disease.code"
              class="disease-card"
              :class="{ disabled: disease.status !== 'active' }"
              @click="selectDisease(disease)"
            >
              <div class="card-icon">{{ getIconClass(disease.code) }}</div>
              <h3>{{ disease.name }}</h3>
              <div class="disease-status">
                <span v-if="disease.status === 'active'" class="available">✅ 可用</span>
                <span v-else class="coming-soon">🚧 {{ disease.status === 'coming_soon' ? '开发中' : '暂不可用' }}</span>
              </div>
              <p class="disease-description">{{ getDiseaseDescription(disease.code) }}</p>
            </div>
          </div>
        </div>

        <!-- 已选疾病信息 -->
        <div class="selected-disease-section" v-if="selectedDisease && !isStarted">
          <div class="back-button-container">
            <el-button @click="backToSelection" :icon="ArrowLeft">返回选择</el-button>
          </div>
          
          <div class="selected-disease-info">
            <h2>{{ getDiseaseName(selectedDisease) }}专业测评</h2>
            <p>{{ getDiseaseDescription(selectedDisease) }}</p>
          </div>
          
          <div class="assessment-features">
            <div v-for="feature in getCurrentDiseaseFeatures()" :key="feature.title" class="feature-item">
              <div class="feature-icon">{{ feature.icon }}</div>
              <h3>{{ feature.title }}</h3>
              <p>{{ feature.description }}</p>
            </div>
          </div>
          
          <div class="start-info">
            <div class="time-estimate">
              <el-icon><Clock /></el-icon>
              <span>预计用时：{{ getEstimatedTime() }}</span>
            </div>
            <div class="question-count">
              <el-icon><Document /></el-icon>
              <span>题目数量：{{ totalQuestions }}题</span>
            </div>
          </div>
          
          <div class="start-actions">
            <el-button type="primary" size="large" class="start-button" @click="startAssessment">
              开始测评
            </el-button>
          </div>
        </div>

        <!-- 测评进度条 -->
        <div class="progress-section" v-if="isStarted">
          <div class="progress-info">
            <span>测评进度</span>
            <span>{{ currentQuestion + 1 }}/{{ totalQuestions }}</span>
          </div>
          <el-progress 
            :percentage="progressPercentage" 
            :stroke-width="6"
            color="#667eea"
          />
        </div>

        <!-- 测评问题界面 -->
        <div class="question-section" v-if="isStarted && !isCompleted">
          <div class="question-card" :class="currentQuestionData.css_class">
            <div class="question-header" :style="{ textAlign: currentQuestionData.layout?.question_alignment || 'center' }">
              <div class="question-number" v-if="currentQuestionData.layout?.show_question_number">
                {{ currentQuestionData.number }}
              </div>
              <h3 class="question-title">{{ currentQuestionData.title }}</h3>
              <p class="question-description" 
                 :class="{ 'multi-select': currentQuestionData.type === '多选' }" 
                 v-if="currentQuestionData.description">
                {{ currentQuestionData.description }}
              </p>
            </div>
            
            <div class="question-options">
              <!-- 单选题 -->
              <el-radio-group 
                v-if="currentQuestionData.type === '单选'"
                v-model="currentAnswer" 
                class="option-group"
                :style="{ 
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2px',
                  width: '100%'
                }"
                @change="handleAnswerChange"
              >
                <el-radio 
                  v-for="option in currentQuestionData.options" 
                  :key="option.value" 
                  :label="option.value"
                  class="option-item"
                >
                  <div class="option-content">
                    <div class="option-text">{{ option.text }}</div>
                    <div class="option-description" v-if="option.description">
                      {{ option.description }}
                    </div>
                  </div>
                </el-radio>
              </el-radio-group>

              <!-- 是非题 -->
              <el-radio-group 
                v-else-if="currentQuestionData.type === '是非'"
                v-model="currentAnswer" 
                class="option-group yes-no-group"
                :style="{ 
                  display: 'grid',
                  gridTemplateColumns: `repeat(${currentQuestionData.layout?.options_per_row || 2}, 1fr)`,
                  gap: '20px',
                  justifyItems: 'center',
                  maxWidth: '400px',
                  margin: '0 auto'
                }"
                @change="handleAnswerChange"
              >
                <el-radio 
                  v-for="option in currentQuestionData.options" 
                  :key="option.value" 
                  :label="option.value"
                  class="option-item yes-no-item"
                >
                  <div class="option-content">
                    <div class="option-text">{{ option.text }}</div>
                  </div>
                </el-radio>
              </el-radio-group>

              <!-- 多选题 -->
              <el-checkbox-group 
                v-else-if="currentQuestionData.type === '多选'"
                v-model="currentAnswerArray"
                class="option-group"
                :style="{ 
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '2px',
                  width: '100%'
                }"
                @change="handleMultiAnswerChange"
              >
                <el-checkbox 
                  v-for="option in currentQuestionData.options" 
                  :key="option.value" 
                  :label="option.value"
                  class="option-item"
                >
                  <div class="option-content">
                    <div class="option-text">{{ option.text }}</div>
                  </div>
                </el-checkbox>
              </el-checkbox-group>
            </div>

            <div class="question-actions">
              <el-button 
                v-if="currentQuestion > 0" 
                @click="previousQuestion"
                :disabled="isSubmitting"
              >
                上一题
              </el-button>
              <el-button 
                type="primary" 
                @click="nextQuestion"
                :disabled="!hasAnswer || isSubmitting"
                :loading="isSubmitting"
              >
                {{ currentQuestion === totalQuestions - 1 ? '完成测评' : '下一题' }}
              </el-button>
            </div>
          </div>
        </div>

        <!-- 测评结果界面 -->
        <div class="result-section" v-if="isCompleted">
          <div class="result-header">
            <el-icon class="success-icon"><SuccessFilled /></el-icon>
            <h2>{{ getDiseaseName(selectedDisease) }}测评报告</h2>
            <p>基于中医理论和您的答题情况，为您生成专业的测评分析报告</p>
          </div>

          <!-- 诊断结果展示 -->
          <div class="diagnosis-result" v-if="diagnosisResult">
            <!-- 测评报告卡片 -->
            <div class="diagnosis-card">
              <h3>📋 您的失眠测评报告</h3>
              
              <div class="diagnosis-summary">
                <div class="syndrome-result">
                  <span class="label">🔸 证型诊断：</span>
                  <span class="syndrome-name">{{ diagnosisResult.syndrome_type }}</span>
                </div>
                <div class="confidence-result">
                  <span class="label">🔸 得分：</span>
                  <span class="confidence-value">{{ (diagnosisResult.confidence * 100).toFixed(0) }}</span>
                </div>
              </div>

              <div class="analysis-section" v-if="diagnosisResult.analysis">
                <h4>📄 病机分析</h4>
                <p>{{ diagnosisResult.analysis }}</p>
              </div>
            </div>

            <!-- 治疗方案 -->
            <div class="treatment-plan">
              <h3>📋 详细治疗方案</h3>
              
              <div class="treatment-sections">
                <div class="treatment-item">
                  <div class="treatment-header">
                    <span class="treatment-icon">💊</span>
                    <h4>中药调理方案</h4>
                  </div>
                  <div class="treatment-content">
                    {{ diagnosisResult.treatment_plan.herbal_medicine }}
                  </div>
                </div>
                
                <div class="treatment-item">
                  <div class="treatment-header">
                    <span class="treatment-icon">🖐️</span>
                    <h4>外治法指导</h4>
                  </div>
                  <div class="treatment-content">
                    {{ diagnosisResult.treatment_plan.external_treatment }}
                  </div>
                </div>
                
                <div class="treatment-item">
                  <div class="treatment-header">
                    <span class="treatment-icon">🍲</span>
                    <h4>食疗建议</h4>
                  </div>
                  <div class="treatment-content">
                    {{ diagnosisResult.treatment_plan.diet_therapy }}
                  </div>
                </div>
                
                <div class="treatment-item">
                  <div class="treatment-header">
                    <span class="treatment-icon">🌱</span>
                    <h4>生活调养</h4>
                  </div>
                  <div class="treatment-content">
                    {{ diagnosisResult.treatment_plan.lifestyle }}
                  </div>
                </div>
              </div>
            </div>

            <!-- 重要免责声明 -->
            <div class="disclaimer">
              <div class="disclaimer-content">
                <span class="disclaimer-icon">⚠️</span>
                <p><strong>重要声明：</strong></p>
                <ul style="margin: 10px 0; padding-left: 20px;">
                  <li>本系统仅供健康参考，不能替代专业医生诊断和治疗</li>
                  <li>任何药物使用必须在专业中医师指导下进行</li>
                  <li>如有严重或持续症状，请立即就医</li>
                  <li>不得将本报告作为自行用药或停药的依据</li>
                </ul>
              </div>
            </div>
          </div>

          <div class="result-actions">
            <el-button type="primary" @click="downloadReport">
              下载报告
            </el-button>
            <el-button @click="restartAssessment">
              重新测评
            </el-button>
          </div>
        </div>
      </div>
    </PageContainer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import PageContainer from '@/components/PageContainer.vue'
import { Clock, Document, SuccessFilled, ArrowLeft } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

// 测评状态
const isStarted = ref(false)
const isCompleted = ref(false)
const isSubmitting = ref(false)
const selectedDisease = ref('')

// 疾病数据
const diseases = ref([
  { code: 'insomnia', name: '失眠', status: 'active' },
  { code: 'stomach', name: '胃病', status: 'coming_soon' },
  { code: 'aging', name: '早衰', status: 'coming_soon' },
  { code: 'consultation', name: '专家咨询', status: 'active' }
])

// 题目相关
const currentQuestion = ref(0)
const currentAnswer = ref('')
const currentAnswerArray = ref<string[]>([])
const answers = ref<any[]>([])
const totalQuestions = ref(19) // 失眠诊断19题
const diagnosisResult = ref(null)

// 测评数据（占位，等待实际内容）
const questions = ref([])

// 计算属性
const progressPercentage = computed(() => {
  return Math.round((currentQuestion.value / totalQuestions.value) * 100)
})

const currentQuestionData = computed(() => {
  return questions.value[currentQuestion.value] || {}
})

// 检查题目是否应该显示
const shouldShowQuestion = (questionId: number) => {
  // 第9题的条件显示逻辑：只有第8题选择了药物才显示
  if (questionId === 9 && selectedDisease.value === 'insomnia') {
    const question8Answer = answers.value.find(a => a.question_id === 8)
    if (question8Answer && question8Answer.selected_options && question8Answer.selected_options.length > 0) {
      const options = question8Answer.selected_options
      
      // 如果只选择了"无"（F选项）-> 不显示第9题
      if (options.length === 1 && (options.includes('F') || options.includes('无'))) {
        return false
      }
      
      // 如果选择了药物（A-E选项中的任意一个，可能还包含F）-> 显示第9题
      const hasMedicine = options.some(opt => 
        ['A', 'B', 'C', 'D', 'E'].includes(opt) ||
        ['苯二氮䓬类：地西泮、劳拉西泮', '非苯二氮䓬类：唑吡坦、右佐匹克隆', 
         '褪黑素受体激动剂：雷美替胺', '食欲素受体拮抗剂：苏沃雷生', 
         '抗抑郁药物：曲唑酮、米氮平'].includes(opt)
      )
      
      return hasMedicine
    }
    // 第8题还没回答，不显示第9题
    return false
  }
  return true
}

const hasAnswer = computed(() => {
  const currentQ = questions.value[currentQuestion.value]
  if (!currentQ) return false
  
  if (currentQ.type === '单选') {
    return currentAnswer.value !== ''
  } else if (currentQ.type === '多选') {
    // 多选题可以一个都不选
    return true
  } else if (currentQ.type === '是非') {
    return currentAnswer.value !== ''
  }
  return false
})

// 方法
const getIconClass = (diseaseCode: string) => {
  const iconMap = {
    insomnia: '🌙',
    stomach: '🫃', 
    aging: '⏰',
    consultation: '👨‍⚕️'
  }
  return iconMap[diseaseCode] || '📋'
}

const selectDisease = async (disease: any) => {
  if (disease.status !== 'active') {
    ElMessage.warning('该功能暂未开放，敬请期待')
    return
  }
  
  // 如果选择专家咨询，显示选择页面而不是直接开始
  if (disease.code === 'consultation') {
    selectedDisease.value = disease.code
    return
  }
  
  selectedDisease.value = disease.code
  
  // 根据疾病类型加载相应的问卷并直接开始测评
  if (disease.code === 'insomnia') {
    await loadInsomniaQuestions()
    // 直接开始测评，跳过介绍页面
    isStarted.value = true
    currentQuestion.value = 0
    currentAnswer.value = ''
  } else if (disease.code === 'stomach') {
    await loadStomachQuestions()
  } else if (disease.code === 'aging') {
    await loadAgingQuestions()
  }
}

const backToSelection = () => {
  selectedDisease.value = ''
  questions.value = []
}

const getDiseaseName = (code: string) => {
  const diseaseMap = {
    insomnia: '失眠',
    stomach: '胃病',
    aging: '早衰',
    consultation: '专家咨询'
  }
  return diseaseMap[code] || ''
}

const getDiseaseDescription = (code: string) => {
  const descMap = {
    insomnia: '基于中医理论的失眠专业测评，通过19项专业问诊，运用二元测评算法，为您提供个性化的失眠治疗方案',
    stomach: '胃病专业测评（开发中）',
    aging: '早衰专业测评（开发中）',
    consultation: '与资深中医师一对一在线咨询，获得专业的健康指导和治疗建议'
  }
  return descMap[code] || ''
}

const getCurrentDiseaseFeatures = () => {
  const featureMap = {
    insomnia: [
      { icon: '🔍', title: '专业问诊', description: '19项标准化失眠评估问题' },
      { icon: '🧠', title: '二元测评', description: '独创的行列交叉测评系统' },
      { icon: '💊', title: '治疗方案', description: '中药、外治、食疗三位一体' }
    ],
    stomach: [
      { icon: '🎯', title: '胃病测评', description: '专业胃病测评（开发中）' }
    ],
    aging: [
      { icon: '🎯', title: '早衰测评', description: '专业早衰测评（开发中）' }
    ],
    consultation: [
      { icon: '👨‍⚕️', title: '专家咨询', description: '资深中医师一对一咨询' },
      { icon: '💬', title: '在线交流', description: '文字、语音、视频多种方式' },
      { icon: '📋', title: '个性方案', description: '针对性治疗建议和调理方案' }
    ]
  }
  return featureMap[selectedDisease.value] || []
}

const getEstimatedTime = () => {
  const timeMap = {
    insomnia: '8-10分钟',
    stomach: '6-8分钟',
    aging: '8-12分钟'
  }
  return timeMap[selectedDisease.value] || '8-10分钟'
}

const loadInsomniaQuestions = async () => {
  try {
    // 调用API获取失眠问卷
    const response = await fetch('/api/diagnosis/insomnia/questionnaire')
    const data = await response.json()
    
    // 检查API响应格式
    if (data.success && data.data) {
      // 转换API返回的问题格式，包含布局信息
      questions.value = data.data.questions.map(q => ({
        id: q.id,
        title: q.text,
        number: q.number || `第${q.id}题`,
        description: q.type === 'multiple' ? '可以多选和不选' : (q.hint || ''),
        category: q.category,
        type: q.type === 'single' ? '单选' : (q.type === 'multiple' ? '多选' : (q.type === 'yes_no' ? '是非' : '单选')),
        css_class: q.css_class,
        layout: q.layout || {
          question_alignment: 'center',
          options_per_row: 3,
          option_alignment: 'left',
          show_question_number: true
        },
        options: q.options.map(opt => ({
          value: opt.value,
          text: opt.label,
          display: opt.display
        }))
      }))
      
      // 保存全局布局配置
      window.layoutConfig = data.data.layout_config || {}
      
      totalQuestions.value = questions.value.length
      
      // 初始化答案数组
      answers.value = questions.value.map(q => ({
        question_id: q.id,
        selected_options: []
      }))
    } else {
      throw new Error('API响应格式错误')
    }
    
  } catch (error) {
    console.error('加载问题失败:', error)
    ElMessage.error('API加载失败，使用默认问题')
    // 如果接口失败，使用默认问题
    
    // 临时模拟数据 - 失眠专业问诊
    questions.value = [
      {
        id: 1,
        title: "您认为自己的睡眠状况如何？",
        description: "请根据最近一个月的情况选择",
        category: "睡眠质量",
        type: "单选",
        options: [
          { value: '好', text: '睡眠质量很好，很少失眠' },
          { value: '一般', text: '睡眠质量一般，偶尔失眠' },
          { value: '较差', text: '睡眠质量较差，经常失眠' },
          { value: '很差', text: '睡眠质量很差，严重失眠' }
        ]
      },
      {
        id: 2,
        title: "通常情况下，您从上床准备睡觉到真正入睡需要多长时间？",
        description: "",
        category: "入睡时间",
        type: "单选",
        options: [
          { value: '5分钟以内', text: '5分钟以内' },
          { value: '6-15分钟', text: '6-15分钟' },
          { value: '16-30分钟', text: '16-30分钟' },
          { value: '31-60分钟', text: '31-60分钟' },
          { value: '60分钟以上', text: '60分钟以上' }
        ]
      },
      {
        id: 3,
        title: "过去一个月内，您每天夜间睡眠时间有多长？",
        description: "",
        category: "睡眠时长",
        type: "单选",
        options: [
          { value: '8小时及以上', text: '8小时及以上' },
          { value: '7-8小时', text: '7-8小时' },
          { value: '6-7小时', text: '6-7小时' },
          { value: '5-6小时', text: '5-6小时' },
          { value: '5小时以下', text: '5小时以下' }
        ]
      },
      {
        id: 4,
        title: "过去一个月内，您夜间平均醒来的次数大约是？",
        description: "",
        category: "夜醒次数",
        type: "单选",
        options: [
          { value: '几乎不醒来', text: '几乎不醒来' },
          { value: '1次', text: '1次' },
          { value: '2-3次', text: '2-3次' },
          { value: '4次及以上', text: '4次及以上' }
        ]
      },
      {
        id: 5,
        title: "您是否经常精神压力大/情绪紧张？",
        description: "",
        category: "精神状态",
        type: "单选",
        options: [
          { value: '是', text: '是' },
          { value: '否', text: '否' }
        ]
      },
      {
        id: 6,
        title: "您近期有无如下问题？",
        description: "",
        category: "身体症状",
        type: "单选",
        options: [
          { value: '时有耳鸣', text: '时有耳鸣' },
          { value: '时感疲乏乏力', text: '时感疲乏，乏力，周身疲倦' },
          { value: '腹胀腹泻不适', text: '腹胀/腹泻不适' }
        ]
      },
      {
        id: 7,
        title: "您是否经常周身酸痛/骨节疼痛？",
        description: "",
        category: "疼痛症状",
        type: "单选",
        options: [
          { value: '是', text: '是' },
          { value: '否', text: '否' }
        ]
      },
      {
        id: 8,
        title: "您近期有无如下问题？",
        description: "",
        category: "特殊症状",
        type: "单选",
        options: [
          { value: '夜间遗精遗尿', text: '夜间遗精/遗尿，心悸加速' },
          { value: '皮肤瘙痒', text: '皮肤瘙痒，发疹麻疹' },
          { value: '咳嗽气短', text: '咳嗽/气短/呼吸困难' }
        ]
      },
      {
        id: 9,
        title: "您是否持续使用电子产品超过3小时/天？",
        description: "",
        category: "生活习惯",
        type: "单选",
        options: [
          { value: '是', text: '是' },
          { value: '否', text: '否' }
        ]
      },
      {
        id: 10,
        title: "您近期有无如下问题？",
        description: "",
        category: "中医症状",
        type: "单选",
        options: [
          { value: '面色暗黑', text: '面色暗黑，无精打采' },
          { value: '容易受惊', text: '容易受惊，害怕' },
          { value: '夜间盗汗', text: '夜间盗汗' }
        ]
      },
      {
        id: 11,
        title: "您是否劳心耗神过度？",
        description: "",
        category: "精神消耗",
        type: "单选",
        options: [
          { value: '是', text: '是' },
          { value: '否', text: '否' }
        ]
      },
      {
        id: 12,
        title: "您近期有无如下问题？",
        description: "",
        category: "肾虚症状",
        type: "单选",
        options: [
          { value: '腰酸无力', text: '腰酸无力' },
          { value: '无此症状', text: '无此症状' }
        ]
      },
      {
        id: 13,
        title: "您是否用脑过度？",
        description: "",
        category: "用脑过度",
        type: "单选",
        options: [
          { value: '是', text: '是' },
          { value: '否', text: '否' }
        ]
      },
      {
        id: 14,
        title: "您近期有无如下问题？",
        description: "可以多选和不选",
        category: "认知功能",
        type: "多选",
        options: [
          { value: '好忘事', text: '好忘事，记忆力下降' },
          { value: '白天嗜睡', text: '白天嗜睡' },
          { value: '偏头痛', text: '偏头痛/头痛' }
        ]
      },
      {
        id: 15,
        title: "您有怎样的睡眠困扰？",
        description: "可以多选和不选",
        category: "睡眠困扰",
        type: "多选",
        options: [
          { value: '反复清醒', text: '反复清醒' },
          { value: '整夜做梦', text: '整夜做梦' },
          { value: '晨起疲倦', text: '晨起疲倦' },
          { value: '难以入眠', text: '难以入眠' }
        ]
      },
      {
        id: 16,
        title: "您是否服用过以下类药物？",
        description: "可以多选和不选",
        category: "用药史",
        type: "多选",
        options: [
          { value: '苯二氮卓类', text: '苯二氮卓类：地西泮、劳拉西泮' },
          { value: '非苯二氮卓类', text: '非苯二氮卓类：唑吡坦、右佐匹克隆' },
          { value: '褪黑素受体激动剂', text: '褪黑素受体激动剂：雷美替胺' },
          { value: '食欲素受体拮抗剂', text: '食欲素受体拮抗剂：苏沃雷生' },
          { value: '抗抑郁药物', text: '抗抑郁药物：曲唑酮、米氮平' },
          { value: '未服用过', text: '未服用过以上药物' }
        ]
      },
      {
        id: 17,
        title: "您服用安眠药时长多久？",
        description: "",
        category: "用药时长",
        type: "单选",
        options: [
          { value: '未服用', text: '未服用安眠药' },
          { value: '1个月以内', text: '1个月以内' },
          { value: '1-3个月', text: '1-3个月（慢性）' },
          { value: '3个月以上', text: '3个月以上（高级）' }
        ]
      },
      {
        id: 18,
        title: "过去一个月内，您是否会在白天出现不可抗拒的睡眠欲望？",
        description: "如工作、学习或开车时突然想睡觉",
        category: "白天嗜睡",
        type: "单选",
        options: [
          { value: '几乎没有', text: '几乎没有' },
          { value: '每周1-2次', text: '每周1-2次' },
          { value: '每周3-5次', text: '每周3-5次' },
          { value: '每天都有', text: '每天都有' }
        ]
      },
      {
        id: 19,
        title: "过去一个月内，您夜间醒来后，再次入睡通常需要多长时间？",
        description: "",
        category: "再入睡时间",
        type: "单选",
        options: [
          { value: '5分钟以内', text: '5分钟以内' },
          { value: '6-15分钟', text: '6-15分钟' },
          { value: '16-30分钟', text: '16-30分钟' },
          { value: '31-60分钟', text: '31-60分钟' },
          { value: '60分钟以上', text: '60分钟以上' }
        ]
      }
    ]
    
    totalQuestions.value = questions.value.length
    
    // 初始化答案数组
    answers.value = questions.value.map(q => ({
      question_id: q.id,
      selected_options: []
    }))
  }
}

const loadStomachQuestions = async () => {
  try {
    // 调用API获取胃病问卷
    const response = await fetch('/api/diagnosis/stomach/questionnaire')
    const data = await response.json()
    
    if (data.questions && data.questions.length > 0) {
      // 转换API返回的问题格式
      questions.value = data.questions.map(q => ({
        id: q.id,
        title: q.text,
        description: q.type === '多选' ? '可以多选和不选' : '',
        category: q.category,
        type: q.type,
        options: q.options.map(opt => ({
          value: opt.value,
          text: opt.label
        }))
      }))
      
      totalQuestions.value = questions.value.length
      
      // 初始化答案数组
      answers.value = questions.value.map(q => ({
        question_id: q.id,
        selected_options: []
      }))
    } else {
      ElMessage.info(data.message || '胃病问卷系统暂未开放')
      totalQuestions.value = 0
      questions.value = []
    }
    
  } catch (error) {
    console.error('加载胃病问卷失败:', error)
    ElMessage.warning('胃病诊断功能开发中，敬请期待')
    totalQuestions.value = 0
    questions.value = []
  }
}

const loadAgingQuestions = async () => {
  try {
    // 调用API获取早衰问卷
    const response = await fetch('/api/diagnosis/aging/questionnaire')
    const data = await response.json()
    
    if (data.questions && data.questions.length > 0) {
      // 转换API返回的问题格式
      questions.value = data.questions.map(q => ({
        id: q.id,
        title: q.text,
        description: q.type === '多选' ? '可以多选和不选' : '',
        category: q.category,
        type: q.type,
        options: q.options.map(opt => ({
          value: opt.value,
          text: opt.label
        }))
      }))
      
      totalQuestions.value = questions.value.length
      
      // 初始化答案数组
      answers.value = questions.value.map(q => ({
        question_id: q.id,
        selected_options: []
      }))
    } else {
      ElMessage.info(data.message || '早衰问卷系统暂未开放')
      totalQuestions.value = 0
      questions.value = []
    }
    
  } catch (error) {
    console.error('加载早衰问卷失败:', error)
    ElMessage.warning('早衰诊断功能开发中，敬请期待')
    totalQuestions.value = 0
    questions.value = []
  }
}

const startAssessment = async () => {
  if (!selectedDisease.value) {
    ElMessage.warning('请先选择诊断类型')
    return
  }
  
  // 根据疾病类型加载相应的问卷
  if (selectedDisease.value === 'insomnia') {
    await loadInsomniaQuestions()
  } else if (selectedDisease.value === 'stomach') {
    await loadStomachQuestions()
  } else if (selectedDisease.value === 'aging') {
    await loadAgingQuestions()
  }
  
  isStarted.value = true
  currentQuestion.value = 0
  currentAnswer.value = ''
}

const handleAnswerChange = (value: string) => {
  // 保存当前答案到答案数组
  if (answers.value[currentQuestion.value]) {
    answers.value[currentQuestion.value].selected_options = [value]
  }
}

const handleMultiAnswerChange = (values: string[]) => {
  // 保存多选答案到答案数组
  if (answers.value[currentQuestion.value]) {
    answers.value[currentQuestion.value].selected_options = values
  }
}

const nextQuestion = async () => {
  // 检查是否有答案
  if (!hasAnswer.value) return
  
  // 特殊流程检查 - 失眠诊断
  if (selectedDisease.value === 'insomnia') {
    const currentQ = questions.value[currentQuestion.value]
    const currentAnswers = answers.value[currentQuestion.value]
    
    // 第1题特殊处理：选择"好"（value="A"）直接完成测评
    if (currentQ.id === 1 && (currentAnswers.selected_options[0] === 'A' || currentAnswers.selected_options[0] === '好')) {
      // 显示祝福信息并直接完成
      diagnosisResult.value = {
        message: "恭喜您！您的睡眠质量很好，请继续保持良好的作息习惯。祝您身体健康！",
        syndrome_type: "无需治疗",
        confidence: 1.0,
        analysis: "您的睡眠状况良好，无需特殊治疗。",
        treatment_plan: {
          herbal_medicine: "无需用药，保持现有良好习惯即可",
          external_treatment: "无需外治，维持规律作息",
          diet_therapy: "保持均衡饮食，避免睡前过饱或饥饿",
          lifestyle: "继续保持良好的睡眠习惯和作息规律"
        },
        is_special_exit: true,
        special_type: "good_sleep"
      }
      isCompleted.value = true
      ElMessage.success('测评完成！您的睡眠质量很好！')
      return
    }
    
    // 第9题特殊处理：选择"3个月以上"（value="C"）推荐专业咨询
    if (currentQ.id === 9 && (currentAnswers.selected_options[0] === 'C' || currentAnswers.selected_options[0] === '3个月以上' || currentAnswers.selected_options[0] === '长期使用')) {
      // 显示专业咨询建议
      diagnosisResult.value = {
        message: "您长期使用安眠药物，建议寻求高级咨询师的专业指导，制定个性化的减药和治疗方案。",
        syndrome_type: "长期用药失眠",
        confidence: 1.0,
        analysis: "长期使用安眠药物需要专业医师指导逐步调整。",
        treatment_plan: {
          herbal_medicine: "需要专业中医师评估后制定个性化中药方案",
          external_treatment: "建议配合专业针灸理疗逐步减药",
          diet_therapy: "配合食疗调养，辅助改善睡眠质量",
          lifestyle: "在专业指导下调整作息，配合心理疏导"
        },
        is_special_exit: true,
        special_type: "long_term_medication",
        recommendation: {
          type: "professional_consultation",
          message: "建议预约高级咨询师制定减药方案"
        }
      }
      isCompleted.value = true
      ElMessage.warning('建议寻求专业咨询师指导')
      return
    }
  }
  
  if (currentQuestion.value === totalQuestions.value - 1) {
    // 最后一题，提交测评
    await submitAssessment()
  } else {
    // 寻找下一个应该显示的题目
    let nextQuestionIndex = currentQuestion.value + 1
    
    // 跳过不应该显示的题目
    while (nextQuestionIndex < totalQuestions.value) {
      const nextQuestion = questions.value[nextQuestionIndex]
      if (nextQuestion && shouldShowQuestion(nextQuestion.id)) {
        break
      }
      nextQuestionIndex++
    }
    
    // 移动到下一题（可能跳过了某题）
    if (nextQuestionIndex < totalQuestions.value) {
      currentQuestion.value = nextQuestionIndex
      loadCurrentAnswers()
    } else {
      // 已经是最后一题，提交测评
      await submitAssessment()
    }
  }
}

const previousQuestion = () => {
  if (currentQuestion.value > 0) {
    // 寻找上一个应该显示的题目
    let prevQuestionIndex = currentQuestion.value - 1
    
    // 跳过不应该显示的题目
    while (prevQuestionIndex >= 0) {
      const prevQuestion = questions.value[prevQuestionIndex]
      if (prevQuestion && shouldShowQuestion(prevQuestion.id)) {
        break
      }
      prevQuestionIndex--
    }
    
    // 移动到上一题
    if (prevQuestionIndex >= 0) {
      currentQuestion.value = prevQuestionIndex
      loadCurrentAnswers()
    }
  }
}

const loadCurrentAnswers = () => {
  // 清空当前答案
  currentAnswer.value = ''
  currentAnswerArray.value = []
  
  // 只有在答案数组存在且有对应题目时才加载
  if (answers.value[currentQuestion.value] && questions.value[currentQuestion.value]) {
    const currentAnswers = answers.value[currentQuestion.value]
    const currentQ = questions.value[currentQuestion.value]
    
    if (currentAnswers.selected_options && currentAnswers.selected_options.length > 0) {
      if (currentQ.type === '单选' || currentQ.type === '是非') {
        currentAnswer.value = currentAnswers.selected_options[0]
      } else if (currentQ.type === '多选') {
        currentAnswerArray.value = [...currentAnswers.selected_options]
      }
    }
  }
}

const submitAssessment = async () => {
  isSubmitting.value = true
  
  try {
    let response
    if (selectedDisease.value === 'insomnia') {
      // 构建要发送的答案数据，过滤掉跳过的题目
      const validAnswers = answers.value.filter(answer => 
        answer.selected_options && answer.selected_options.length > 0
      )
      
      const requestData = {
        answers: validAnswers
      }
      
      response = await fetch('/api/diagnosis/insomnia/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(requestData)
      })
      
      if (response.ok) {
        const data = await response.json()
        if (data.success && data.data) {
          const diagnosisData = data.data.diagnosis_result
          
          // 检查后端返回的特殊流程标记
          if (diagnosisData.special_flow) {
            if (diagnosisData.special_flow === 'good_sleep') {
              // 第1题"好"的特殊处理
              diagnosisResult.value = {
                message: "恭喜您！您的睡眠质量很好，请继续保持良好的作息习惯。祝您身体健康！",
                syndrome_type: "无需治疗",
                confidence: 1.0,
                analysis: "您的睡眠状况良好，无需特殊治疗。",
                treatment_plan: {
                  herbal_medicine: "无需用药，保持现有良好习惯即可",
                  external_treatment: "无需外治，维持规律作息",
                  diet_therapy: "保持均衡饮食，避免睡前过饱或饥饿",
                  lifestyle: "继续保持良好的睡眠习惯和作息规律"
                },
                is_special_exit: true,
                special_type: "good_sleep"
              }
              ElMessage.success('测评完成！您的睡眠质量很好！')
            } else if (diagnosisData.special_flow === 'long_term_medication') {
              // 第9题"3个月以上"的特殊处理
              diagnosisResult.value = {
                message: "您长期使用安眠药物，建议寻求高级咨询师的专业指导，制定个性化的减药和治疗方案。",
                syndrome_type: "长期用药失眠",
                confidence: 1.0,
                analysis: "长期使用安眠药物需要专业医师指导逐步调整。",
                treatment_plan: {
                  herbal_medicine: "需要专业中医师评估后制定个性化中药方案",
                  external_treatment: "建议配合专业针灸理疗逐步减药",
                  diet_therapy: "配合食疗调养，辅助改善睡眠质量",
                  lifestyle: "在专业指导下调整作息，配合心理疏导"
                },
                is_special_exit: true,
                special_type: "long_term_medication",
                recommendation: {
                  type: "professional_consultation",
                  message: "建议预约高级咨询师制定减药方案"
                }
              }
              ElMessage.warning('建议寻求专业咨询师指导')
            }
          } else {
            // 正常诊断结果处理
            diagnosisResult.value = {
              message: "诊断完成",
              syndrome_type: diagnosisData.syndrome_type || diagnosisData.final_syndrome,
              confidence: diagnosisData.confidence_score || diagnosisData.confidence,
              analysis: diagnosisData.description || diagnosisData.analysis,
              treatment_plan: {
                herbal_medicine: diagnosisData.treatment_plan?.herbal_medicine || "请咨询专业中医师获得具体用药建议",
                external_treatment: diagnosisData.treatment_plan?.external_treatment || "请咨询专业中医师获得外治法指导",
                diet_therapy: diagnosisData.treatment_plan?.diet_therapy || "请咨询专业中医师获得食疗建议",
                lifestyle: diagnosisData.treatment_plan?.lifestyle || "请咨询专业中医师获得生活调养建议"
              },
              diagnosis_result: diagnosisData,
              timestamp: data.data.timestamp,
              base_score: diagnosisData.base_score,
              insomnia_level: diagnosisData.insomnia_level,
              detailed_scores: diagnosisData.detailed_scores
            }
            ElMessage.success('测评完成！基于专业诊断引擎')
          }
          
          // 显示结果页面
          await new Promise(resolve => setTimeout(resolve, 500))
          isCompleted.value = true
          
        } else {
          ElMessage.error('诊断数据格式错误：' + (data.error || '未知错误'))
          console.error('API返回错误:', data)
        }
      } else {
        const errorText = await response.text()
        console.error('HTTP错误:', response.status, errorText)
        ElMessage.error(`诊断服务异常 (${response.status})，请稍后重试`)
      }
    } else {
      ElMessage.warning('该疾病类型的诊断功能尚未开放')
    }
    
  } catch (error) {
    console.error('诊断API调用失败:', error)
    ElMessage.error('网络连接失败，请检查网络后重试')
  } finally {
    isSubmitting.value = false
  }
}

const downloadReport = () => {
  // 下载报告功能
  console.log('下载测评报告')
}

const getSyndromeDetails = () => {
  if (!diagnosisResult.value || !diagnosisResult.value.syndrome_patterns) {
    return null
  }
  
  const finalSyndrome = diagnosisResult.value.diagnosis.final_syndrome
  // 根据最终证型查找对应的证型详情
  const syndromeMap = {
    '证型1': '骨髓空虚',
    '证型2': '脑髓空虚', 
    '证型3': '肝血不足',
    '证型4': '肝阴不足',
    '证型5': '肾阴虚',
    '证型6': '肾阳虚'
  }
  
  const syndromeName = syndromeMap[finalSyndrome] || '骨髓空虚'
  return diagnosisResult.value.syndrome_patterns[syndromeName] || null
}

const restartAssessment = () => {
  isStarted.value = false
  isCompleted.value = false
  currentQuestion.value = 0
  currentAnswer.value = ''
  answers.value = []
  selectedDisease.value = ''
  diagnosisResult.value = null
  questions.value = []
}

onMounted(async () => {
  // 从后端加载可用的诊断类型
  try {
    const response = await fetch('/api/diagnosis/diseases')
    const data = await response.json()
    diseases.value = data.diseases
  } catch (error) {
    console.error('加载诊断类型失败:', error)
    // 使用默认的疾病列表
    diseases.value = [
      { code: 'insomnia', name: '失眠', status: 'active' },
      { code: 'stomach', name: '胃病', status: 'active' },
      { code: 'aging', name: '早衰', status: 'active' }
    ]
  }
})
</script>

<style scoped>
.assessment {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.assessment-content {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  margin: 20px 0;
}

/* 标题区域 */
.assessment-header {
  text-align: center;
  padding: 60px 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.assessment-header::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 70%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
}

.assessment-title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  position: relative;
  z-index: 1;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.assessment-subtitle {
  font-size: 1.6rem;
  font-weight: 400;
  opacity: 0.95;
  margin-bottom: 2rem;
  position: relative;
  z-index: 1;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

.assessment-intro {
  position: relative;
  z-index: 1;
  max-width: 600px;
  margin: 0 auto;
}

.assessment-intro p {
  font-size: 1.1rem;
  line-height: 1.6;
  opacity: 0.9;
}

/* 进度条 */
.progress-section {
  padding: 30px 40px;
  background: #f8f9fa;
  border-bottom: 1px solid #e9ecef;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-weight: 600;
  color: #495057;
}

/* 开始界面 */
.start-section {
  padding: 50px 40px;
  text-align: center;
}

.assessment-features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 30px;
  margin-bottom: 40px;
}

.feature-item {
  padding: 30px 20px;
  border-radius: 15px;
  background: #f8f9fa;
  transition: transform 0.3s ease;
}

.feature-item:hover {
  transform: translateY(-5px);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 20px;
}

.feature-item h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2d3436;
  margin-bottom: 10px;
}

.feature-item p {
  color: #636e72;
  line-height: 1.6;
}

.start-info {
  display: flex;
  justify-content: center;
  gap: 40px;
  margin-bottom: 40px;
  flex-wrap: wrap;
}

.time-estimate,
.question-count {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #6c757d;
  font-weight: 500;
}

.start-button {
  padding: 15px 40px;
  font-size: 1.2rem;
  font-weight: 600;
  border-radius: 30px;
}

/* 问题界面 */
.question-section {
  padding: 20px 40px;
}

.question-card {
  max-width: 800px;
  margin: 0 auto;
}

.question-header {
  margin-bottom: 20px;
}

.question-number {
  font-size: 1.2rem;
  font-weight: 700;
  color: #667eea;
  margin-bottom: 10px;
}

.question-title {
  font-size: 1.8rem;
  font-weight: 600;
  color: #2d3436;
  margin-bottom: 10px;
}

.question-description {
  color: #636e72;
  font-size: 1rem;
  margin: 0;
}

.question-description.multi-select {
  color: #e74c3c;
  font-weight: 500;
}

.question-options {
  margin-bottom: 25px;
}

.option-group {
  width: 100%;
  /* Grid布局由Vue动态设置 */
}

.option-item {
  width: 100%;
  margin-bottom: 0;
  padding: 10px 15px;
  border: none;
  background: transparent;
  transition: all 0.3s ease;
  cursor: pointer;
  display: flex !important;
  align-items: flex-start !important;
  justify-self: stretch;
  min-height: auto;
  box-sizing: border-box;
}

.option-item:hover {
  background-color: #f8f9ff;
  border-radius: 8px;
}

.option-item.is-checked {
  background-color: #e6f3ff;
  border-radius: 8px;
}

.option-content {
  margin-left: 10px;
  width: 100%;
  flex: 1;
}

/* 强制所有选项对齐 */
.option-group .el-radio,
.option-group .el-checkbox {
  width: 100% !important;
  margin-right: 0 !important;
  display: flex !important;
  align-items: flex-start !important;
}

.option-group .el-radio__input,
.option-group .el-checkbox__input {
  margin-top: 2px !important;
}

.option-group .el-radio__label,
.option-group .el-checkbox__label {
  width: 100% !important;
  flex: 1 !important;
  padding-left: 10px !important;
  line-height: 1.3 !important;
}

.option-text {
  font-weight: 500;
  color: #2d3436;
  margin-bottom: 2px;
  font-size: 1rem;
  line-height: 1.3;
  width: 100%;
}

.option-description {
  font-size: 0.9rem;
  color: #636e72;
}

/* 是非题专门样式 */
.yes-no-group {
  display: grid !important;
  grid-template-columns: repeat(2, 1fr) !important;
  gap: 20px !important;
  justify-items: center !important;
  max-width: 400px !important;
  margin: 0 auto !important;
}

.yes-no-item {
  min-width: 120px;
  text-align: center;
  justify-self: center;
}

.yes-no-item .option-content {
  margin-left: 0;
  text-align: center;
}

.question-actions {
  display: flex;
  justify-content: flex-start;
  gap: 15px;
}

.question-actions .el-button {
  flex: 0 0 auto;
  min-width: 100px;
  max-width: 120px;
}

/* 多选题规则说明 */
.multi-select-note {
  margin-bottom: 15px;
  text-align: right;
}

.rule-text {
  color: #e74c3c;
  font-size: 0.9rem;
  font-weight: 500;
}

/* 结果界面 */
.result-section {
  padding: 50px 40px;
  text-align: center;
}

.result-header {
  margin-bottom: 40px;
}

.success-icon {
  font-size: 4rem;
  color: #67c23a;
  margin-bottom: 20px;
}

.result-header h2 {
  font-size: 2.5rem;
  font-weight: 700;
  color: #2d3436;
  margin-bottom: 15px;
}

.result-header p {
  font-size: 1.1rem;
  color: #636e72;
}

.result-placeholder {
  margin-bottom: 40px;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.result-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

/* 病症选择样式 */
.disease-selection {
  padding: 50px 40px;
  text-align: center;
}

.selection-header {
  margin-bottom: 40px;
}

.selection-header h2 {
  font-size: 2.2rem;
  font-weight: 700;
  color: #2d3436;
  margin-bottom: 15px;
}

.selection-header p {
  font-size: 1.1rem;
  color: #636e72;
  max-width: 600px;
  margin: 0 auto;
}

.disease-cards {
  display: flex;
  justify-content: center;
  align-items: stretch;
  gap: 30px;
  margin-top: 30px;
  max-width: 1000px;
  margin-left: auto;
  margin-right: auto;
  flex-wrap: wrap;
}

.disease-card {
  border: 2px solid #e9ecef;
  border-radius: 15px;
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white;
  position: relative;
  overflow: hidden;
  min-height: 250px;
  width: 200px;
  flex: 0 0 auto;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.disease-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.disease-card:hover::before {
  opacity: 1;
}

.disease-card:hover:not(.disabled) {
  border-color: #667eea;
  transform: translateY(-5px);
  box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
}

.disease-card.disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.card-icon {
  font-size: 3rem;
  color: #667eea;
  margin-bottom: 15px;
  position: relative;
  z-index: 1;
}

.disease-card h3 {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2d3436;
  margin-bottom: 12px;
  position: relative;
  z-index: 1;
}

.coming-soon {
  color: #f39c12;
  font-weight: 500;
}

.available {
  color: #27ae60;
  font-weight: 500;
}

.disease-features {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 8px;
  position: relative;
  z-index: 1;
}

.disease-features span {
  background: #e3f2fd;
  color: #1976d2;
  padding: 4px 8px;
  border-radius: 15px;
  font-size: 0.8rem;
  font-weight: 500;
}

.disease-description {
  color: #636e72;
  font-size: 0.9rem;
  line-height: 1.4;
  margin-top: 10px;
  position: relative;
  z-index: 1;
}

.back-button-container {
  margin-bottom: 30px;
  text-align: left;
}

.selected-disease-info {
  text-align: center;
  margin-bottom: 40px;
}

.selected-disease-info h2 {
  font-size: 2rem;
  font-weight: 700;
  color: #2d3436;
  margin-bottom: 15px;
}

.selected-disease-info p {
  font-size: 1rem;
  color: #636e72;
  max-width: 800px;
  margin: 0 auto;
  line-height: 1.6;
}

/* 诊断结果样式 */
.diagnosis-result {
  max-width: 900px;
  margin: 0 auto;
}

.diagnosis-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.diagnosis-card h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3436;
  margin-bottom: 25px;
  text-align: center;
}

.diagnosis-summary {
  display: flex;
  flex-direction: column;
  gap: 15px;
  margin-bottom: 25px;
}

.syndrome-result, .confidence-result {
  display: flex;
  align-items: center;
  font-size: 1.1rem;
}

.label {
  font-weight: 500;
  color: #2d3436;
  margin-right: 8px;
}

.syndrome-name {
  font-size: 1.3rem;
  font-weight: 700;
  color: #667eea;
}

.confidence-value {
  font-size: 1.2rem;
  font-weight: 600;
  color: #27ae60;
}

.score-badge, .level-badge {
  display: inline-block;
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  margin-left: 10px;
  box-shadow: 0 2px 8px rgba(102, 126, 234, 0.3);
  animation: pulse-badge 2s infinite;
}

.score-badge {
  background: linear-gradient(45deg, #e74c3c, #c0392b);
  box-shadow: 0 2px 8px rgba(231, 76, 60, 0.3);
}

.level-badge {
  background: linear-gradient(45deg, #f39c12, #e67e22);
  box-shadow: 0 2px 8px rgba(243, 156, 18, 0.3);
}

@keyframes pulse-badge {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

.analysis-section {
  border-top: 1px solid #e9ecef;
  padding-top: 20px;
}

.analysis-section h4 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2d3436;
  margin-bottom: 15px;
}

.analysis-section p {
  line-height: 1.6;
  color: #636e72;
}

.syndrome-card {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.syndrome-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.syndrome-header h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3436;
  margin: 0;
}

.confidence-badge {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 8px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.syndrome-card .syndrome-name {
  font-size: 2rem;
  font-weight: 700;
  color: #667eea;
  text-align: center;
  margin-bottom: 30px;
  padding: 20px;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border-radius: 10px;
}

.all-scores {
  margin-top: 30px;
}

.all-scores h4 {
  font-size: 1.2rem;
  font-weight: 600;
  color: #2d3436;
  margin-bottom: 20px;
}

.score-list {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.score-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.score-item.primary {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  border: 2px solid #667eea;
}

.score-item .syndrome-name {
  font-weight: 500;
  color: #2d3436;
}

.score-bar {
  display: flex;
  align-items: center;
  gap: 15px;
  flex: 1;
  max-width: 200px;
  margin-left: 20px;
}

.bar-fill {
  height: 8px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
  transition: width 0.8s ease;
  position: relative;
  flex: 1;
}

.score-value {
  font-weight: 600;
  color: #667eea;
  min-width: 40px;
  text-align: right;
}

.treatment-plan {
  background: white;
  border: 1px solid #e9ecef;
  border-radius: 15px;
  padding: 30px;
  margin-bottom: 30px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.treatment-plan h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #2d3436;
  margin-bottom: 25px;
  text-align: center;
}

.treatment-sections {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.treatment-item {
  background: #f8f9fa;
  border-radius: 12px;
  padding: 20px;
  transition: transform 0.3s ease;
}

.treatment-item:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.treatment-header {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.treatment-icon {
  font-size: 1.5rem;
  margin-right: 12px;
}

.treatment-item h4 {
  font-size: 1.1rem;
  font-weight: 600;
  color: #2d3436;
  margin: 0;
}

.treatment-content {
  color: #636e72;
  line-height: 1.6;
  font-size: 0.95rem;
  padding-left: 35px;
}

.disclaimer {
  margin-bottom: 30px;
}

.disclaimer-content {
  display: flex;
  align-items: flex-start;
  padding: 15px;
  background: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 8px;
}

.disclaimer-icon {
  font-size: 1.2rem;
  margin-right: 10px;
  margin-top: 2px;
}

.disclaimer-content p {
  margin: 0;
  color: #856404;
  font-size: 0.9rem;
  line-height: 1.5;
}

/* 证型得分分析 */
.scores-section {
  margin-top: 30px;
  padding: 25px;
  background: #f8f9fa;
  border-radius: 12px;
}

.scores-section h4 {
  margin-bottom: 20px;
  color: #495057;
  font-weight: 600;
}

.scores-grid {
  display: grid;
  gap: 15px;
}

.scores-grid .score-item {
  display: grid;
  grid-template-columns: 120px 1fr 80px;
  align-items: center;
  gap: 15px;
  padding: 10px 0;
}

.scores-grid .score-label {
  font-weight: 500;
  color: #495057;
  font-size: 0.9rem;
}

.scores-grid .score-bar {
  height: 8px;
  background: #e9ecef;
  border-radius: 4px;
  overflow: hidden;
}

.scores-grid .score-progress {
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 4px;
  transition: width 0.3s ease;
}

.scores-grid .score-value {
  text-align: right;
  font-weight: 600;
  color: #667eea;
  font-size: 0.9rem;
}

/* 证型详情 */
.syndrome-details {
  margin-top: 25px;
  padding: 20px;
  background: #fff;
  border: 1px solid #dee2e6;
  border-radius: 12px;
}

.syndrome-details h4 {
  margin-bottom: 15px;
  color: #495057;
  font-weight: 600;
}

.syndrome-info p {
  margin: 8px 0;
  line-height: 1.6;
  color: #6c757d;
}

/* 治疗方案样式更新 */
.formula-item, .external-item, .diet-item {
  margin-bottom: 20px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border-left: 4px solid #667eea;
}

.formula-item h5, .external-item h5, .diet-item h5 {
  margin-bottom: 10px;
  color: #495057;
  font-weight: 600;
}

.formula-ingredients, .formula-indications {
  margin: 8px 0;
  line-height: 1.5;
}

.diet-item .warning {
  color: #dc3545;
  font-weight: 500;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .assessment-header {
    padding: 40px 20px;
  }
  
  .assessment-title {
    font-size: 2.5rem;
  }
  
  .assessment-subtitle {
    font-size: 1.3rem;
  }
  
  .start-section,
  .question-section,
  .result-section {
    padding: 30px 20px;
  }
  
  .assessment-features {
    grid-template-columns: 1fr;
    gap: 20px;
  }
  
  .start-info {
    flex-direction: column;
    gap: 15px;
  }
  
  .question-actions {
    flex-direction: column;
  }
  
  .question-actions .el-button {
    max-width: none;
  }
  
  .disease-selection {
    padding: 30px 20px;
  }
  
  .disease-cards {
    flex-direction: column;
    align-items: center;
    gap: 15px;
    margin-top: 20px;
  }
  
  .disease-card {
    width: 100%;
    max-width: 300px;
    padding: 25px 20px;
  }
  
  .treatment-sections {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .syndrome-header {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }
  
  .score-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 10px;
  }
  
  .score-bar {
    width: 100%;
    margin-left: 0;
  }
  
  .option-group {
    grid-template-columns: 1fr !important;
    gap: 10px !important;
  }
  
  .option-item {
    width: 100%;
    min-width: auto;
  }
}
</style>