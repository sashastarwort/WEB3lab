<template>
  <main class="container flex-grow-1 pt-5 mt-5 pb-4">
    <!-- Clock -->
    <div class="text-center mb-4">
      <div class="clock-display text-warning">{{ clock }}</div>
      <p class="text-secondary small mb-0">{{ dateStr }}</p>
    </div>

    <div class="row g-4">
      <!-- Add alarm form -->
      <div class="col-md-5 col-lg-4">
        <div class="card card-custom bg-dark shadow rounded-3 h-100">
          <div class="card-body p-4">
            <h4 class="card-title text-light mb-4">
              <i class="bi bi-plus-circle text-warning me-2"></i>Додати новий
            </h4>

            <div v-if="formError" class="alert alert-danger small p-2 mb-3">{{ formError }}</div>
            <div v-if="formSuccess" class="alert alert-success small p-2 mb-3">{{ formSuccess }}</div>

            <div class="mb-3">
              <label class="form-label text-secondary small">Назва будильника</label>
              <div class="input-group">
                <span class="input-group-text bg-black border-secondary">
                  <i class="bi bi-tag text-warning"></i>
                </span>
                <input v-model="form.label" type="text" class="form-control border-secondary"
                  placeholder="Наприклад: Прокинутись" />
              </div>
            </div>

            <div class="mb-3">
              <label class="form-label text-secondary small">Дата спрацювання</label>
              <div class="input-group">
                <span class="input-group-text bg-black border-secondary">
                  <i class="bi bi-calendar-event text-warning"></i>
                </span>
                <input v-model="form.date" type="date" class="form-control border-secondary" />
              </div>
            </div>

            <div class="mb-4">
              <label class="form-label text-secondary small">Час спрацювання</label>
              <div class="input-group">
                <span class="input-group-text bg-black border-secondary">
                  <i class="bi bi-clock text-warning"></i>
                </span>
                <input v-model="form.time" type="time" class="form-control border-secondary" />
              </div>
            </div>

            <div v-if="!auth.isLoggedIn" class="alert alert-warning small p-2 mb-3">
              <i class="bi bi-info-circle me-1"></i>
              <RouterLink to="/login" class="text-dark fw-semibold">Увійдіть</RouterLink>,
              щоб зберігати між сесіями.
            </div>

            <button class="btn btn-warning w-100 text-dark fw-bold" :disabled="saving" @click="saveAlarm">
              <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
              <i v-else class="bi bi-save me-1"></i>Зберегти будильник
            </button>
          </div>
        </div>
      </div>

      <!-- Alarms list -->
      <div class="col-md-7 col-lg-8">
        <div class="card card-custom bg-dark shadow rounded-3 h-100">
          <div class="card-body p-4">
            <div class="d-flex justify-content-between align-items-center mb-4">
              <h4 class="card-title text-light mb-0">
                <i class="bi bi-list-stars text-warning me-2"></i>Заведені зараз
              </h4>
              <span class="badge bg-warning text-dark">{{ activeCount }}</span>
            </div>

            <div v-if="store.loading" class="text-center py-5">
              <div class="spinner-border text-warning"></div>
            </div>

            <div v-else-if="!auth.isLoggedIn" class="alert bg-black text-center rounded-3 border-secondary p-5">
              <i class="bi bi-person-lock text-muted mb-3 d-block" style="font-size:3rem;"></i>
              <h5 class="text-secondary">Увійдіть, щоб бачити будильники</h5>
              <RouterLink to="/login" class="btn btn-outline-warning btn-sm mt-2">Увійти</RouterLink>
            </div>

            <div v-else-if="store.alarms.length === 0"
              class="alert bg-black text-center rounded-3 border-secondary p-5">
              <i class="bi bi-alarm-fill text-muted mb-3 d-block" style="font-size:3rem;"></i>
              <h5 class="text-secondary">Немає заведених будильників</h5>
              <p class="text-muted small mb-0">Використай форму зліва, щоб додати перший.</p>
            </div>

            <template v-else>
              <AlarmCard
                v-for="alarm in store.alarms"
                :key="alarm.id"
                :alarm="alarm"
                @toggle="store.toggleAlarm($event)"
                @remove="store.removeAlarm($event)"
              />
            </template>
          </div>
        </div>
      </div>
    </div>

    <!-- Ring overlay -->
    <AlarmRing :visible="ring.visible" :label="ring.label" @dismiss="ring.visible = false" />
  </main>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { useAuthStore }   from '../stores/auth'
import { useAlarmsStore } from '../stores/alarms'
import AlarmCard  from '../components/AlarmCard.vue'
import AlarmRing  from '../components/AlarmRing.vue'

const auth  = useAuthStore()
const store = useAlarmsStore()

// ── Clock ──────────────────────────────────────────────────────────────────
const clock   = ref('')
const dateStr = ref('')
let clockTimer = null

function tick() {
  const now = new Date()
  clock.value   = now.toLocaleTimeString('uk-UA')
  dateStr.value = now.toLocaleDateString('uk-UA', { weekday:'long', year:'numeric', month:'long', day:'numeric' })
}
tick()

// ── Form ───────────────────────────────────────────────────────────────────
const form = reactive({
  label: '',
  date:  new Date().toISOString().split('T')[0],
  time:  '',
})
const saving      = ref(false)
const formError   = ref('')
const formSuccess = ref('')

async function saveAlarm() {
  formError.value   = ''
  formSuccess.value = ''

  if (!form.date || !form.time) { formError.value = 'Вкажіть дату та час'; return }

  saving.value = true
  try {
    await store.addAlarm({ label: form.label, date: form.date, time: form.time })
    formSuccess.value = 'Будильник збережено ✓'
    form.label = ''
    form.time  = ''
    setTimeout(() => { formSuccess.value = '' }, 3000)
  } catch (e) {
    formError.value = e.response?.data?.error || 'Помилка збереження'
  } finally {
    saving.value = false
  }
}

// ── Active count ───────────────────────────────────────────────────────────
const activeCount = computed(() =>
  store.alarms.filter(a => a.enabled && !a.fired).length
)

// ── Alarm checker ──────────────────────────────────────────────────────────
const ring = reactive({ visible: false, label: '' })
let checkTimer = null

function checkAlarms() {
  const now = new Date()
  store.alarms.forEach(a => {
    if (!a.enabled || a.fired) return
    const diff = now - new Date(a.datetime)
    if (diff >= 0 && diff < 30_000) {
      store.markFired(a.id)
      ring.label   = a.label
      ring.visible = true
    }
  })
}

// ── Lifecycle ──────────────────────────────────────────────────────────────
onMounted(async () => {
  clockTimer = setInterval(tick, 1000)
  checkTimer = setInterval(checkAlarms, 1000)
  if (auth.isLoggedIn) await store.fetchAlarms()
})

onUnmounted(() => {
  clearInterval(clockTimer)
  clearInterval(checkTimer)
})
</script>

<style scoped>
.clock-display {
  font-size: 3.2rem;
  font-weight: 700;
  font-variant-numeric: tabular-nums;
  letter-spacing: 2px;
}
</style>
