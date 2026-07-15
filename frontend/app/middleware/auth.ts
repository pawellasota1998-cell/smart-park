export default defineNuxtRouteMiddleware(async () => {
  const { isAuthenticated, fetchCurrentUser } = useAuth()

  if (isAuthenticated.value) {
    return
  }
  const user = await fetchCurrentUser()
  if (!user) {
    return navigateTo('/login')
  }
})
