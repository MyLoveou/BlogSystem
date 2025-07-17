<template>
  <textarea 
    :value="source" 
    @input="$emit('update:source', $event.target.value)"
    @drop="onDrop"
    @paste="onPaste"
    class="editor"
    placeholder="开始写作吧 ~ 支持 ==高亮==、- [ ] 任务列表、表格、数学公式等"
  ></textarea>
</template>

<script setup>
defineProps({
  source: String
});

defineEmits(['update:source']);

const onDrop = (e) => {
  e.preventDefault();
  const file = e.dataTransfer.files[0];
  if (file && file.name.endsWith('.md')) {
    defineEmits('uploadMdFile', { target: { files: [file] } });
  }
};

const onPaste = (e) => {
  const items = e.clipboardData.items;
  for (const item of items) {
    if (item.kind === 'file' && item.type.startsWith('image/')) {
      alert('暂不支持粘贴图片，请先上传到图床再插入 URL');
    }
  }
};
</script>

<style scoped>
.editor {
  resize: none;
  outline: none;
  border-radius: 0 0 0 var(--border-radius);
  font-size: 1rem;
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
</style>