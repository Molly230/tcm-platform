<template>
  <div id="app">
    <NavigationBar />
    <router-view />
  </div>
</template>

<script setup lang="ts">
import NavigationBar from './components/NavigationBar.vue'
</script>

<style>
/* 全局重置样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html, body {
  height: 100%;
  margin: 0;
  padding: 0;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: #2c3e50;
  min-height: 100vh;
  width: 100%;
}

/* 移除默认的text-align: center，让内容正常布局 */
</style>