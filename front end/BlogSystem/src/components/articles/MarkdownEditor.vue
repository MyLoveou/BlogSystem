<template>
  <section class="markdown-editor-wrapper">
    <nav class="toolbar">
      <button @click="wrapSelection('**', '**')" title="粗体">
        <i class="fas fa-bold"></i>
      </button>
      <button @click="wrapSelection('*', '*')" title="斜体">
        <i class="fas fa-italic"></i>
      </button>
      <button @click="insertAtLineStart('## ')" title="标题">
        <i class="fas fa-heading"></i>
      </button>
      <button @click="wrapSelection('```', '\n```')" title="代码块">
        <i class="fas fa-code"></i>
      </button>
      <button @click="insertAtLineStart('- [ ] ')" title="任务列表">
        <i class="fas fa-tasks"></i>
      </button>
      <button @click="insertLink()" title="链接">
        <i class="fas fa-link"></i>
      </button>
      <button @click="insertImage()" title="图片">
        <i class="fas fa-image"></i>
      </button>
      <button @click="insertFormula()" title="数学公式">
        <i class="fas fa-square-root-alt"></i>
      </button>

      <!-- 上传 .md 按钮 -->
      <input type="file" accept=".md" @change="uploadMdFile" ref="mdFileInput" class="hidden" />
      <button @click="$refs.mdFileInput.click()" title="上传 .md">
        <i class="fas fa-file-upload"></i>
      </button>
      <!-- 元数据编辑按钮 -->
      <button @click="showMetaDialog = true" title="编辑元数据">
        <i class="fas fa-tags"></i>
      </button>
      <button @click="submitArticle" title="发布文章">
        <i class="fas fa-paper-plane"></i>
      </button>
    </nav>
    <!-- 在toolbar下方添加 -->
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
     <!-- 元数据编辑对话框 -->
    <el-dialog v-model="showMetaDialog" title="编辑文章元数据" width="500px">
      <el-form label-width="80px">
        <el-form-item label="分类">
          <el-select
            v-model="metaData.categories"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="输入分类"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="标签">
          <el-select
            v-model="metaData.tags"
            multiple
            filterable
            allow-create
            default-first-option
            placeholder="输入标签"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showMetaDialog = false">取消</el-button>
        <el-button type="primary" @click="saveMetaData">保存</el-button>
      </template>
    </el-dialog>

    <!-- 编辑-预览 - 图片查看三栏 -->
    <div class="editor-container">
      <!-- 左侧图片上传栏 -->
      <aside class="image-panel">
        <h4><i class="fas fa-images"></i> 图片仓库</h4>
        <el-upload :http-request="customUpload" :before-upload="beforeUpload" :on-success="onImgSuccess" multiple>
          <i class="fas fa-cloud-upload-alt" />
          <div class="tip">拖拽或点击上传</div>
        </el-upload>
        <!-- 显示元数据 -->
        <div class="metadata-display" v-if="metaData.categories.length || metaData.tags.length">
          <h5>分类</h5>
          <div class="tag-list">
            <el-tag v-for="cat in metaData.categories" :key="cat" size="small">{{ cat }}</el-tag>
          </div>
          <h5>标签</h5>
          <div class="tag-list">
            <el-tag v-for="tag in metaData.tags" :key="tag" type="info" size="small">{{ tag }}</el-tag>
          </div>
        </div>

        <!-- 列表 -->
        <ul class="img-list">
          <li v-for="img in imageList" :key="img.image">
            <img :src="img.image" />
            <span>{{ img.name }}</span>
            <button @click="copy(img.image)"><i class="fas fa-copy"></i></button>
            <button @click="deleteImage(img.id)"><i class="fas fa-trash"></i></button>
          </li>
        </ul>
      </aside>
      <textarea v-model="source" @drop="onDrop" @paste="onPaste" @input="renderMd" class="editor"
        placeholder="开始写作吧 ~ 支持 ==高亮==、- [ ] 任务列表、表格、数学公式等"></textarea>

      <article class="preview" v-html="html" ref="preview"></article>

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
// 扩展插件
import mark from 'markdown-it-mark';
import taskLists from 'markdown-it-task-lists';
import anchor from 'markdown-it-anchor';
import toc from 'markdown-it-toc-done-right';
import katex from 'katex';
import 'katex/dist/katex.min.css';
// import { renderMathInElement } from 'katex';
import renderMathInElement from 'katex/contrib/auto-render/auto-render';
// import 'katex/dist/katex.css'; // 别忘了样式
import { debounce } from 'lodash-es';
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
})

// 对话框显示状态
const showMetaDialog = ref(false)

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
  .use(mark) // ==高亮==
  .use(taskLists) // - [x] 任务列表
  .use(anchor) // 标题锚点
  .use(toc); // 目录

// 渲染 Markdown（去除YAML部分）
const html = computed(() => {
  const content = source.value.replace(/^---[\s\S]*?---/, '').trim()
  return md.render(content)
});

// 解析YAML元数据
const parseMetaData = () => {
  const yamlMatch = source.value.match(/^---\n([\s\S]*?)\n---/)
  if (yamlMatch) {
    try {
      const parsed = yaml.load(yamlMatch[1])
      metaData.value = {
        categories: Array.isArray(parsed.categories) ? parsed.categories : [],
        tags: Array.isArray(parsed.tags) ? parsed.tags : []
      }
    } catch (e) {
      console.error('YAML解析失败:', e)
    }
  }
}

// 保存元数据到YAML
const saveMetaData = () => {
  const yamlStr = yaml.dump({
    categories: metaData.value.categories,
    tags: metaData.value.tags
  }, { lineWidth: -1 })
  
  const yamlBlock = `---\n${yamlStr}---`
  
  // 检查是否已存在YAML块
  if (/^---[\s\S]*?---/.test(source.value)) {
    source.value = source.value.replace(/^---[\s\S]*?---/, yamlBlock)
  } else {
    source.value = `${yamlBlock}\n\n${source.value}`
  }
  
  showMetaDialog.value = false
}


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

const onDrop = (e) => {
  e.preventDefault();
  const file = e.dataTransfer.files[0];
  if (file && file.name.endsWith('.md')) uploadMdFile({ target: { files: [file] } });
};

const onPaste = (e) => {
  const items = e.clipboardData.items;
  for (const item of items) {
    if (item.kind === 'file' && item.type.startsWith('image/')) {
      alert('暂不支持粘贴图片，请先上传到图床再插入 URL');
    }
  }
};

/* 渲染数学公式 */
const renderMath = () => {
  const preview = document.querySelector('.preview');
  renderMathInElement(preview, {
    delimiters: [
      { left: '$$', right: '$$', display: true },
      { left: '$', right: '$', display: false }
    ]
  });
};

/* 主逻辑 */
onMounted(() => {
  parseMetaData()
  fetchImages()
});

const renderMd = () => {
  renderMath();
  // 在这里可以添加其他渲染逻辑
};

/* 粒子背景 */
onMounted(() => {
  renderMd();
});

import { postArticle } from '@/apis/articles';
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

// 提交文章
const submitArticle = () => {
    // 设置内容字段
  article.value.content = source.value;
  article.value.html_content = html.value;
  // 前端验证
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



  // 提交请求
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
      // 处理错误
      if (error.response && error.response.status === 400) {
        ElMessage.error(`错误: ${error.response.data.error}`);
      } else {
        ElMessage.error('文章上传失败: ' + error.message);
      }
    });
};

import { ElMessage } from 'element-plus'

const { customUpload, imageList, onImgSuccess, beforeUpload, fetchImages, deleteImage } = useImageUpload()

// 复制到剪贴板
const copy = (url) => {
  navigator.clipboard.writeText(url)
  ElMessage.success('已复制')
}
// 改进：监听 source 的变化，实时解析
watch(source, debounce(() => {
  parseMetaData();        // 每当 Markdown 内容变化时重新解析元数据
}, 300), { deep: true }); // deep: true 确保能检测到字符串内部的变化
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
  overflow: hidden; /* 隐藏最外层滚动轴 */
}
/* 元数据显示样式 */
.metadata-display {
  margin: 15px 0;
  padding: 10px;
  background: rgba(122, 90, 245, 0.1);
  border-radius: 8px;
}

.metadata-display h5 {
  margin: 5px 0;
  color: var(--accent);
  font-size: 0.85rem;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 8px;
}

.tag-list .el-tag {
  margin: 2px;
}

.particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
}
/* 在style部分添加 */
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
/* 工具栏样式 */
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

/* 编辑器和预览器样式 */
.editor-container {
  display: grid;
  grid-template-columns: 200px 1fr 1fr;
  height: 70vh;
  height: calc(100vh - 180px); /* 动态计算高度，确保内容区域可滚动 */
  /* position: relative; */
  /* z-index: 1; */
}

.editor,
.preview {
  padding: 20px;
  background: rgba(15, 14, 23, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(122, 90, 245, 0.2);
  color: var(--light);
  line-height: 1.8;
  overflow-y: auto;
}

.editor {
  resize: none;
  outline: none;
  border-radius: 0 0 0 var(--border-radius);
  font-size: 1rem;
}

.preview {
  border-left: none;
  border-radius: 0 0 var(--border-radius) 0;
}

/* 数学公式样式 */
.preview :not(pre)>.katex {
  display: inline-block !important;
  margin: 0 4px;
  vertical-align: middle;
}

.preview .katex-block {
  display: block;
  margin: 1em 0;
  text-align: center;
}

/* 嵌套列表样式 - 修复的关键 */
.preview ul,
.preview ol {
  padding-left: 1.5em;
  margin: 1em 0;
}

.preview ul ul,
.preview ol ol,
.preview ul ol,
.preview ol ul {
  padding-left: 1.8em;
  margin: 0.5em 0;
}

.preview li {
  margin: 0.5em 0;
  position: relative;
}

.preview li::before {
  content: '';
  position: absolute;
  left: -1.2em;
  top: 0.7em;
  width: 6px;
  height: 6px;
  background: var(--primary);
  border-radius: 50%;
}

.preview ul ul li::before {
  background: var(--secondary);
}

.preview ul ul ul li::before {
  background: var(--accent);
}

.image-panel {
  background: rgba(15, 14, 23, 0.7);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(122, 90, 245, 0.2);
  border-left: none;
  border-radius: 0 0 var(--border-radius) 0;
  padding: 15px;
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 200px;
  overflow-y: auto;
}

.image-panel h4 {
  color: var(--accent);
  font-size: 1rem;
  margin: 0;
}

.uploader {
  border: 2px dashed var(--primary);
  border-radius: 8px;
  padding: 20px 5px;
  text-align: center;
  color: var(--gray);
}

.uploader:hover {
  border-color: var(--accent);
}

.img-list {
  list-style: none;
  padding: 0;
  margin: 0;
  flex: 1;
}

.img-list li {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.img-list img {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 6px;
}

.img-list span {
  flex: 1;
  font-size: 0.75rem;
  color: var(--light);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.img-list button {
  background: none;
  border: none;
  color: var(--accent);
  cursor: pointer;
}

/* 响应式增强：移动端隐藏侧边栏，改为抽屉 */
@media (max-width: 768px) {
  .editor-container {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;
  }

  .image-panel {
    display: none;
    /* 可用 <el-drawer> 触发 */
  }
}
</style>