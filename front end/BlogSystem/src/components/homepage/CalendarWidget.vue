<template>
  <div class="calendar-widget animate-fade delay-1">
    <div class="calendar-header">
      <h3 class="calendar-title">{{ currentYear }}年{{ currentMonth }}月</h3>
      <div class="calendar-controls">
        <button @click="prevMonth"><i class="fas fa-chevron-left"></i></button>
        <button @click="nextMonth"><i class="fas fa-chevron-right"></i></button>
      </div>
    </div>
    <div class="calendar-grid">
      <div v-for="day in weekDays" :key="day" class="calendar-day">{{ day }}</div>
      <div v-for="(date, index) in calendarDates" :key="index" class="calendar-date" :class="{
        'today': isToday(date),
        'event': hasEvent(date)
      }">
        {{ date.getDate() }}
      </div>
    </div>
  </div>
</template>

<script setup>

import { computed, ref } from 'vue'
const weekDays = ['日', '一', '二', '三', '四', '五', '六']
const currentDate = ref(new Date())
const eventDates = [16, 24]

const currentYear = computed(() => {
  return currentDate.value.getFullYear()
})
const currentMonth = computed(() => {
  return currentDate.value.getMonth() + 1
})
const calendarDates = computed(() => {
  const year = currentDate.value.getFullYear();
  const month = currentDate.value.getMonth();

  // 获取当月第一天
  const firstDay = new Date(year, month, 1);
  // 获取当月最后一天
  const lastDay = new Date(year, month + 1, 0);

  // 日历数组
  const dates = [];

  // 添加上个月最后几天
  const prevMonthLastDay = new Date(year, month, 0).getDate();
  const firstDayOfWeek = firstDay.getDay();
  for (let i = firstDayOfWeek - 1; i >= 0; i--) {
    const date = new Date(year, month - 1, prevMonthLastDay - i);
    dates.push(date);
  }

  // 添加当月日期
  for (let i = 1; i <= lastDay.getDate(); i++) {
    dates.push(new Date(year, month, i));
  }

  // 添加下个月前几天
  const totalCells = 42; // 6行 * 7列
  const nextDays = totalCells - dates.length;
  for (let i = 1; i <= nextDays; i++) {
    dates.push(new Date(year, month + 1, i));
  }

  return dates;
})
function prevMonth() {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() - 1, 1);
  console.log(currentDate.value)
}
function nextMonth() {
  currentDate.value = new Date(currentDate.value.getFullYear(), currentDate.value.getMonth() + 1, 1);
}
function isToday(date) {
  const today = new Date();
  return date.getDate() === today.getDate() &&
    date.getMonth() === today.getMonth() &&
    date.getFullYear() === today.getFullYear();
}
function hasEvent(date) {
  return eventDates.includes(date.getDate()) &&
    date.getMonth() === currentDate.value.getMonth() &&
    date.getFullYear() === currentDate.value.getFullYear();
}
</script>

<style scoped>
.calendar-widget {
  background: rgba(15, 14, 23, 0.7);
  backdrop-filter: blur(10px);
  border-radius: var(--border-radius);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  padding: 25px;
  transition: var(--transition);
  border: 1px solid rgba(122, 90, 245, 0.2);
}

.calendar-widget:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(122, 90, 245, 0.2);
}

.calendar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.calendar-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: var(--light);
}

.calendar-controls button {
  background: none;
  border: none;
  cursor: pointer;
  color: var(--gray);
  font-size: 1.2rem;
  transition: var(--transition);
  padding: 5px;
  width: 35px;
  height: 35px;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

.calendar-controls button:hover {
  background: rgba(122, 90, 245, 0.2);
  color: var(--light);
}

.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  gap: 8px;
}

.calendar-day {
  text-align: center;
  padding: 10px 0;
  font-weight: 500;
  color: var(--gray);
  font-size: 0.9rem;
}

.calendar-date {
  text-align: center;
  padding: 10px 0;
  border-radius: 50%;
  cursor: pointer;
  transition: var(--transition);
  position: relative;
  z-index: 1;
}

.calendar-date:hover {
  background: rgba(122, 90, 245, 0.2);
}

.calendar-date.today {
  background: var(--primary);
  color: white;
  box-shadow: 0 0 10px rgba(122, 90, 245, 0.5);
}

.calendar-date.event::after {
  content: '';
  position: absolute;
  bottom: 5px;
  left: 50%;
  transform: translateX(-50%);
  width: 5px;
  height: 5px;
  background: var(--secondary);
  border-radius: 50%;
}
</style>