<script setup lang="ts">
definePageMeta({
  middleware: 'auth',
})

const { currentUser, fetchCurrentUser } = useAuth()

await fetchCurrentUser()
</script>

<template>
  <section class="space-y-6">
    <div class="rounded-2xl border bg-white p-8 shadow-sm">
      <p class="text-sm font-medium uppercase tracking-wide text-blue-700">Panel użytkownika</p>

      <h1 class="mt-3 text-3xl font-bold tracking-tight text-slate-950">Witaj w Euro Park</h1>

      <p class="mt-4 max-w-2xl text-slate-600">
        W kolejnym etapie dodamy tutaj listę Twoich wniosków parkingowych oraz formularz tworzenia
        nowego wniosku.
      </p>
    </div>

    <div v-if="currentUser" class="rounded-2xl border bg-white p-8 shadow-sm">
      <h2 class="text-lg font-semibold text-slate-950">Aktualny użytkownik</h2>

      <dl class="mt-4 grid gap-3 text-sm md:grid-cols-2">
        <div>
          <dt class="text-slate-500">Imię i nazwisko</dt>
          <dd class="font-medium text-slate-900">
            {{ currentUser.first_name }} {{ currentUser.last_name }}
          </dd>
        </div>

        <div>
          <dt class="text-slate-500">Email</dt>
          <dd class="font-medium text-slate-900">
            {{ currentUser.email }}
          </dd>
        </div>

        <div>
          <dt class="text-slate-500">Rola</dt>
          <dd class="font-medium text-slate-900">
            {{ currentUser.role }}
          </dd>
        </div>

        <div>
          <dt class="text-slate-500">Status konta</dt>
          <dd class="font-medium text-slate-900">
            {{ currentUser.is_active ? 'Aktywne' : 'Nieaktywne' }}
          </dd>
        </div>
      </dl>
    </div>
  </section>
</template>
