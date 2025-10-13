<template>
  <view class="my-courses">
    <text class="title">我的课程</text>
    <view class="coming-soon">
      <text>功能开发中...</text>
    </view>
  </view>
</template>

<script>
export default {
  name: 'MyCourses'
}
</script>

<style scoped>
.my-courses {
  padding: 40rpx;
  text-align: center;
}
.title {
  font-size: 36rpx;
  font-weight: bold;
  display: block;
  margin-bottom: 40rpx;
}
.coming-soon {
  color: #999;
  font-size: 28rpx;
}
</style>