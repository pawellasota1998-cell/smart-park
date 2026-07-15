<script setup lang="ts">
definePageMeta({
  middleware: 'guest',
})

const { register } = useAuth()
const { getErrorMessage } = useApiError()

const form = reactive({
  email: '',
  password: '',
  first_name: '',
  last_name: '',
})

const pending = ref(false)
const errorMessage = ref<string | null>(null)
const successMessage = ref<string | null>(null)

async function submitRegister() {
  pending.value = true
  errorMessage.value = null
  successMessage.value = null

  try {
    await register({
      email: form.email,
      password: form.password,
      first_name: form.first_name,
      last_name: form.last_name,
    })

    successMessage.value = 'Konto zostało utworzone. Możesz się zalogować.'

    form.email = ''
    form.password = ''
    form.first_name = ''
    form.last_name = ''
  } catch (error) {
    errorMessage.value = getErrorMessage(error)
  } finally {
    pending.value = false
  }
}
</script>

<template>
  <section class="mx-auto max-w-md">
    <div class="rounded-2xl border bg-white p-8 shadow-sm">
      <h1 class="text-2xl font-bold text-slate-950">Rejestracja</h1>

      <p class="mt-2 text-sm text-slate-600">Utwórz konto użytkownika Euro Park.</p>

      <UiBaseAlert v-if="errorMessage" variant="error" class="mt-6">
        {{ errorMessage }}
      </UiBaseAlert>

      <UiBaseAlert v-if="successMessage" variant="success" class="mt-6">
        {{ successMessage }}
      </UiBaseAlert>

      <form class="mt-6 space-y-4" @submit.prevent="submitRegister">
        <div>
          <label class="text-sm font-medium text-slate-700" for="first_name"> Imię </label>

          <input
            id="first_name"
            v-model="form.first_name"
            type="text"
            autocomplete="given-name"
            required
            class="mt-1 w-full rounded-lg border px-3 py-2 text-sm outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <div>
          <label class="text-sm font-medium text-slate-700" for="last_name"> Nazwisko </label>

          <input
            id="last_name"
            v-model="form.last_name"
            type="text"
            autocomplete="family-name"
            required
            class="mt-1 w-full rounded-lg border px-3 py-2 text-sm outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <div>
          <label class="text-sm font-medium text-slate-700" for="email"> Email </label>

          <input
            id="email"
            v-model="form.email"
            type="email"
            autocomplete="email"
            required
            class="mt-1 w-full rounded-lg border px-3 py-2 text-sm outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <div>
          <label class="text-sm font-medium text-slate-700" for="password"> Hasło </label>

          <input
            id="password"
            v-model="form.password"
            type="password"
            autocomplete="new-password"
            minlength="8"
            required
            class="mt-1 w-full rounded-lg border px-3 py-2 text-sm outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
          />

          <p class="mt-1 text-xs text-slate-500">Minimum 8 znaków.</p>
        </div>

        <button
          type="submit"
          :disabled="pending"
          class="w-full rounded-lg bg-blue-700 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-800 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {{ pending ? 'Tworzenie konta...' : 'Zarejestruj się' }}
        </button>
      </form>

      <p class="mt-6 text-sm text-slate-600">
        Masz już konto?
        <NuxtLink to="/login" class="font-medium"> Zaloguj się </NuxtLink>
      </p>
    </div>
  </section>
</template>
