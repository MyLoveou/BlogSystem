<template>
  <div class="profile-card animate-fade">
    <div class="avatar-container">
      <img src="https://images.unsplash.com/photo-1635107510862-53886e926b74?ixlib=rb-4.0.3&auto=format&fit=crop&w=500&q=80" alt="Avatar" class="avatar">
      <div class="avatar-frame"></div>
    </div>
    <h2 class="name">无人知我意</h2>
    <p class="title">二次元爱好者 | 前端开发</p>
    <p class="motto">寻一片乐土，创造自己的世界</p>
    <div class="social-links">
      <a href="#"><i class="fab fa-bilibili"></i></a>
      <a href="#"><i class="fab fa-weibo"></i></a>
      <a href="#"><i class="fab fa-github"></i></a>
      <a href="#"><i class="fab fa-pixiv"></i></a>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ProfileCard'
}
</script>

<style scoped>
.profile-card {
  background: rgba(15, 14, 23, 0.7);
  backdrop-filter: blur(10px);
  border-radius: var(--border-radius);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  padding: 30px;
  text-align: center;
  transition: var(--transition);
  position: relative;
  overflow: hidden;
  border: 1px solid rgba(122, 90, 245, 0.2);
}

.profile-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle, rgba(122, 90, 245, 0.1) 0%, transparent 70%);
  z-index: -1;
}

.profile-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 12px 40px rgba(122, 90, 245, 0.2);
}

.avatar-container {
  position: relative;
  width: 150px;
  height: 150px;
  margin: 0 auto 20px;
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 3px solid var(--primary);
  box-shadow: 0 0 20px rgba(122, 90, 245, 0.4);
}

.avatar-frame {
  position: absolute;
  top: -10px;
  left: -10px;
  width: calc(100% + 20px);
  height: calc(100% + 20px);
  border: 2px solid var(--secondary);
  border-radius: 50%;
  animation: rotate 20s linear infinite;
}

@keyframes rotate {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.name {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 5px;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.title {
  color: var(--gray);
  font-size: 1.1rem;
  margin-bottom: 20px;
}

.motto {
  font-style: italic;
  color: var(--light);
  margin-bottom: 25px;
  padding: 0 15px;
  position: relative;
  font-size: 1.1rem;
  line-height: 1.8;
}

.motto::before, .motto::after {
  content: '"';
  font-size: 2.5rem;
  color: var(--secondary);
  position: absolute;
  opacity: 0.5;
}

.motto::before {
  top: -20px;
  left: -10px;
}

.motto::after {
  bottom: -35px;
  right: -10px;
}

.social-links {
  display: flex;
  justify-content: center;
  gap: 15px;
  margin-top: 20px;
}

.social-links a {
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: rgba(122, 90, 245, 0.2);
  color: var(--light);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: var(--transition);
  font-size: 1.2rem;
  position: relative;
  overflow: hidden;
}

.social-links a::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, var(--primary), var(--secondary));
  opacity: 0;
  transition: var(--transition);
  z-index: -1;
}

.social-links a:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 15px rgba(122, 90, 245, 0.4);
}

.social-links a:hover::before {
  opacity: 1;
}
</style>