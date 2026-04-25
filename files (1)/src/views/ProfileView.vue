<template>
  <main class="container my-5 flex-grow-1 pt-5">

    <!-- Guest -->
    <div v-if="!auth.isLoggedIn" class="text-center py-5">
      <i class="bi bi-person-lock text-warning mb-3 d-block" style="font-size:4rem;"></i>
      <h4 class="text-light">Увійдіть у свій акаунт</h4>
      <p class="text-secondary">Щоб переглянути профіль, спочатку потрібно авторизуватись.</p>
      <RouterLink to="/login" class="btn btn-warning text-dark fw-bold px-4">Увійти</RouterLink>
    </div>

    <!-- Logged in -->
    <div v-else class="row justify-content-center">
      <div class="col-md-10 col-lg-8">

        <div v-if="alertMsg" class="alert mb-3"
          :class="`alert-${alertType}`">{{ alertMsg }}</div>

        <div class="card card-custom bg-dark shadow-lg rounded-4">
          <div class="card-body p-4 p-md-5">
            <div class="text-center mb-5">
              <i class="bi bi-person-circle text-warning mb-3 d-block" style="font-size:4.5rem;"></i>
              <h3 class="card-title text-light fw-bold">Вітаємо, {{ firstName }}!</h3>
              <p class="text-secondary small">Ваш персональний кабінет</p>
            </div>

            <!-- Profile table -->
            <div class="table-responsive bg-black bg-opacity-50 p-2 p-md-4 rounded-4 border border-secondary mb-5">
              <table class="table table-dark align-middle mb-0">
                <tbody>
                  <tr>
                    <th style="width:40%;color:#6c757d;border-color:rgba(255,255,255,0.1)">
                      <i class="bi bi-person-badge me-2 text-warning"></i>Повне ім'я:
                    </th>
                    <td style="border-color:rgba(255,255,255,0.1)">
                      <span v-if="!editing">{{ auth.user?.name }}</span>
                      <input v-else v-model="editForm.name" type="text"
                        class="form-control form-control-sm border-secondary bg-black text-light" />
                    </td>
                  </tr>
                  <tr>
                    <th style="color:#6c757d;border-color:rgba(255,255,255,0.1)">
                      <i class="bi bi-envelope-at me-2 text-warning"></i>Email:
                    </th>
                    <td style="border-color:rgba(255,255,255,0.1)">{{ auth.user?.email }}</td>
                  </tr>
                  <tr>
                    <th style="color:#6c757d;border-color:rgba(255,255,255,0.1)">
                      <i class="bi bi-gender-ambiguous me-2 text-warning"></i>Стать:
                    </th>
                    <td style="border-color:rgba(255,255,255,0.1)">
                      <span v-if="!editing">{{ genderLabel }}</span>
                      <select v-else v-model="editForm.gender"
                        class="form-select form-select-sm border-secondary bg-black text-light">
                        <option value="male">Чоловіча</option>
                        <option value="female">Жіноча</option>
                      </select>
                    </td>
                  </tr>
                  <tr>
                    <th style="color:#6c757d;border-color:rgba(255,255,255,0.1)">
                      <i class="bi bi-calendar-event me-2 text-warning"></i>Дата народження:
                    </th>
                    <td style="border-color:rgba(255,255,255,0.1)">
                      <span v-if="!editing">{{ dobLabel }}</span>
                      <input v-else v-model="editForm.dob" type="date"
                        class="form-control form-control-sm border-secondary bg-black text-light" />
                    </td>
                  </tr>
                  <tr>
                    <th style="color:#6c757d;border-color:rgba(255,255,255,0.1)">
                      <i class="bi bi-calendar-check me-2 text-warning"></i>Реєстрація:
                    </th>
                    <td style="border-color:rgba(255,255,255,0.1)">{{ registeredLabel }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Actions -->
            <div class="d-grid d-md-flex justify-content-md-center gap-3">
              <template v-if="!editing">
                <button class="btn btn-outline-warning px-4 rounded-pill" @click="startEdit">
                  <i class="bi bi-pencil-square me-2"></i>Редагувати
                </button>
              </template>
              <template v-else>
                <button class="btn btn-warning px-4 rounded-pill" :disabled="saving" @click="saveProfile">
                  <span v-if="saving" class="spinner-border spinner-border-sm me-1"></span>
                  <i v-else class="bi bi-check-lg me-2"></i>Зберегти
                </button>
                <button class="btn btn-outline-secondary px-4 rounded-pill" @click="cancelEdit">
                  <i class="bi bi-x-lg me-2"></i>Скасувати
                </button>
              </template>
              <button class="btn btn-outline-danger px-4 rounded-pill" @click="handleLogout">
                <i class="bi bi-box-arrow-right me-2"></i>Вийти
              </button>
            </div>

          </div>
        </div>
      </div>
    </div>
  </main>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth   = useAuthStore()
const router = useRouter()

const editing  = ref(false)
const saving   = ref(false)
const alertMsg  = ref('')
const alertType = ref('success')

const editForm = reactive({ name: '', gender: '', dob: '' })

function fmtDate(iso) {
  if (!iso) return '—'
  return new Date(iso).toLocaleDateString('uk-UA', { day: 'numeric', month: 'long', year: 'numeric' })
}

const firstName      = computed(() => auth.user?.name?.split(' ')[0] || '')
const genderLabel    = computed(() => auth.user?.gender === 'male' ? 'Чоловіча' : auth.user?.gender === 'female' ? 'Жіноча' : '—')
const dobLabel       = computed(() => fmtDate(auth.user?.dob))
const registeredLabel = computed(() => fmtDate(auth.user?.created_at))

function startEdit() {
  editForm.name   = auth.user?.name   || ''
  editForm.gender = auth.user?.gender || ''
  editForm.dob    = auth.user?.dob    || ''
  editing.value   = true
}

function cancelEdit() { editing.value = false }

async function saveProfile() {
  if (!editForm.name.trim() || editForm.name.trim().length < 2) {
    showAlert("Ім'я занадто коротке", 'danger'); return
  }
  saving.value = true
  try {
    await auth.updateProfile(editForm)
    editing.value = false
    showAlert('Профіль успішно оновлено ✓')
  } catch (e) {
    showAlert(e.response?.data?.error || 'Помилка збереження', 'danger')
  } finally {
    saving.value = false
  }
}

function showAlert(msg, type = 'success') {
  alertMsg.value  = msg
  alertType.value = type
  setTimeout(() => { alertMsg.value = '' }, 3000)
}

function handleLogout() { auth.logout(); router.push('/login') }
</script>
