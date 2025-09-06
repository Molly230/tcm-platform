<template>
  <div class="consultation">
    <PageContainer>
      
      <div class="consultation-content">
        <h2>健康咨询</h2>
        <p>请选择您需要的咨询服务类型：</p>
        
        <el-row :gutter="20" class="service-options">
          <el-col :span="12">
            <el-card class="service-card" @click="selectService('ai')">
              <h3>AI智能问诊</h3>
              <p>基于中医理论的智能问诊系统</p>
              <p class="price">¥9.9/次</p>
              <el-button type="primary">立即咨询</el-button>
            </el-card>
          </el-col>
          <el-col :span="12">
            <el-card class="service-card" @click="selectService('expert')">
              <h3>专家咨询</h3>
              <p>与资深中医师一对一交流</p>
              <p class="price">¥50-500/次</p>
              <el-button type="primary">选择专家</el-button>
            </el-card>
          </el-col>
        </el-row>
        
        <!-- AI智能问诊 -->
        <div class="ai-consultation" v-if="selectedService === 'ai'">
          <h3>AI智能问诊</h3>
          <el-form :model="aiForm" label-width="120px" class="ai-form">
            <el-form-item label="主要症状">
              <el-input v-model="aiForm.symptoms" type="textarea" placeholder="请描述您的主要症状"></el-input>
            </el-form-item>
            <el-form-item label="持续时间">
              <el-input v-model="aiForm.duration" placeholder="症状持续多长时间了？"></el-input>
            </el-form-item>
            <el-form-item label="既往病史">
              <el-input v-model="aiForm.medicalHistory" type="textarea" placeholder="请描述您的既往病史"></el-input>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="submitAIConsultation">提交问诊</el-button>
            </el-form-item>
          </el-form>
        </div>

        <!-- 专家咨询 -->
        <div class="expert-consultation" v-if="selectedService === 'expert'">
          <h3>专家咨询</h3>
          <p>与资深中医师一对一交流，获得专业健康建议</p>
          
          <!-- 专家筛选 -->
          <div class="experts-filter">
            <el-select v-model="selectedCategory" placeholder="选择专家类别">
              <el-option label="全部" value=""></el-option>
              <el-option label="中医内科" value="internal"></el-option>
              <el-option label="中医妇科" value="gynecology"></el-option>
              <el-option label="中医儿科" value="pediatrics"></el-option>
              <el-option label="针灸推拿" value="acupuncture"></el-option>
              <el-option label="中医养生" value="health"></el-option>
            </el-select>
            
            <el-input v-model="searchKeyword" placeholder="搜索专家姓名" style="width: 300px; margin-left: 20px;">
              <template #append>
                <el-button icon="Search" @click="searchExperts"></el-button>
              </template>
            </el-input>
          </div>
          
          <!-- 专家列表 -->
          <el-row :gutter="20" class="experts-list">
            <el-col :span="8" v-for="expert in filteredExperts" :key="expert.id">
              <el-card class="expert-card">
                <div class="expert-header">
                  <img :src="expert.avatar" :alt="expert.name" class="expert-avatar">
                  <div class="expert-info">
                    <h3>{{ expert.name }}</h3>
                    <p class="expert-title">{{ expert.title }}</p>
                    <p class="expert-category">{{ expert.category }}</p>
                  </div>
                </div>
                <div class="expert-details">
                  <p class="expert-description">{{ expert.description }}</p>
                  <div class="expert-stats">
                    <span>好评率: {{ expert.rating }}%</span>
                    <span>咨询次数: {{ expert.consultations }}</span>
                  </div>
                  <div class="expert-prices">
                    <span class="price">文字咨询: ¥{{ expert.textPrice }}/次</span>
                    <span class="price">语音咨询: ¥{{ expert.voicePrice }}/次</span>
                    <span class="price">视频咨询: ¥{{ expert.videoPrice }}/次</span>
                  </div>
                  <el-button type="primary" @click="bookConsultation(expert.id)">预约咨询</el-button>
                </div>
              </el-card>
            </el-col>
          </el-row>
        </div>
      </div>
    </PageContainer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import PageContainer from '../components/PageContainer.vue'
import { PLACEHOLDER_IMAGES } from '@/utils/placeholder'

// 定义响应式数据
const selectedService = ref('')
const selectedCategory = ref('')
const searchKeyword = ref('')

const aiForm = ref({
  symptoms: '',
  duration: '',
  medicalHistory: ''
})

// 专家数据
const experts = ref([
  {
    id: 1,
    name: '张医师',
    title: '主任医师',
    category: '中医内科',
    avatar: PLACEHOLDER_IMAGES.expert,
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
    avatar: PLACEHOLDER_IMAGES.expert,
    description: '专注于妇科疾病治疗15年，对月经不调、不孕不育等有丰富经验。',
    rating: 96,
    consultations: 800,
    textPrice: 60,
    voicePrice: 120,
    videoPrice: 250
  },
  {
    id: 3,
    name: '王医师',
    title: '主治医师',
    category: '针灸推拿',
    avatar: PLACEHOLDER_IMAGES.expert,
    description: '针灸推拿科专家，擅长治疗颈椎病、腰椎间盘突出等骨科疾病。',
    rating: 97,
    consultations: 1500,
    textPrice: 40,
    voicePrice: 80,
    videoPrice: 150
  },
  {
    id: 4,
    name: '陈医师',
    title: '主任医师',
    category: '中医养生',
    avatar: PLACEHOLDER_IMAGES.expert,
    description: '中医养生专家，专注于亚健康调理和慢性病预防。',
    rating: 99,
    consultations: 2000,
    textPrice: 70,
    voicePrice: 150,
    videoPrice: 300
  }
])

// 过滤专家
const filteredExperts = computed(() => {
  let result = experts.value
  
  // 按类别过滤
  if (selectedCategory.value) {
    result = result.filter(expert => expert.category.includes(selectedCategory.value))
  }
  
  // 按关键字搜索
  if (searchKeyword.value) {
    result = result.filter(expert => 
      expert.name.includes(searchKeyword.value) || 
      expert.title.includes(searchKeyword.value)
    )
  }
  
  return result
})

// 选择服务类型
const selectService = (service: string) => {
  selectedService.value = service
}

// 提交AI问诊
const submitAIConsultation = () => {
  console.log('提交AI问诊:', aiForm.value)
  // 这里可以调用后端API
}

// 搜索专家
const searchExperts = () => {
  // 搜索逻辑已经在computed中实现
  console.log('搜索专家:', searchKeyword.value)
}

// 预约咨询
const bookConsultation = (expertId: number) => {
  console.log('预约咨询:', expertId)
  // 这里可以调用后端API
}

</script>

<style scoped>
.consultation {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.consultation-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.consultation-content h2 {
  color: #333;
  margin-bottom: 20px;
}

.service-options {
  margin: 30px 0;
}

.service-card {
  cursor: pointer;
  text-align: center;
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  transition: all 0.3s;
}

.service-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 4px 20px 0 rgba(0, 0, 0, 0.1);
}

.service-card h3 {
  color: #409eff;
  margin-bottom: 10px;
}

.price {
  color: #f56c6c;
  font-weight: bold;
  margin: 15px 0;
}

.ai-consultation {
  margin-top: 30px;
  padding-top: 30px;
  border-top: 1px solid #eee;
}

.ai-form {
  max-width: 600px;
  margin: 20px auto;
}

/* 专家咨询样式 */
.expert-consultation {
  margin-top: 30px;
  padding-top: 30px;
  border-top: 1px solid #eee;
}

.experts-filter {
  margin-bottom: 30px;
  display: flex;
  align-items: center;
}

.expert-card {
  margin-bottom: 20px;
}

.expert-header {
  display: flex;
  align-items: center;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.expert-avatar {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  margin-right: 15px;
}

.expert-info h3 {
  margin: 0 0 5px 0;
  color: #333;
}

.expert-title {
  color: #666;
  margin: 5px 0;
}

.expert-category {
  color: #409eff;
  font-weight: bold;
}

.expert-description {
  color: #666;
  margin: 15px 0;
  height: 60px;
  overflow: hidden;
}

.expert-stats {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  color: #999;
}

.expert-prices {
  margin-bottom: 15px;
}

.expert-prices .price {
  display: block;
  color: #f56c6c;
  font-weight: bold;
  margin-bottom: 5px;
}
</style>