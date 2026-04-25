<template>
  <main class="container flex-grow-1 d-flex justify-content-center align-items-center pt-5 mt-5 pb-4">
    <div class="card card-custom bg-dark shadow-lg rounded-3 w-100" style="max-width:450px;">
      <div class="card-body p-5">
        <div class="text-center mb-4">
          <i class="bi bi-box-arrow-in-right text-warning d-block mb-2" style="font-size:2.5rem;"></i>
          <h2 class="card-title text-warning fw-bold">Авторизація</h2>
          <p class="text-secondary small">Введи свої дані для входу</p>
        </div>

        <div v-if="error" class="alert alert-danger small mb-3">{{ error }}</div>
        <div v-if="success" class="alert alert-success small mb-3">{{ success }}</div>

        <div class="mb-3">
          <label class="form-label text-secondary small">Електронна пошта</label>
          <div class="input-group">
            <span class="input-group-text bg-black border-secondary">
              <i class="bi bi-envelope text-muted"></i>
            </span>
            <input v-model="form.email" type="email"
              class="form-control border-secondary"
              :class="{ 'is-invalid': errors.email }"
              placeholder="name@example.com"
              @keydown.enter="handleLogin" />
            <div class="invalid-feedback">{{ errors.email }}</div>
          </div>
        </div>

        <div class="mb-4">
          <label class="form-label text-secondary small">Пароль</label>
          <div class="input-group">
            <span class="input-group-text bg-black border-secondary">
              <i class="bi bi-lock text-muted"></i>
            </span>
            <input v-model="form.password" :type="showPass ? 'text' : 'password'"
              class="form-control border-secondary"
              :class="{ 'is-invalid': errors.password }"
              placeholder="••••••••"
              @keydown.enter="handleLogin" />
            <button class="btn btn-outline-secondary border-secondary" type="button"
              @click="showPass = !showPass">
              <i :class="`bi bi-${showPass ? 'eye-slash' : 'eye'}`"></i>
            </button>
            <div class="invalid-feedback">{{ errors.password }}</div>
          </div>
        </div>

        <button class="btn btn-warning w-100 text-dark fw-bold shadow-sm mb-3"
          :disabled="loading" @click="handleLogin">
          <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
          <i v-else class="bi bi-check2-circle me-1"></i>Увійти
        </button>

        <div class="text-center">
          <small class="text-secondary">
            Ще немає акаунта?
            <RouterLink to="/register" class="text-warning text-decoration-none fw-semibold">
              Створити зараз
            </RouterLink>
          </small>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth    = useAuthStore()
const router  = useRouter()
const loading = ref(false)
const showPass = ref(false)
const error   = ref('')
const success = ref('')
const errors  = reactive({ email: '', password: '' })

const form = reactive({ email: '', password: '' })

function validate() {
  errors.email = errors.password = ''
  let ok = true
  if (!form.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    errors.email = 'Введіть коректний email'; ok = false
  }
  if (!form.password) {
    errors.password = 'Введіть пароль'; ok = false
  }
  return ok
}

async function handleLogin() {
  error.value = ''
  if (!validate()) return
  loading.value = true
  try {
    await auth.login({ email: form.email, password: form.password })
    success.value = 'Вхід успішний! Переходимо...'
    setTimeout(() => router.push('/'), 800)
  } catch (e) {
    error.value = e.response?.data?.error || 'Помилка входу'
  } finally {
    loading.value = false
  }
}
</script>
