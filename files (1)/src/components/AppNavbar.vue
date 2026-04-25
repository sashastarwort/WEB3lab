<template>
  <nav class="navbar navbar-expand-lg navbar-dark bg-dark bg-opacity-75 navbar-custom fixed-top border-bottom border-secondary">
    <div class="container">
      <RouterLink class="navbar-brand text-light fw-bold fs-4" to="/">
        <i class="bi bi-cpu text-warning me-2"></i>ML Alarm
      </RouterLink>

      <button class="navbar-toggler" type="button"
        data-bs-toggle="collapse" data-bs-target="#navbarNav">
        <span class="navbar-toggler-icon"></span>
      </button>

      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <RouterLink class="nav-link text-light" to="/">
              <i class="bi bi-alarm me-1"></i>Будильник
            </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link text-light" to="/profile">
              <i class="bi bi-person me-1"></i>Профіль
            </RouterLink>
          </li>
          <li class="nav-item">
            <RouterLink class="nav-link text-light" to="/about">
              <i class="bi bi-info-circle me-1"></i>Про додаток
            </RouterLink>
          </li>

          <template v-if="!auth.isLoggedIn">
            <li class="nav-item">
              <RouterLink class="nav-link text-light" to="/login">
                <i class="bi bi-box-arrow-in-right me-1"></i>Вхід
              </RouterLink>
            </li>
            <li class="nav-item">
              <RouterLink class="nav-link text-light" to="/register">
                <i class="bi bi-person-plus me-1"></i>Реєстрація
              </RouterLink>
            </li>
          </template>

          <li v-else class="nav-item">
            <a class="nav-link text-light" href="#" @click.prevent="handleLogout">
              <i class="bi bi-box-arrow-right me-1"></i>Вийти
            </a>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const auth   = useAuthStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push('/login')
}
</script>
