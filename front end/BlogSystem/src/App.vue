<template>
  <div id="app">
    <Background />
    <Navbar />
    <RouterView />
  </div>
</template>

<script setup>
import Background from '@/components/Background.vue'
import Navbar from '@/components/navbar.vue'
import { RouterView } from 'vue-router'
</script>

<style lang="less">
/* 全局样式 */
@import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
@import url('https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&display=swap');

:root {
  --primary: #7a5af5;
  --secondary: #ff6b9c;
  --accent: #00d0ff;
  --dark: #0f0e17;
  --darker: #0a0a12;
  --light: #fffffe;
  --gray: #a7a9be;
  --border-radius: 16px;
  --transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
}

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Noto Sans SC', sans-serif;
  background: linear-gradient(135deg, var(--darker), var(--dark));
  color: var(--light);
  line-height: 1.6;
  min-height: 100vh;
  position: relative;
  overflow-x: hidden;
}

/* 动画效果 */
@keyframes fadeIn {
  from { opacity: 0; transform: translateY(20px); }
  to { opacity: 1; transform: translateY(0); }
}

.animate-fade {
  animation: fadeIn 0.8s ease forwards;
  opacity: 0;
}

.delay-1 { animation-delay: 0.1s; }
.delay-2 { animation-delay: 0.2s; }
.delay-3 { animation-delay: 0.3s; }
.delay-4 { animation-delay: 0.4s; }

/* 装饰元素 */
.decoration {
  position: absolute;
  z-index: -1;
  opacity: 0.1;
}

.decoration-1 {
  top: 10%;
  right: 10%;
  font-size: 15rem;
  color: var(--primary);
  transform: rotate(15deg);
}

.decoration-2 {
  bottom: 20%;
  left: 5%;
  font-size: 12rem;
  color: var(--secondary);
  transform: rotate(-10deg);
}
</style>