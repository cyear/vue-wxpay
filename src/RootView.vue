<script setup>
import { ref } from "vue";
import axios from 'axios';
import { showToast } from '@nutui/nutui';
import '@nutui/nutui/dist/packages/toast/style';

const searchValue = ref('');
const search = function () {
  const keyword = searchValue.value;
  showToast.text('搜索: ' + keyword);
}

const card_click = function (event) {
  const id = event.currentTarget.id;
  showToast.text('点击: ' + id);
  console.log(states);
  window.location.href = '#/buy?id=' + id;
}
const states = ref([]);

axios.get('/api/get').then(response => {
  states.value = response.data;
}).catch(error => {
  console.error(error);
});
</script>

<template>
  <nut-searchbar v-model="searchValue" @search="search"></nut-searchbar>

<div v-for="state in states" :key="state.id">
  <nut-divider />
  <nut-card
    :img-url="state.imgUrl"
    :title="state.title"
    :price="state.price"
    :vipPrice="state.vipPrice"
    :shopDesc="state.shopDesc"
    :delivery="state.delivery"
    :shopName="state.shopName"
    @click="card_click"
    :id="state.id"
  ></nut-card>
</div>

</template>

<style>

</style>
