<template>
  <div class="course-detail">
    <PageContainer>
      <template #breadcrumb>
        <el-breadcrumb separator="/">
          <el-breadcrumb-item :to="{ path: '/' }">方案</el-breadcrumb-item>
          <el-breadcrumb-item :to="{ path: '/courses' }">课程中心</el-breadcrumb-item>
          <el-breadcrumb-item>{{ course?.title }}</el-breadcrumb-item>
        </el-breadcrumb>
      </template>
      
      <div class="course-content" v-if="course">
        <div class="course-header">
          <div class="course-info">
            <h1>{{ course.title }}</h1>
            <p class="course-description">{{ course.description }}</p>
            <div class="course-meta">
              <span class="instructor">👨‍🏫 {{ course.instructor || '中医专家' }}</span>
              <span class="duration">⏱️ {{ course.duration }}</span>
              <span class="lessons">📚 {{ course.total_lessons }}课时</span>
              <span class="price">💰 {{ course.is_free ? '免费' : `¥${course.price}` }}</span>
            </div>
            
            <div class="enrollment-section" v-if="!enrollment?.enrolled">
              <el-button 
                type="primary" 
                size="large" 
                @click="enrollCourse"
                :loading="enrolling"
              >
                {{ course.is_free ? '免费学习' : `¥${course.price} 立即购买` }}
              </el-button>
            </div>
            
            <div class="progress-section" v-else>
              <div class="progress-info">
                <span>学习进度: {{ Math.round((enrollment.progress || 0) * 100) }}%</span>
                <span>已完成: {{ enrollment.completed_lessons || 0 }}/{{ course.total_lessons }}课时</span>
              </div>
              <el-progress 
                :percentage="Math.round((enrollment.progress || 0) * 100)"
                :stroke-width="8"
                color="#409eff"
              ></el-progress>
            </div>
          </div>
          
          <div class="course-cover">
            <img :src="course.image_url" :alt="course.title" />
          </div>
        </div>
        
        <!-- 视频播放区域 -->
        <div class="video-section" v-if="selectedLesson && (enrollment?.enrolled || selectedLesson.is_free)">
          <div class="video-header">
            <h3>{{ selectedLesson.title }}</h3>
            <div class="lesson-meta">
              <span>第{{ selectedLesson.order }}课</span>
              <span v-if="selectedLesson.duration">{{ formatDuration(selectedLesson.duration) }}</span>
            </div>
          </div>
          
          <SimpleVideoPlayer 
            :lesson-id="selectedLesson.id"
            :user-id="userId"
            @progress-update="updateProgress"
          />
        </div>
        
        <!-- 课程目录 -->
        <div class="lessons-section">
          <h3>课程目录</h3>
          <div class="lessons-list">
            <div 
              v-for="lesson in lessons" 
              :key="lesson.id"
              class="lesson-item"
              :class="{ 
                active: selectedLesson?.id === lesson.id,
                locked: !enrollment?.enrolled && !lesson.is_free,
                completed: isLessonCompleted(lesson.id)
              }"
              @click="selectLesson(lesson)"
            >
              <div class="lesson-number">{{ lesson.order }}</div>
              <div class="lesson-info">
                <h4>{{ lesson.title }}</h4>
                <p>{{ lesson.description }}</p>
                <div class="lesson-meta">
                  <span v-if="lesson.duration">{{ formatDuration(lesson.duration) }}</span>
                  <span v-if="lesson.is_free" class="free-tag">免费</span>
                  <span v-if="!enrollment?.enrolled && !lesson.is_free" class="lock-tag">🔒</span>
                </div>
              </div>
              <div class="lesson-status">
                <span v-if="isLessonCompleted(lesson.id)" class="completed">✓</span>
                <span v-else-if="enrollment?.enrolled" class="available">▶️</span>
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <div class="loading" v-else-if="loading">
        <el-loading element-loading-text="加载课程信息..."></el-loading>
      </div>
    </PageContainer>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useUserStore } from '../stores/user'
import { authFetch, checkAuth } from '../utils/auth'
import PageContainer from '../components/PageContainer.vue'
import SimpleVideoPlayer from '../components/SimpleVideoPlayer.vue'

const route = useRoute()
const router = useRouter()
const userStore = useUserStore()

// 响应式数据
const courseId = ref(parseInt(route.params.id as string))
const userId = computed(() => userStore.getUserIdString() || 'guest')
const realUserId = computed(() => userStore.getUserId())
const course = ref<any>(null)
const lessons = ref<any[]>([])
const selectedLesson = ref<any>(null)
const enrollment = ref<any>(null)
const loading = ref(true)
const enrolling = ref(false)

// 加载课程信息
const loadCourseInfo = async () => {
  try {
    // 并行加载课程信息、课时列表和用户报名状态
    const [courseRes, lessonsRes, enrollmentRes] = await Promise.all([
      authFetch(`/api/courses/${courseId.value}`, {}, false),
      authFetch(`/api/courses/${courseId.value}/lessons`, {}, false),
      authFetch(`/api/courses/${courseId.value}/enrollment/${userId.value}`, {}, false)
    ])
    
    if (courseRes.ok) course.value = await courseRes.json()
    if (lessonsRes.ok) lessons.value = await lessonsRes.json()
    if (enrollmentRes.ok) enrollment.value = await enrollmentRes.json()
    
    // 如果已经报名，选择上次观看的课程或第一课
    if (enrollment.value?.enrolled) {
      const lastWatchedId = enrollment.value.last_watched_lesson_id
      selectedLesson.value = lastWatchedId 
        ? lessons.value.find(l => l.id === lastWatchedId)
        : lessons.value[0]
    }
    
  } catch (error) {
    console.error('加载课程信息失败:', error)
    ElMessage.error('课程加载失败，请刷新页面重试')
  } finally {
    loading.value = false
  }
}

// 报名课程
const enrollCourse = async () => {
  if (enrolling.value) return
  
  // 检查用户是否登录
  if (!checkAuth()) {
    return
  }
  
  enrolling.value = true
  try {
    const response = await authFetch(`/api/courses/${courseId.value}/enroll`, {
      method: 'POST',
      body: JSON.stringify({
        user_id: realUserId.value
      })
    })
    
    if (response.ok) {
      ElMessage.success('报名成功！开始学习吧')
      // 重新加载报名状态
      const enrollmentRes = await authFetch(`/api/courses/${courseId.value}/enrollment/${userId.value}`, {}, false)
      if (enrollmentRes.ok) {
        enrollment.value = await enrollmentRes.json()
      }
      
      // 选择第一课开始学习
      if (lessons.value.length > 0) {
        selectedLesson.value = lessons.value[0]
      }
    }
  } catch (error) {
    console.error('报名失败:', error)
    // authFetch已处理错误提示，这里不需要重复提示
  } finally {
    enrolling.value = false
  }
}

// 选择课时
const selectLesson = (lesson: any) => {
  // 检查是否有权限观看
  if (!lesson.is_free && !enrollment.value?.enrolled) {
    ElMessage.warning('请先购买课程')
    return
  }
  
  // 设置选中的课时，无论是否报名，免费课时都可以观看
  selectedLesson.value = lesson
  console.log('选择了课时:', lesson.title)
}

// 检查课时是否已完成
const isLessonCompleted = (lessonId: number): boolean => {
  // 这里可以从观看记录中检查
  return false
}

// 更新学习进度
const updateProgress = (progressData: any) => {
  // 更新本地进度状态
  if (enrollment.value) {
    enrollment.value.progress = progressData.progress
    enrollment.value.completed_lessons = progressData.completed_lessons
  }
}

// 格式化时长
const formatDuration = (seconds: number): string => {
  const minutes = Math.floor(seconds / 60)
  const remainingSeconds = seconds % 60
  return `${minutes}分${remainingSeconds}秒`
}

onMounted(() => {
  loadCourseInfo()
})
</script>

<style scoped>
.course-detail {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.course-content {
  background-color: white;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.course-header {
  display: flex;
  gap: 30px;
  padding: 30px;
  border-bottom: 1px solid #eee;
}

.course-info {
  flex: 1;
}

.course-info h1 {
  font-size: 28px;
  color: #333;
  margin-bottom: 15px;
}

.course-description {
  color: #666;
  font-size: 16px;
  line-height: 1.6;
  margin-bottom: 20px;
}

.course-meta {
  display: flex;
  gap: 20px;
  margin-bottom: 25px;
  flex-wrap: wrap;
}

.course-meta span {
  padding: 5px 12px;
  background: #f0f0f0;
  border-radius: 15px;
  font-size: 14px;
  color: #666;
}

.course-cover {
  width: 300px;
  flex-shrink: 0;
}

.course-cover img {
  width: 100%;
  border-radius: 8px;
}

.enrollment-section {
  margin-top: 20px;
}

.progress-section {
  margin-top: 20px;
}

.progress-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  font-size: 14px;
  color: #666;
}

.video-section {
  padding: 30px;
  border-bottom: 1px solid #eee;
}

.video-header {
  margin-bottom: 20px;
}

.video-header h3 {
  color: #333;
  margin-bottom: 5px;
}

.lesson-meta {
  color: #666;
  font-size: 14px;
}

.lessons-section {
  padding: 30px;
}

.lessons-section h3 {
  margin-bottom: 20px;
  color: #333;
}

.lessons-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.lesson-item {
  display: flex;
  align-items: center;
  padding: 15px 20px;
  border: 1px solid #eee;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s;
}

.lesson-item:hover:not(.locked) {
  border-color: #409eff;
  background-color: #f0f8ff;
}

.lesson-item.active {
  border-color: #409eff;
  background-color: #e6f3ff;
}

.lesson-item.locked {
  opacity: 0.6;
  cursor: not-allowed;
}

.lesson-item.completed {
  background-color: #f0f9ff;
  border-color: #67c23a;
}

.lesson-number {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #409eff;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  margin-right: 15px;
  flex-shrink: 0;
}

.lesson-item.locked .lesson-number {
  background: #ccc;
}

.lesson-item.completed .lesson-number {
  background: #67c23a;
}

.lesson-info {
  flex: 1;
}

.lesson-info h4 {
  margin: 0 0 5px 0;
  color: #333;
  font-size: 16px;
}

.lesson-info p {
  margin: 0 0 8px 0;
  color: #666;
  font-size: 14px;
}

.lesson-meta {
  display: flex;
  gap: 10px;
  font-size: 12px;
}

.free-tag {
  color: #67c23a;
  font-weight: bold;
}

.lock-tag {
  color: #999;
}

.lesson-status {
  margin-left: 15px;
  font-size: 18px;
}

.completed {
  color: #67c23a;
}

.available {
  color: #409eff;
}

.loading {
  height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>