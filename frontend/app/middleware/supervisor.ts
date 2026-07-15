export default defineNuxtRouteMiddleware(async () => {
  const { currentUser, fetchCurrentUser } = useAuth()
  const user = currentUser.value ?? (await fetchCurrentUser())

  if (!user) {
    return navigateTo('/login')
  }

  if (user.role !== 'SUPERVISOR' && user.role !== 'ADMIN') {
    return navigateTo('/dashboard')
  }
})
