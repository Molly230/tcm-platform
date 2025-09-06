<template>
  <div class="order-management">
    <div class="page-header">
      <div class="header-content">
        <h2>📋 订单管理</h2>
        <p>管理平台订单状态、支付和发货信息</p>
      </div>
      <div class="header-actions">
        <el-button type="primary">
          <el-icon><Download /></el-icon>
          导出订单
        </el-button>
        <el-button :loading="loading">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-section">
      <div class="stat-card">
        <div class="stat-icon total">📋</div>
        <div class="stat-info">
          <div class="stat-number">2,845</div>
          <div class="stat-label">订单总数</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon pending">⏳</div>
        <div class="stat-info">
          <div class="stat-number">156</div>
          <div class="stat-label">待处理</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon shipped">🚚</div>
        <div class="stat-info">
          <div class="stat-number">89</div>
          <div class="stat-label">已发货</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon revenue">💰</div>
        <div class="stat-info">
          <div class="stat-number">¥125,680</div>
          <div class="stat-label">本月收入</div>
        </div>
      </div>
    </div>

    <div class="content-placeholder">
      <el-empty description="订单管理功能开发中..." />
      <p style="color: #666; margin-top: 20px; text-align: center;">
        该模块包含订单列表、状态管理、物流跟踪、退款处理等功能
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Download, Refresh } from '@element-plus/icons-vue'

const loading = ref(false)
</script>

<style scoped>
.order-management {
  padding: 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
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

.header-actions {
  display: flex;
  gap: 12px;
}

.stats-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.stat-icon {
  width: 48px;
  height: 48px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  margin-right: 16px;
}

.stat-icon.total { background: #e6f7ff; }
.stat-icon.pending { background: #fff0e6; }
.stat-icon.shipped { background: #f6ffed; }
.stat-icon.revenue { background: #f9f0ff; }

.stat-number {
  font-size: 24px;
  font-weight: 600;
  color: #333;
}

.stat-label {
  font-size: 14px;
  color: #666;
  margin-top: 4px;
}

.content-placeholder {
  background: white;
  border-radius: 8px;
  padding: 60px 20px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}
</style>