<template>
  <view class="container">
    <view class="header">
      <text class="title">课程中心</text>
      <text class="subtitle">系统性中医养生课程，提升您的健康素养</text>
    </view>
    
    <view class="tabs">
      <view class="tab" :class="{ active: activeTab === 'popular' }" @click="switchTab('popular')">
        热门课程
      </view>
      <view class="tab" :class="{ active: activeTab === 'latest' }" @click="switchTab('latest')">
        最新课程
      </view>
      <view class="tab" :class="{ active: activeTab === 'free' }" @click="switchTab('free')">
        免费课程
      </view>
    </view>
    
    <view class="courses-list">
      <view class="course-card" v-for="course in currentCourses" :key="course.id" @click="enrollCourse(course.id)">
        <image :src="course.image" class="course-image"></image>
        <view class="course-info">
          <text class="course-title">{{ course.title }}</text>
          <text class="course-description">{{ course.description }}</text>
          <view class="course-meta">
            <text class="course-duration">{{ course.duration }}</text>
            <text class="course-price" :class="{ free: course.price === 0 }">
              {{ course.price === 0 ? '免费' : `¥${course.price}` }}
            </text>
          </view>
        </view>
      </view>
    </view>
  </view>
</template>

<script>
export default {
  data() {
    return {
      activeTab: 'popular',
      courses: {
        popular: [
          {
            id: 1,
            title: '中医基础理论',
            description: '学习中医的基本概念和理论体系',
            duration: '10课时',
            price: 99,
            image: 'https://via.placeholder.com/300x200?text=中医基础理论'
          },
          {
            id: 2,
            title: '四季养生法',
            description: '根据四季变化调整养生方法',
            duration: '8课时',
            price: 79,
            image: 'https://via.placeholder.com/300x200?text=四季养生法'
          }
        ],
        latest: [
          {
            id: 3,
            title: '经络按摩',
            description: '学习经络穴位按摩保健方法',
            duration: '6课时',
            price: 59,
            image: 'https://via.placeholder.com/300x200?text=经络按摩'
          }
        ],
        free: [
          {
            id: 4,
            title: '中医养生入门',
            description: '中医养生的基本概念和方法',
            duration: '5课时',
            price: 0,
            image: 'https://via.placeholder.com/300x200?text=中医养生入门'
          }
        ]
      }
    }
  },
  computed: {
    currentCourses() {
      return this.courses[this.activeTab] || []
    }
  },
  methods: {
    switchTab(tab) {
      this.activeTab = tab
    },
    enrollCourse(courseId) {
      console.log('查看课程:', courseId)
      // 跳转到课程详情页面，这里临时跳转到视频播放页面
      uni.navigateTo({
        url: `/pages/video-player/video-player?lessonId=1&userId=user_123`
      })
    }
  }
}
</script>

<style>
.container {
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 30px;
}

.title {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 10px;
}

.subtitle {
  font-size: 16px;
  color: #666;
  display: block;
}

.tabs {
  display: flex;
  border-bottom: 1px solid #eee;
  margin-bottom: 20px;
}

.tab {
  flex: 1;
  text-align: center;
  padding: 15px 0;
  color: #666;
}

.tab.active {
  color: #409eff;
  border-bottom: 2px solid #409eff;
}

.course-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  margin-bottom: 20px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.course-image {
  width: 100%;
  height: 150px;
}

.course-info {
  padding: 15px;
}

.course-title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 8px;
}

.course-description {
  font-size: 14px;
  color: #666;
  display: block;
  margin-bottom: 15px;
  height: 40px;
  overflow: hidden;
}

.course-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.course-duration {
  font-size: 12px;
  color: #999;
}

.course-price {
  font-size: 16px;
  color: #f56c6c;
  font-weight: bold;
}

.course-price.free {
  color: #409eff;
}
</style>