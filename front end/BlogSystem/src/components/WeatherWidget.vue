<template>
  <div class="weather-widget animate-fade delay-2">
    <div class="weather-header">
      <div class="weather-location">秋叶原</div>
      <div class="weather-time">{{ formattedDate }}</div>
    </div>
    <div class="weather-main">
      <div class="weather-icon">
        <i class="fas fa-cloud-moon"></i>
      </div>
      <div class="weather-temp">19°C</div>
    </div>
    <div class="weather-details">
      <div class="weather-detail">
        <i class="fas fa-wind"></i>
        <div>3 km/h</div>
      </div>
      <div class="weather-detail">
        <i class="fas fa-tint"></i>
        <div>65%</div>
      </div>
      <div class="weather-detail">
        <i class="fas fa-sun"></i>
        <div>06:23</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const formattedDate = computed(() => {
  const date = new Date();
  const options = { month: 'long', day: 'numeric', weekday: 'long' };
  return date.toLocaleDateString('zh-CN', options);
})
</script>

<style lang="less" scoped>
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

.weather-icon {
  font-size: 4rem;
  margin-right: 15px;
  color: var(--accent);
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