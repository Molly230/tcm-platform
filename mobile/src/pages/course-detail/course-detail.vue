<template>
  <view class="course-detail">
    <text class="title">课程详情</text>
    <view class="coming-soon">
      <text>功能开发中...</text>
    </view>
  </view>
</template>

<script>
export default {
  name: 'CourseDetail'
}
</script>

<style scoped>
.course-detail {
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