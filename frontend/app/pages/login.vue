<script setup lang="ts">
definePageMeta({
  middleware: 'guest',
})

const { login } = useAuth()
const { getErrorMessage } = useApiError()

const form = reactive({
  email: '',
  password: '',
})

const pending = ref(false)
const errorMessage = ref<string | null>(null)

async function submitLogin() {
  pending.value = true
  errorMessage.value = null

  try {
    await login({
      email: form.email,
      password: form.password,
    })

    await navigateTo('/dashboard')
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
      <h1 class="text-2xl font-bold text-slate-950">Logowanie</h1>

      <p class="mt-2 text-sm text-slate-600">Zaloguj się, aby przejść do panelu użytkownika.</p>

      <UiBaseAlert v-if="errorMessage" variant="error" class="mt-6">
        {{ errorMessage }}
      </UiBaseAlert>

      <form class="mt-6 space-y-4" @submit.prevent="submitLogin">
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
            autocomplete="current-password"
            required
            class="mt-1 w-full rounded-lg border px-3 py-2 text-sm outline-none focus:border-blue-600 focus:ring-2 focus:ring-blue-100"
          />
        </div>

        <button
          type="submit"
          :disabled="pending"
          class="w-full rounded-lg bg-blue-700 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-800 disabled:cursor-not-allowed disabled:opacity-60"
        >
          {{ pending ? 'Logowanie...' : 'Zaloguj się' }}
        </button>
      </form>

      <p class="mt-6 text-sm text-slate-600">
        Nie masz konta?
        <NuxtLink to="/register" class="font-medium"> Zarejestruj się </NuxtLink>
      </p>
    </div>
  </section>
</template>
