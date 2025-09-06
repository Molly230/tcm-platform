<template>
  <div style="padding: 20px; text-align: center; font-size: 24px;">
    <h1>🎉 前端正常工作！</h1>
    <p>如果你能看到这个页面，说明前端已经成功启动</p>
    <br>
    <el-button type="primary" @click="testClick">点击测试</el-button>
    <br><br>
    <p>时间: {{ currentTime }}</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const currentTime = ref(new Date().toLocaleString())

const testClick = () => {
  alert('前端交互正常！')
}

onMounted(() => {
  setInterval(() => {
    currentTime.value = new Date().toLocaleString()
  }, 1000)
})
</script>