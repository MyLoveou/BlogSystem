import { ref, computed, watch, onMounted } from 'vue'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js/lib/common'
import 'highlight.js/styles/atom-one-dark.css'
import mark from 'markdown-it-mark'
import taskLists from 'markdown-it-task-lists'
import anchor from 'markdown-it-anchor'
import toc from 'markdown-it-toc-done-right'
import katex from 'katex'
import 'katex/dist/katex.min.css'
import renderMathInElement from 'katex/contrib/auto-render/auto-render'
import yaml from 'js-yaml'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { debounce } from 'lodash-es'
import useImageUpload from '@/apis/useImageUpload'

const md = new MarkdownIt({
  html: true, linkify: true, typographer: true,
  highlight: (str, lang) => lang && hljs.getLanguage(lang)
    ? `<pre class="hljs"><code>${hljs.highlight(str, { language: lang }).value}</code></pre>`
    : `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`
}).use(mark).use(taskLists).use(anchor).use(toc)

const source     = ref('')
const html       = computed(() => md.render(source.value.replace(/^---[\s\S]*?---/, '').trim()))
const metaData   = ref({ categories: [], tags: [] })
const article    = ref({ title: '', content: '', html_content: '', excerpt: '', categories: [], tags: [], status: 'published' })
const imageList  = ref([])
const showMetaDialog = ref(false)

// 图片仓库逻辑
const { customUpload, onImgSuccess, beforeUpload, fetchImages, deleteImage } = useImageUpload()
const copy = url => { navigator.clipboard.writeText(url); ElMessage.success('已复制') }

// 解析 YAML
const parseMetaData = () => {
  const match = source.value.match(/^---\n([\s\S]*?)\n---/)
  if (match) try {
    const parsed = yaml.load(match[1])
    metaData.value = { categories: parsed.categories || [], tags: parsed.tags || [] }
  } catch (e) { console.error('YAML解析失败:', e) }
}
const saveMetaData = () => {
  const block = `---\n${yaml.dump(metaData.value, { lineWidth: -1 })}---`
  source.value = source.value.replace(/^---[\s\S]*?---/, block) || `${block}\n\n${source.value}`
  showMetaDialog.value = false
}

// 工具栏命令
const wrapSelection = (prefix, suffix) => {
  const ta = document.querySelector('.editor')
  const [s, e] = [ta.selectionStart, ta.selectionEnd]
  const selected = ta.value.substring(s, e)
  ta.value = ta.value.slice(0, s) + prefix + selected + suffix + ta.value.slice(e)
  ta.focus()
  ta.setSelectionRange(s + prefix.length, e + prefix.length)
}
const insertAtLineStart = prefix => {
  const ta = document.querySelector('.editor')
  const pos = ta.selectionStart
  const lineStart = ta.value.lastIndexOf('\n', pos - 1) + 1
  ta.value = ta.value.slice(0, lineStart) + prefix + ta.value.slice(lineStart)
  ta.focus()
  ta.setSelectionRange(pos + prefix.length, pos + prefix.length)
}
const insertLink = () => {
  const url = prompt('请输入链接地址：')
  url && wrapSelection(`[${url}]`, '')
}
const insertImage = () => {
  const url = prompt('请输入图片地址：')
  url && wrapSelection(`![${url}]`, '')
}
const insertFormula = () => {
  const isBlock = confirm('是否插入块级公式？')
  isBlock ? insertAtLineStart('\n$$\n') : insertAtLineStart('$')
}

// 上传 & 拖放
const uploadMdFile = e => {
  const file = e.target.files[0]
  if (!file || !file.name.endsWith('.md')) return
  const reader = new FileReader()
  reader.onload = ev => { source.value = ev.target.result; parseMetaData() }
  reader.readAsText(file, 'utf-8')
}
const onDrop = e => {
  e.preventDefault()
  uploadMdFile({ target: { files: [e.dataTransfer.files[0]] } })
}
const onPaste = e => {
  [...e.clipboardData.items].forEach(item => {
    if (item.kind === 'file' && item.type.startsWith('image/')) {
      alert('暂不支持粘贴图片，请先上传到图床再插入 URL')
    }
  })
}

const renderMd = () => {
  nextTick(() => {
    const preview = document.querySelector('.preview')
    if (preview) {
      renderMathInElement(preview, {
        delimiters: [{ left: '$$', right: '$$', display: true }, { left: '$', right: '$', display: false }]
      })
    }
  })
}
const renderMath = () => {
  renderMathInElement(document.querySelector('.preview'), {
    delimiters: [{ left: '$$', right: '$$', display: true }, { left: '$', right: '$', display: false }]
  })
}

// 发布文章
const submitArticle = async () => {
  if (!article.value.title.trim()) return ElMessage.error('请输入文章标题')
  if (!article.value.excerpt.trim()) return ElMessage.error('请输入摘要')
  article.value.content = source.value
  article.value.html_content = html.value

  const payload = {
    ...article.value,
    category_ids: await strArr2Ids(metaData.value.categories, 'categories'),
    tag_ids: await strArr2Ids(metaData.value.tags, 'tags')
  }

  try {
    await axios.post('/api/articles/', payload)
    ElMessage.success('文章发布成功')
    Object.assign(article.value, { title: '', excerpt: '', content: '', html_content: '', categories: [], tags: [] })
    source.value = ''
  } catch (e) {
    const msg = e.response?.data?.detail || e.response?.data || e.message
    ElMessage.error(typeof msg === 'string' ? msg : JSON.stringify(msg))
  }
}

// 把字符串 => id
async function strArr2Ids(names, endpoint) {
  if (!names.length) return []
  const ids = []
  for (const name of names) {
    const { data } = await axios.get(`/${endpoint}/?search=${encodeURIComponent(name)}`)
    if (data.results.length) {
      ids.push(data.results[0].id)
    } else {
      const { data: created } = await axios.post(`/${endpoint}/`, { name })
      ids.push(created.id)
    }
  }
  return ids
}

watch(source, debounce(parseMetaData, 300), { deep: true })

export default function useMarkdown() {
  return {
    source, html, metaData, article, imageList, showMetaDialog,
    renderMd, parseMetaData, saveMetaData, onDrop, onPaste, uploadMdFile, copy, deleteImage,
    wrapSelection, insertAtLineStart, insertLink, insertImage, insertFormula, submitArticle
  }
}