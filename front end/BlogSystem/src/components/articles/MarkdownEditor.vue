<template>
  <section class="markdown-editor-wrapper">
    <Toolbar
      @wrap-selection="wrapSelection"
      @insert-at-line-start="insertAtLineStart"
      @insert-link="insertLink"
      @insert-image="insertImage"
      @insert-formula="insertFormula"
      @upload-md-file="uploadMdFile"
      @show-meta-dialog="showMetaDialog = true"
      @submit-article="submitArticle"
    />
    
    <ArticleMeta :article="article" />
    
    <MetaDataDialog
      v-model:showMetaDialog="showMetaDialog"
      :meta-data="metaData"
      @save="saveMetaData"
    />
    
    <div class="editor-container">
      <ImagePanel
        :meta-data="metaData"
        :image-list="imageList"
        :custom-upload="customUpload"
        :before-upload="beforeUpload"
        :on-img-success="onImgSuccess"
        :delete-image="deleteImage"
      />
      
      <Editor
        :source="source"
        @update:source="source = $event"
        @upload-md-file="uploadMdFile"
      />
      
      <Preview :html="html" />
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue';
import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js/lib/common';
import 'highlight.js/styles/atom-one-dark.css';
import useImageUpload from '@/apis/useImageUpload.js'
import yaml from 'js-yaml'
import mark from 'markdown-it-mark';
import taskLists from 'markdown-it-task-lists';
import anchor from 'markdown-it-anchor';
import toc from 'markdown-it-toc-done-right';
import katex from 'katex';
import 'katex/dist/katex.min.css';
import renderMathInElement from 'katex/contrib/auto-render/auto-render';
import { debounce } from 'lodash-es';
import { ElMessage } from 'element-plus'
import { postArticle } from '@/apis/articles';

import Toolbar from './Toolbar.vue';
import ArticleMeta from './ArticleMeta.vue';
import MetaDataDialog from './MetaDataDialog.vue';
import ImagePanel from './ImagePanel.vue';
import Editor from './Editor.vue';
import Preview from './Preview.vue';

// 初始 Markdown 内容
const source = ref(`---
categories:
  - 技术
  - Vue
tags:
  - markdown
  - 编辑器
  - 元数据
---

# Hello 星尘

> 在虚拟与现实之间寻找平衡 ✨

- 支持 **粗体**、*斜体*、==高亮==
- 任务列表：
  - [x] 完成组件开发
  - [ ] 上传测试
  - 嵌套列表：
    - 二级列表项 1
    - 二级列表项 2

## 代码示例

\`\`\`js
import { useMarkdown } from '@/composables/useMarkdown';
\`\`\`

## 数学公式

行内公式：$E = mc^2$

块级公式：
$$
\int_{-\infty}^\infty e^{-x^2} dx = \sqrt{\pi}
$$

| 库名         | 作用           |
|--------------|----------------|
| markdown-it  | 核心解析器     |
| highlight.js | 代码高亮       |
| mark         | ==高亮==扩展   |
| katex        | 数学公式渲染   |
`);

// 元数据
const metaData = ref({
  categories: [],
  tags: []
});

// 对话框显示状态
const showMetaDialog = ref(false);

// 文章表单数据
const article = ref({
  title: '',
  content: '',
  html_content: '',
  excerpt: '',
  categories: [],
  tags: [],
  status: 'published'
});

// 配置 Markdown-it
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight(str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang }).value}</code></pre>`;
      } catch { }
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`;
  },
})
  .use(mark)
  .use(taskLists)
  .use(anchor)
  .use(toc);

// 渲染 Markdown（去除YAML部分）
const html = computed(() => {
  const content = source.value.replace(/^---[\s\S]*?---/, '').trim();
  return md.render(content);
});

// 解析YAML元数据
const parseMetaData = () => {
  const yamlMatch = source.value.match(/^---\n([\s\S]*?)\n---/);
  if (yamlMatch) {
    try {
      const parsed = yaml.load(yamlMatch[1]);
      metaData.value = {
        categories: Array.isArray(parsed.categories) ? parsed.categories : [],
        tags: Array.isArray(parsed.tags) ? parsed.tags : []
      };
    } catch (e) {
      console.error('YAML解析失败:', e);
    }
  }
};

// 保存元数据到YAML
const saveMetaData = () => {
  const yamlStr = yaml.dump({
    categories: metaData.value.categories,
    tags: metaData.value.tags
  }, { lineWidth: -1 });
  
  const yamlBlock = `---\n${yamlStr}---`;
  
  if (/^---[\s\S]*?---/.test(source.value)) {
    source.value = source.value.replace(/^---[\s\S]*?---/, yamlBlock);
  } else {
    source.value = `${yamlBlock}\n\n${source.value}`;
  }
  
  showMetaDialog.value = false;
};

/* 工具栏功能 */
const wrapSelection = (prefix, suffix) => {
  const ta = document.querySelector('.editor');
  const start = ta.selectionStart;
  const end = ta.selectionEnd;
  const selected = ta.value.substring(start, end);
  source.value = ta.value.slice(0, start) + prefix + selected + suffix + ta.value.slice(end);
  ta.focus();
  ta.setSelectionRange(start + prefix.length, end + prefix.length);
};

const insertAtLineStart = (prefix) => {
  const ta = document.querySelector('.editor');
  const pos = ta.selectionStart;
  const lineStart = ta.value.lastIndexOf('\n', pos - 1) + 1;
  source.value = ta.value.slice(0, lineStart) + prefix + ta.value.slice(lineStart);
  ta.focus();
  ta.setSelectionRange(pos + prefix.length, pos + prefix.length);
};

const insertLink = () => {
  const url = prompt('请输入链接地址：');
  if (url) wrapSelection(`[${url}]`, '');
};

const insertImage = () => {
  const url = prompt('请输入图片地址：');
  if (url) wrapSelection(`![${url}]`, '');
};

const insertFormula = () => {
  const isBlock = confirm('是否插入块级公式？（否则为行内公式）');
  const ta = document.querySelector('.editor');
  const pos = ta.selectionStart;
  const lineStart = ta.value.lastIndexOf('\n', pos - 1) + 1;
  const prefix = isBlock ? '\n$$\n' : '';
  const suffix = isBlock ? '\n$$' : '';
  source.value = ta.value.slice(0, lineStart) + prefix + ta.value.slice(lineStart);
  ta.focus();
  ta.setSelectionRange(pos + prefix.length, pos + prefix.length);
};

/* 上传功能 */
const uploadMdFile = (e) => {
  const file = e.target.files[0];
  if (!file || !file.name.endsWith('.md')) return;
  const reader = new FileReader();
  reader.onload = (ev) => (source.value = ev.target.result);
  reader.readAsText(file, 'utf-8');
};

/* 渲染数学公式 */
const renderMath = () => {
  const preview = document.querySelector('.preview');
  if (preview) {
    renderMathInElement(preview, {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '$', right: '$', display: false }
      ]
    });
  }
};

const renderMd = () => {
  renderMath();
};

onMounted(() => {
  parseMetaData();
  fetchImages();
  renderMd();
});

// 图片上传相关逻辑
const { customUpload, imageList, onImgSuccess, beforeUpload, fetchImages, deleteImage } = useImageUpload();

// 提交文章
const submitArticle = () => {
  article.value.content = source.value;
  article.value.html_content = html.value;
  
  if (!article.value.title.trim()) {
    ElMessage.error('请输入文章标题');
    return;
  }
  
  if (!article.value.content.trim()) {
    ElMessage.error('请输入文章内容');
    return;
  }
  
  if (!article.value.excerpt.trim()) {
    ElMessage.error('请输入文章摘要');
    return;
  }

  // 设置分类和标签
  article.value.categories = metaData.value.categories;
  article.value.tags = metaData.value.tags;

  postArticle(article.value)
    .then(() => {
      ElMessage.success('文章上传成功！');
      // 清空表单
      article.value = {
        title: '',
        content: '',
        html_content: '',
        excerpt: '',
        categories: [],
        tags: [],
        status: 'published'
      };
      source.value = '';
    })
    .catch((error) => {
      if (error.response && error.response.status === 400) {
        ElMessage.error(`错误: ${error.response.data.error}`);
      } else {
        ElMessage.error('文章上传失败: ' + error.message);
      }
    });
};

watch(source, debounce(() => {
  parseMetaData();
  renderMath();
}, 300), { deep: true });
</script>

<style scoped>
/* 主题变量 */
:root {
  --primary: #7a5af5;
  --secondary: #ff6b9c;
  --accent: #00d0ff;
  --dark: #0f0e17;
  --darker: #0a0a12;
  --light: #fffffe;
  --gray: #a7a9be;
  --border-radius: 16px;
  --transition: all 0.3s ease;
}

.markdown-editor-wrapper {
  position: relative;
  padding: 20px;
  font-family: 'Noto Sans SC', sans-serif;
  min-height: 80vh;
  overflow: hidden;
}

.editor-container {
  display: grid;
  grid-template-columns: 200px 1fr 1fr;
  height: calc(100vh - 180px);
}

@media (max-width: 768px) {
  .editor-container {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;
  }
}
</style>