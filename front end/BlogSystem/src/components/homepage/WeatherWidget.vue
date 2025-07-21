<template>
  <div class="weather-widget animate-fade delay-2">
    <div class="weather-header">
      <div class="weather-location">{{ cityName }}</div>
      <div class="weather-time">{{ formattedDate }}</div>
    </div>

    <div class="weather-main">
      <div class="weather-icon">
        <i :class="[faIcon, 'weather-icon-large']"></i>
      </div>
      <div class="weather-temp">{{ todaynow.temp }}°C</div>
    </div>

    <div class="weather-details">
      <div class="weather-detail">
        <i class="fas fa-wind"></i>
        <div>{{ todaynow.windDir }} {{ todaynow.windScale }}级</div>
      </div>
      <div class="weather-detail">
        <i class="fas fa-tint"></i>
        <div>{{ todaynow.humidity }}%</div>
      </div>
      <div class="weather-detail">
        <i class="fas fa-cloud-rain"></i>
        <div>{{ todaynow.precip || '0' }} mm</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

/* ===== 父组件通过 props 传进来，也可以直接 fetch ===== */
const props = defineProps({
  weather: {
    type: Object,
    required: true
  }
})

/* 城市名：location=101010100 写死为北京，也可把 cityName 放进 API */
const cityName = '武汉'
// console.log(props.weather.now)
/* 日期 */
const formattedDate = computed(() => {
  const date = new Date()
  return date.toLocaleDateString('zh-CN', {
    month: 'long',
    day: 'numeric',
    weekday: 'long'
  })
})
// console.log(props.weather.now)
/* 当前天气字段 */
const todaynow = computed(() => props.weather.now)
console.log(todaynow)
const weatherText = computed(() => todaynow.text)

// /* 和风官方图标映射 */
// const iconUrl = computed(
//   () => `https://a.hecdn.net/img/common/icon/202106d/${todaynow.icon}.png`
// )

const iconMap = {
  100: 'fas fa-sun',           // 晴
  101: 'fas fa-cloud-sun',     // 多云
  104: 'fas fa-cloud',         // 阴
  300: 'fas fa-cloud-rain',    // 小雨
  301: 'fas fa-cloud-showers-heavy', // 中雨
  404: 'fas fa-cloud-snow',    // 雨夹雪
  500: 'fas fa-snowflake',     // 小雪
  999: 'fas fa-smog',          // 雾 / 霾
  // ……按需要补全
}
const faIcon = computed(() => iconMap[todaynow.value.icon] || 'fas fa-question')
</script>

<style lang="less" scoped>

.weather-icon-large {
  font-size: 3.2rem;   /* ↓↓↓ 想多大调多大 */
  color: var(--accent);
  filter: drop-shadow(0 0 6px rgba(0, 208, 255, 0.5));
}
/* 样式保持不变 */
.weather-widget {
  background: linear-gradient(135deg, rgba(122, 90, 245, 0.3), rgba(255, 107, 156, 0.3));
  backdrop-filter: blur(10px);
  border-radius: var(--border-radius);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  padding: 25px;
  color: white;
  transition: var(--transition);
  border: 1px solid rgba(122, 90, 245, 0.2);
}
.weather-widget:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(122, 90, 245, 0.2);
}
.weather-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}
.weather-location {
  font-size: 1.3rem;
  font-weight: 600;
}
.weather-main {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.weather-icon img {
  width: 64px;
  height: 64px;
  filter: drop-shadow(0 0 5px rgba(0, 208, 255, 0.5));
}
.weather-temp {
  font-size: 2.8rem;
  font-weight: 700;
  text-shadow: 0 0 10px rgba(0, 208, 255, 0.5);
}
.weather-details {
  display: flex;
  justify-content: space-between;
  font-size: 0.95rem;
  background: rgba(0, 0, 0, 0.2);
  border-radius: 12px;
  padding: 12px;
}
.weather-detail {
  text-align: center;
  flex: 1;
}
.weather-detail i {
  display: block;
  margin-bottom: 5px;
  font-size: 1.2rem;
  color: var(--accent);
}
</style>