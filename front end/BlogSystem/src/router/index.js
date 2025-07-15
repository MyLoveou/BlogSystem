import { createRouter, createWebHistory } from 'vue-router'
import Homepage from '@/views/Homepage.vue'
import MarkdownEditor from '@/views/MarkdownEditor.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { name: 'homePage', component: Homepage, path: '' },
    { name: 'editor', component: MarkdownEditor, path: '/editor' },
  ],
})

export default router
