<template>
  <div class="articles-section">
    <h2 class="section-title animate-fade">最新推荐 <i class="fas fa-fire"></i></h2>
    <div class="articles-grid">
      <ArticleCard 
        v-for="(article, index) in articles" 
        :key="article.id"
        :article="article"
        :class="`animate-fade delay-${index}`"
      />
    </div>
  </div>
</template>

<script>
import ArticleCard from './ArticleCard.vue'

export default {
  components: {
    ArticleCard
  },
  data() {
    return {
      articles: [
        {
          id: 1,
          title: '二次元角色绘画技巧：从线稿到上色',
          excerpt: '分享我多年来积累的二次元角色绘画技巧，包括线稿绘制、色彩搭配和光影处理，适合初学者和进阶画师...',
          category: '绘画教程',
          date: '2023-10-15',
          views: 1245,
          image: 'https://images.unsplash.com/photo-1542831371-29b0f74f9713?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
        },
        {
          id: 2,
          title: '2023年秋季新番推荐：不容错过的5部作品',
          excerpt: '本季度最值得期待的5部动漫作品，从热血战斗到治愈日常，总有一部能触动你的心弦...',
          category: '动漫推荐',
          date: '2023-10-10',
          views: 987,
          image: 'https://images.unsplash.com/photo-1618336753974-aae8e04506aa?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
        },
        {
          id: 3,
          title: '用Three.js创建二次元风格3D场景',
          excerpt: '探索如何使用Three.js和着色器技术创建具有二次元风格的3D场景，为你的网站添加独特视觉效果...',
          category: '前端技术',
          date: '2023-10-05',
          views: 1532,
          image: 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
        },
        {
          id: 4,
          title: '我的2023年手办收藏展示与心得',
          excerpt: '分享今年入手的精品手办，包括开箱体验、细节展示和收藏心得，一起感受二次元周边的魅力...',
          category: '手办收藏',
          date: '2023-09-28',
          views: 876,
          image: 'https://images.unsplash.com/photo-1555066931-4365d14bab8c?ixlib=rb-4.0.3&auto=format&fit=crop&w=600&q=80'
        }
      ]
    }
  }
}
</script>

<style scoped>
.articles-section {
  margin-top: 10px;
}

.section-title {
  font-size: 1.8rem;
  font-weight: 700;
  margin-bottom: 25px;
  color: var(--light);
  position: relative;
  padding-left: 20px;
  display: flex;
  align-items: center;
}

.section-title::before {
  content: '';
  position: absolute;
  left: 0;
  height: 100%;
  width: 6px;
  background: linear-gradient(to bottom, var(--primary), var(--secondary));
  border-radius: 10px;
}

.section-title i {
  margin-left: 15px;
  color: var(--secondary);
  font-size: 1.5rem;
}

.articles-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 25px;
}
</style>