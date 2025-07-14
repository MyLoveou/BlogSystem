import { createRouter, createWebHistory } from 'vue-router'
import Homepage from '@/views/Homepage.vue'
const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { name: 'homePage', component: Homepage, path: '' },
  ],
})

export default router
