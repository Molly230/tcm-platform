<template>
  <div class="consultation-management">
    <div class="page-header">
      <div class="header-content">
        <h2>💬 咨询管理</h2>
        <p>管理用户咨询记录、专家回复和服务质量</p>
      </div>
      <div class="header-actions">
        <el-button type="primary">
          <el-icon><ChatLineRound /></el-icon>
          查看咨询
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
        <div class="stat-icon total">💬</div>
        <div class="stat-info">
          <div class="stat-number">8,924</div>
          <div class="stat-label">咨询总数</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon ai">🤖</div>
        <div class="stat-info">
          <div class="stat-number">6,789</div>
          <div class="stat-label">AI咨询</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon expert">👨‍⚕️</div>
        <div class="stat-info">
          <div class="stat-number">2,135</div>
          <div class="stat-label">专家咨询</div>
        </div>
      </div>
      
      <div class="stat-card">
        <div class="stat-icon satisfaction">⭐</div>
        <div class="stat-info">
          <div class="stat-number">4.8</div>
          <div class="stat-label">满意度评分</div>
        </div>
      </div>
    </div>

    <div class="content-placeholder">
      <el-empty description="咨询管理功能开发中..." />
      <p style="color: #666; margin-top: 20px; text-align: center;">
        该模块包含咨询记录、专家分配、质量监控、统计分析等功能
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { ChatLineRound, Refresh } from '@element-plus/icons-vue'

const loading = ref(false)
</script>

<style scoped>
.consultation-management {
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
.stat-icon.ai { background: #f9f0ff; }
.stat-icon.expert { background: #fff0e6; }
.stat-icon.satisfaction { background: #f6ffed; }

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