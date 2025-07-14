<template>
  <div class="article-card" :class="customClass">
    <div class="card-image">
      <img :src="article.image" :alt="article.title">
      <div class="card-badge">{{ article.category }}</div>
    </div>
    <div class="card-content">
      <h3 class="card-title">{{ article.title }}</h3>
      <p class="card-excerpt">{{ article.excerpt }}</p>
      <div class="card-meta">
        <span><i class="far fa-calendar"></i> {{ article.date }}</span>
        <span><i class="far fa-eye"></i> {{ article.views }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ArticleCard',
  props: {
    article: {
      type: Object,
      required: true
    },
    customClass: {
      type: String,
      default: ''
    }
  }
}
</script>

<style scoped>
.article-card {
  background: rgba(15, 14, 23, 0.7);
  backdrop-filter: blur(10px);
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: var(--transition);
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid rgba(122, 90, 245, 0.2);
  position: relative;
}

.article-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 15px 50px rgba(122, 90, 245, 0.3);
  border: 1px solid rgba(122, 90, 245, 0.5);
}

.card-image {
  height: 200px;
  position: relative;
  overflow: hidden;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.7s ease;
}

.article-card:hover .card-image img {
  transform: scale(1.1);
}

.card-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  background: linear-gradient(90deg, var(--primary), var(--secondary));
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
  z-index: 2;
}

.card-content {
  padding: 20px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.card-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: var(--light);
  transition: var(--transition);
  line-height: 1.4;
}

.card-title:hover {
  color: var(--accent);
}

.card-excerpt {
  color: var(--gray);
  margin-bottom: 15px;
  flex-grow: 1;
  line-height: 1.7;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  color: var(--gray);
  font-size: 0.9rem;
  padding-top: 15px;
  border-top: 1px solid rgba(122, 90, 245, 0.2);
}
</style>