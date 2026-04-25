<template>
  <div class="alarm-item rounded-3 p-3 mb-3 bg-black bg-opacity-50"
    :class="{ 'disabled-alarm': !alarm.enabled }">
    <div class="d-flex align-items-center justify-content-between">
      <div class="flex-grow-1">
        <div class="d-flex align-items-center gap-2 mb-1 flex-wrap">
          <span class="fw-semibold text-light">{{ alarm.label }}</span>
          <span v-if="alarm.fired" class="badge bg-secondary" style="font-size:.7rem;">Спрацював</span>
          <span v-else-if="!alarm.enabled" class="badge bg-secondary" style="font-size:.7rem;">Вимкнено</span>
          <span v-else-if="cd" class="badge bg-warning text-dark" style="font-size:.7rem;">через {{ cd }}</span>
        </div>
        <div class="text-muted small">
          <i class="bi bi-calendar3 me-1"></i>{{ dateLabel }}
          <i class="bi bi-clock ms-2 me-1"></i>{{ timeLabel }}
        </div>
      </div>

      <div class="d-flex gap-2 ms-3">
        <button v-if="!alarm.fired"
          class="btn btn-sm btn-outline-secondary border-0"
          :title="alarm.enabled ? 'Вимкнути' : 'Увімкнути'"
          @click="$emit('toggle', alarm.id)">
          <i :class="`bi bi-${alarm.enabled ? 'pause-circle' : 'play-circle'} text-warning`"></i>
        </button>
        <button class="btn btn-sm btn-outline-secondary border-0"
          title="Видалити" @click="$emit('remove', alarm.id)">
          <i class="bi bi-trash text-danger"></i>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAlarmsStore } from '../stores/alarms'

const props = defineProps({ alarm: { type: Object, required: true } })
defineEmits(['toggle', 'remove'])

const store = useAlarmsStore()

const cd = computed(() => store.countdown(props.alarm.datetime))

const dateLabel = computed(() =>
  new Date(props.alarm.datetime).toLocaleDateString('uk-UA', {
    day: 'numeric', month: 'short', year: 'numeric'
  })
)
const timeLabel = computed(() =>
  new Date(props.alarm.datetime).toLocaleTimeString('uk-UA', {
    hour: '2-digit', minute: '2-digit'
  })
)
</script>

<style scoped>
.alarm-item {
  transition: all 0.3s ease;
  border: 1px solid rgba(255,255,255,0.08);
}
.alarm-item:hover { border-color: rgba(255,193,7,0.3); }
.disabled-alarm   { opacity: 0.45; }
</style>
