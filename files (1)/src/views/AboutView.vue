<template>
  <main class="container my-5 flex-grow-1 d-flex justify-content-center align-items-center pt-5">
    <div class="card card-custom bg-dark shadow-lg rounded-4 w-100" style="max-width:650px;">
      <div class="card-body p-4 p-md-5 text-center">
        <div class="mb-4">
          <img src="/Alarm.jpg" alt="ML Alarm Logo"
            class="img-fluid logo-glow mb-3 shadow" style="max-width:180px;"
            @error="e => e.target.style.display='none'" />
          <h1 class="display-5 fw-bold text-warning mb-0">ML Alarm</h1>
          <span class="badge bg-warning text-dark rounded-pill px-3 py-1 mt-2 fw-bold shadow-sm">Версія 3.0</span>
        </div>

        <div class="text-start bg-black bg-opacity-50 p-4 rounded-3 border border-secondary mb-4">
          <h5 class="text-light mb-3"><i class="bi bi-stars text-warning me-2"></i>Наша місія</h5>
          <p class="text-secondary mb-0">
            Ми створили <strong>ML Alarm</strong> для тих, хто цінує свій час та прагне кожної секунди
            бути продуктивним. Це не просто будильник — це інструмент для вашої дисципліни та
            комфортного початку дня.
          </p>
        </div>

        <div class="row g-3 text-start mb-4">
          <div class="col-md-6" v-for="feat in features" :key="feat.icon">
            <div class="p-3 border border-secondary border-opacity-25 rounded-3 h-100">
              <i :class="`bi bi-${feat.icon} text-warning mb-2 d-block`"></i>
              <h6 class="text-light">{{ feat.title }}</h6>
              <p class="small text-secondary mb-0">{{ feat.desc }}</p>
            </div>
          </div>
        </div>

        <!-- Component diagram -->
        <div class="text-start bg-black bg-opacity-50 p-4 rounded-3 border border-secondary mb-4">
          <h5 class="text-light mb-3"><i class="bi bi-diagram-3 text-warning me-2"></i>Vue-компоненти</h5>
          <div class="d-flex flex-wrap gap-2 justify-content-center">
            <span v-for="c in components" :key="c"
              class="badge bg-dark border border-warning text-warning px-3 py-2">
              {{ c }}
            </span>
          </div>
          <p class="text-secondary small mt-3 mb-0">
            Взаємодія через <strong>Pinia stores</strong> (auth, alarms) та
            <strong>Axios</strong> REST API до Flask/SQLite бекенду.
          </p>
        </div>

        <p class="text-muted small mb-0">
          <i class="bi bi-code-slash me-1"></i>
          HTML5, CSS3, Bootstrap 5, Vue 3 + Vite, Pinia, Vue Router, Axios, Python Flask, SQLite.
        </p>
      </div>
    </div>
  </main>
</template>

<script setup>
const features = [
  { icon: 'lightning-charge-fill', title: 'Швидкість',  desc: 'Миттєве налаштування на будь-якому пристрої.' },
  { icon: 'shield-check',          title: 'Надійність', desc: 'Ваші будильники збережені у базі даних.' },
  { icon: 'person-check',          title: 'Акаунт',     desc: 'JWT авторизація та безпечне зберігання.' },
  { icon: 'code-slash',            title: 'Технології', desc: 'Vue 3, Vite, Pinia, Flask, SQLite, REST API.' },
]

const components = [
  'App.vue', 'AppNavbar.vue', 'AppFooter.vue',
  'AlarmCard.vue', 'AlarmRing.vue',
  'HomeView.vue', 'LoginView.vue', 'RegisterView.vue',
  'ProfileView.vue', 'AboutView.vue',
]
</script>

<style scoped>
.logo-glow { filter: drop-shadow(0 0 15px rgba(255,193,7,0.2)); border-radius: 20px; }
</style>
