<template>
  <Teleport to="body">
    <div v-if="visible" class="alarm-overlay d-flex align-items-center justify-content-center">
      <div class="text-center p-5 rounded-4 border border-warning" style="background:#111;max-width:400px;width:90%;">
        <span class="ring-icon mb-3 d-block">
          <i class="bi bi-alarm-fill text-warning" style="font-size:4rem;"></i>
        </span>
        <h2 class="text-warning fw-bold mb-2">Будильник спрацював!</h2>
        <p class="text-light mb-4">{{ label }}</p>
        <button class="btn btn-warning btn-lg text-dark fw-bold px-5" @click="dismiss">
          <i class="bi bi-x-circle me-2"></i>Вимкнути
        </button>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, watch } from 'vue'

const props  = defineProps({ label: String, visible: Boolean })
const emit   = defineEmits(['dismiss'])
let audioCtx = null
let timer    = null

watch(() => props.visible, (v) => {
  if (v) { playBeep(); timer = setTimeout(dismiss, 60_000) }
  else   { stopAudio(); clearTimeout(timer) }
})

function dismiss() { emit('dismiss') }

function stopAudio() {
  if (audioCtx) { try { audioCtx.close() } catch (_) {} audioCtx = null }
}

function playBeep() {
  try {
    audioCtx  = new (window.AudioContext || window.webkitAudioContext)()
    const t   = audioCtx.currentTime
    const seq = [[880,0],[880,0.28],[1100,0.56],[880,1.4],[880,1.68],[1100,1.96],[880,2.8],[880,3.08],[1100,3.36]]
    seq.forEach(([freq, start]) => {
      const osc  = audioCtx.createOscillator()
      const gain = audioCtx.createGain()
      osc.connect(gain); gain.connect(audioCtx.destination)
      osc.type = 'sine'; osc.frequency.value = freq
      gain.gain.setValueAtTime(0.35, t + start)
      gain.gain.exponentialRampToValueAtTime(0.001, t + start + 0.22)
      osc.start(t + start); osc.stop(t + start + 0.22)
    })
  } catch (_) {}
}
</script>

<style scoped>
.alarm-overlay {
  position: fixed; inset: 0; z-index: 9999;
  background: rgba(0,0,0,0.88);
}
@keyframes pulseGlow {
  0%,100% { box-shadow: 0 0 0 0 rgba(255,193,7,0.5); }
  50%      { box-shadow: 0 0 0 10px rgba(255,193,7,0); }
}
.ring-icon {
  animation: pulseGlow 0.8s infinite;
  border-radius: 50%; display: inline-block; padding: 1rem;
}
</style>
