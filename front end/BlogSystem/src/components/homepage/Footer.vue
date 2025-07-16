<template>
  <footer class="footer">
    <div class="footer-content">
      <div class="footer-column">
        <h3>关于博客</h3>
        <p style="margin-bottom: 20px; line-height: 1.7;">分享技术与生活，记录兴趣与成长的点滴。</p>
        <div class="social-links">
          <a href="#"><i class="fab fa-bilibili"></i></a>
          <a href="#"><i class="fab fa-weibo"></i></a>
          <a href="#"><i class="fab fa-github"></i></a>
          <a href="#"><i class="fab fa-pixiv"></i></a>
        </div>
      </div>
      <div class="footer-column">
        <h3>内容分类</h3>
        <ul class="footer-links">
          <!-- <li><a href="#"><i class="fas fa-paint-brush"></i> 插画教程</a></li>
          <li><a href="#"><i class="fas fa-film"></i> 动漫推荐</a></li>
          <li><a href="#"><i class="fas fa-laptop-code"></i> 前端技术</a></li>
          <li><a href="#"><i class="fas fa-figure"></i> 手办收藏</a></li>
          <li><a href="#"><i class="fas fa-gamepad"></i> 游戏评测</a></li> -->
        </ul>
      </div>
      <div class="footer-column">
        <h3>快速链接</h3>
        <ul class="footer-links">
          <!-- <li><a href="#"><i class="fas fa-home"></i> 首页</a></li>
          <li><a href="#"><i class="fas fa-book"></i> 文章归档</a></li>
          <li><a href="#"><i class="fas fa-images"></i> 作品画廊</a></li>
          <li><a href="#"><i class="fas fa-info-circle"></i> 关于我</a></li>
          <li><a href="#"><i class="fas fa-envelope"></i> 联系</a></li> -->
        </ul>
      </div>
      <div class="footer-column">
        <h3>友情链接</h3>
        <ul class="footer-links">
          <!-- <li><a href="#"><i class="fas fa-paw"></i> 喵星人画室</a></li>
          <li><a href="#"><i class="fas fa-gamepad"></i> 二次元游戏社区</a></li>
          <li><a href="#"><i class="fas fa-camera"></i> Cosplay世界</a></li>
          <li><a href="#"><i class="fas fa-music"></i> 动漫音乐站</a></li> -->
        </ul>
      </div>
    </div>
    <div class="copyright">
      &copy; 2023 人间の无味 | 个人博客 | 保留所有权利 | 豫ICP备2025113250号-1
    </div>
  </footer>
</template>

<script>
export default {
  name: 'Footer'
}
</script>

<style scoped>
.footer {
  background: rgba(10, 10, 18, 0.95);
  backdrop-filter: blur(10px);
  color: var(--gray);
  padding: 50px 0 20px;
  margin-top: 80px;
  border-top: 1px solid rgba(122, 90, 245, 0.2);
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 40px;
  max-width: 1200px;
  margin: 0 auto 40px;
  padding: 0 20px;
}

.footer-column h3 {
  color: var(--light);
  font-size: 1.3rem;
  margin-bottom: 20px;
  position: relative;
  padding-bottom: 10px;
}

.footer-column h3::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  border-radius: 3px;
}

.footer-links {
  list-style: none;
}

.footer-links li {
  margin-bottom: 15px;
}

.footer-links a {
  color: var(--gray);
  text-decoration: none;
  transition: var(--transition);
  display: flex;
  align-items: center;
  gap: 10px;
}

.footer-links a:hover {
  color: var(--accent);
  padding-left: 5px;
}

.footer-links a i {
  width: 20px;
  text-align: center;
}

.copyright {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid rgba(122, 90, 245, 0.1);
  font-size: 0.9rem;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 20px 0;
}

.social-links {
  display: flex;
  gap: 15px;
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