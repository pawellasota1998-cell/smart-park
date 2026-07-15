<script setup lang="ts">
import type { ApplicationStatus } from '~/types/application'
const props = defineProps<{
  status: ApplicationStatus
}>()
const statusLabel = computed(() => {
  const labels: Record<ApplicationStatus, string> = {
    PENDING: 'Oczekuje',
    APPROVED: 'Zaakceptowany',
    REJECTED: 'Odrzucony',
    NEEDS_CHANGES: 'Do poprawy',
  }
  return labels[props.status]
})

const statusClasses = computed(() => {
  const classes: Record<ApplicationStatus, string> = {
    PENDING: 'border-yellow-200 bg-yellow-50 text-yellow-800',
    APPROVED: 'border-green-200 bg-green-50 text-green-800',
    REJECTED: 'border-red-200 bg-red-50 text-red-800',
    NEEDS_CHANGES: 'border-blue-200 bg-blue-50 text-blue-800',
  }

  return classes[props.status]
})
</script>

<template>
  <span
    class="inline-flex rounded-full border px-2.5 py-1 text-xs font-semibold"
    :class="statusClasses"
  >
    {{ statusLabel }}
  </span>
</template>
