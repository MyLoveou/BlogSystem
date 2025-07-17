<template>
  <div class="article-meta">
    <input 
      v-model="article.title" 
      placeholder="文章标题" 
      class="title-input"
      required
    />
    <textarea 
      v-model="article.excerpt" 
      placeholder="文章摘要（最多200字）" 
      maxlength="200"
      class="excerpt-input"
    ></textarea>
  </div>
</template>

<script setup>
defineProps({
  article: {
    type: Object,
    required: true
  }
});
</script>

<style scoped>
.article-meta {
  padding: 15px 20px;
  background: rgba(15, 14, 23, 0.7);
  border: 1px solid rgba(122, 90, 245, 0.2);
  border-top: none;
}

.title-input {
  width: 100%;
  background: transparent;
  border: none;
  color: var(--light);
  font-size: 1.5rem;
  margin-bottom: 10px;
  outline: none;
}

.excerpt-input {
  width: 100%;
  background: transparent;
  border: none;
  color: var(--gray);
  resize: vertical;
  min-height: 60px;
  outline: none;
}
</style>