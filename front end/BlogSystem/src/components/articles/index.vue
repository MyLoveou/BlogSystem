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
      <input v-model="article.title" placeholder="文章标题" class="title-input" required />
      <textarea v-model="article.excerpt" placeholder="文章摘要（最多200字）" maxlength="200" class="excerpt-input"></textarea>
    </div>
    <!-- 元数据编辑对话框 -->
    <el-dialog v-model="showMetaDialog" title="编辑文章元数据" width="500px">
      <el-form label-width="80px">
        <el-form-item label="分类">
          <el-select v-model="metaData.categories" multiple filterable allow-create default-first-option
            placeholder="输入分类" style="width: 100%"> 
            <el-option v-for="c in allCategories" :key="c" :label="c" :value="c" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="metaData.tags" multiple filterable allow-create default-first-option placeholder="输入标签"
            style="width: 100%">
            <el-option v-for="t in allTags" :key="t" :label="t" :value="t" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showMetaDialog = false">取消</el-button>
        <el-button type="primary" @click="saveMetaData">保存</el-button>
      </template>
    </el-dialog>

    <!-- ===================== 新布局：左右两栏 + 分隔线 ===================== -->
    <div class="editor-container">
      <!-- 左侧编辑器 -->
      <textarea v-model="source" @drop="onDrop" @paste="onPaste" @input="renderMd" class="editor"
        placeholder="开始写作吧 ~" />
      <!-- 可拖拽分隔线 -->
      <div class="split-line" @mousedown="startDrag"></div>
      <!-- 右侧预览 -->
      <article class="preview" v-html="html" ref="preview"></article>
    </div>

    <!-- ===================== 图片仓库抽屉 ===================== -->
    <el-drawer v-model="showDrawer" title="图片仓库" direction="rtl" size="280px">
      <aside class="image-panel-drawer">
        <el-upload :http-request="customUpload" :before-upload="beforeUpload" :on-success="onImgSuccess" multiple drag>
          <i class="fas fa-cloud-upload-alt" style="font-size:32px;color:var(--accent)" />
          <div class="tip">拖拽或点击上传</div>
        </el-upload>

        <ul class="img-list">
          <li v-for="img in imageList" :key="img.image">
            <img :src="img.image" />
            <span>{{ img.name }}</span>
            <div class="img-actions">
              <button @click="copy(img.image)"><i class="fas fa-copy" /></button>
              <button @click="deleteImage(img.id)"><i class="fas fa-trash" /></button>
            </div>
          </li>
        </ul>
      </aside>
    </el-drawer>

    <!-- 右下角唤起图片仓库的悬浮按钮 -->
    <el-button circle class="float-img-btn" @click="showDrawer = true">
      <i class="fas fa-images" />
    </el-button>
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
import { postArticle, getCategoryList, getTagList, createCategory, createTag } from '@/apis/articles'

// 统一把“本地字符串数组”与“后端返回数组”比对，对缺失项调用创建接口
// const ensureBackendItems = async ( localArr, remoteArr, createFn ) => {
//   // console.log(localArr)
//   const remoteNames = new Set(remoteArr.map(r => r.name))
//   const toCreate = localArr.filter(name => !remoteNames.has(name))
//   console.log(toCreate)

//   // 并发创建
//   const created = await Promise.all(
//     toCreate.map(name => createFn(name).then(res => res.data))
//   )
//   // 合并：已有 + 新建
//   return [
//     ...remoteArr.filter(r => localArr.includes(r.name)),
//     ...created
//   ]
// }
// 初始 Markdown 内容
const source = ref(`---
categories:
  - 技术
  - Vue
tags:
  - markdown
  - 编辑器
  - 元数据
cover_image:
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
  tags: [],
  cover_image: '',
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
        tags: Array.isArray(parsed.tags) ? parsed.tags : [],
        cover_image: parsed.cover_image || '',
      }
      console.log(metaData.value)
    } catch (e) {
      console.error('YAML解析失败:', e)
    }
  }
}

// 保存元数据到YAML
const saveMetaData = async () => {

  // 1. 拿到用户最终选择/输入的数组（包含新建）
  const localCats = metaData.value.categories
  const localTags = metaData.value.tags

  // // 2. 与后端比对，新建没有的
  // const finalCats = await ensureBackendItems(localCats, allCategories.value, createCategory)
  // const finalTags = await ensureBackendItems(localTags, allTags.value, createTag)
  console.log(localCats, localTags, 1)

  // 3. 回写到 article
  article.value.categories = localCats.map(c => c.name)
  article.value.tags = localTags.map(t => t.name)
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
const allCategories = ref([])
const allTags = ref([])
/* 主逻辑 */
onMounted(async () => {
  parseMetaData()
  fetchImages()
  renderMd()
  const [cats, tags] = await Promise.all([getCategoryList(), getTagList()])
  console.log(cats,tags)
  allCategories.value = cats.map(c => c.name)
  allTags.value = tags.map(t => t.name)
});

const renderMd = () => {
  renderMath();
  // 在这里可以添加其他渲染逻辑
};

// 文章表单数据
const article = ref({
  title: '',
  content: '',
  cover_image: '',
  html_content: '',
  excerpt: '',
  categories: [],
  tags: [],
  status: 'published'
});

// 提交文章
const submitArticle = () => {
  // 设置内容字段
  article.value.content = source.value
  article.value.html_content = html.value
  article.value.tags = metaData.value.tags
  article.value.categories = metaData.value.categories
  console.log(article.value)
  // article.value.excerpt
  // artice.value.cover_image
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

const showDrawer = ref(false)

/* 分隔线拖拽逻辑（简单版） */
const isDragging = ref(false)
const editorContainer = ref(null)
function startDrag(e) {
  isDragging.value = true
  document.addEventListener('mousemove', onDrag)
  document.addEventListener('mouseup', stopDrag)
}
function onDrag(e) {
  if (!isDragging.value) return
  const containerRect = editorContainer.value.getBoundingClientRect()
  const percent = ((e.clientX - containerRect.left) / containerRect.width) * 100
  if (percent < 20 || percent > 80) return
  editorContainer.value.style.gridTemplateColumns = `${percent}% 4px ${100 - percent}%`
}
function stopDrag() {
  isDragging.value = false
  document.removeEventListener('mousemove', onDrag)
  document.removeEventListener('mouseup', stopDrag)
}





</script>

<style scoped>
/* ===== 全局变量 ===== */
:root {
  --primary: #7a5af5;
  --secondary: #ff6b9c;
  --accent: #00d0ff;
  --dark: #0f0e17;
  --darker: #0a0a12;
  --light: #fffffe;
  --gray: #a7a9be;
  --radius: 12px;
  --shadow: 0 8px 32px rgba(15, 14, 23, .6);
  --transition: all .25s ease;
}

/* ===== 滚动条 ===== */
::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

::-webkit-scrollbar-track {
  background: transparent;
}

::-webkit-scrollbar-thumb {
  background: var(--primary);
  border-radius: 3px;
}

/* ===== 外层 ===== */
.markdown-editor-wrapper {
  height: 100vh;
  background: linear-gradient(135deg, #0f0e17 0%, #1a1929 100%);
  display: flex;
  flex-direction: column;
  color: var(--light);
  font-family: 'Noto Sans SC', sans-serif;
  overflow: hidden;
}

/* ===== 工具栏 ===== */
.toolbar {
  display: flex;
  gap: 8px;
  padding: 12px 20px;
  background: rgba(15, 14, 23, .7);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(122, 90, 245, .2);
}

.toolbar button {
  width: 40px;
  height: 40px;
  border: none;
  border-radius: var(--radius);
  background: rgba(122, 90, 245, .15);
  color: var(--light);
  transition: var(--transition);
  display: grid;
  place-items: center;
}

.toolbar button:hover {
  background: var(--primary);
  box-shadow: 0 0 12px var(--primary);
}

/* ===== 标题 / 摘要 ===== */
.article-meta {
  padding: 15px 20px;
  background: rgba(15, 14, 23, .5);
  border-bottom: 1px solid rgba(122, 90, 245, .2);
}

.title-input {
  width: 100%;
  font-size: 1.6rem;
  background: transparent;
  border: none;
  color: var(--light);
  outline: none;
  margin-bottom: 10px;
}

.excerpt-input {
  width: 100%;
  min-height: 60px;
  resize: vertical;
  background: transparent;
  border: none;
  color: var(--gray);
  outline: none;
}

/* ===== 左右两栏 + 分隔线 ===== */
.editor-container {
  flex: 1;
  display: grid;
  grid-template-columns: 55% 4px 1fr;
  height: 0;
  /* 让 flex 撑开 */
}

.editor,
.preview {
  padding: 20px;
  background: rgba(15, 14, 23, .6);
  backdrop-filter: blur(10px);
  border: none;
  color: var(--light);
  line-height: 1.8;
  overflow-y: auto;
}

.editor {
  resize: none;
  outline: none;
  border-radius: 0;
  font-size: 1rem;
}

.preview {
  border-radius: 0;
}

.split-line {
  background: rgba(122, 90, 245, .2);
  cursor: col-resize;
  transition: var(--transition);
}

.split-line:hover {
  background: var(--primary);
}

/* ===== 预览区美化 ===== */
.preview h1,
.preview h2,
.preview h3,
.preview h4,
.preview h5,
.preview h6 {
  margin: 1.2em 0 .6em;
  color: var(--accent);
  font-weight: 600;
}

.preview code {
  background: rgba(0, 208, 255, .12);
  color: var(--accent);
  padding: 2px 6px;
  border-radius: 4px;
}

.preview pre {
  background: var(--darker);
  border-left: 4px solid var(--primary);
  padding: 16px;
  border-radius: var(--radius);
  overflow-x: auto;
}

.preview blockquote {
  border-left: 4px solid var(--secondary);
  padding-left: 1em;
  color: var(--gray);
  font-style: italic;
}

.preview table {
  width: 100%;
  border-collapse: collapse;
  margin: 1em 0;
}

.preview th,
.preview td {
  padding: 8px 12px;
  border: 1px solid rgba(122, 90, 245, .2);
}

.preview th {
  background: rgba(122, 90, 245, .15);
}

/* ===== 图片仓库抽屉 ===== */
.image-panel-drawer {
  padding: 0 10px;
}

.img-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.img-list li {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 10px 0;
}

.img-list img {
  width: 50px;
  height: 50px;
  object-fit: cover;
  border-radius: var(--radius);
}

.img-list span {
  flex: 1;
  font-size: .8rem;
  color: var(--light);
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.img-actions button {
  background: none;
  border: none;
  color: var(--accent);
  margin: 3px;
  cursor: pointer;
  transition: var(--transition);
}

.img-actions button:hover {
  color: var(--secondary);
}

/* ===== 悬浮按钮 ===== */
.float-img-btn {
  position: fixed;
  right: 30px;
  bottom: 30px;
  width: 56px;
  height: 56px;
  z-index: 1000;
  background: var(--primary);
  color: var(--light);
  box-shadow: var(--shadow);
}

.float-img-btn:hover {
  background: var(--secondary);
}

/* ===== 移动端适配 ===== */
@media (max-width: 768px) {
  .editor-container {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr 1fr;
  }

  .split-line {
    display: none;
  }
}
</style>