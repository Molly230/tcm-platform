<template>
  <view class="container">
    <view class="header">
      <text class="title">专家咨询</text>
      <text class="subtitle">与资深中医师一对一交流</text>
    </view>
    
    <view class="experts-filter">
      <picker mode="selector" :range="categories" @change="onCategoryChange">
        <view class="picker">
          选择专家类别: {{ selectedCategory }}
        </view>
      </picker>
      
      <input v-model="searchKeyword" placeholder="搜索专家姓名" class="search-input" />
      <button class="search-btn" @click="searchExperts">搜索</button>
    </view>
    
    <view class="experts-list">
      <view class="expert-card" v-for="expert in filteredExperts" :key="expert.id" @click="bookConsultation(expert.id)">
        <view class="expert-header">
          <image :src="expert.avatar" class="expert-avatar"></image>
          <view class="expert-info">
            <text class="expert-name">{{ expert.name }}</text>
            <text class="expert-title">{{ expert.title }}</text>
            <text class="expert-category">{{ expert.category }}</text>
          </view>
        </view>
        
        <view class="expert-details">
          <text class="expert-description">{{ expert.description }}</text>
          
          <view class="expert-stats">
            <text>好评率: {{ expert.rating }}%</text>
            <text>咨询次数: {{ expert.consultations }}</text>
          </view>
          
          <view class="expert-prices">
            <text class="price">文字咨询: ¥{{ expert.textPrice }}/次</text>
            <text class="price">语音咨询: ¥{{ expert.voicePrice }}/次</text>
            <text class="price">视频咨询: ¥{{ expert.videoPrice }}/次</text>
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
      categories: ['全部', '中医内科', '中医妇科', '中医儿科', '针灸推拿', '中医养生'],
      selectedCategory: '全部',
      searchKeyword: '',
      experts: [
        {
          id: 1,
          name: '张医师',
          title: '主任医师',
          category: '中医内科',
          avatar: 'https://via.placeholder.com/100x100?text=张医师',
          description: '从事中医内科临床工作20年，擅长治疗消化系统疾病和呼吸系统疾病。',
          rating: 98,
          consultations: 1200,
          textPrice: 50,
          voicePrice: 100,
          videoPrice: 200
        },
        {
          id: 2,
          name: '李医师',
          title: '副主任医师',
          category: '中医妇科',
          avatar: 'https://via.placeholder.com/100x100?text=李医师',
          description: '专注于妇科疾病治疗15年，对月经不调、不孕不育等有丰富经验。',
          rating: 96,
          consultations: 800,
          textPrice: 60,
          voicePrice: 120,
          videoPrice: 250
        }
      ]
    }
  },
  computed: {
    filteredExperts() {
      let result = this.experts
      
      // 按类别过滤
      if (this.selectedCategory !== '全部') {
        result = result.filter(expert => expert.category.includes(this.selectedCategory))
      }
      
      // 按关键字搜索
      if (this.searchKeyword) {
        result = result.filter(expert => 
          expert.name.includes(this.searchKeyword) || 
          expert.title.includes(this.searchKeyword)
        )
      }
      
      return result
    }
  },
  methods: {
    onCategoryChange(e) {
      this.selectedCategory = this.categories[e.detail.value]
    },
    searchExperts() {
      // 搜索逻辑已经在computed中实现
      console.log('搜索专家:', this.searchKeyword)
    },
    bookConsultation(expertId) {
      console.log('预约咨询:', expertId)
      // 这里可以调用后端API
      uni.showToast({
        title: '预约成功',
        icon: 'success'
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

.experts-filter {
  margin-bottom: 20px;
}

.picker {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  margin-bottom: 10px;
}

.search-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-sizing: border-box;
  margin-bottom: 10px;
}

.search-btn {
  background: #409eff;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 10px;
  width: 100%;
}

.expert-card {
  background: #fff;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.expert-header {
  display: flex;
  align-items: center;
  padding-bottom: 10px;
  border-bottom: 1px solid #eee;
  margin-bottom: 10px;
}

.expert-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  margin-right: 15px;
}

.expert-info {
  flex: 1;
}

.expert-name {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  display: block;
  margin-bottom: 3px;
}

.expert-title {
  font-size: 14px;
  color: #666;
  display: block;
  margin-bottom: 3px;
}

.expert-category {
  font-size: 14px;
  color: #409eff;
  font-weight: bold;
  display: block;
}

.expert-description {
  font-size: 14px;
  color: #666;
  margin-bottom: 10px;
  display: block;
}

.expert-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  color: #999;
  font-size: 12px;
}

.expert-prices {
  margin-bottom: 10px;
}

.price {
  display: block;
  color: #f56c6c;
  font-weight: bold;
  font-size: 14px;
  margin-bottom: 3px;
}
</style>