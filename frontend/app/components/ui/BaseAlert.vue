<template>
  <div class="rounded-lg border px-4 py-3 text-sm" :class="variantClasses">
    <slot />
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    variant?: 'error' | 'success' | 'info'
  }>(),
  {
    variant: 'info',
  },
)

const variantClasses = computed(() => {
  if (props.variant === 'error') {
    return 'border-red-200 bg-red-50 text-red-800'
  }

  if (props.variant === 'success') {
    return 'border-green-200 bg-green-50 text-green-800'
  }

  return 'border-blue-200 bg-blue-50 text-blue-800'
})
</script>
