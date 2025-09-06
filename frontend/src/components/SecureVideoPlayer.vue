<template>
  <div class="secure-video-container" ref="containerRef" @contextmenu.prevent>
    <div class="video-wrapper" v-show="!isBlocked">
      <video 
        ref="videoRef"
        :src="videoUrl"
        @loadedmetadata="onVideoLoaded"
        @timeupdate="onTimeUpdate"
        @ended="onVideoEnded"
        controlslist="nodownload nofullscreen noremoteplayback"
        disablepictureinpicture
        @contextmenu.prevent
      ></video>
      
      <div class="watermark" v-if="watermarkConfig">
        {{ watermarkText }}
      </div>
      
      <div class="video-controls">
        <button @click="togglePlay" class="play-btn">
          {{ isPlaying ? '⏸️' : '▶️' }}
        </button>
        <div class="progress-bar" @click="seekTo">
          <div class="progress-fill" :style="{ width: progressPercent + '%' }"></div>
        </div>
        <span class="time-display">{{ formatTime(currentTime) }} / {{ formatTime(duration) }}</span>
      </div>
    </div>
    
    <div class="blocked-message" v-if="isBlocked">
      <h3>🚫 检测到违规操作</h3>
      <p>为保护版权，视频已暂停播放</p>
      <el-button type="primary" @click="resumeVideo">继续播放</el-button>
    </div>
    
    <div class="loading" v-if="isLoading">
      <el-loading element-loading-text="视频加载中..."></el-loading>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'

interface Props {
  lessonId: number
  userId: string
}

interface WatermarkConfig {
  type: string
  content: string
  position: string
  opacity: number
  font_size: number
  color: string
  interval: number
}

interface SecurityConfig {
  disable_right_click: boolean
  disable_dev_tools: boolean
  disable_screen_capture: boolean
  heartbeat_interval: number
}

const props = defineProps<Props>()

// 响应式变量
const containerRef = ref<HTMLElement>()
const videoRef = ref<HTMLVideoElement>()
const videoUrl = ref('')
const isLoading = ref(true)
const isPlaying = ref(false)
const isBlocked = ref(false)
const currentTime = ref(0)
const duration = ref(0)
const accessToken = ref('')
const watermarkConfig = ref<WatermarkConfig>()
const securityConfig = ref<SecurityConfig>()
const watermarkText = ref('')

let heartbeatTimer: number | null = null
let watermarkTimer: number | null = null
let screenCaptureDetector: any = null

// 计算属性
const progressPercent = computed(() => {
  return duration.value > 0 ? (currentTime.value / duration.value) * 100 : 0
})

// 初始化视频播放器
const initializePlayer = async () => {
  try {
    const response = await fetch(`/api/video/lessons/${props.lessonId}/play-url?user_id=${props.userId}`)
    const data = await response.json()
    
    if (response.ok) {
      videoUrl.value = data.video_url
      accessToken.value = data.access_token
      watermarkConfig.value = data.watermark_config
      securityConfig.value = data.security_config
      
      await nextTick()
      setupSecurityFeatures()
      startHeartbeat()
    } else {
      throw new Error(data.detail || '获取视频地址失败')
    }
  } catch (error) {
    console.error('初始化播放器失败:', error)
    ElMessage.error('视频加载失败')
  } finally {
    isLoading.value = false
  }
}

// 设置安全功能
const setupSecurityFeatures = () => {
  if (!securityConfig.value) return
  
  // 禁用右键菜单
  if (securityConfig.value.disable_right_click) {
    document.addEventListener('contextmenu', preventContextMenu)
  }
  
  // 禁用开发者工具
  if (securityConfig.value.disable_dev_tools) {
    document.addEventListener('keydown', preventDevTools)
  }
  
  // 检测录屏
  if (securityConfig.value.disable_screen_capture) {
    detectScreenCapture()
  }
  
  // 设置水印
  if (watermarkConfig.value) {
    setupWatermark()
  }
}

// 防止右键菜单
const preventContextMenu = (e: MouseEvent) => {
  e.preventDefault()
  return false
}

// 防止开发者工具快捷键
const preventDevTools = (e: KeyboardEvent) => {
  // 禁用F12, Ctrl+Shift+I, Ctrl+U等
  if (
    e.key === 'F12' ||
    (e.ctrlKey && e.shiftKey && e.key === 'I') ||
    (e.ctrlKey && e.shiftKey && e.key === 'C') ||
    (e.ctrlKey && e.key === 'U')
  ) {
    e.preventDefault()
    blockVideo('检测到开发者工具使用')
    return false
  }
}

// 检测录屏
const detectScreenCapture = () => {
  // 检测录屏API
  if ('getDisplayMedia' in navigator.mediaDevices) {
    // 定期检查是否有录屏
    screenCaptureDetector = setInterval(() => {
      if (document.visibilityState === 'hidden') {
        blockVideo('检测到可能的录屏行为')
      }
    }, 1000)
  }
  
  // 检测窗口失焦
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      pauseVideo()
    }
  })
  
  // 检测窗口大小变化（可能是录屏软件）
  window.addEventListener('resize', () => {
    // 检测是否有异常的窗口大小变化
    const suspiciousResize = window.outerWidth !== window.innerWidth + 16 || 
                            window.outerHeight !== window.innerHeight + 90
    if (suspiciousResize) {
      blockVideo('检测到可疑的窗口操作')
    }
  })
}

// 设置水印
const setupWatermark = () => {
  if (!watermarkConfig.value) return
  
  watermarkText.value = watermarkConfig.value.content
  
  // 动态水印（每隔几秒钟变化位置）
  watermarkTimer = setInterval(() => {
    updateWatermarkPosition()
  }, watermarkConfig.value.interval * 1000)
}

// 更新水印位置
const updateWatermarkPosition = () => {
  const watermark = containerRef.value?.querySelector('.watermark') as HTMLElement
  if (watermark) {
    const positions = ['top-left', 'top-right', 'bottom-left', 'bottom-right']
    const randomPosition = positions[Math.floor(Math.random() * positions.length)]
    watermark.className = `watermark ${randomPosition}`
  }
}

// 阻止视频播放
const blockVideo = (reason: string) => {
  isBlocked.value = true
  pauseVideo()
  ElMessage.error(`视频已暂停: ${reason}`)
  
  // 记录违规行为
  recordViolation(reason)
}

// 恢复视频播放
const resumeVideo = () => {
  isBlocked.value = false
}

// 记录违规行为
const recordViolation = (reason: string) => {
  fetch(`/api/video/lessons/${props.lessonId}/violation`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      user_id: props.userId,
      reason: reason,
      timestamp: Date.now()
    })
  }).catch(console.error)
}

// 开始心跳检测
const startHeartbeat = () => {
  if (!securityConfig.value?.heartbeat_interval) return
  
  heartbeatTimer = setInterval(async () => {
    try {
      const response = await fetch(`/api/video/lessons/${props.lessonId}/heartbeat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id: props.userId,
          current_time: Math.floor(currentTime.value),
          token: accessToken.value
        })
      })
      
      const result = await response.json()
      
      if (!response.ok || !result.continue_play) {
        blockVideo('会话已过期，请重新加载')
      }
    } catch (error) {
      console.error('心跳检测失败:', error)
    }
  }, securityConfig.value.heartbeat_interval * 1000)
}

// 视频控制方法
const togglePlay = () => {
  if (!videoRef.value || isBlocked.value) return
  
  if (isPlaying.value) {
    pauseVideo()
  } else {
    playVideo()
  }
}

const playVideo = () => {
  if (videoRef.value && !isBlocked.value) {
    videoRef.value.play()
    isPlaying.value = true
  }
}

const pauseVideo = () => {
  if (videoRef.value) {
    videoRef.value.pause()
    isPlaying.value = false
  }
}

const seekTo = (event: MouseEvent) => {
  if (!videoRef.value || !duration.value || isBlocked.value) return
  
  const progressBar = event.currentTarget as HTMLElement
  const rect = progressBar.getBoundingClientRect()
  const percent = (event.clientX - rect.left) / rect.width
  const newTime = percent * duration.value
  
  videoRef.value.currentTime = newTime
  currentTime.value = newTime
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
  }
}

const onVideoEnded = () => {
  isPlaying.value = false
  // 标记课程完成
  markLessonCompleted()
}

const markLessonCompleted = async () => {
  try {
    await fetch(`/api/video/lessons/${props.lessonId}/complete`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        user_id: props.userId,
        token: accessToken.value
      })
    })
  } catch (error) {
    console.error('标记课程完成失败:', error)
  }
}

// 格式化时间
const formatTime = (seconds: number): string => {
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
}

// 生命周期
onMounted(() => {
  initializePlayer()
})

onUnmounted(() => {
  // 清理定时器和事件监听
  if (heartbeatTimer) clearInterval(heartbeatTimer)
  if (watermarkTimer) clearInterval(watermarkTimer)
  if (screenCaptureDetector) clearInterval(screenCaptureDetector)
  
  document.removeEventListener('contextmenu', preventContextMenu)
  document.removeEventListener('keydown', preventDevTools)
})
</script>

<style scoped>
.secure-video-container {
  position: relative;
  width: 100%;
  background: #000;
  border-radius: 8px;
  overflow: hidden;
}

.video-wrapper {
  position: relative;
  width: 100%;
  height: 500px;
}

video {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.watermark {
  position: absolute;
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
  pointer-events: none;
  z-index: 10;
  padding: 5px 10px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  user-select: none;
}

.watermark.top-left {
  top: 20px;
  left: 20px;
}

.watermark.top-right {
  top: 20px;
  right: 20px;
}

.watermark.bottom-left {
  bottom: 60px;
  left: 20px;
}

.watermark.bottom-right {
  bottom: 60px;
  right: 20px;
}

.video-controls {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  padding: 10px 15px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.play-btn {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  cursor: pointer;
}

.progress-bar {
  flex: 1;
  height: 4px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 2px;
  cursor: pointer;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: #409eff;
  border-radius: 2px;
  transition: width 0.1s;
}

.time-display {
  color: white;
  font-size: 12px;
  min-width: 100px;
  text-align: right;
}

.blocked-message {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 300px;
  background: #f5f5f5;
  text-align: center;
}

.blocked-message h3 {
  color: #f56c6c;
  margin-bottom: 10px;
}

.loading {
  height: 300px;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* 防止选择和拖拽 */
.secure-video-container * {
  user-select: none;
  -webkit-user-drag: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
}

/* 隐藏video的默认控件 */
video::-webkit-media-controls {
  display: none !important;
}

video::-webkit-media-controls-panel {
  display: none !important;
}
</style>