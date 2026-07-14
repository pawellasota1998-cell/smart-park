<script setup lang="ts">
const { currentUser, isAuthenticated, logout, fetchCurrentUser } = useAuth()

await fetchCurrentUser()
</script>

<template>
  <div class="min-h-screen bg-slate-50">
    <header class="border-b bg-white">
      <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <NuxtLink to="/" class="text-lg font-bold text-slate-900"> Euro Park </NuxtLink>

        <nav class="flex items-center gap-4 text-sm">
          <NuxtLink to="/" class="text-slate-700 hover:text-slate-950"> Start </NuxtLink>

          <NuxtLink to="/health" class="text-slate-700 hover:text-slate-950"> API Health </NuxtLink>

          <NuxtLink
            v-if="isAuthenticated"
            to="/dashboard"
            class="text-slate-700 hover:text-slate-950"
          >
            Panel
          </NuxtLink>

          <NuxtLink v-if="!isAuthenticated" to="/login" class="text-slate-700 hover:text-slate-950">
            Logowanie
          </NuxtLink>

          <NuxtLink
            v-if="!isAuthenticated"
            to="/register"
            class="text-slate-700 hover:text-slate-950"
          >
            Rejestracja
          </NuxtLink>

          <span v-if="currentUser" class="hidden text-slate-500 md:inline">
            {{ currentUser.first_name }}
          </span>

          <button
            v-if="isAuthenticated"
            type="button"
            class="rounded-lg border px-3 py-1.5 text-sm font-medium text-slate-700 hover:bg-slate-100"
            @click="logout"
          >
            Wyloguj
          </button>
        </nav>
      </div>
    </header>

    <main class="mx-auto max-w-6xl px-4 py-8">
      <slot />
    </main>
  </div>
</template>
