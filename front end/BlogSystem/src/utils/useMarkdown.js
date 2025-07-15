import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js/lib/common'
import mark from 'markdown-it-mark'
import taskLists from 'markdown-it-task-lists'
import anchor from 'markdown-it-anchor'
import toc from 'markdown-it-toc-done-right'
import 'highlight.js/styles/atom-one-dark.css'

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight(str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return `<pre class="hljs"><code>${hljs.highlight(str, { language: lang }).value}</code></pre>`
      } catch {}
    }
    return `<pre class="hljs"><code>${md.utils.escapeHtml(str)}</code></pre>`
  }
})
  .use(mark)           // ==高亮==
  .use(taskLists)      // - [x] 任务列表
  .use(anchor)         // 标题锚点
  .use(toc)            // 目录

export default function useMarkdown() {
  return (src) => md.render(src)
}