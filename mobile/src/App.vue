<template>
  <view class="app">
    <router-view />
  </view>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
.app {
  font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
  font-size: 14px;
  color: #333;
}

/* 全局样式 */
button {
  outline: none;
}

input, textarea {
  outline: none;
}
</style>