<template>
  <div class="tracking-timeline">
    <div v-if="loading" class="loading-state">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>加载物流信息中...</span>
    </div>

    <div v-else-if="error" class="error-state">
      <el-icon><WarningFilled /></el-icon>
      <span>{{ error }}</span>
    </div>

    <div v-else-if="!trackingHistory || trackingHistory.length === 0" class="empty-state">
      <el-icon><Box /></el-icon>
      <span>暂无物流信息</span>
    </div>

    <el-timeline v-else>
      <el-timeline-item
        v-for="(item, index) in trackingHistory"
        :key="index"
        :timestamp="item.time"
        :type="getTimelineType(index)"
        :size="index === 0 ? 'large' : 'normal'"
        placement="top"
      >
        <div class="timeline-content">
          <div class="status-text">{{ item.status }}</div>
          <div v-if="item.location" class="location-text">
            <el-icon><Location /></el-icon>
            {{ item.location }}
          </div>
        </div>
      </el-timeline-item>
    </el-timeline>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { Loading, WarningFilled, Box, Location } from '@element-plus/icons-vue'

interface TrackingItem {
  time: string
  status: string
  location?: string
}

interface Props {
  trackingHistory?: TrackingItem[]
  loading?: boolean
  error?: string
}

const props = withDefaults(defineProps<Props>(), {
  trackingHistory: () => [],
  loading: false,
  error: ''
})

const getTimelineType = (index: number) => {
  // 最新的一条显示为success，其他为info
  return index === 0 ? 'success' : 'info'
}
</script>

<style scoped>
.tracking-timeline {
  padding: 20px;
  min-height: 200px;
}

.loading-state,
.error-state,
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 40px 20px;
  color: var(--el-text-color-secondary);
}

.loading-state .el-icon {
  font-size: 32px;
}

.error-state {
  color: var(--el-color-danger);
}

.error-state .el-icon {
  font-size: 32px;
}

.empty-state .el-icon {
  font-size: 48px;
  color: var(--el-text-color-placeholder);
}

.timeline-content {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-text {
  font-size: 14px;
  color: var(--el-text-color-primary);
  font-weight: 500;
}

.location-text {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 13px;
  color: var(--el-text-color-secondary);
}

.location-text .el-icon {
  font-size: 14px;
}

:deep(.el-timeline-item__timestamp) {
  color: var(--el-text-color-secondary);
  font-size: 12px;
}

:deep(.el-timeline-item__node--large) {
  width: 16px;
  height: 16px;
}

:deep(.el-timeline-item__node--success) {
  background-color: var(--el-color-success);
}
</style>
