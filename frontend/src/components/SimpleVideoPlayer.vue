<template>
  <div class="simple-video-player">
    <div class="video-container" v-if="lesson">
      <video 
        ref="videoRef"
        :src="videoUrl"
        controls
        @loadedmetadata="onVideoLoaded"
        @timeupdate="onTimeUpdate"
        @ended="onVideoEnded"
        :poster="lesson.cover_url"
        class="video-element"
      >
        您的浏览器不支持视频播放
      </video>
      
      <div class="video-info">
        <h4>{{ lesson.title }}</h4>
        <p class="lesson-description">{{ lesson.description }}</p>
        <div class="video-meta">
          <span class="duration">⏱️ {{ formatDuration(lesson.duration) }}</span>
          <span class="order">第{{ lesson.order }}课</span>
          <span class="status" v-if="lesson.is_free">🆓 免费观看</span>
        </div>
      </div>
    </div>
    
    <div class="loading" v-else-if="loading">
      <el-loading element-loading-text="加载视频中..."></el-loading>
    </div>
    
    <div class="error" v-else>
      <el-empty description="视频暂不可用" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'

interface Props {
  lessonId: number
  userId: string
}

interface Lesson {
  id: number
  course_id: number
  title: string
  description: string
  order: number
  duration: number
  video_url: string
  cover_url: string
  is_free: boolean
  status: string
}

const props = defineProps<Props>()
const emit = defineEmits<{
  progressUpdate: [progress: number]
}>()

const videoRef = ref<HTMLVideoElement>()
const lesson = ref<Lesson>()
const loading = ref(true)
const currentTime = ref(0)
const duration = ref(0)

// 计算视频URL - 优先使用真实视频，fallback到示例视频
const videoUrl = computed(() => {
  if (!lesson.value) return ''
  
  // 检查是否是示例视频URL
  if (lesson.value.video_url.includes('sample-videos.com')) {
    // 使用Big Buck Bunny示例视频（公开可用）
    return 'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
  }
  
  // 检查是否是本地上传的视频
  if (lesson.value.video_url.startsWith('/uploads/')) {
    return `http://localhost:8000${lesson.value.video_url}`
  }
  
  // 返回原始URL
  return lesson.value.video_url
})

// 获取课时信息
const fetchLesson = async () => {
  try {
    loading.value = true
    // 首先尝试直接获取课时
    let response = await fetch(`/api/courses/lessons/${props.lessonId}`)
    
    if (!response.ok) {
      // 如果直接获取失败，通过遍历所有课程来找到对应课时
      console.log('直接获取课时失败，尝试通过课程列表查找...')
      lesson.value = await findLessonFromCourses()
      return
    }
    
    lesson.value = await response.json()
    
  } catch (error) {
    console.error('加载课时失败:', error)
    try {
      // 备用方案：通过课程API查找
      lesson.value = await findLessonFromCourses()
    } catch (fallbackError) {
      ElMessage.error('课时加载失败')
    }
  } finally {
    loading.value = false
  }
}

// 从课程列表中查找课时（备用方案）
const findLessonFromCourses = async () => {
  const coursesResponse = await fetch('/api/courses/')
  const courses = await coursesResponse.json()
  
  for (const course of courses) {
    const lessonsResponse = await fetch(`/api/courses/${course.id}/lessons`)
    const lessons = await lessonsResponse.json()
    
    const targetLesson = lessons.find(l => l.id === props.lessonId)
    if (targetLesson) {
      return targetLesson
    }
  }
  
  throw new Error('课时未找到')
}

// 视频事件处理
const onVideoLoaded = () => {
  if (videoRef.value) {
    duration.value = videoRef.value.duration
  }
}

const onTimeUpdate = () => {
  if (videoRef.value) {
    currentTime.value = videoRef.value.currentTime
    
    // 发送进度更新事件
    const progress = duration.value > 0 ? currentTime.value / duration.value : 0
    emit('progressUpdate', progress)
  }
}

const onVideoEnded = () => {
  // 标记课程完成
  markLessonCompleted()
  ElMessage.success('课程学习完成！')
}

// 标记课程完成
const markLessonCompleted = async () => {
  try {
    await fetch(`/api/courses/lessons/${props.lessonId}/complete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: props.userId
      })
    })
  } catch (error) {
    console.error('标记课程完成失败:', error)
  }
}

// 格式化时长
const formatDuration = (seconds: number): string => {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}分${secs}秒`
}

// 监听lesson ID变化
watch(() => props.lessonId, () => {
  if (props.lessonId) {
    fetchLesson()
  }
}, { immediate: true })

onMounted(() => {
  if (props.lessonId) {
    fetchLesson()
  }
})
</script>

<style scoped>
.simple-video-player {
  width: 100%;
  background: #f5f5f5;
  border-radius: 8px;
  overflow: hidden;
}

.video-container {
  background: white;
}

.video-element {
  width: 100%;
  height: 400px;
  object-fit: contain;
  background: #000;
}

.video-info {
  padding: 20px;
  border-top: 1px solid #eee;
}

.video-info h4 {
  margin: 0 0 10px 0;
  color: #333;
  font-size: 18px;
  font-weight: 600;
}

.lesson-description {
  color: #666;
  margin-bottom: 15px;
  line-height: 1.5;
}

.video-meta {
  display: flex;
  gap: 15px;
  align-items: center;
  font-size: 14px;
  color: #888;
}

.video-meta .status {
  color: #67c23a;
  font-weight: 500;
}

.loading, .error {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .video-element {
    height: 250px;
  }
  
  .video-info {
    padding: 15px;
  }
  
  .video-meta {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}
</style>