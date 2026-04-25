<template>
  <main class="container flex-grow-1 d-flex justify-content-center align-items-center pt-5 mt-5 pb-4">
    <div class="card card-custom bg-dark shadow-lg rounded-3 w-100" style="max-width:500px;">
      <div class="card-body p-4 p-md-5">
        <div class="text-center mb-4">
          <i class="bi bi-person-plus text-warning d-block mb-2" style="font-size:2.5rem;"></i>
          <h2 class="card-title text-warning fw-bold">Реєстрація</h2>
          <p class="text-secondary small">Створіть свій профіль у ML Alarm</p>
        </div>

        <div v-if="error" class="alert alert-danger small mb-3">{{ error }}</div>
        <div v-if="success" class="alert alert-success small mb-3">{{ success }}</div>

        <!-- Name -->
        <div class="mb-3">
          <label class="form-label text-secondary small">Ім'я та Прізвище</label>
          <div class="input-group">
            <span class="input-group-text bg-black border-secondary"><i class="bi bi-person text-muted"></i></span>
            <input v-model="form.name" type="text" class="form-control border-secondary"
              :class="{ 'is-invalid': errors.name }" placeholder="Введіть ваше ім'я" />
            <div class="invalid-feedback">{{ errors.name }}</div>
          </div>
        </div>

        <!-- Email -->
        <div class="mb-3">
          <label class="form-label text-secondary small">Електронна пошта</label>
          <div class="input-group">
            <span class="input-group-text bg-black border-secondary"><i class="bi bi-envelope text-muted"></i></span>
            <input v-model="form.email" type="email" class="form-control border-secondary"
              :class="{ 'is-invalid': errors.email }" placeholder="ivan@example.com" />
            <div class="invalid-feedback">{{ errors.email }}</div>
          </div>
        </div>

        <!-- Gender -->
        <div class="mb-3">
          <label class="form-label d-block text-secondary small">Стать</label>
          <div class="d-flex gap-4 p-2 bg-black bg-opacity-25 rounded border border-secondary border-opacity-25"
            :class="{ 'border-danger': errors.gender }">
            <div class="form-check">
              <input v-model="form.gender" class="form-check-input border-secondary" type="radio"
                id="genderMale" value="male" />
              <label class="form-check-label text-light small" for="genderMale">Чоловіча</label>
            </div>
            <div class="form-check">
              <input v-model="form.gender" class="form-check-input border-secondary" type="radio"
                id="genderFemale" value="female" />
              <label class="form-check-label text-light small" for="genderFemale">Жіноча</label>
            </div>
          </div>
          <div v-if="errors.gender" class="text-danger small mt-1">{{ errors.gender }}</div>
        </div>

        <!-- DOB -->
        <div class="mb-3">
          <label class="form-label text-secondary small">Дата народження</label>
          <div class="input-group">
            <span class="input-group-text bg-black border-secondary"><i class="bi bi-calendar3 text-muted"></i></span>
            <input v-model="form.dob" type="date" class="form-control border-secondary"
              :class="{ 'is-invalid': errors.dob }" />
            <div class="invalid-feedback">{{ errors.dob }}</div>
          </div>
        </div>

        <!-- Password -->
        <div class="mb-4">
          <label class="form-label text-secondary small">Створити пароль</label>
          <div class="input-group">
            <span class="input-group-text bg-black border-secondary"><i class="bi bi-shield-lock text-muted"></i></span>
            <input v-model="form.password" :type="showPass ? 'text' : 'password'"
              class="form-control border-secondary"
              :class="{ 'is-invalid': errors.password }"
              placeholder="Мінімум 6 символів" />
            <button class="btn btn-outline-secondary border-secondary" type="button"
              @click="showPass = !showPass">
              <i :class="`bi bi-${showPass ? 'eye-slash' : 'eye'}`"></i>
            </button>
            <div class="invalid-feedback">{{ errors.password }}</div>
          </div>
        </div>

        <button class="btn btn-warning w-100 text-dark fw-bold shadow-sm mb-3"
          :disabled="loading" @click="handleRegister">
          <span v-if="loading" class="spinner-border spinner-border-sm me-1"></span>
          <i v-else class="bi bi-person-check me-1"></i>Зареєструватися
        </button>

        <div class="text-center">
          <small class="text-secondary">
            Вже є акаунт?
            <RouterLink to="/login" class="text-warning text-decoration-none fw-semibold">Увійти</RouterLink>
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
const errors  = reactive({ name: '', email: '', gender: '', dob: '', password: '' })
const form    = reactive({ name: '', email: '', gender: '', dob: '', password: '' })

function validate() {
  Object.keys(errors).forEach(k => errors[k] = '')
  let ok = true
  if (!form.name.trim() || form.name.trim().length < 2) { errors.name = "Введіть ім'я (мінімум 2 символи)"; ok = false }
  if (!form.email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) { errors.email = 'Введіть коректну електронну пошту'; ok = false }
  if (!form.gender) { errors.gender = 'Оберіть стать'; ok = false }
  if (!form.dob)    { errors.dob = 'Вкажіть дату народження'; ok = false }
  if (!form.password || form.password.length < 6) { errors.password = 'Пароль — мінімум 6 символів'; ok = false }
  return ok
}

async function handleRegister() {
  error.value = ''
  if (!validate()) return
  loading.value = true
  try {
    await auth.register(form)
    success.value = 'Реєстрація успішна! Переходимо...'
    setTimeout(() => router.push('/profile'), 1000)
  } catch (e) {
    error.value = e.response?.data?.error || 'Помилка реєстрації'
  } finally {
    loading.value = false
  }
}
</script>
