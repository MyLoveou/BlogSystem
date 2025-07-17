<template>
  <article class="preview" v-html="html"></article>
</template>

<script setup>
defineProps({
  html: String
});
</script>

<style scoped>
.preview {
  border-left: none;
  border-radius: 0 0 var(--border-radius) 0;
  padding: 20px;
  background: rgba(15, 14, 23, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(122, 90, 245, 0.2);
  color: var(--light);
  line-height: 1.8;
  overflow-y: auto;
  width: 100%;
  height: 100%;
}

/* 数学公式样式 */
:deep(.preview) :not(pre)>.katex {
  display: inline-block !important;
  margin: 0 4px;
  vertical-align: middle;
}

:deep(.preview) .katex-block {
  display: block;
  margin: 1em 0;
  text-align: center;
}

/* 嵌套列表样式 */
:deep(.preview) ul,
:deep(.preview) ol {
  padding-left: 1.5em;
  margin: 1em 0;
}

:deep(.preview) ul ul,
:deep(.preview) ol ol,
:deep(.preview) ul ol,
:deep(.preview) ol ul {
  padding-left: 1.8em;
  margin: 0.5em 0;
}

:deep(.preview) li {
  margin: 0.5em 0;
  position: relative;
}

:deep(.preview) li::before {
  content: '';
  position: absolute;
  left: -1.2em;
  top: 0.7em;
  width: 6px;
  height: 6px;
  background: var(--primary);
  border-radius: 50%;
}

:deep(.preview) ul ul li::before {
  background: var(--secondary);
}

:deep(.preview) ul ul ul li::before {
  background: var(--accent);
}
</style>