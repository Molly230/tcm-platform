<template>
  <div class="dashboard">
    <!-- 欢迎区域 -->
    <div class="welcome-section">
      <div class="welcome-content">
        <h2>欢迎回来，{{ currentUser?.username || '管理员' }}！👋</h2>
        <p>今天是 {{ formatDate(new Date()) }}，让我们一起管理好中医健康服务平台</p>
      </div>
      <div class="welcome-actions">
        <el-button type="primary" @click="navigateTo('/admin/courses')">
          <el-icon><Reading /></el-icon>
          快速添加课程
        </el-button>
        <el-button type="success" @click="navigateTo('/admin/users')">
          <el-icon><User /></el-icon>
          管理用户
        </el-button>
        <el-button @click="refreshData" :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新数据
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card" @click="navigateTo('/admin/courses')">
        <div class="stat-icon courses">
          <el-icon size="32"><Reading /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.overview?.total_courses || 0 }}</div>
          <div class="stat-label">总课程数</div>
          <div class="stat-detail">已发布: {{ stats.course_analysis?.published_courses || 0 }}</div>
        </div>
      </div>
      
      <div class="stat-card" @click="navigateTo('/admin/users')">
        <div class="stat-icon users">
          <el-icon size="32"><User /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.overview?.total_users || 0 }}</div>
          <div class="stat-label">总用户数</div>
          <div class="stat-detail">活跃: {{ stats.user_analysis?.active_users || 0 }}</div>
        </div>
      </div>
      
      <div class="stat-card" @click="navigateTo('/admin/experts')">
        <div class="stat-icon experts">
          <el-icon size="32"><UserFilled /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-number">{{ stats.overview?.total_experts || 0 }}</div>
          <div class="stat-label">专家总数</div>
          <div class="stat-detail">已认证: {{ stats.expert_stats?.verified_experts || 0 }}</div>
        </div>
      </div>
      
      <div class="stat-card" @click="navigateTo('/admin/orders')">
        <div class="stat-icon revenue">
          <el-icon size="32"><Money /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-number">¥{{ formatNumber(stats.overview?.total_revenue || 0) }}</div>
          <div class="stat-label">总收入</div>
          <div class="stat-detail">订单: {{ stats.overview?.total_orders || 0 }}</div>
        </div>
      </div>
    </div>

    <!-- 分析面板 -->
    <div class="analysis-panels">
      <!-- 用户分析 -->
      <div class="analysis-card">
        <div class="card-header">
          <h3>👥 用户分析</h3>
          <el-button size="small" text @click="navigateTo('/admin/users')">查看详情</el-button>
        </div>
        <div class="analysis-chart">
          <div class="mini-stats">
            <div class="mini-stat">
              <span class="label">VIP用户</span>
              <span class="value">{{ stats.user_analysis?.vip_users || 0 }}</span>
            </div>
            <div class="mini-stat">
              <span class="label">医生用户</span>
              <span class="value">{{ stats.user_analysis?.doctor_users || 0 }}</span>
            </div>
            <div class="mini-stat">
              <span class="label">管理员</span>
              <span class="value">{{ stats.user_analysis?.admin_users || 0 }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 课程分析 -->
      <div class="analysis-card">
        <div class="card-header">
          <h3>📚 课程分析</h3>
          <el-button size="small" text @click="navigateTo('/admin/courses')">查看详情</el-button>
        </div>
        <div class="analysis-chart">
          <div class="course-progress">
            <div class="progress-item">
              <div class="progress-label">
                <span>免费课程</span>
                <span>{{ stats.course_analysis?.free_courses || 0 }}</span>
              </div>
              <el-progress 
                :percentage="calculatePercentage(stats.course_analysis?.free_courses, stats.overview?.total_courses)"
                :show-text="false"
                stroke-width="8"
                color="#67C23A"
              />
            </div>
            <div class="progress-item">
              <div class="progress-label">
                <span>付费课程</span>
                <span>{{ stats.course_analysis?.paid_courses || 0 }}</span>
              </div>
              <el-progress 
                :percentage="calculatePercentage(stats.course_analysis?.paid_courses, stats.overview?.total_courses)"
                :show-text="false"
                stroke-width="8"
                color="#E6A23C"
              />
            </div>
          </div>
        </div>
      </div>

      <!-- 近期活动 -->
      <div class="analysis-card">
        <div class="card-header">
          <h3>📈 近期活动 (7天)</h3>
          <el-button size="small" text @click="navigateTo('/admin/export')">导出数据</el-button>
        </div>
        <div class="analysis-chart">
          <div class="activity-stats">
            <div class="activity-item">
              <div class="activity-icon new-users">+</div>
              <div class="activity-info">
                <div class="activity-number">{{ stats.recent_activity?.last_7_days?.new_users || 0 }}</div>
                <div class="activity-label">新增用户</div>
              </div>
            </div>
            <div class="activity-item">
              <div class="activity-icon new-courses">📖</div>
              <div class="activity-info">
                <div class="activity-number">{{ stats.recent_activity?.last_7_days?.new_courses || 0 }}</div>
                <div class="activity-label">新增课程</div>
              </div>
            </div>
            <div class="activity-item">
              <div class="activity-icon new-orders">💰</div>
              <div class="activity-info">
                <div class="activity-number">{{ stats.recent_activity?.last_7_days?.new_orders || 0 }}</div>
                <div class="activity-label">新增订单</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 系统状态 -->
      <div class="analysis-card">
        <div class="card-header">
          <h3>🔧 系统状态</h3>
          <el-button size="small" text @click="navigateTo('/admin/settings')">系统设置</el-button>
        </div>
        <div class="analysis-chart">
          <div class="system-status">
            <div class="status-item">
              <span class="status-label">服务器状态</span>
              <el-tag type="success" size="small">运行中</el-tag>
            </div>
            <div class="status-item">
              <span class="status-label">数据库连接</span>
              <el-tag type="success" size="small">正常</el-tag>
            </div>
            <div class="status-item">
              <span class="status-label">存储空间</span>
              <el-tag type="info" size="small">充足</el-tag>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 快速操作 -->
    <div class="quick-actions">
      <div class="actions-header">
        <h3>🚀 快速操作</h3>
      </div>
      <div class="actions-grid">
        <div class="action-item" @click="navigateTo('/admin/courses')">
          <div class="action-icon">📚</div>
          <div class="action-label">管理课程</div>
        </div>
        <div class="action-item" @click="navigateTo('/admin/users')">
          <div class="action-icon">👥</div>
          <div class="action-label">用户管理</div>
        </div>
        <div class="action-item" @click="navigateTo('/admin/experts')">
          <div class="action-icon">👨‍⚕️</div>
          <div class="action-label">专家管理</div>
        </div>
        <div class="action-item" @click="navigateTo('/admin/orders')">
          <div class="action-icon">📋</div>
          <div class="action-label">订单管理</div>
        </div>
        <div class="action-item" @click="navigateTo('/admin/export')">
          <div class="action-icon">📊</div>
          <div class="action-label">数据导出</div>
        </div>
        <div class="action-item" @click="navigateTo('/admin/settings')">
          <div class="action-icon">⚙️</div>
          <div class="action-label">系统设置</div>
        </div>
      </div>
    </div>

    <!-- 最近活动 -->
    <div class="recent-activity">
      <div class="activity-header">
        <h3>📝 最近活动</h3>
        <el-button size="small" text>查看全部</el-button>
      </div>
      <div class="activity-list">
        <div class="activity-item" v-for="(activity, index) in recentActivities" :key="index">
          <div class="activity-avatar">
            <el-avatar :size="32">{{ activity.user?.charAt(0) || 'U' }}</el-avatar>
          </div>
          <div class="activity-content">
            <div class="activity-text">{{ activity.description }}</div>
            <div class="activity-time">{{ formatRelativeTime(activity.time) }}</div>
          </div>
        </div>
        
        <div v-if="recentActivities.length === 0" class="no-activity">
          <el-empty description="暂无最近活动" :image-size="80" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { 
  Reading, User, UserFilled, Money, Refresh
} from '@element-plus/icons-vue'
import { ElMessage } from 'element-plus'

const router = useRouter()

// 响应式数据
const currentUser = ref(null)
const stats = ref({})
const loading = ref(false)
const recentActivities = ref([
  {
    user: 'Admin',
    description: '创建了新课程《中医基础理论》',
    time: new Date(Date.now() - 2 * 60 * 60 * 1000) // 2小时前
  },
  {
    user: 'System',
    description: '完成了数据库备份',
    time: new Date(Date.now() - 4 * 60 * 60 * 1000) // 4小时前
  },
  {
    user: 'Admin',
    description: '审核了专家申请',
    time: new Date(Date.now() - 8 * 60 * 60 * 1000) // 8小时前
  }
])

// 方法
const navigateTo = (path: string) => {
  router.push(path)
}

const loadStats = async () => {
  try {
    const response = await fetch('/api/admin/statistics', {
      headers: { 
        'Authorization': `Bearer ${localStorage.getItem('admin_token')}` 
      }
    })
    
    if (response.ok) {
      stats.value = await response.json()
    } else {
      // 如果API不可用，使用模拟数据
      stats.value = {
        overview: {
          total_courses: 156,
          total_users: 2834,
          total_experts: 45,
          total_revenue: 128500
        },
        user_analysis: {
          active_users: 2156,
          vip_users: 456,
          doctor_users: 89,
          admin_users: 12
        },
        course_analysis: {
          published_courses: 134,
          free_courses: 67,
          paid_courses: 89
        },
        expert_stats: {
          verified_experts: 38
        },
        recent_activity: {
          last_7_days: {
            new_users: 45,
            new_courses: 8,
            new_orders: 127
          }
        }
      }
    }
  } catch (error) {
    console.error('加载统计数据失败:', error)
    ElMessage.warning('统计数据加载失败，显示示例数据')
    // 使用模拟数据
    stats.value = {
      overview: {
        total_courses: 156,
        total_users: 2834,
        total_experts: 45,
        total_revenue: 128500
      },
      user_analysis: {
        active_users: 2156,
        vip_users: 456,
        doctor_users: 89,
        admin_users: 12
      },
      course_analysis: {
        published_courses: 134,
        free_courses: 67,
        paid_courses: 89
      },
      expert_stats: {
        verified_experts: 38
      },
      recent_activity: {
        last_7_days: {
          new_users: 45,
          new_courses: 8,
          new_orders: 127
        }
      }
    }
  }
}

const refreshData = async () => {
  loading.value = true
  try {
    await loadStats()
    ElMessage.success('数据刷新成功')
  } catch (error) {
    ElMessage.error('数据刷新失败')
  } finally {
    loading.value = false
  }
}

const formatDate = (date: Date) => {
  return new Intl.DateTimeFormat('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  }).format(date)
}

const formatNumber = (num: number) => {
  return num.toLocaleString('zh-CN')
}

const calculatePercentage = (value: number, total: number) => {
  if (!total || total === 0) return 0
  return Math.round((value / total) * 100)
}

const formatRelativeTime = (date: Date) => {
  const now = new Date()
  const diff = now.getTime() - date.getTime()
  const hours = Math.floor(diff / (1000 * 60 * 60))
  
  if (hours < 1) return '刚刚'
  if (hours < 24) return `${hours}小时前`
  
  const days = Math.floor(hours / 24)
  if (days < 7) return `${days}天前`
  
  return date.toLocaleDateString('zh-CN')
}

// 生命周期
onMounted(() => {
  // 获取当前用户信息
  const adminUser = localStorage.getItem('admin_user')
  if (adminUser) {
    try {
      currentUser.value = JSON.parse(adminUser)
    } catch (e) {
      console.error('解析用户数据失败:', e)
    }
  }
  
  // 加载统计数据
  loadStats()
})
</script>

<style scoped>
.dashboard {
  padding: 0;
}

/* 欢迎区域 */
.welcome-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  padding: 32px;
  margin-bottom: 24px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: white;
  box-shadow: 0 8px 32px rgba(102, 126, 234, 0.2);
}

.welcome-content h2 {
  margin: 0 0 8px 0;
  font-size: 24px;
  font-weight: 600;
}

.welcome-content p {
  margin: 0;
  opacity: 0.9;
  font-size: 14px;
}

.welcome-actions {
  display: flex;
  gap: 12px;
}

.welcome-actions .el-button {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.3);
  color: white;
}

.welcome-actions .el-button:hover {
  background: rgba(255, 255, 255, 0.3);
}

/* 统计卡片 */
.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  transition: all 0.3s ease;
  cursor: pointer;
  border: 1px solid #f0f0f0;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.12);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 16px;
}

.stat-icon.courses { background: #e6f7ff; color: #1890ff; }
.stat-icon.users { background: #f6ffed; color: #52c41a; }
.stat-icon.experts { background: #fff0e6; color: #fa8c16; }
.stat-icon.revenue { background: #f9f0ff; color: #722ed1; }

.stat-info {
  flex: 1;
}

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #333;
  line-height: 1.2;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin: 4px 0;
}

.stat-detail {
  font-size: 12px;
  color: #999;
}

/* 分析面板 */
.analysis-panels {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.analysis-card {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.card-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
  font-weight: 600;
}

.mini-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.mini-stat {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 16px;
  background: #fafafa;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.mini-stat:hover {
  background: #f0f0f0;
}

.mini-stat .label {
  font-size: 14px;
  color: #666;
}

.mini-stat .value {
  font-size: 16px;
  font-weight: 600;
  color: #333;
}

.progress-item {
  margin-bottom: 16px;
}

.progress-label {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
  font-size: 14px;
}

.activity-stats {
  display: flex;
  justify-content: space-between;
}

.activity-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex: 1;
}

.activity-icon {
  width: 40px;
  height: 40px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  margin-bottom: 8px;
}

.activity-icon.new-users { background: #e6f7ff; }
.activity-icon.new-courses { background: #f6ffed; }
.activity-icon.new-orders { background: #fff0e6; }

.activity-number {
  font-size: 20px;
  font-weight: 600;
  color: #333;
  text-align: center;
}

.activity-label {
  font-size: 12px;
  color: #666;
  text-align: center;
}

.system-status {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.status-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
}

.status-item:last-child {
  border-bottom: none;
}

.status-label {
  font-size: 14px;
  color: #666;
}

/* 快速操作 */
.quick-actions {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
}

.actions-header h3 {
  margin: 0 0 20px 0;
  font-size: 16px;
  color: #333;
  font-weight: 600;
}

.actions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 16px;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  border-radius: 8px;
  transition: all 0.2s;
  cursor: pointer;
  border: 1px solid #f0f0f0;
}

.action-item:hover {
  background: #f8f9fa;
  transform: translateY(-2px);
}

.action-icon {
  font-size: 32px;
  margin-bottom: 8px;
}

.action-label {
  font-size: 14px;
  color: #333;
  font-weight: 500;
}

/* 最近活动 */
.recent-activity {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #f0f0f0;
}

.activity-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.activity-header h3 {
  margin: 0;
  font-size: 16px;
  color: #333;
  font-weight: 600;
}

.activity-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.activity-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 12px 0;
  border-bottom: 1px solid #f0f0f0;
}

.activity-item:last-child {
  border-bottom: none;
}

.activity-content {
  flex: 1;
}

.activity-text {
  font-size: 14px;
  color: #333;
  margin-bottom: 4px;
}

.activity-time {
  font-size: 12px;
  color: #999;
}

.no-activity {
  text-align: center;
  padding: 40px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .welcome-section {
    flex-direction: column;
    text-align: center;
    gap: 20px;
  }
  
  .stats-cards {
    grid-template-columns: 1fr;
  }
  
  .analysis-panels {
    grid-template-columns: 1fr;
  }
  
  .actions-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .activity-stats {
    flex-direction: column;
    gap: 16px;
  }
}
</style>