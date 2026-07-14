<template>
  <section class="space-y-6">
    <div class="rounded-3xl border bg-white p-8 shadow-lg">
      <h1 class="text-2xl font-bold tracking-tight text-slate-950">
        System obsługi wniosków parkingowych
      </h1>

      <p class="mt-4 max-w-2xl text-slate-600">
        Frontend Nuxt dla aplikacji Euro Park. W kolejnych etapach dodamy logowanie, panel
        użytkownika, panel nadzorcy oraz obsługę szlabanu.
      </p>

      <div class="mt-6 flex gap-3">
        <NuxtLink
          to="/dashboard"
          class="rounded-lg bg-blue-700 px-4 py-2 text-sm font-semibold text-white hover:bg-blue-800"
        >
          Przejdź do panelu
        </NuxtLink>

        <NuxtLink
          to="/health"
          class="rounded-lg border px-4 py-2 text-sm font-semibold text-slate-800 hover:bg-slate-100"
        >
          Sprawdź API
        </NuxtLink>
      </div>
    </div>
  </section>
</template>
