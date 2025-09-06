<template>
  <view class="video-player-page">
    <!-- 导航栏 -->
    <view class="navbar">
      <view class="nav-left" @click="goBack">
        <text class="back-icon">←</text>
      </view>
      <view class="nav-title">{{ lessonInfo.title }}</view>
      <view class="nav-right"></view>
    </view>
    
    <!-- 视频播放区域 -->
    <view class="video-container" v-if="!isBlocked">
      <video
        :id="videoId"
        :src="videoUrl"
        :controls="false"
        :show-center-play-btn="false"
        :show-progress="false"
        :show-fullscreen-btn="false"
        @loadedmetadata="onVideoLoaded"
        @timeupdate="onTimeUpdate"
        @ended="onVideoEnded"
        @error="onVideoError"
        class="video-element"
      ></video>
      
      <!-- 水印 -->
      <view class="watermark" v-if="watermarkText" :class="watermarkPosition">
        {{ watermarkText }}
      </view>
      
      <!-- 自定义控制栏 -->
      <view class="video-controls" v-show="showControls">
        <view class="controls-row">
          <button @click="togglePlay" class="play-btn">
            {{ isPlaying ? '⏸️' : '▶️' }}
          </button>
          
          <view class="progress-container" @click="seekTo">
            <view class="progress-bar">
              <view class="progress-fill" :style="{ width: progressPercent + '%' }"></view>
            </view>
          </view>
          
          <text class="time-text">{{ formatTime(currentTime) }} / {{ formatTime(duration) }}</text>
        </view>
      </view>
      
      <!-- 点击显示控制栏 -->
      <view class="tap-area" @click="toggleControls"></view>
    </view>
    
    <!-- 被阻止的消息 -->
    <view class="blocked-overlay" v-if="isBlocked">
      <view class="blocked-content">
        <text class="blocked-icon">🚫</text>
        <text class="blocked-title">检测到违规操作</text>
        <text class="blocked-desc">为保护版权，视频已暂停播放</text>
        <button class="resume-btn" @click="resumeVideo">继续播放</button>
      </view>
    </view>
    
    <!-- 加载状态 -->
    <view class="loading-overlay" v-if="isLoading">
      <text class="loading-text">视频加载中...</text>
    </view>
    
    <!-- 课程信息 -->
    <view class="lesson-info" v-if="lessonInfo.title">
      <text class="lesson-title">{{ lessonInfo.title }}</text>
      <text class="lesson-desc" v-if="lessonInfo.description">{{ lessonInfo.description }}</text>
      <view class="lesson-meta">
        <text class="meta-item">第{{ lessonInfo.order }}课</text>
        <text class="meta-item" v-if="lessonInfo.duration">{{ formatDuration(lessonInfo.duration) }}</text>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      videoId: 'secureVideo',
      lessonId: 0,
      userId: '',
      videoUrl: '',
      accessToken: '',
      
      // 视频状态
      isLoading: true,
      isPlaying: false,
      isBlocked: false,
      currentTime: 0,
      duration: 0,
      
      // 界面状态
      showControls: true,
      controlsTimer: null,
      
      // 安全相关
      watermarkText: '',
      watermarkPosition: 'top-right',
      watermarkTimer: null,
      heartbeatTimer: null,
      
      // 课程信息
      lessonInfo: {}
    }
  },
  
  computed: {
    progressPercent() {
      return this.duration > 0 ? (this.currentTime / this.duration) * 100 : 0
    }
  },
  
  onLoad(options) {
    this.lessonId = parseInt(options.lessonId)
    this.userId = options.userId || 'user_123'
    this.initializePlayer()
  },
  
  onUnload() {
    this.cleanup()
  },
  
  onHide() {
    // 页面隐藏时暂停视频
    this.pauseVideo()
    this.blockVideo('检测到页面切换')
  },
  
  onShow() {
    // 页面显示时检查状态
    if (this.isBlocked) {
      this.resumeVideo()
    }
  },
  
  methods: {
    // 初始化播放器
    async initializePlayer() {
      try {
        const response = await uni.request({
          url: `/api/video/lessons/${this.lessonId}/play-url`,
          method: 'GET',
          data: {
            user_id: this.userId
          }
        })
        
        if (response.data) {
          const data = response.data
          this.videoUrl = data.video_url
          this.accessToken = data.access_token
          this.watermarkText = data.watermark_config?.content || ''
          this.lessonInfo = data.lesson_info || {}
          
          this.setupWatermark(data.watermark_config)
          this.startHeartbeat(data.security_config)
        }
      } catch (error) {
        console.error('初始化播放器失败:', error)
        uni.showToast({ title: '视频加载失败', icon: 'error' })
      } finally {
        this.isLoading = false
      }
    },
    
    // 设置水印
    setupWatermark(config) {
      if (!config || !config.interval) return
      
      this.watermarkTimer = setInterval(() => {
        // 随机更换水印位置
        const positions = ['top-left', 'top-right', 'bottom-left', 'bottom-right']
        this.watermarkPosition = positions[Math.floor(Math.random() * positions.length)]
      }, config.interval * 1000)
    },
    
    // 开始心跳检测
    startHeartbeat(config) {
      if (!config?.heartbeat_interval) return
      
      this.heartbeatTimer = setInterval(async () => {
        try {
          const response = await uni.request({
            url: `/api/video/lessons/${this.lessonId}/heartbeat`,
            method: 'POST',
            data: {
              user_id: this.userId,
              current_time: Math.floor(this.currentTime),
              token: this.accessToken
            }
          })
          
          if (!response.data?.continue_play) {
            this.blockVideo('会话已过期')
          }
        } catch (error) {
          console.error('心跳检测失败:', error)
        }
      }, config.heartbeat_interval * 1000)
    },
    
    // 视频控制
    togglePlay() {
      if (this.isBlocked) return
      
      if (this.isPlaying) {
        this.pauseVideo()
      } else {
        this.playVideo()
      }
    },
    
    playVideo() {
      if (this.isBlocked) return
      
      const videoContext = uni.createVideoContext(this.videoId, this)
      videoContext.play()
      this.isPlaying = true
    },
    
    pauseVideo() {
      const videoContext = uni.createVideoContext(this.videoId, this)
      videoContext.pause()
      this.isPlaying = false
    },
    
    seekTo(event) {
      if (this.isBlocked || !this.duration) return
      
      const rect = event.detail || event.target.getBoundingClientRect()
      // 这里需要根据实际点击位置计算进度
      // 简化处理，实际项目中需要更精确的计算
      const percent = 0.5 // 示例值
      const newTime = percent * this.duration
      
      const videoContext = uni.createVideoContext(this.videoId, this)
      videoContext.seek(newTime)
      this.currentTime = newTime
    },
    
    // 控制栏显示/隐藏
    toggleControls() {
      this.showControls = !this.showControls
      
      if (this.showControls) {
        // 3秒后自动隐藏控制栏
        clearTimeout(this.controlsTimer)
        this.controlsTimer = setTimeout(() => {
          this.showControls = false
        }, 3000)
      }
    },
    
    // 阻止播放
    blockVideo(reason) {
      this.isBlocked = true
      this.pauseVideo()
      
      uni.showToast({
        title: `视频已暂停: ${reason}`,
        icon: 'error',
        duration: 3000
      })
      
      // 记录违规行为
      this.recordViolation(reason)
    },
    
    // 恢复播放
    resumeVideo() {
      this.isBlocked = false
    },
    
    // 记录违规
    async recordViolation(reason) {
      try {
        await uni.request({
          url: `/api/video/lessons/${this.lessonId}/violation`,
          method: 'POST',
          data: {
            user_id: this.userId,
            reason: reason,
            timestamp: Date.now()
          }
        })
      } catch (error) {
        console.error('记录违规失败:', error)
      }
    },
    
    // 视频事件处理
    onVideoLoaded(event) {
      this.duration = event.detail.duration
      this.isLoading = false
    },
    
    onTimeUpdate(event) {
      this.currentTime = event.detail.currentTime
    },
    
    onVideoEnded() {
      this.isPlaying = false
      this.markLessonCompleted()
    },
    
    onVideoError(event) {
      console.error('视频播放错误:', event)
      uni.showToast({ title: '播放失败', icon: 'error' })
    },
    
    // 标记完成
    async markLessonCompleted() {
      try {
        await uni.request({
          url: `/api/video/lessons/${this.lessonId}/complete`,
          method: 'POST',
          data: {
            user_id: this.userId,
            token: this.accessToken
          }
        })
        
        uni.showToast({ title: '课程已完成', icon: 'success' })
      } catch (error) {
        console.error('标记完成失败:', error)
      }
    },
    
    // 工具方法
    formatTime(seconds) {
      const mins = Math.floor(seconds / 60)
      const secs = Math.floor(seconds % 60)
      return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
    },
    
    formatDuration(seconds) {
      const minutes = Math.floor(seconds / 60)
      return `${minutes}分${seconds % 60}秒`
    },
    
    // 返回
    goBack() {
      uni.navigateBack()
    },
    
    // 清理
    cleanup() {
      if (this.watermarkTimer) clearInterval(this.watermarkTimer)
      if (this.heartbeatTimer) clearInterval(this.heartbeatTimer)
      if (this.controlsTimer) clearTimeout(this.controlsTimer)
    }
  }
}
</script>

<style>
.video-player-page {
  height: 100vh;
  background: #000;
  position: relative;
}

.navbar {
  display: flex;
  align-items: center;
  height: 44px;
  padding: 0 15px;
  background: rgba(0, 0, 0, 0.8);
  position: relative;
  z-index: 100;
}

.nav-left {
  width: 40px;
}

.back-icon {
  color: white;
  font-size: 20px;
}

.nav-title {
  flex: 1;
  text-align: center;
  color: white;
  font-size: 16px;
  font-weight: bold;
}

.nav-right {
  width: 40px;
}

.video-container {
  position: relative;
  height: 250px;
  background: #000;
}

.video-element {
  width: 100%;
  height: 100%;
}

.watermark {
  position: absolute;
  color: rgba(255, 255, 255, 0.6);
  font-size: 12px;
  padding: 4px 8px;
  background: rgba(0, 0, 0, 0.3);
  border-radius: 4px;
  z-index: 10;
  pointer-events: none;
}

.watermark.top-left {
  top: 10px;
  left: 10px;
}

.watermark.top-right {
  top: 10px;
  right: 10px;
}

.watermark.bottom-left {
  bottom: 60px;
  left: 10px;
}

.watermark.bottom-right {
  bottom: 60px;
  right: 10px;
}

.video-controls {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.7));
  padding: 10px 15px;
  z-index: 20;
}

.controls-row {
  display: flex;
  align-items: center;
}

.play-btn {
  background: none;
  border: none;
  color: white;
  font-size: 20px;
  margin-right: 10px;
}

.progress-container {
  flex: 1;
  margin-right: 10px;
}

.progress-bar {
  height: 3px;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 1.5px;
  position: relative;
}

.progress-fill {
  height: 100%;
  background: #409eff;
  border-radius: 1.5px;
}

.time-text {
  color: white;
  font-size: 12px;
  min-width: 80px;
}

.tap-area {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 50px;
  z-index: 15;
}

.blocked-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 50;
}

.blocked-content {
  text-align: center;
  color: white;
}

.blocked-icon {
  font-size: 48px;
  display: block;
  margin-bottom: 15px;
}

.blocked-title {
  font-size: 18px;
  font-weight: bold;
  display: block;
  margin-bottom: 10px;
}

.blocked-desc {
  font-size: 14px;
  color: #ccc;
  display: block;
  margin-bottom: 20px;
}

.resume-btn {
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px 20px;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 30;
}

.loading-text {
  color: white;
  font-size: 16px;
}

.lesson-info {
  padding: 20px;
  background: white;
}

.lesson-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 10px;
}

.lesson-desc {
  font-size: 14px;
  color: #666;
  line-height: 1.5;
  display: block;
  margin-bottom: 15px;
}

.lesson-meta {
  display: flex;
  gap: 15px;
}

.meta-item {
  font-size: 12px;
  color: #999;
}
</style>