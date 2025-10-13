<template>
  <div class="assessment-view">
    <div class="assessment-header">
      <h1>健康认知测评</h1>
      <p class="intro">一共 8 道题（单选题）。<br/>按自己的真实想法选，答完有答案和解析。</p>
    </div>

    <div class="assessment-content">
      <!-- 问题列表 -->
      <div v-if="!showResults" class="questions-container">
        <div v-for="(question, index) in questions" :key="index" class="question-card">
          <div class="question-number">第 {{ index + 1 }} 题</div>
          <h3 class="question-title">{{ question.title }}</h3>
          <div class="options">
            <div
              v-for="(option, optionIndex) in question.options"
              :key="optionIndex"
              class="option-item"
              :class="{ 'selected': answers[index] === optionIndex }"
              @click="selectAnswer(index, optionIndex)"
            >
              <span class="option-label">{{ String.fromCharCode(65 + optionIndex) }}.</span>
              <span class="option-text">{{ option }}</span>
            </div>
          </div>
        </div>

        <div class="submit-section">
          <el-button type="primary" size="large" @click="submitAssessment" :disabled="!isAllAnswered">
            查看结果
          </el-button>
          <p v-if="!isAllAnswered" class="tip">请完成所有题目后提交</p>
        </div>
      </div>

      <!-- 结果展示 -->
      <div v-else class="results-container">
        <div class="score-card">
          <div class="score-number">{{ score }}</div>
          <div class="score-label">分</div>
          <div class="score-level">{{ scoreLevel }}</div>
          <div class="score-desc">{{ scoreLevelDesc }}</div>
        </div>

        <div class="answers-review">
          <h2>答案与解析</h2>
          <div v-for="(question, index) in questions" :key="index" class="answer-card">
            <div class="answer-header">
              <span class="question-num">第 {{ index + 1 }} 题</span>
              <span class="answer-status" :class="{ 'correct': answers[index] === question.correctAnswer, 'wrong': answers[index] !== question.correctAnswer }">
                {{ answers[index] === question.correctAnswer ? '✓ 正确' : '✗ 错误' }}
              </span>
            </div>
            <h4>{{ question.title }}</h4>
            <p class="your-answer">你的答案：{{ String.fromCharCode(65 + answers[index]) }}. {{ question.options[answers[index]] }}</p>
            <p class="correct-answer">正确答案：{{ String.fromCharCode(65 + question.correctAnswer) }}</p>
            <div class="explanation">
              <strong>解析：</strong>{{ question.explanation }}
            </div>
          </div>
        </div>

        <div class="action-buttons">
          <el-button type="primary" @click="resetAssessment">重新测评</el-button>
          <el-button @click="$router.push('/')">返回首页</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'

const questions = ref([
  {
    title: '到底什么是 "健康"？哪个说法最对？',
    options: [
      '身体没病，体检单上各项指标都正常',
      '身体没病、心情好，能正常上班、过日子',
      '身体好、心情好，还能跟人好好相处，这三方面都没问题',
      '精力足，能干活、运动，不用吃药'
    ],
    correctAnswer: 2,
    explanation: '世界卫生组织对健康的定义是：身体、心理和社会适应三方面都处于良好状态。A 只考虑身体；B 忽略了社会适应；D 精力好不代表心理和社会适应好，所以 A、B、D 错。'
  },
  {
    title: '怎么吃才健康？下列说法正确的是？',
    options: [
      '少吃油盐糖、多吃蔬菜，就是健康饮食',
      '谷薯类（米饭、红薯等）、蔬菜水果、肉蛋奶、大豆坚果都得吃，搭配着来',
      '想减肥，就少吃主食，甚至不吃主食',
      '天然食物肯定比加工食品好，加工食品一口都不能吃'
    ],
    correctAnswer: 1,
    explanation: '《中国居民膳食指南》建议食物多样化，谷薯类、蔬果、肉蛋奶、大豆坚果都得吃。A 只强调少吃某些东西，没说要吃什么；C 主食提供能量，不吃会营养不良；D 加工食品（比如酸奶、罐头）只要选对了也能吃，所以 A、C、D 错。'
  },
  {
    title: '运动和健康的关系，哪个想法是对的？',
    options: [
      '运动越累、时间越长，对身体越好，哪怕累到不想动',
      '每周至少 150 分钟中等强度运动（比如快走），或 75 分钟高强度运动（比如跑步）',
      '运动只能减肥，对健康没啥别的用',
      '年纪大了就别运动了，容易受伤'
    ],
    correctAnswer: 1,
    explanation: '世卫组织建议：成年人每周至少 150 分钟中等强度运动，或 75 分钟高强度运动。A 运动过度会伤身；C 运动还能降低慢性病风险、改善心情；D 老年人适度运动（比如散步、太极）能延缓衰老，所以 A、C、D 错。'
  },
  {
    title: '睡眠和健康的关系，哪个理解对？',
    options: [
      '只要睡够 8 小时，什么时候睡、怎么睡都行',
      '成年人每天睡 7-9 小时，最好晚上 11 点前入睡，睡眠质量比时长更重要',
      '周末补觉能弥补平时睡眠不足，对健康没影响',
      '失眠只能靠吃安眠药，其他方法没用'
    ],
    correctAnswer: 1,
    explanation: '成年人每天睡 7-9 小时，晚上 11 点前入睡符合生物钟。A 睡眠时间固定很重要；C 周末补觉不能完全弥补平时睡眠不足；D 失眠可以通过调整作息、放松训练改善，不一定吃药，所以 A、C、D 错。'
  },
  {
    title: '压力和健康的关系，哪个说法对？',
    options: [
      '压力都是坏的，应该完全避免',
      '适度压力能激励人进步，过度压力会损害健康，关键是学会管理压力',
      '压力只影响心情，不会影响身体健康',
      '压力大就得靠喝酒、抽烟缓解，没别的办法'
    ],
    correctAnswer: 1,
    explanation: '适度压力（比如工作挑战）能提升表现，过度压力会导致焦虑、失眠、免疫力下降。A 完全没压力会缺乏动力；C 压力会影响身体（比如血压升高）；D 喝酒、抽烟会加重健康问题，可以通过运动、做喜欢的事改善心情，所以 A、C、D 错。'
  },
  {
    title: '定期体检的作用，哪个理解对？',
    options: [
      '很多病早期没症状（比如早期癌症），定期体检才能早发现',
      '体检项目越多越好，能查出所有健康问题',
      '要根据年龄、性别、家里人有没有遗传病等，选适合自己的体检项目',
      '体检报告说 "没异常"，就说明身体完全健康，之后不用管了'
    ],
    correctAnswer: 0,
    explanation: 'A 很多病早期没症状（比如早期癌症），定期体检才能早发现；B 项目太多浪费钱，也不是所有项目都适合你；D 报告 "没异常" 不代表完全健康，还得靠平时好好吃饭、睡觉维护，所以 B、D 错。C 也对，但 A 更全面地说明了体检的核心作用。'
  },
  {
    title: '什么是 "亚健康"？哪个理解对？',
    options: [
      '亚健康是身体在提醒你 "要注意了"，不调整可能会生病',
      '亚健康只是自己感觉不舒服，没实际健康风险，不用在意',
      '亚健康只能靠吃药调理，改生活习惯没用',
      '只有上班的人才会亚健康，学生和老人不会有'
    ],
    correctAnswer: 0,
    explanation: '亚健康是介于健康和生病之间的状态，比如总觉得累、失眠。B 说没风险，错；C 改生活习惯（比如早睡、运动）能改善亚健康，不用吃药；D 学生（学业压力大）、老人（身体机能下降）也可能亚健康，所以 B、C、D 错。'
  },
  {
    title: '怎么养成健康习惯？哪个说法对？',
    options: [
      '健康习惯要一次全养成，比如同时戒烟、运动、节食',
      '偶尔打破健康习惯没关系，总体上保持就行，不用太严格',
      '健康习惯要长期坚持，可从小事开始，比如先每天散步 10 分钟，再慢慢加时间',
      '养成健康习惯全靠意志力，意志力强就能轻松做到'
    ],
    correctAnswer: 2,
    explanation: 'A 一次养成多个习惯太难，容易放弃；B 偶尔打破没问题，但常打破就不算习惯了；D 养成习惯不光靠意志力，还需要家人支持、用闹钟提醒等方法，所以 A、B、D 错。'
  }
])

const answers = ref<number[]>(Array(8).fill(-1))
const showResults = ref(false)

const isAllAnswered = computed(() => {
  return answers.value.every(answer => answer !== -1)
})

const score = computed(() => {
  let correctCount = 0
  questions.value.forEach((question, index) => {
    if (answers.value[index] === question.correctAnswer) {
      correctCount++
    }
  })
  return Math.round(correctCount * 12.5)
})

const scoreLevel = computed(() => {
  const s = score.value
  if (s >= 87.5) return '优秀'
  if (s >= 75) return '良好'
  if (s >= 62.5) return '及格'
  return '需加强'
})

const scoreLevelDesc = computed(() => {
  const s = score.value
  if (s >= 87.5) {
    return '你的健康认知非常好！对健康有全面、科学的理解，能避开常见错误想法，���能力自己制定健康计划，建议多关注新的健康知识，保持认知更新。'
  }
  if (s >= 75) {
    return '你的健康认知不错！大部分健康知识都掌握了，但还有些地方可以提升，建议针对答错的题目加强学习。'
  }
  if (s >= 62.5) {
    return '你的健康认知还可以！基本健康知识有了解，但对一些细节理解不够准确，建议系统学习健康知识。'
  }
  return '你的健康认知需要加强！很多基础健康知识理解有误，建议从头系统学习，避免因错误认知损害健康。'
})

const selectAnswer = (questionIndex: number, optionIndex: number) => {
  answers.value[questionIndex] = optionIndex
}

const submitAssessment = () => {
  showResults.value = true
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

const resetAssessment = () => {
  answers.value = Array(8).fill(-1)
  showResults.value = false
  window.scrollTo({ top: 0, behavior: 'smooth' })
}
</script>

<style scoped>
.assessment-view {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 40px 20px;
}

.assessment-header {
  max-width: 900px;
  margin: 0 auto 40px;
  text-align: center;
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.assessment-header h1 {
  font-size: 2.5rem;
  color: #2d3748;
  margin-bottom: 20px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.intro {
  font-size: 1.1rem;
  color: #4a5568;
  line-height: 1.8;
}

.assessment-content {
  max-width: 900px;
  margin: 0 auto;
}

.questions-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.question-card {
  background: white;
  padding: 30px;
  border-radius: 16px;
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
}

.question-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 30px rgba(0,0,0,0.12);
}

.question-number {
  display: inline-block;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  padding: 6px 16px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  margin-bottom: 15px;
}

.question-title {
  font-size: 1.3rem;
  color: #2d3748;
  margin-bottom: 20px;
  line-height: 1.6;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.option-item {
  display: flex;
  align-items: flex-start;
  padding: 16px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.option-item:hover {
  border-color: #667eea;
  background: #f7fafc;
}

.option-item.selected {
  border-color: #667eea;
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1));
}

.option-label {
  font-weight: 700;
  color: #667eea;
  margin-right: 12px;
  flex-shrink: 0;
}

.option-text {
  color: #4a5568;
  line-height: 1.6;
}

.submit-section {
  background: white;
  padding: 30px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}

.submit-section .el-button {
  min-width: 200px;
  height: 50px;
  font-size: 1.1rem;
}

.tip {
  margin-top: 15px;
  color: #718096;
  font-size: 0.95rem;
}

.results-container {
  display: flex;
  flex-direction: column;
  gap: 30px;
}

.score-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 50px;
  border-radius: 20px;
  text-align: center;
  box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
}

.score-number {
  font-size: 5rem;
  font-weight: 900;
  margin-bottom: 10px;
}

.score-label {
  font-size: 1.5rem;
  margin-bottom: 20px;
  opacity: 0.9;
}

.score-level {
  font-size: 2rem;
  font-weight: 700;
  margin-bottom: 15px;
}

.score-desc {
  font-size: 1.1rem;
  line-height: 1.8;
  opacity: 0.95;
  max-width: 700px;
  margin: 0 auto;
}

.answers-review {
  background: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}

.answers-review h2 {
  font-size: 2rem;
  color: #2d3748;
  margin-bottom: 30px;
  text-align: center;
}

.answer-card {
  padding: 25px;
  border: 2px solid #e2e8f0;
  border-radius: 12px;
  margin-bottom: 20px;
}

.answer-card:last-child {
  margin-bottom: 0;
}

.answer-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 15px;
}

.question-num {
  font-weight: 700;
  color: #667eea;
}

.answer-status {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.9rem;
  font-weight: 600;
}

.answer-status.correct {
  background: #d4edda;
  color: #155724;
}

.answer-status.wrong {
  background: #f8d7da;
  color: #721c24;
}

.answer-card h4 {
  color: #2d3748;
  margin-bottom: 12px;
  font-size: 1.1rem;
}

.your-answer, .correct-answer {
  color: #4a5568;
  margin: 8px 0;
}

.explanation {
  background: #f7fafc;
  padding: 15px;
  border-radius: 8px;
  margin-top: 12px;
  line-height: 1.7;
  color: #4a5568;
}

.explanation strong {
  color: #667eea;
}

.action-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  padding: 20px;
}

.action-buttons .el-button {
  min-width: 150px;
  height: 45px;
}

@media (max-width: 768px) {
  .assessment-header h1 {
    font-size: 1.8rem;
  }

  .intro {
    font-size: 1rem;
  }

  .question-card {
    padding: 20px;
  }

  .question-title {
    font-size: 1.1rem;
  }

  .score-number {
    font-size: 3.5rem;
  }

  .score-level {
    font-size: 1.5rem;
  }

  .answers-review {
    padding: 25px;
  }

  .action-buttons {
    flex-direction: column;
  }

  .action-buttons .el-button {
    width: 100%;
  }
}
</style>
