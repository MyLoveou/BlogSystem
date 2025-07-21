<template>
  <section class="article-list">
    <!-- loading -->
    <div v-if="loading" class="loading-container">
      <div class="loading-spinner"></div>
      <div>加载中...</div>
    </div>

    <!-- empty -->
    <div v-else-if="!list.length" class="empty-container">
      <i class="far fa-file-alt"></i>
      <p>暂无文章</p>
    </div>

    <!-- 列表 -->
    <div v-else class="grid-container">
      <ArticleCard
        v-for="item in list"
        :key="item.id"
        :article="item"
        class="article-item"
      />
    </div>
  </section>
</template>

<script setup>
import ArticleCard from '../ArticleCard.vue'
import { getArticleList } from "@/apis/articles.js"
import { ref, onMounted } from 'vue'

const list    = ref([])
const loading = ref(true)

async function fetchData() {
  try {
    const data = await getArticleList({ /* 你的查询参数 */ })
    console.log(data, 0)
    list.value = data   // 根据后端分页结构取
    console.log(list.value, 1)
  } finally {
    loading.value = false
  }
}

onMounted(fetchData)
</script>

<style scoped>
.article-list {
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 20px;
}

.grid-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
}

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  color: #a0aec0;
}

.loading-spinner {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(122, 90, 245, 0.2);
  border-top: 4px solid #7a5af5;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-bottom: 20px;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.empty-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 0;
  color: #718096;
}

.empty-container i {
  font-size: 3rem;
  margin-bottom: 20px;
  opacity: 0.6;
}

.empty-container p {
  font-size: 1.2rem;
}

/* 响应式调整 */
@media (min-width: 1200px) {
  .grid-container {
    grid-template-columns: repeat(3, 1fr);
  }
}

@media (min-width: 768px) and (max-width: 1199px) {
  .grid-container {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .article-list {
    padding: 20px 15px;
  }
  
  .grid-container {
    gap: 20px;
  }
}
</style>