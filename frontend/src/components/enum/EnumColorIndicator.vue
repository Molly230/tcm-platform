<template>
  <div
    class="enum-color-indicator"
    :style="{ backgroundColor: color }"
  ></div>
</template>

<script setup lang="ts">
interface Props {
  color: string
}

withDefaults(defineProps<Props>(), {
  color: '#409EFF'
})
</script>

<style scoped>
.enum-color-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}
</style>