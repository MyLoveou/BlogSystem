<template>
  <nav class="navbar">
    <div class="navbar-container">
      <router-link to="/" class="logo animate-fade">
        <i class="fas fa-paw"></i> 人间<span>の无味</span>
      </router-link>
      <div class="nav-links">
        <router-link to="/" class="animate-fade delay-1" :class="{ active: $route.path === '/' }">首页</router-link>
        <router-link to="/articles" class="animate-fade delay-2">文章</router-link>
        <router-link to="/categority" class="animate-fade delay-3">分类</router-link>
        <router-link to="/tag" class="animate-fade delay-3">标签</router-link>
        <router-link to="/recommend" class="animate-fade delay-3">推荐</router-link>
        <router-link to="/about" class="animate-fade delay-3">关于</router-link>
      </div>
    </div>
  </nav>
</template>

<script>

</script>

<style scoped>
.navbar {
  background: rgba(15, 14, 23, 0.85);
  backdrop-filter: blur(10px);
  padding: 15px 0;
  position: sticky;
  top: 0;
  z-index: 100;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  border-bottom: 1px solid rgba(122, 90, 245, 0.2);
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

.logo {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--light);
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo span {
  color: var(--secondary);
}

.nav-links {
  display: flex;
  gap: 30px;
}

.nav-links a {
  color: var(--gray);
  text-decoration: none;
  font-weight: 500;
  position: relative;
  padding: 5px 0;
  transition: var(--transition);
}

.nav-links a:hover, 
.nav-links a.active {
  color: var(--light);
}

.nav-links a::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  transition: var(--transition);
}

.nav-links a:hover::after,
.nav-links a.active::after {
  width: 100%;
}
</style>