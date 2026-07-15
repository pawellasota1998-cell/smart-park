// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },
  modules: ['@nuxtjs/tailwindcss', '@nuxt/eslint'],
  css: ['~/assets/css/main.css'],

  runtimeConfig: {
    public: {
      apiBaseUrl: process.env.NUXT_PUBLIC_API_BASE_URL,
    },
  },

  app: {
    head: {
      title: 'Euro Park',
      htmlAttrs: {
        lang: 'pl',
      },
      meta: [
        {
          name: 'description',
          content: 'Panel do obsługi wniosków parkingowych Euro Park.',
        },
      ],
    },
  },
})
