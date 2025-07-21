<template>
  <article
    class="article-card"
    :class="[customClass, { 'is-draft': isDraft }]"
  >
    <!-- 封面 -->
    <div class="card-image">
      <img
        :src="cover"
        :alt="title"
        @error="coverError"
        class="card-image-content"
      />
      <span v-if="badgeText" class="card-badge">{{ badgeText }}</span>
    </div>

    <!-- 内容区 -->
    <div class="card-content">
      <h3 class="card-title">{{ title }}</h3>
      <p class="card-excerpt">{{ excerpt }}</p>

      <div class="card-meta">
        <span class="meta-item">
          <i class="far fa-calendar" />
          {{ formattedDate }}
        </span>
        <span class="meta-item">
          <i class="far fa-eye" />
          {{ viewsCount }}
        </span>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import dayjs from 'dayjs'         // 如不想引入可自行实现格式化

/* ---------------- props ---------------- */
const props = defineProps({
  article: { type: Object, required: true },
  customClass: { type: String, default: '' }
})

// 封面图兜底
const cover = computed(
  () => props.article.cover_image_url || 'https://api.rls.ovh/adaptive'
)

// 日期格式化
const formattedDate = computed(() =>
  props.article.published_at
    ? dayjs(props.article.published_at).format('YYYY-MM-DD')
    : '未发布'
)
/* ---------------- computed ---------------- */
const title       = computed(() => props.article.title || '无标题')
const excerpt     = computed(() => props.article.excerpt || '')
const badgeText   = computed(() => props.article.primary_category || '') // 
const viewsCount  = computed(() => props.article.views_count || 0)
const isDraft     = computed(() => props.article.status === 'draft')
/* ---------------- methods ---------------- */
function coverError(e) {
  e.target.src = 'https://via.placeholder.com/400x200?text=Error'
}
</script>

<style scoped>
.article-card {
  background: rgba(15, 14, 23, 0.7);
  backdrop-filter: blur(10px);
  border-radius: 16px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  height: 100%;
  border: 1px solid rgba(122, 90, 245, 0.2);
  position: relative;
  transform: translateY(0);
}

.article-card:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 50px rgba(122, 90, 245, 0.3);
  border: 1px solid rgba(122, 90, 245, 0.5);
}

.card-image {
  height: 200px;
  position: relative;
  overflow: hidden;
}

.card-image-content {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.7s ease;
  display: block;
}

.article-card:hover .card-image-content {
  transform: scale(1.05);
}

.card-badge {
  position: absolute;
  top: 12px;
  right: 12px;
  background: linear-gradient(90deg, #7a5af5, #ff6b6b);
  color: white;
  padding: 6px 14px;
  border-radius: 16px;
  font-size: 0.85rem;
  font-weight: 600;
  z-index: 2;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.article-card.is-draft .card-badge {
  background: linear-gradient(90deg, #6c757d, #adb5bd);
}

.article-card.is-draft {
  opacity: 0.85;
  filter: saturate(0.8);
}

.card-content {
  padding: 20px;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
}

.card-title {
  font-size: 1.25rem;
  font-weight: 700;
  margin-bottom: 12px;
  color: #fff;
  transition: color 0.3s ease;
  line-height: 1.4;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-title:hover {
  color: #7a5af5;
}

.card-excerpt {
  color: #a0aec0;
  margin-bottom: 15px;
  flex-grow: 1;
  line-height: 1.6;
  font-size: 0.95rem;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-meta {
  display: flex;
  justify-content: space-between;
  color: #718096;
  font-size: 0.85rem;
  padding-top: 15px;
  border-top: 1px solid rgba(122, 90, 245, 0.2);
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .card-image {
    height: 180px;
  }
  
  .card-content {
    padding: 16px;
  }
  
  .card-title {
    font-size: 1.15rem;
  }
}
</style>