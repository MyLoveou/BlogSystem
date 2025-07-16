<template>
  <div class="sidebar">
    <ProfileCard />
    <CalendarWidget />
    <WeatherWidget />
  </div>
</template>

<script>
import ProfileCard from './profileCard.vue'
import CalendarWidget from './CalendarWidget.vue'
import WeatherWidget from './weatherWidget.vue'

export default {
  components: {
    ProfileCard,
    CalendarWidget,
    WeatherWidget
  }
}
</script>

<style scoped>
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 30px;
}
</style>