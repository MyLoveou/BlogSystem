import { createRouter, createWebHistory } from 'vue-router'
import Homepage from '@/views/Homepage.vue'
// import MarkdownEditor from '@/views/MarkdownEditor.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { name: 'homePage', component: Homepage, path: '' },
    { path: '/login', name: 'Login', component: () => import('@/views/Login.vue') },
    { name: 'editor', component: () => import('@/views/MarkdownEditor.vue'), path: '/editor' },
  ],
})

export default router
