<script setup lang="ts">
const { result, pending, errorMessage, checkAccess, clearResult } = useBarrierAccess()
const form = reactive({
  registration_number: '',
})

const resultTitle = computed(() => {
  if (!result.value) {
    return ''
  }

  return result.value.access_granted ? 'Dostęp przyznany' : 'Odmowa dostępu'
})
const resultMessage = computed(() => {
  if (!result.value) {
    return ''
  }

  if (result.value.access_granted) {
    return `Pojazd ${result.value.registration_number} ma zaakceptowany wniosek parkingowy.`
  }
  return `Pojazd ${result.value.registration_number} nie ma aktywnego zaakceptowanego wniosku.`
})

const resultVariant = computed(() => {
  if (!result.value) {
    return 'info'
  }

  return result.value.access_granted ? 'success' : 'error'
})

async function submitCheckAccess() {
  clearResult()
  try {
    await checkAccess({
      registration_number: form.registration_number,
    })
  } catch {
    // errorMessage jest ustawiany w useBarrierAccess()
  }
}
</script>
<template>
  <section class="mx-auto max-w-2xl space-y-6">
    <div class="rounded-2xl border bg-white p-8 shadow-sm">
      <p class="text-sm font-medium uppercase tracking-wide text-blue-700">Szlaban</p>
      <h1 class="mt-3 text-3xl font-bold tracking-tight text-slate-950">
        Sprawdzenie dostępu pojazdu
      </h1>
      <p class="mt-4 text-slate-600">
        Wpisz numer rejestracyjny pojazdu. System sprawdzi, czy istnieje zaakceptowany wniosek
        parkingowy dla tego numeru.
      </p>
    </div>

    <UiBaseAlert v-if="errorMessage" variant="error">
      {{ errorMessage }}
    </UiBaseAlert>
    <UiBaseAlert v-if="result" :variant="resultVariant">
      <div class="space-y-1">
        <p class="font-semibold">
          {{ resultTitle }}
        </p>

        <p>
          {{ resultMessage }}
        </p>
      </div>
    </UiBaseAlert>
    <div class="rounded-2xl border bg-white p-6 shadow-sm">
      <form class="space-y-5" @submit.prevent="submitCheckAccess">
        <div>
          <label class="text-sm font-medium text-slate-700" for="registration_number">
            Numer rejestracyjny
          </label>
          <input
            id="registration_number"
            v-model="form.registration_number"
            type="text"
            minlength="4"
            maxlength="15"
            required
            placeholder="np. WA12345"
            class="mt-1 w-full rounded-lg border px-3 py-2 text-sm uppercase outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
          />
          <p class="mt-1 text-xs text-slate-500">
            Możesz wpisać numer ze spacją lub myślnikiem, np. WA 12345 albo WA-12345.
          </p>
        </div>
        <button
          type="submit"
          :disabled="pending"
          class="w-full rounded-lg bg-blue-700 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-800 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {{ pending ? 'Sprawdzanie...' : 'Sprawdź dostęp' }}
        </button>
      </form>
    </div>
  </section>
</template>
