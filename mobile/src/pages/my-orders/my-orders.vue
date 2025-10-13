<template>
  <view class="my-orders">
    <text class="title">我的订单</text>
    <view class="coming-soon">
      <text>功能开发中...</text>
    </view>
  </view>
</template>

<script>
export default {
  name: 'MyOrders'
}
</script>

<style scoped>
.my-orders {
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