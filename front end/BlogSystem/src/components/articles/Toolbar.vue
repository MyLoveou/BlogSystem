<template>
  <nav class="toolbar">
    <button @click="emit('wrapSelection', '**', '**')" title="粗体">
      <i class="fas fa-bold"></i>
    </button>
    <button @click="emit('wrapSelection', '*', '*')" title="斜体">
      <i class="fas fa-italic"></i>
    </button>
    <button @click="emit('insertAtLineStart', '## ')" title="标题">
      <i class="fas fa-heading"></i>
    </button>
    <button @click="emit('wrapSelection', '```', '\n```')" title="代码块">
      <i class="fas fa-code"></i>
    </button>
    <button @click="emit('insertAtLineStart', '- [ ] ')" title="任务列表">
      <i class="fas fa-tasks"></i>
    </button>
    <button @click="emit('insertLink')" title="链接">
      <i class="fas fa-link"></i>
    </button>
    <button @click="emit('insertImage')" title="图片">
      <i class="fas fa-image"></i>
    </button>
    <button @click="emit('insertFormula')" title="数学公式">
      <i class="fas fa-square-root-alt"></i>
    </button>

    <!-- 上传 .md 按钮 -->
    <input type="file" accept=".md" @change="emit('uploadMdFile', $event)" ref="mdFileInput" class="hidden" />
    <button @click="$refs.mdFileInput.click()" title="上传 .md">
      <i class="fas fa-file-upload"></i>
    </button>
    
    <!-- 元数据编辑按钮 -->
    <button @click="emit('showMetaDialog')" title="编辑元数据">
      <i class="fas fa-tags"></i>
    </button>
    
    <button @click="emit('submitArticle')" title="发布文章">
      <i class="fas fa-paper-plane"></i>
    </button>
  </nav>
</template>

<script setup>
defineEmits([
  'wrapSelection',
  'insertAtLineStart',
  'insertLink',
  'insertImage',
  'insertFormula',
  'uploadMdFile',
  'showMetaDialog',
  'submitArticle'
]);
</script>

<style scoped>
.toolbar {
  display: flex;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(15, 14, 23, 0.7);
  backdrop-filter: blur(10px);
  border-radius: var(--border-radius) var(--border-radius) 0 0;
  border: 1px solid rgba(122, 90, 245, 0.2);
  border-bottom: none;
  position: relative;
  z-index: 2;
}

.toolbar button {
  width: 38px;
  height: 38px;
  border: none;
  border-radius: 8px;
  background: rgba(122, 90, 245, 0.2);
  color: var(--light);
  cursor: pointer;
  transition: var(--transition);
  display: grid;
  place-items: center;
}

.toolbar button:hover {
  background: var(--primary);
  box-shadow: 0 0 10px var(--primary);
}

.hidden {
  display: none;
}
</style>