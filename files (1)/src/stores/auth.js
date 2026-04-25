import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('ml_alarm_token') || null)
  const user = ref(null)
  const isLoggedIn = computed(() => !!token.value && !!user.value)

  async function fetchMe() {
    if (!token.value) return
    try {
      const res = await api.get('/auth/me')
      user.value = res.data
    } catch {
      logout()
    }
  }

  async function login(payload) {
    const res = await api.post('/auth/login', payload)
    localStorage.setItem('ml_alarm_token', res.data.token)
    token.value = res.data.token
    user.value = res.data.user
  }

  async function register(payload) {
    const res = await api.post('/auth/register', payload)
    localStorage.setItem('ml_alarm_token', res.data.token)
    token.value = res.data.token
    user.value = res.data.user
  }

  async function updateProfile(payload) {
    const res = await api.patch('/auth/me', payload)
    user.value = res.data
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('ml_alarm_token')
  }

  return { token, user, isLoggedIn, fetchMe, login, register, updateProfile, logout }
})