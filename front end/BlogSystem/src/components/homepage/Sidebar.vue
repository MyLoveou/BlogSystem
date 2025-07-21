<template>
  <div class="sidebar">
    <ProfileCard />
    <CalendarWidget />
    <WeatherWidget v-if="weather" :weather="weather" />
    <div v-else>天气加载中…</div>
  </div>
</template>

<script setup>

import { ref, onMounted } from 'vue'
import ProfileCard from './ProfileCard.vue'
import CalendarWidget from './CalendarWidget.vue'
import WeatherWidget from './WeatherWidget.vue'
import { getWeatherData } from '@/apis/weather'

const weather = ref(null)

onMounted(async () => {
  try {
    const { data } = await getWeatherData()   // 这里 data 就是后端返回的整条 JSON
    weather.value = data
  } catch (e) {
    console.error('获取天气失败', e)
  }
})
</script>

<style scoped>
/* 关键：粘性定位 */
.sidebar {
  position: sticky;   /* 粘性 */
  top: 30px;          /* 距离视口顶部 30px 时“粘住” */
  align-self: flex-start; /* 防止在 flex 布局中被拉伸 */
  
  display: flex;
  flex-direction: column;
  gap: 30px;
}
</style>