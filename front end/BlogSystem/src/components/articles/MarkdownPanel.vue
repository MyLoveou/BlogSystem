<template>
  <aside class="image-panel">
    <h4><i class="fas fa-images"/> 图片仓库</h4>
    <slot name="upload"/>
    <div v-if="categories.length || tags.length" class="metadata-display">
      <h5>分类</h5>
      <div class="tag-list"><el-tag v-for="c in categories" :key="c" size="small">{{ c }}</el-tag></div>
      <h5>标签</h5>
      <div class="tag-list"><el-tag v-for="t in tags" :key="t" type="info" size="small">{{ t }}</el-tag></div>
    </div>
    <ul class="img-list">
      <li v-for="img in imageList" :key="img.image">
        <img :src="img.image"/>
        <span>{{ img.name }}</span>
        <button @click="$emit('copy', img.image)"><i class="fas fa-copy"/></button>
        <button @click="$emit('delete-img', img.id)"><i class="fas fa-trash"/></button>
      </li>
    </ul>
  </aside>
</template>

<script setup>
defineProps(['imageList', 'categories', 'tags'])
defineEmits(['copy', 'delete-img'])
</script>