export default defineNuxtRouteMiddleware(async () => {
  const { isAuthenticated, fetchCurrentUser } = useAuth()

  if (isAuthenticated.value) {
    return navigateTo('/dashboard')
  }
  const user = await fetchCurrentUser()

  if (user) {
    return navigateTo('/dashboard')
  }
})
