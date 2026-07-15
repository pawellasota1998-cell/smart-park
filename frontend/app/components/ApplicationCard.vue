<script setup lang="ts">
import type { ParkingApplicationRead } from '~/types/application'
import { canEditApplication } from '~/types/application'

const props = defineProps<{
  application: ParkingApplicationRead
}>()

const emit = defineEmits<{
  edit: [application: ParkingApplicationRead]
}>()

const createdAt = computed(() => {
  return new Intl.DateTimeFormat('pl-PL', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(props.application.created_at))
})

const reviewedAt = computed(() => {
  if (!props.application.reviewed_at) {
    return null
  }

  return new Intl.DateTimeFormat('pl-PL', {
    dateStyle: 'medium',
    timeStyle: 'short',
  }).format(new Date(props.application.reviewed_at))
})
</script>

<template>
  <article class="rounded-2xl border bg-white p-5 shadow-sm">
    <div class="flex items-start justify-between gap-4">
      <div>
        <h3 class="text-lg font-semibold text-slate-950">
          {{ application.registration_number }}
        </h3>

        <p class="mt-1 text-sm text-slate-500">
          Preferowane piętro: {{ application.preferred_floor }}
        </p>
      </div>

      <UiApplicationStatusBadge :status="application.status" />
    </div>

    <dl class="mt-4 grid gap-3 text-sm md:grid-cols-2">
      <div>
        <dt class="text-slate-500">Data złożenia</dt>
        <dd class="font-medium text-slate-900">
          {{ createdAt }}
        </dd>
      </div>

      <div v-if="reviewedAt">
        <dt class="text-slate-500">Data rozpatrzenia</dt>
        <dd class="font-medium text-slate-900">
          {{ reviewedAt }}
        </dd>
      </div>
    </dl>

    <UiBaseAlert v-if="application.supervisor_comment" variant="info" class="mt-4">
      <div class="flex items-start justify-between gap-4">
        <span class="font-semibold">Komentarz nadzorcy:</span>
        {{ application.supervisor_comment }}
      </div>
    </UiBaseAlert>

    <div class="mt-5 flex justify-end">
      <button
        v-if="canEditApplication(application)"
        type="button"
        class="rounded-lg border px-4 py-2 text-sm font-semibold text-slate-700 hover:bg-slate-100"
        @click="emit('edit', application)"
      >
        Edytuj
      </button>
    </div>
  </article>
</template>
