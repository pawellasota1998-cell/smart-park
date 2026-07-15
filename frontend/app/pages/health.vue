<script setup lang="ts">
const { getHealth, getReadiness } = useHealth()

const {
  data: health,
  pending: healthPending,
  error: healthError,
  refresh: refreshHealth,
} = await getHealth()

const {
  data: readiness,
  pending: readinessPending,
  error: readinessError,
  refresh: refreshReadiness,
} = await getReadiness()

function refreshAll() {
  refreshHealth()
  refreshReadiness()
}
</script>

<template>
  <section class="space-y-6">
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold text-slate-950">Status API</h1>
        <p class="mt-1 text-sm text-slate-600">
          Pierwsze połączenie frontendu Nuxt z backendem FastAPI.
        </p>
      </div>

      <button
        type="button"
        class="rounded-xl bg-gray-400 px-4 py-2 text-sm font-semibold text-white hover:bg-gray-500"
        @click="refreshAll"
      >
        Odśwież
      </button>
    </div>

    <div class="grid gap-4 md:grid-cols-2">
      <article class="rounded-3xl border bg-white p-5 shadow-sm">
        <h2 class="font-semibold text-slate-950">Health</h2>

        <p v-if="healthPending" class="mt-3 text-sm text-slate-500">Ładowanie...</p>

        <p v-else-if="healthError" class="mt-3 text-sm text-red-700">
          Nie udało się połączyć z /health.
        </p>

        <pre v-else class="mt-3 overflow-auto rounded-lg bg-slate-950 p-4 text-sm text-slate-50">{{
          health
        }}</pre>
      </article>

      <article class="rounded-3xl border bg-white p-5 shadow-sm">
        <h2 class="font-semibold text-slate-950">Readiness</h2>

        <p v-if="readinessPending" class="mt-3 text-sm text-slate-500">Ładowanie...</p>

        <p v-else-if="readinessError" class="mt-3 text-sm text-red-700">
          Nie udało się połączyć z /health/ready.
        </p>

        <pre v-else class="mt-3 overflow-auto rounded-lg bg-slate-950 p-4 text-sm text-slate-50">{{
          readiness
        }}</pre>
      </article>
    </div>
  </section>
</template>
