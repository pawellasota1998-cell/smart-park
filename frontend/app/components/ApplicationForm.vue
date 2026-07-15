<script setup lang="ts">
import type {
  ParkingApplicationCreatePayload,
  ParkingApplicationUpdatePayload,
} from '~/types/application'
const props = withDefaults(
  defineProps<{
    initialRegistrationNumber?: string
    initialPreferredFloor?: number
    submitLabel?: string
    pending?: boolean
  }>(),
  {
    initialRegistrationNumber: '',
    initialPreferredFloor: 0,
    submitLabel: 'Zapisz',
    pending: false,
  },
)

const emit = defineEmits<{
  submit: [payload: ParkingApplicationCreatePayload | ParkingApplicationUpdatePayload]
  cancel: []
}>()

const form = reactive({
  registration_number: props.initialRegistrationNumber,
  preferred_floor: props.initialPreferredFloor,
})

function submitForm() {
  emit('submit', {
    registration_number: form.registration_number,
    preferred_floor: Number(form.preferred_floor),
  })
}
</script>

<template>
  <form class="space-y-4" @submit.prevent="submitForm">
    <div>
      <label class="text-sm font-medium text-slate-700" for="registration_number">
        Numer rejestracyjny
      </label>
      <input
        id="registration_number"
        v-model="form.registration_number"
        type="text"
        required
        minlength="4"
        maxlength="15"
        placeholder="np. WA12345"
        class="mt-1 w-full rounded-lg border px-3 py-2 text-sm outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
      />
      <p class="mt-1 text-xs text-slate-500">Spacje i myślniki zostaną usunięte przez backend.</p>
    </div>

    <div>
      <label class="text-sm font-medium text-slate-700" for="preferred_floor">
        Preferowane piętro
      </label>
      <input
        id="preferred_floor"
        v-model.number="form.preferred_floor"
        type="number"
        min="-5"
        max="20"
        required
        class="mt-1 w-full rounded-lg border px-3 py-2 text-sm outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
      />
    </div>
    <div class="flex gap-3">
      <button
        type="submit"
        :disabled="pending"
        class="rounded-lg bg-gray-400 px-4 py-2 text-sm font-semibold text-white hover:bg-gray-500 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {{ pending ? 'Zapisywanie...' : submitLabel }}
      </button>
      <button
        type="button"
        class="rounded-lg border px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
        @click="emit('cancel')"
      >
        Anuluj
      </button>
    </div>
  </form>
</template>
