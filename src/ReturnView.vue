<script setup>
//import { ref } from 'vue';
import { showToast } from '@nutui/nutui';
import '@nutui/nutui/dist/packages/toast/style';

//const id = ref(window.location.hash.split('?')[1].split('=')[1])

showToast.success("支付成功！");

</script>

<template>

  <nut-navbar @on-click-back="back" @on-click-title="title" title="订单详情">
    <template #left>
      <a href="#/" style="text-decoration: none;">返回</a>
    </template>
    <template #right>
      <ShareN width="16px"></ShareN>
    </template>
  </nut-navbar>
  <div id="buy">
    <p>订单已完成！</p>
  </div>

</template>
