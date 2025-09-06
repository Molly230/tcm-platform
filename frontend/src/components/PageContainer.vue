<template>
  <div class="page-container">
    <!-- 主内容 -->
    <main class="main-content">
      <slot name="breadcrumb"></slot>
      <slot></slot>
    </main>
    
    <!-- 简单页脚 -->
    <footer class="simple-footer">
      <p>© 2025 中医健康服务平台. 传承中医文化，服务大众健康.</p>
    </footer>
  </div>
</template>

<script setup lang="ts">
// 简化的页面容器组件
</script>

<style scoped>
.page-container {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
}

/* 导航样式已删除 */

.main-content {
  flex: 1;
  width: 100%;
  overflow: auto;
}

.simple-footer {
  background: white;
  color: #666;
  text-align: center;
  padding: 20px;
  margin-top: 60px;
}

.simple-footer p {
  margin: 0;
}
</style>