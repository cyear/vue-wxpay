<script setup>
import { ref, computed } from "vue";
//import { showToast } from '@nutui/nutui';
import '@nutui/nutui/dist/packages/toast/style';
import { Home, My } from '@nutui/icons-vue';
import RootView from './RootView.vue';
import MyView from './MyView.vue';
import BuyView from './BuyView.vue';
import ReturnView from './ReturnView.vue';

const routes = {
  '/': RootView,
  '/#/': RootView,
  '/my': MyView,
  '/buy': BuyView,
  '/return': ReturnView,
};

const currentPath = ref(window.location.hash);
window.addEventListener('hashchange', () => {
  currentPath.value = window.location.hash;
  console.log(currentPath.value);
});

const currentView = computed(() => {
  const [path, query] = currentPath.value.split('?');
  console.log(path.slice(1))
  const route = routes[path.slice(1)] || RootView;
  return {
    component: route,
    query: query ? Object.fromEntries(new URLSearchParams(query)) : {}
  };
});


function tabSwitch(item, index) {
  console.log(item, index);
}
const imgSrc = ref('//img11.360buyimg.com/imagetools/jfs/t1/57345/6/20069/8019/62b995cdEd96fef03/51d3302dfeccd1d2.png');
const flag = ref(false);

</script>

<template>

  <nut-watermark v-if="!flag" class="mark1" :z-index="1" content="大数据技术223101"></nut-watermark>

<div height="90%">
  <component :is="currentView.component" />
</div>

<div style="position:fixed; bottom:0; width: 100%">
  <nut-tabbar @tab-switch="tabSwitch">
     <nut-tabbar-item href="#/" tab-title="首页">
        <template #icon>
          <Home></Home>
        </template>
      </nut-tabbar-item>
      <nut-tabbar-item href="#/my" tab-title="我的">
        <template #icon>
          <My></My>
        </template>
      </nut-tabbar-item>
  </nut-tabbar>
</div>

    <nut-watermark
      v-if="flag"
      class="mark1"
      :image-width="60"
      :image-height="23"
      :z-index="1"
      :image="imgSrc"
    >
    </nut-watermark>

</template>

<style lang="scss" scoped>
  .wrap {
    width: 100%;
    height: 240px;
    display: block;
    background: #fff;
    >img {
      width: 100%;
    }
    .mark1 {
      width: 100%;
      top: 50px;
    }
    .nut-button{
      margin-right: 10px;
    }
  }

#app {
  max-width: 1280px;
  margin: 0 auto;
  padding: 2rem;
  text-align: center;
}
</style>
