<template>
  <div class="insomnia-assessment">
    <PageContainer>
      <div class="assessment-content">
        <!-- 失眠测评标题区域 -->
        <div class="assessment-header">
          <h1 class="assessment-title">失眠测评</h1>
          <p class="assessment-subtitle">基于19题专业失眠评估系统，运用中医理论精准诊断</p>
        </div>

        <!-- 测评进度条 -->
        <div class="progress-section" v-if="!isCompleted && questions.length > 0">
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
        <div class="question-section" v-if="!isCompleted && questions.length > 0">
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
            <h2>失眠测评报告</h2>
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
            <el-button @click="goToHome">
              返回首页
            </el-button>
          </div>
        </div>
      </div>
    </PageContainer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import PageContainer from '@/components/PageContainer.vue'
import { Clock, Document, SuccessFilled } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 测评状态
const isStarted = ref(false)
const isCompleted = ref(false)
const isSubmitting = ref(false)

// 题目相关
const currentQuestion = ref(0)
const currentAnswer = ref('')
const currentAnswerArray = ref<string[]>([])
const answers = ref<any[]>([])
const totalQuestions = ref(19) // 失眠诊断19题
const diagnosisResult = ref(null)

// 测评数据
const questions = ref([])

// 计算属性
const progressPercentage = computed(() => {
  return Math.round((currentQuestion.value / totalQuestions.value) * 100)
})

const currentQuestionData = computed(() => {
  return questions.value[currentQuestion.value] || {}
})

const hasAnswer = computed(() => {
  const currentQ = questions.value[currentQuestion.value]
  if (!currentQ) return false
  
  if (currentQ.type === '单选') {
    return currentAnswer.value !== ''
  } else if (currentQ.type === '多选') {
    return true
  } else if (currentQ.type === '是非') {
    return currentAnswer.value !== ''
  }
  return false
})

// 方法
const goToHome = () => {
  router.push('/')
}

const loadInsomniaQuestions = async () => {
  // ... 这里复制原来AssessmentView中的loadInsomniaQuestions函数内容
  // 为了简化，先用一个简单的实现
  try {
    const response = await fetch('/api/diagnosis/insomnia/questionnaire')
    const data = await response.json()
    
    if (data.success && data.data) {
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
      
      totalQuestions.value = questions.value.length
      
      answers.value = questions.value.map(q => ({
        question_id: q.id,
        selected_options: []
      }))
    } else {
      throw new Error('API响应格式错误')
    }
  } catch (error) {
    console.error('加载问题失败:', error)
    ElMessage.error('加载失眠测评问题失败')
    router.push('/')
  }
}

const startAssessment = async () => {
  await loadInsomniaQuestions()
  isStarted.value = true
  currentQuestion.value = 0
  currentAnswer.value = ''
}

const handleAnswerChange = (value: string) => {
  if (answers.value[currentQuestion.value]) {
    answers.value[currentQuestion.value].selected_options = [value]
  }
}

const handleMultiAnswerChange = (values: string[]) => {
  if (answers.value[currentQuestion.value]) {
    answers.value[currentQuestion.value].selected_options = values
  }
}

const nextQuestion = async () => {
  if (!hasAnswer.value) return
  
  if (currentQuestion.value === totalQuestions.value - 1) {
    await submitAssessment()
  } else {
    currentQuestion.value++
    loadCurrentAnswers()
  }
}

const previousQuestion = () => {
  if (currentQuestion.value > 0) {
    currentQuestion.value--
    loadCurrentAnswers()
  }
}

const loadCurrentAnswers = () => {
  currentAnswer.value = ''
  currentAnswerArray.value = []
  
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
    const validAnswers = answers.value.filter(answer => 
      answer.selected_options && answer.selected_options.length > 0
    )
    
    const requestData = {
      answers: validAnswers
    }
    
    const response = await fetch('/api/diagnosis/insomnia/analyze', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestData)
    })
    
    if (response.ok) {
      const data = await response.json()
      if (data.success && data.data) {
        const diagnosisData = data.data.diagnosis_result
        
        diagnosisResult.value = {
          syndrome_type: diagnosisData.syndrome_type || diagnosisData.final_syndrome,
          confidence: diagnosisData.confidence_score || diagnosisData.confidence,
          analysis: diagnosisData.description || diagnosisData.analysis,
          treatment_plan: {
            herbal_medicine: diagnosisData.treatment_plan?.herbal_medicine || "请咨询专业中医师获得具体用药建议",
            external_treatment: diagnosisData.treatment_plan?.external_treatment || "请咨询专业中医师获得外治法指导",
            diet_therapy: diagnosisData.treatment_plan?.diet_therapy || "请咨询专业中医师获得食疗建议",
            lifestyle: diagnosisData.treatment_plan?.lifestyle || "请咨询专业中医师获得生活调养建议"
          }
        }
        
        isCompleted.value = true
        ElMessage.success('测评完成！')
      } else {
        ElMessage.error('诊断数据格式错误')
      }
    } else {
      ElMessage.error('诊断服务异常，请稍后重试')
    }
    
  } catch (error) {
    console.error('诊断API调用失败:', error)
    ElMessage.error('网络连接失败，请检查网络后重试')
  } finally {
    isSubmitting.value = false
  }
}

const downloadReport = () => {
  console.log('下载测评报告')
}

const restartAssessment = () => {
  isStarted.value = false
  isCompleted.value = false
  currentQuestion.value = 0
  currentAnswer.value = ''
  answers.value = []
  diagnosisResult.value = null
  questions.value = []
}

onMounted(async () => {
  // 自动加载失眠问卷并开始
  await loadInsomniaQuestions()
  isStarted.value = true
})
</script>

<style scoped>
/* 这里复制原来AssessmentView.vue中的相关样式，简化处理 */
.insomnia-assessment {
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

.assessment-header {
  text-align: center;
  padding: 60px 40px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  position: relative;
  overflow: hidden;
}

.assessment-title {
  font-size: 3.5rem;
  font-weight: 800;
  margin-bottom: 1rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.assessment-subtitle {
  font-size: 1.6rem;
  font-weight: 400;
  opacity: 0.95;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
}

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

.question-options {
  margin-bottom: 25px;
}

.option-group {
  width: 100%;
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

.option-text {
  font-weight: 500;
  color: #2d3436;
  margin-bottom: 2px;
  font-size: 1rem;
  line-height: 1.3;
  width: 100%;
}

.question-actions {
  display: flex;
  justify-content: flex-start;
  gap: 15px;
}

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

.result-actions {
  display: flex;
  justify-content: center;
  gap: 20px;
  flex-wrap: wrap;
}

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
  
  .result-actions {
    flex-direction: column;
    align-items: center;
  }
}
</style>