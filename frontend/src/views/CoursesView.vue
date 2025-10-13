<template>
  <div class="courses">

    <!-- 核心理念 -->
    <section class="core-philosophy">
      <div class="section-header">
        <span class="section-tag">Health Cognition</span>
        <h2>认知决定健康，让每个人成为健康管理专家</h2>
      </div>

      <!-- 左右布局：方法论卡片 + 4个步骤 -->
      <div class="methodology-layout">
        <!-- 左侧：方法论卡片（可点击跳转） -->
        <div class="insight-card clickable" @click="goToThreeLayerSystem">
          <div class="insight-icon">🔬</div>
          <p>用培训医生的专业体系，让普通人掌握健康管理技能</p>
          <div class="click-hint">点击了解详情 →</div>
        </div>

        <!-- 右侧：16字步骤 -->
        <div class="steps-compact">
          <div class="step-compact">医生思维</div>
          <div class="step-compact">案例驱动</div>
          <div class="step-compact">工具应用</div>
          <div class="step-compact">个性指导</div>
        </div>
      </div>
    </section>

    <!-- 课程展示区域 -->
    <section class="courses-section">
      <div class="container">
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
          <el-icon class="is-loading"><Loading /></el-icon>
          <p>加载课程中...</p>
        </div>

        <!-- 书签式系列卡片 -->
        <div v-else-if="allCourses.length > 0">
          <div class="series-bookmarks">
            <!-- 基础理论书签 -->
            <div
              class="bookmark-card"
              :class="{ active: activeSeriesIndex === 0, 'has-courses': courseSeries.theory.length > 0 }"
              @click="toggleSeries(0)"
            >
              <div class="bookmark-icon">📚</div>
              <div class="bookmark-content">
                <h3>基础理论</h3>
                <p>系统学习中医理论基础、中药方剂知识</p>
                <div class="bookmark-count">{{ courseSeries.theory.length }} 门课程</div>
              </div>
              <div class="bookmark-arrow" v-if="activeSeriesIndex === 0">▼</div>
            </div>

            <!-- 实操演示书签 -->
            <div
              class="bookmark-card"
              :class="{ active: activeSeriesIndex === 1, 'has-courses': courseSeries.practical.length > 0 }"
              @click="toggleSeries(1)"
            >
              <div class="bookmark-icon">🎯</div>
              <div class="bookmark-content">
                <h3>实操演示</h3>
                <p>临床实践、养生保健、针灸推拿实操技能</p>
                <div class="bookmark-count">{{ courseSeries.practical.length }} 门课程</div>
              </div>
              <div class="bookmark-arrow" v-if="activeSeriesIndex === 1">▼</div>
            </div>

            <!-- 逐病精讲书签 -->
            <div
              class="bookmark-card"
              :class="{ active: activeSeriesIndex === 2, 'has-courses': courseSeries.disease.length > 0 }"
              @click="toggleSeries(2)"
            >
              <div class="bookmark-icon">💊</div>
              <div class="bookmark-content">
                <h3>逐病精讲</h3>
                <p>针对具体疾病的深度讲解和调理方案</p>
                <div class="bookmark-count">{{ courseSeries.disease.length }} 门课程</div>
              </div>
              <div class="bookmark-arrow" v-if="activeSeriesIndex === 2">▼</div>
            </div>

            <!-- 全面学医书签 -->
            <div
              class="bookmark-card"
              :class="{ active: activeSeriesIndex === 3, 'has-courses': courseSeries.comprehensive.length > 0 }"
              @click="toggleSeries(3)"
            >
              <div class="bookmark-icon">🎓</div>
              <div class="bookmark-content">
                <h3>全面学医</h3>
                <p>系统全面的中医学习体系</p>
                <div class="bookmark-count">{{ courseSeries.comprehensive.length }} 门课程</div>
              </div>
              <div class="bookmark-arrow" v-if="activeSeriesIndex === 3">▼</div>
            </div>
          </div>

          <!-- 课程展示区域 -->
          <transition name="fade">
            <div v-if="activeSeriesIndex !== null && currentSeriesCourses.length > 0" class="courses-display">
              <div class="course-grid">
                <div v-for="course in currentSeriesCourses" :key="course.id" class="course-card" @click="goToCourseDetail(course.id)">
                  <div class="course-image">
                    <img :src="course.image_url || '/default-course.jpg'" :alt="course.title">
                    <span v-if="course.is_free" class="free-badge">免费</span>
                    <span v-else class="price-badge">¥{{ course.price }}</span>
                  </div>
                  <div class="course-info">
                    <h4>{{ course.title }}</h4>
                    <p class="course-desc">{{ course.description }}</p>
                    <div class="course-meta">
                      <span><el-icon><User /></el-icon> {{ course.instructor || '巫闪闪' }}</span>
                      <span><el-icon><Clock /></el-icon> {{ course.total_lessons }}课时</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </transition>
        </div>

        <!-- 无课程提示 -->
        <div v-else class="no-courses">
          <el-icon><Warning /></el-icon>
          <p>暂无课程，敬请期待...</p>
        </div>
      </div>
    </section>

    <!-- 巫闪闪个人签名 -->
    <div class="wushanshan-signature">
      <div class="signature-content">
        <p>💫 <strong>我是巫闪闪，让健康触手可及，让生命闪闪发光</strong></p>
        <p>人人都有机会健康 ✨</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { Loading, User, Clock, Warning } from '@element-plus/icons-vue'

const router = useRouter()

// 响应式数据
const loading = ref(false)
const allCourses = ref<any[]>([])
const activeSeriesIndex = ref<number | null>(null)

// 课程分类映射
const courseSeries = computed(() => {
  return {
    // 基础理论：理论基础 + 中药方剂
    theory: allCourses.value.filter(course =>
      ['THEORY', 'PHARMACY'].includes(course.category)
    ),
    // 实操演示：临床实践 + 养生保健 + 针灸推拿
    practical: allCourses.value.filter(course =>
      ['CLINICAL', 'WELLNESS', 'ACUPUNCTURE'].includes(course.category)
    ),
    // 逐病精讲
    disease: allCourses.value.filter(course =>
      course.category === 'DISEASE_SPECIFIC'
    ),
    // 全面学医
    comprehensive: allCourses.value.filter(course =>
      course.category === 'COMPREHENSIVE'
    )
  }
})

// 当前选中系列的课程
const currentSeriesCourses = computed(() => {
  if (activeSeriesIndex.value === null) return []
  const seriesMap = [
    courseSeries.value.theory,
    courseSeries.value.practical,
    courseSeries.value.disease,
    courseSeries.value.comprehensive
  ]
  return seriesMap[activeSeriesIndex.value] || []
})

// 切换系列
const toggleSeries = (index: number) => {
  if (activeSeriesIndex.value === index) {
    activeSeriesIndex.value = null
  } else {
    activeSeriesIndex.value = index
  }
}

// 跳转到三层体系详情页
const goToThreeLayerSystem = () => {
  router.push('/three-layer-system')
}

// 跳转到课程详情页
const goToCourseDetail = (courseId: number) => {
  router.push(`/courses/${courseId}`)
}

// 获取课程列表
const fetchCourses = async () => {
  loading.value = true
  try {
    // 直接使用fetch因为后端返回的是数组而非标准API响应格式
    const response = await fetch('/api/courses/?limit=100')
    const data = await response.json()

    if (Array.isArray(data)) {
      // 只显示已发布的课程
      allCourses.value = data.filter((course: any) => course.is_published)
      console.log('已加载课程数量:', allCourses.value.length)

      // 默认展开第一个有课程的系列
      if (courseSeries.value.theory.length > 0) {
        activeSeriesIndex.value = 0
      } else if (courseSeries.value.practical.length > 0) {
        activeSeriesIndex.value = 1
      } else if (courseSeries.value.disease.length > 0) {
        activeSeriesIndex.value = 2
      } else if (courseSeries.value.comprehensive.length > 0) {
        activeSeriesIndex.value = 3
      }
    } else {
      console.error('API返回格式异常:', data)
      ElMessage.warning('获取课程列表格式异常')
    }
  } catch (error) {
    console.error('获取课程列表失败:', error)
    ElMessage.error('获取课程列表失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 页面加载时获取课程
onMounted(() => {
  fetchCourses()
})
</script>

<style scoped>
.courses {
  min-height: 100vh;
  background-color: #f5f5f5;
}

/* 核心理念section样式 */
.core-philosophy {
  max-width: 1400px;
  margin: 0 auto;
  padding: 80px 60px;
  background: rgba(255, 255, 255, 0.95);
}

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
}

.section-header h2 {
  font-size: 3.2rem;
  color: #1a202c;
  margin-bottom: 24px;
  font-weight: 800;
  line-height: 1.2;
  background: linear-gradient(135deg, #2d3748, #4a5568);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* 方法论左右布局 */
.methodology-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 40px;
  align-items: center;
}

.insight-card {
  background: white;
  border-radius: 20px;
  padding: 50px 40px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.1);
  text-align: center;
  transition: transform 0.3s ease;
  cursor: pointer;
}

.insight-card:hover {
  transform: translateY(-10px);
}

.click-hint {
  margin-top: 15px;
  color: #667eea;
  font-weight: 600;
  font-size: 1rem;
}

.insight-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.insight-card p {
  font-size: 1.1rem;
  color: #4a5568;
  line-height: 1.6;
}

/* 右侧16字步骤 */
.steps-compact {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.step-compact {
  background: white;
  padding: 30px 20px;
  border-radius: 12px;
  text-align: center;
  font-size: 1.2rem;
  font-weight: 600;
  color: #2d3748;
  box-shadow: 0 8px 20px rgba(0,0,0,0.08);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.step-compact:hover {
  transform: translateY(-8px);
  border-color: #667eea;
  box-shadow: 0 15px 35px rgba(102, 126, 234, 0.2);
}

/* 课程展示区域 */
.courses-section {
  background: #f5f5f5;
  padding: 60px 0;
}

.container {
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 加载状态 */
.loading-state {
  text-align: center;
  padding: 60px 0;
}

.loading-state .el-icon {
  font-size: 48px;
  color: #409EFF;
  margin-bottom: 15px;
}

.loading-state p {
  color: #666;
  font-size: 1.1rem;
}

/* 书签式系列卡片 */
.series-bookmarks {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}

.bookmark-card {
  background: white;
  border-radius: 16px;
  padding: 30px 20px;
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  border: 3px solid transparent;
  position: relative;
  overflow: hidden;
}

.bookmark-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  transform: scaleX(0);
  transition: transform 0.3s ease;
}

.bookmark-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.bookmark-card:hover::before {
  transform: scaleX(1);
}

.bookmark-card.active {
  border-color: #667eea;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.3);
  transform: translateY(-4px);
}

.bookmark-card.active::before {
  transform: scaleX(1);
}

.bookmark-card:not(.has-courses) {
  opacity: 0.5;
  cursor: not-allowed;
}

.bookmark-icon {
  font-size: 3rem;
  margin-bottom: 15px;
}

.bookmark-content h3 {
  font-size: 1.4rem;
  color: #2d3748;
  margin-bottom: 10px;
  font-weight: 700;
}

.bookmark-content p {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.5;
  margin-bottom: 12px;
  min-height: 2.8em;
}

.bookmark-count {
  display: inline-block;
  padding: 4px 12px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 600;
}

.bookmark-arrow {
  margin-top: 15px;
  color: #667eea;
  font-size: 1.2rem;
  font-weight: bold;
  animation: bounce 1s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(5px); }
}

/* 课程展示区域 */
.courses-display {
  background: white;
  border-radius: 20px;
  padding: 40px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
}

/* 课程网格 */
.course-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
}

/* 课程卡片 */
.course-card {
  background: white;
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  cursor: pointer;
}

.course-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.course-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.course-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.free-badge, .price-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 600;
  color: white;
}

.free-badge {
  background: #67C23A;
}

.price-badge {
  background: #F56C6C;
}

.course-info {
  padding: 20px;
}

.course-info h4 {
  font-size: 1.3rem;
  color: #2d3748;
  margin-bottom: 10px;
  font-weight: 700;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.course-desc {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
  min-height: 3em;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #999;
  font-size: 0.9rem;
  border-top: 1px solid #f0f0f0;
  padding-top: 12px;
}

.course-meta span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.course-meta .el-icon {
  font-size: 14px;
}

/* 无课程状态 */
.no-courses {
  text-align: center;
  padding: 80px 20px;
  color: #999;
}

.no-courses .el-icon {
  font-size: 64px;
  margin-bottom: 20px;
  color: #C0C4CC;
}

.no-courses p {
  font-size: 1.2rem;
}

/* 淡入淡出动画 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* 巫闪闪个人签名样式 */
.wushanshan-signature {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 25px 20px;
  text-align: center;
  margin-top: 0;
}

.signature-content {
  max-width: 800px;
  margin: 0 auto;
}

.signature-content p {
  margin-bottom: 15px;
  font-size: 1.2rem;
  line-height: 1.6;
}

.signature-content p:last-child {
  margin-bottom: 0;
  font-size: 1.1rem;
  opacity: 0.9;
}

.signature-content strong {
  font-weight: 700;
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .series-bookmarks {
    grid-template-columns: repeat(2, 1fr);
  }

  .course-grid {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 25px;
  }

  .methodology-layout {
    grid-template-columns: 1fr;
    gap: 30px;
  }
}

@media (max-width: 768px) {
  .core-philosophy {
    padding: 40px 20px;
  }

  .series-bookmarks {
    grid-template-columns: 1fr;
    gap: 15px;
  }

  .bookmark-card {
    padding: 25px 20px;
  }

  .courses-display {
    padding: 25px 20px;
  }

  .course-grid {
    grid-template-columns: 1fr;
    gap: 20px;
  }

  .course-image {
    height: 180px;
  }

  .course-info h4 {
    font-size: 1.2rem;
  }

  .methodology-layout {
    grid-template-columns: 1fr;
  }

  .steps-compact {
    grid-template-columns: 1fr 1fr;
    gap: 15px;
  }

  .step-compact {
    padding: 20px 15px;
    font-size: 1rem;
  }

  .wushanshan-signature {
    padding: 20px 15px;
  }

  .signature-content p {
    font-size: 1.1rem;
  }

  .signature-content p:last-child {
    font-size: 1rem;
  }
}
</style>
