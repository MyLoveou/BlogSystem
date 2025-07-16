<template>
  <section class="markdown-editor-wrapper">
    <!-- 粒子背景 -->
    <div class="particles" ref="particles"></div>

    <!-- 工具栏 -->
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
    </nav>

    <!-- 编辑-预览双栏 -->
    <div class="editor-container">
      <textarea
        v-model="source"
        @drop="onDrop"
        @paste="onPaste"
        @input="renderMd"
        class="editor"
        placeholder="开始写作吧 ~ 支持 ==高亮==、- [ ] 任务列表、表格、数学公式等"
      ></textarea>

      <article class="preview" v-html="html" ref="preview"></article>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import MarkdownIt from 'markdown-it';
import hljs from 'highlight.js/lib/common';
import 'highlight.js/styles/atom-one-dark.css';

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

// 初始 Markdown 内容
const source = ref(`# Hello 星尘

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

行内公式：\(E = mc^2\)

块级公式：
\[
\int_{-\infty}^\infty e^{-x^2} dx = \sqrt{\pi}
\]

| 库名         | 作用           |
|--------------|----------------|
| markdown-it  | 核心解析器     |
| highlight.js | 代码高亮       |
| mark         | ==高亮==扩展   |
| katex        | 数学公式渲染   |
`);

// 配置 Markdown-it
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight(str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang }).value}</code></pre>`;
      } catch {}
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`;
  },
})
  .use(mark) // ==高亮==
  .use(taskLists) // - [x] 任务列表
  .use(anchor) // 标题锚点
  .use(toc); // 目录

// 渲染 Markdown
const html = computed(() => md.render(source.value));

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
  renderMd();
});

const renderMd = () => {
  renderMath();
  // 在这里可以添加其他渲染逻辑
};

/* 粒子背景 */
onMounted(() => {
  const particlesContainer = document.querySelector('.particles');
  for (let i = 0; i < 30; i++) {
    const particle = document.createElement('div');
    particle.className = 'particle';
    particle.style.width = particle.style.height = `${Math.random() * 10 + 3}px`;
    particle.style.left = `${Math.random() * 100}%`;
    particle.style.top = `${Math.random() * 100}%`;
    particle.style.background = ['#7a5af5', '#ff6b9c', '#00d0ff'][i % 3];
    particle.style.animationDuration = `${Math.random() * 20 + 10}s`;
    particlesContainer.appendChild(particle);
  }
  // 初始化渲染
  renderMd();
});
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
}

.particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 0;
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
  grid-template-columns: 1fr 1fr;
  height: 70vh;
  position: relative;
  z-index: 1;
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
.preview :not(pre) > .katex {
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
.preview ul, .preview ol {
  padding-left: 1.5em;
  margin: 1em 0;
}

.preview ul ul, .preview ol ol, 
.preview ul ol, .preview ol ul {
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
/* 响应式布局 */
@media (max-width: 768px) {
  .editor-container {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;
  }
  .editor,
  .preview {
    border-radius: 0;
  }
}
</style>