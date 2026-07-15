<template>
  <section class="space-y-6">
    <div class="rounded-2xl border bg-white p-8 shadow-lg">
      <h1 class="text-2xl font-bold tracking-tight text-slate-950">
        System obsługi wniosków parkingowych
      </h1>

      <p class="mt-4 max-w-2xl text-slate-600">
        Kompleksowy system obsługi wniosków parkingowych dla mieszkańców i administratorów. Składaj
        wnioski o miejsce parkingowe, śledź ich status oraz weryfikuj uprawnienia pojazdów do wjazdu
        na teren parkingu.
      </p>

      <div class="mt-6 flex gap-3">
        <NuxtLink
          to="/dashboard"
          class="rounded-lg bg-gray-400 px-4 py-2 text-sm font-semibold text-white hover:bg-gray-500"
        >
          Przejdź do panelu
        </NuxtLink>
        <NuxtLink
          to="/barrier"
          class="rounded-lg border px-4 py-2 text-sm font-semibold text-slate-800 hover:bg-slate-100"
        >
          Sprawdź szlaban
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
