<template>
  <div class="data-export">
    <div class="page-header">
      <div class="header-content">
        <h2>📊 数据导出</h2>
        <p>导出平台各类数据报表和统计信息</p>
      </div>
    </div>

    <!-- 导出卡片 -->
    <div class="export-cards">
      <div class="export-card">
        <div class="export-icon">👥</div>
        <div class="export-info">
          <h3>用户数据</h3>
          <p>导出用户注册信息、角色权限等数据</p>
          <div class="export-buttons">
            <el-button size="small" @click="exportData('users', 'csv')">CSV格式</el-button>
            <el-button size="small" @click="exportData('users', 'json')">JSON格式</el-button>
          </div>
        </div>
      </div>

      <div class="export-card">
        <div class="export-icon">📚</div>
        <div class="export-info">
          <h3>课程数据</h3>
          <p>导出课程信息、分类、价格等数据</p>
          <div class="export-buttons">
            <el-button size="small" @click="exportData('courses', 'csv')">CSV格式</el-button>
            <el-button size="small" @click="exportData('courses', 'json')">JSON格式</el-button>
          </div>
        </div>
      </div>

      <div class="export-card">
        <div class="export-icon">📈</div>
        <div class="export-info">
          <h3>学习数据</h3>
          <p>导出学习进度、完成情况等数据</p>
          <div class="export-buttons">
            <el-button size="small" @click="exportData('enrollments', 'csv')">CSV格式</el-button>
            <el-button size="small" @click="exportData('enrollments', 'json')">JSON格式</el-button>
          </div>
        </div>
      </div>

      <div class="export-card">
        <div class="export-icon">👨‍⚕️</div>
        <div class="export-info">
          <h3>专家数据</h3>
          <p>导出专家信息、认证状态等数据</p>
          <div class="export-buttons">
            <el-button size="small" @click="exportData('experts', 'csv')">CSV格式</el-button>
            <el-button size="small" @click="exportData('experts', 'json')">JSON格式</el-button>
          </div>
        </div>
      </div>

      <div class="export-card">
        <div class="export-icon">📋</div>
        <div class="export-info">
          <h3>订单数据</h3>
          <p>导出订单详情、支付信息等数据</p>
          <div class="export-buttons">
            <el-button size="small" @click="exportData('orders', 'csv')">CSV格式</el-button>
            <el-button size="small" @click="exportData('orders', 'json')">JSON格式</el-button>
          </div>
        </div>
      </div>

      <div class="export-card">
        <div class="export-icon">💬</div>
        <div class="export-info">
          <h3>咨询数据</h3>
          <p>导出咨询记录、回复内容等数据</p>
          <div class="export-buttons">
            <el-button size="small" @click="exportData('consultations', 'csv')">CSV格式</el-button>
            <el-button size="small" @click="exportData('consultations', 'json')">JSON格式</el-button>
          </div>
        </div>
      </div>
    </div>

    <!-- 导出历史 -->
    <div class="export-history">
      <div class="history-header">
        <h3>📝 导出历史</h3>
        <el-button size="small" @click="loadHistory">刷新</el-button>
      </div>
      <div class="history-list">
        <div class="history-item" v-for="(item, index) in exportHistory" :key="index">
          <div class="history-info">
            <div class="history-title">{{ item.title }}</div>
            <div class="history-time">{{ item.time }}</div>
          </div>
          <div class="history-actions">
            <el-tag :type="item.status === 'success' ? 'success' : 'danger'" size="small">
              {{ item.status === 'success' ? '成功' : '失败' }}
            </el-tag>
            <el-button v-if="item.status === 'success'" size="small" text>下载</el-button>
          </div>
        </div>
        
        <div v-if="exportHistory.length === 0" class="no-history">
          <el-empty description="暂无导出记录" :image-size="60" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'

const exportHistory = ref([
  {
    title: '用户数据导出 (CSV)',
    time: '2024-01-15 14:30:25',
    status: 'success'
  },
  {
    title: '课程数据导出 (JSON)',
    time: '2024-01-15 10:15:42',
    status: 'success'
  },
  {
    title: '订单数据导出 (CSV)',
    time: '2024-01-14 16:45:18',
    status: 'failed'
  }
])

const exportData = async (type: string, format: string) => {
  try {
    ElMessage.loading('正在导出数据...')
    
    // 模拟导出API调用
    const response = await fetch(`/api/admin/export/${type}?format=${format}`, {
      headers: { 'Authorization': `Bearer ${localStorage.getItem('admin_token')}` }
    })
    
    if (response.ok) {
      // 这里实现实际的文件下载逻辑
      ElMessage.success(`${type}数据导出成功`)
    } else {
      throw new Error('导出失败')
    }
  } catch (error) {
    ElMessage.error('导出失败，请重试')
  }
}

const loadHistory = () => {
  ElMessage.info('导出历史已刷新')
}

onMounted(() => {
  // 组件加载时的初始化逻辑
})
</script>

<style scoped>
.data-export {
  padding: 0;
}

.page-header {
  margin-bottom: 24px;
  padding: 24px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.header-content h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  color: #333;
}

.header-content p {
  margin: 0;
  color: #666;
  font-size: 14px;
}

.export-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.export-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  display: flex;
  gap: 16px;
  transition: all 0.3s ease;
}

.export-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.export-icon {
  width: 50px;
  height: 50px;
  border-radius: 8px;
  background: #f0f9ff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  flex-shrink: 0;
}

.export-info {
  flex: 1;
}

.export-info h3 {
  margin: 0 0 8px 0;
  font-size: 16px;
  color: #333;
  font-weight: 600;
}

.export-info p {
  margin: 0 0 16px 0;
  font-size: 14px;
  color: #666;
  line-height: 1.4;
}

.export-buttons {
  display: flex;
  gap: 8px;
}

.export-history {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.history-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.history-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
  font-weight: 600;
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 0;
  border-bottom: 1px solid #f0f0f0;
}

.history-item:last-child {
  border-bottom: none;
}

.history-info {
  flex: 1;
}

.history-title {
  font-size: 14px;
  color: #333;
  font-weight: 500;
  margin-bottom: 4px;
}

.history-time {
  font-size: 12px;
  color: #999;
}

.history-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.no-history {
  text-align: center;
  padding: 40px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .export-cards {
    grid-template-columns: 1fr;
  }
  
  .export-card {
    flex-direction: column;
    text-align: center;
  }
  
  .history-item {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .history-actions {
    align-self: flex-end;
  }
}
</style>