<template>
  <el-option
    :label="item.zh"
    :value="item.code"
    :disabled="disabled"
  >
    <div class="enum-option-content">
      <div class="option-main">
        <EnumColorIndicator :color="item.color" />
        <span class="option-label">{{ item.zh }}</span>
      </div>
      <div class="option-meta">
        <el-tag size="small" type="info">{{ item.code }}</el-tag>
      </div>
    </div>
    <div v-if="showDescription && item.description" class="option-description">
      {{ item.description }}
    </div>
  </el-option>
</template>

<script setup lang="ts">
import type { EnumItem } from '@/services/EnumService'
import EnumColorIndicator from './EnumColorIndicator.vue'

interface Props {
  item: EnumItem
  showDescription?: boolean
  disabled?: boolean
}

withDefaults(defineProps<Props>(), {
  showDescription: false,
  disabled: false
})
</script>

<style scoped>
.enum-option-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

.option-main {
  display: flex;
  align-items: center;
  gap: 8px;
  flex: 1;
}

.option-label {
  font-size: 14px;
}

.option-meta {
  flex-shrink: 0;
}

.option-description {
  margin-top: 4px;
  font-size: 12px;
  color: var(--el-text-color-secondary);
  line-height: 1.4;
}
</style>