import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api'

export const useAlarmsStore = defineStore('alarms', () => {
  const alarms  = ref([])
  const loading = ref(false)
  const error   = ref(null)

  async function fetchAlarms() {
    loading.value = true
    error.value   = null
    try {
      const res    = await api.get('/alarms')
      alarms.value = res.data
    } catch (e) {
      error.value = e.response?.data?.error || 'Помилка завантаження'
    } finally {
      loading.value = false
    }
  }

  async function addAlarm(payload) {
    const res = await api.post('/alarms', payload)
    alarms.value.push(res.data)
    return res.data
  }

  async function toggleAlarm(id) {
    const alarm = alarms.value.find(a => a.id === id)
    if (!alarm) return
    const res = await api.patch(`/alarms/${id}`, { enabled: !alarm.enabled })
    Object.assign(alarm, res.data)
  }

  async function markFired(id) {
    const alarm = alarms.value.find(a => a.id === id)
    if (!alarm) return
    const res = await api.patch(`/alarms/${id}`, { fired: true })
    Object.assign(alarm, res.data)
  }

  async function removeAlarm(id) {
    await api.delete(`/alarms/${id}`)
    alarms.value = alarms.value.filter(a => a.id !== id)
  }

  function countdown(dt) {
    const diff = new Date(dt) - new Date()
    if (diff <= 0) return null
    const h = Math.floor(diff / 3_600_000)
    const m = Math.floor((diff % 3_600_000) / 60_000)
    const s = Math.floor((diff % 60_000) / 1_000)
    if (h > 0) return `${h}г ${m}хв`
    if (m > 0) return `${m}хв ${s}с`
    return `${s}с`
  }

  return { alarms, loading, error, fetchAlarms, addAlarm, toggleAlarm, markFired, removeAlarm, countdown }
})
