<template>
  <div class="my">
    <PageContainer>
      <div class="my-content">
        <h2>我的</h2>
        <p>个人中心，管理您的学习进度和账户信息</p>
        
        <el-row :gutter="20" class="my-sections">
          <el-col :span="8">
            <el-card class="section-card" @click="goToSection('courses')">
              <div class="card-icon">
                <el-icon size="40"><Reading /></el-icon>
              </div>
              <h3>我的课程</h3>
              <p>查看学习进度和已购课程</p>
            </el-card>
          </el-col>
          
          <el-col :span="8">
            <el-card class="section-card" @click="goToSection('consultations')">
              <div class="card-icon">
                <el-icon size="40"><ChatDotRound /></el-icon>
              </div>
              <h3>我的咨询</h3>
              <p>查看咨询历史和专家回复</p>
            </el-card>
          </el-col>
          
          <el-col :span="8">
            <el-card class="section-card" @click="goToSection('profile')">
              <div class="card-icon">
                <el-icon size="40"><User /></el-icon>
              </div>
              <h3>个人资料</h3>
              <p>管理个人信息和账户设置</p>
            </el-card>
          </el-col>
        </el-row>
        
        <el-row :gutter="20" class="my-sections">
          <el-col :span="8">
            <el-card class="section-card" @click="goToSection('orders')">
              <div class="card-icon">
                <el-icon size="40"><ShoppingBag /></el-icon>
              </div>
              <h3>我的订单</h3>
              <p>查看购买记录和订单状态</p>
            </el-card>
          </el-col>
          
          <el-col :span="8">
            <el-card class="section-card" @click="goToSection('favorites')">
              <div class="card-icon">
                <el-icon size="40"><Star /></el-icon>
              </div>
              <h3>我的收藏</h3>
              <p>管理收藏的课程和专家</p>
            </el-card>
          </el-col>
          
          <el-col :span="8">
            <el-card class="section-card" @click="goToSection('settings')">
              <div class="card-icon">
                <el-icon size="40"><Setting /></el-icon>
              </div>
              <h3>设置</h3>
              <p>账户安全和通知设置</p>
            </el-card>
          </el-col>
        </el-row>
      </div>
    </PageContainer>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  Reading, 
  ChatDotRound, 
  User, 
  ShoppingBag, 
  Star, 
  Setting 
} from '@element-plus/icons-vue'
import PageContainer from '../components/PageContainer.vue'

const router = useRouter()

// 跳转到相应功能页面
const goToSection = (section: string) => {
  switch (section) {
    case 'courses':
      ElMessage.info('我的课程功能开发中...')
      break
    case 'consultations':
      ElMessage.info('我的咨询功能开发中...')
      break
    case 'profile':
      ElMessage.info('个人资料功能开发中...')
      break
    case 'orders':
      router.push('/my/orders')
      break
    case 'favorites':
      ElMessage.info('我的收藏功能开发中...')
      break
    case 'settings':
      ElMessage.info('设置功能开发中...')
      break
    default:
      console.log('Unknown section:', section)
  }
}
</script>

<style scoped>
.my {
  min-height: 100vh;
  background-color: #f5f5f5;
}

.my-content {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.my-content h2 {
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.my-content p {
  text-align: center;
  color: #666;
  margin-bottom: 40px;
}

.my-sections {
  margin-bottom: 30px;
}

.section-card {
  text-align: center;
  cursor: pointer;
  transition: all 0.3s ease;
  height: 200px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.section-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px 0 rgba(0, 0, 0, 0.15);
}

.card-icon {
  margin-bottom: 15px;
  color: #409eff;
}

.section-card h3 {
  margin: 10px 0;
  color: #333;
  font-size: 18px;
}

.section-card p {
  color: #666;
  font-size: 14px;
  margin: 0;
}
</style>