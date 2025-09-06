<template>
  <div class="courses">
    <PageContainer>
      
      <div class="courses-content" v-loading="loading">
        <div class="course-philosophy">
          <h1 class="philosophy-title">重构你的健康认知</h1>
        </div>
        
        
        <el-tabs v-model="activeTab" class="courses-tabs">
          <el-tab-pane label="全部课程" name="all">
            <div class="courses-grid">
              <el-card class="course-card" v-for="course in allCourses" :key="course.id">
                <img :src="course.image" :alt="course.title" class="course-image">
                <div class="course-info">
                  <h3>{{ course.title }}</h3>
                  <p class="course-description">{{ course.description }}</p>
                  <p class="course-instructor" v-if="course.instructor">
                    <el-icon><User /></el-icon>
                    {{ course.instructor }}
                  </p>
                  <div class="course-meta">
                    <span class="course-duration">{{ course.duration }}</span>
                    <span class="course-price">{{ course.is_free ? '免费' : `¥${course.price}` }}</span>
                    <span class="course-category">{{ getCategoryName(course.category) }}</span>
                  </div>
                  <el-button type="primary" @click="enrollCourse(course.id)">立即学习</el-button>
                </div>
              </el-card>
            </div>
            <div v-if="allCourses.length === 0 && !loading" class="no-courses">
              <p>暂无课程数据</p>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="中医基础" name="basic">
            <div class="category-intro">
              <h2>中医基础理论</h2>
              <p>从阴阳五行到脏腑经络，奠定中医思维基础</p>
            </div>
            <div class="courses-grid">
              <el-card class="course-card" v-for="course in basicCourses" :key="course.id">
                <img :src="course.image" :alt="course.title" class="course-image">
                <div class="course-info">
                  <h3>{{ course.title }}</h3>
                  <p class="course-description">{{ course.description }}</p>
                  <p class="course-instructor" v-if="course.instructor">
                    <el-icon><User /></el-icon>
                    {{ course.instructor }}
                  </p>
                  <div class="course-meta">
                    <span class="course-duration">{{ course.duration }}</span>
                    <span class="course-price">{{ course.is_free ? '免费' : `¥${course.price}` }}</span>
                  </div>
                  <el-button type="primary" @click="enrollCourse(course.id)">立即学习</el-button>
                </div>
              </el-card>
            </div>
            <div v-if="basicCourses.length === 0 && !loading" class="no-courses">
              <p>暂无中医基础课程</p>
            </div>
          </el-tab-pane>
          
          
          <el-tab-pane label="逐病精讲" name="disease-focused">
            <div class="category-intro featured">
              <h2>逐病精讲专题</h2>
              <p>针对常见疾病，深入讲解中医诊治思路</p>
            </div>
            <div class="courses-grid">
              <el-card class="course-card" v-for="course in diseaseFocusedCourses" :key="course.id">
                <img :src="course.image" :alt="course.title" class="course-image">
                <div class="course-info">
                  <h3>{{ course.title }}</h3>
                  <p class="course-description">{{ course.description }}</p>
                  <p class="course-instructor" v-if="course.instructor">
                    <el-icon><User /></el-icon>
                    {{ course.instructor }}
                  </p>
                  <div class="course-meta">
                    <span class="course-duration">{{ course.duration }}</span>
                    <span class="course-price">{{ course.is_free ? '免费' : `¥${course.price}` }}</span>
                  </div>
                  <el-button type="primary" @click="enrollCourse(course.id)">立即学习</el-button>
                </div>
              </el-card>
            </div>
            <div v-if="diseaseFocusedCourses.length === 0 && !loading" class="no-courses">
              <p>暂无逐病精讲课程</p>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="全面学医" name="comprehensive">
            <div class="category-intro featured">
              <h2>全面学医系统</h2>
              <p>系统性中医学习，从入门到精通的完整体系</p>
            </div>
            <div class="courses-grid">
              <el-card class="course-card" v-for="course in comprehensiveCourses" :key="course.id">
                <img :src="course.image" :alt="course.title" class="course-image">
                <div class="course-info">
                  <h3>{{ course.title }}</h3>
                  <p class="course-description">{{ course.description }}</p>
                  <p class="course-instructor" v-if="course.instructor">
                    <el-icon><User /></el-icon>
                    {{ course.instructor }}
                  </p>
                  <div class="course-meta">
                    <span class="course-duration">{{ course.duration }}</span>
                    <span class="course-price">{{ course.is_free ? '免费' : `¥${course.price}` }}</span>
                  </div>
                  <el-button type="primary" @click="enrollCourse(course.id)">立即学习</el-button>
                </div>
              </el-card>
            </div>
            <div v-if="comprehensiveCourses.length === 0 && !loading" class="no-courses">
              <p>暂无全面学医课程</p>
            </div>
          </el-tab-pane>
          
          <el-tab-pane label="免费体验" name="free">
            <div class="category-intro special">
              <h2>免费课程体验</h2>
              <p>精选免费课程，让您先体验中医学习的魅力</p>
            </div>
            <div class="courses-grid">
              <el-card class="course-card" v-for="course in freeCourses" :key="course.id">
                <img :src="course.image" :alt="course.title" class="course-image">
                <div class="course-info">
                  <h3>{{ course.title }}</h3>
                  <p class="course-description">{{ course.description }}</p>
                  <p class="course-instructor" v-if="course.instructor">
                    <el-icon><User /></el-icon>
                    {{ course.instructor }}
                  </p>
                  <div class="course-meta">
                    <span class="course-duration">{{ course.duration }}</span>
                    <span class="course-price">免费</span>
                    <span class="course-category">{{ getCategoryName(course.category) }}</span>
                  </div>
                  <el-button type="primary" @click="enrollCourse(course.id)">立即学习</el-button>
                </div>
              </el-card>
            </div>
            <div v-if="freeCourses.length === 0 && !loading" class="no-courses">
              <p>暂无免费课程</p>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </PageContainer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { User } from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'
import PageContainer from '../components/PageContainer.vue'
import { PLACEHOLDER_IMAGES } from '@/utils/placeholder'

const router = useRouter()

// 定义响应式数据
const activeTab = ref('all')
const allCourses = ref([])
const loading = ref(true)

// 计算属性用于筛选课程
const basicCourses = computed(() => allCourses.value.filter(course => course.category === 'basic'))
const diseaseFocusedCourses = computed(() => allCourses.value.filter(course => course.category === '逐病精讲'))
const comprehensiveCourses = computed(() => allCourses.value.filter(course => course.category === '全面学医'))
const freeCourses = computed(() => allCourses.value.filter(course => course.is_free))

// 分类名称映射
const getCategoryName = (category: string) => {
  const categoryMap = {
    'basic': '中医基础',
    'seasonal': '四季养生', 
    'diet': '药膳食疗',
    'massage': '推拿按摩',
    'herb': '本草方剂',
    '逐病精讲': '逐病精讲',
    '全面学医': '全面学医'
  }
  return categoryMap[category] || category
}

// 获取课程数据
const fetchCourses = async () => {
  try {
    loading.value = true
    const response = await fetch('/api/courses/')
    
    if (!response.ok) {
      throw new Error('获取课程数据失败')
    }
    
    const courses = await response.json()
    
    // 处理课程数据
    const processedCourses = courses.map(course => ({
      id: course.id,
      title: course.title,
      description: course.description,
      category: course.category,  // 重要：包含分类字段
      duration: `${course.total_lessons}课时`,
      price: course.is_free ? 0 : course.price,
      image: course.image_url || PLACEHOLDER_IMAGES.course,
      instructor: course.instructor,
      total_lessons: course.total_lessons,
      is_free: course.is_free
    }))
    
    allCourses.value = processedCourses
    
  } catch (error) {
    console.error('获取课程失败:', error)
    ElMessage.error('获取课程失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

// 查看课程详情
const viewCourse = (courseId: number) => {
  router.push(`/courses/${courseId}`)
}

// 为了保持兼容性，保留原方法  
const enrollCourse = (courseId: number) => {
  viewCourse(courseId)
}

// 挂载时获取课程数据
onMounted(() => {
  fetchCourses()
})
</script>

<style scoped>
.courses {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.courses-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}


/* 健康哲学标题区域 */
.course-philosophy {
  text-align: center;
  margin-bottom: 40px;
  padding: 40px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 15px;
  color: white;
  position: relative;
  overflow: hidden;
}

.course-philosophy::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 30% 70%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
}

.philosophy-title {
  font-size: 3rem;
  font-weight: 800;
  margin-bottom: 1rem;
  position: relative;
  z-index: 1;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  letter-spacing: -1px;
}

.philosophy-subtitle {
  font-size: 1.5rem;
  font-weight: 400;
  opacity: 0.95;
  position: relative;
  z-index: 1;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
  line-height: 1.4;
  max-width: 600px;
  margin: 0 auto;
}

/* 健康误区引言 */
.misconceptions-intro {
  text-align: center;
  padding: 40px 20px;
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  border-radius: 15px;
  color: white;
  margin-bottom: 40px;
  position: relative;
  overflow: hidden;
}

.misconceptions-intro::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="1"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
  opacity: 0.3;
}

.intro-title {
  position: relative;
  z-index: 1;
  font-size: 2.5rem;
  font-weight: 700;
  line-height: 1.2;
  margin-bottom: 2rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.intro-title .highlight {
  color: #ff6b6b;
  text-shadow: 0 0 20px rgba(255, 107, 107, 0.5);
  font-weight: 900;
}

.intro-subtitle {
  position: relative;
  z-index: 1;
  font-size: 1.3rem;
  opacity: 0.95;
  line-height: 1.5;
  margin: 0;
  font-weight: 300;
}

.intro-subtitle strong {
  color: #ffd93d;
  font-weight: 700;
  font-size: 1.1em;
  text-shadow: 0 0 15px rgba(255, 217, 61, 0.3);
}

/* 分类介绍样式 */
.category-intro {
  text-align: center;
  padding: 30px 20px;
  margin-bottom: 30px;
  background: linear-gradient(135deg, #4CAF50 0%, #45a049 100%);
  border-radius: 12px;
  color: white;
  position: relative;
  overflow: hidden;
}

.category-intro::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: radial-gradient(circle at 70% 30%, rgba(255, 255, 255, 0.1) 0%, transparent 50%);
}

.category-intro h2 {
  position: relative;
  z-index: 1;
  font-size: 1.8rem;
  font-weight: 600;
  margin-bottom: 0.8rem;
  text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.2);
}

.category-intro p {
  position: relative;
  z-index: 1;
  font-size: 1.1rem;
  opacity: 0.95;
  margin: 0;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.1);
}

.category-intro.featured {
  background: linear-gradient(135deg, #ff6b6b 0%, #ee5a52 100%);
}

.category-intro.special {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.course-category {
  background-color: #f0f0f0;
  color: #666;
  padding: 2px 8px;
  border-radius: 12px;
  font-size: 11px;
  margin-left: 8px;
}


.course-card {
  margin-bottom: 20px;
  transition: all 0.3s ease;
}

.course-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.12);
}

.course-image {
  width: 100%;
  height: 150px;
  object-fit: cover;
}

.course-info {
  padding: 15px 0;
}

.course-info h3 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 16px;
}

.course-description {
  color: #666;
  margin-bottom: 10px;
  height: 40px;
  overflow: hidden;
  font-size: 14px;
  line-height: 1.4;
}

.course-instructor {
  color: #888;
  font-size: 12px;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.course-duration {
  color: #999;
  font-size: 12px;
}

.course-price {
  color: #f56c6c;
  font-weight: bold;
  font-size: 14px;
}

.no-courses {
  text-align: center;
  padding: 40px;
  color: #999;
}

.el-button {
  width: 100%;
}

.courses-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  width: 100%;
}

@media (max-width: 768px) {
  .courses-grid {
    grid-template-columns: 1fr;
  }
}
</style>