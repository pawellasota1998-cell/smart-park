<template>
  <div class="min-h-screen bg-slate-50">
    <header class="border-b bg-white">
      <div class="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <NuxtLink to="/" class="text-lg font-bold text-slate-900"> Euro Park </NuxtLink>

        <nav class="flex items-center gap-4 text-sm">
          <NuxtLink to="/" class="text-slate-700 hover:text-slate-950"> Start </NuxtLink>

          <NuxtLink to="/health" class="text-slate-700 hover:text-slate-950"> API Health </NuxtLink>

          <NuxtLink to="/login" class="text-slate-700 hover:text-slate-950"> Logowanie </NuxtLink>
        </nav>
      </div>
    </header>

    <main class="mx-auto max-w-6xl px-4 py-8">
      <slot />
    </main>
  </div>
</template>
