<template>
  <div>
    <div class="background"></div>
    <div class="particles" id="particles"></div>
    <div class="decoration decoration-1">
      <i class="fas fa-star"></i>
    </div>
    <div class="decoration decoration-2">
      <i class="fas fa-moon"></i>
    </div>
  </div>
</template>

<script setup>


// 创建粒子背景
function createParticles() {
  const container = document.getElementById('particles');
  const particleCount = 30;

  for (let i = 0; i < particleCount; i++) {
    const particle = document.createElement('div');
    particle.classList.add('particle');

    // 随机大小
    const size = Math.random() * 10 + 3;
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;

    // 随机位置
    const posX = Math.random() * 100;
    const posY = Math.random() * 100;
    particle.style.left = `${posX}%`;
    particle.style.top = `${posY}%`;

    // 随机颜色
    const colors = ['#7a5af5', '#ff6b9c', '#00d0ff'];
    const color = colors[Math.floor(Math.random() * colors.length)];
    particle.style.background = color;

    // 随机动画时长
    const duration = Math.random() * 20 + 10;
    particle.style.animationDuration = `${duration}s`;

    container.appendChild(particle);
  }
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function () {
  createParticles();

  // 为卡片添加悬停效果
  const cards = document.querySelectorAll('.article-card, .profile-card, .calendar-widget, .weather-widget');
  cards.forEach(card => {
    card.addEventListener('mouseenter', function () {
      this.style.zIndex = 10;
    });

    card.addEventListener('mouseleave', function () {
      this.style.zIndex = '';
    });
  });
});
</script>

<style>
.background {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
  opacity: 0.1;
  /* background: url('../../public/background.avif') no-repeat center center; */
  background-size: cover;
}

.particles {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: -1;
}

.particle {
  position: absolute;
  background: rgba(122, 90, 245, 0.3);
  border-radius: 50%;
  animation: float 15s infinite linear;
}

@keyframes float {
  0% {
    transform: translateY(0) translateX(0) rotate(0deg);
  }

  100% {
    transform: translateY(-100vh) translateX(100px) rotate(360deg);
  }
}
</style>