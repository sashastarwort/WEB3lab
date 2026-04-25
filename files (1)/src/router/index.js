import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const routes = [
  { path: '/', component: () => import('../views/HomeView.vue') },
  { path: '/login', component: () => import('../views/LoginView.vue') },
  { path: '/register', component: () => import('../views/RegisterView.vue') },
  { path: '/profile', component: () => import('../views/ProfileView.vue') },
  { path: '/about', component: () => import('../views/AboutView.vue') },
]

const router = createRouter({ history: createWebHistory(), routes })

export default router