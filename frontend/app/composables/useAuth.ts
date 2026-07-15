import type { LoginCredentials, RegisterPayload, TokenResponse, UserRead } from '~/types/auth'

export function useAuth() {
  const currentUser = useState<UserRead | null>('auth.currentUser', () => null)
  const initialized = useState<boolean>('auth.initialized', () => false)

  const accessToken = useCookie<string | null>('euro_park_access_token', {
    default: () => null,
    sameSite: 'lax',
    maxAge: 60 * 15,
  })

  const refreshToken = useCookie<string | null>('euro_park_refresh_token', {
    default: () => null,
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 7,
  })

  const isAuthenticated = computed(() => Boolean(accessToken.value && currentUser.value))

  const setTokens = (tokenResponse: TokenResponse) => {
    accessToken.value = tokenResponse.access_token
    refreshToken.value = tokenResponse.refresh_token
  }

  const clearSession = () => {
    accessToken.value = null
    refreshToken.value = null
    currentUser.value = null
    initialized.value = true
  }

  const loadCurrentUser = async () => {
    if (!accessToken.value) {
      currentUser.value = null
      initialized.value = true
      return null
    }

    const { apiFetch } = useApiClient()

    const user = await apiFetch<UserRead>('/auth/me')

    currentUser.value = user
    initialized.value = true

    return user
  }

  const refreshTokens = async (): Promise<boolean> => {
    if (!refreshToken.value) {
      clearSession()
      return false
    }
    try {
      const tokenResponse = await $fetch<TokenResponse>(useApiUrl('/auth/refresh'), {
        method: 'POST',
        body: {
          refresh_token: refreshToken.value,
        },
      })

      setTokens(tokenResponse)
      return true
    } catch {
      clearSession()
      return false
    }
  }

  const fetchCurrentUser = async () => {
    try {
      return await loadCurrentUser()
    } catch {
      const refreshed = await refreshTokens()
      if (!refreshed) {
        return null
      }
      try {
        return await loadCurrentUser()
      } catch {
        clearSession()
        return null
      }
    }
  }
  const login = async (credentials: LoginCredentials) => {
    const formData = new URLSearchParams()

    formData.set('username', credentials.email)
    formData.set('password', credentials.password)

    const tokenResponse = await $fetch<TokenResponse>(useApiUrl('/auth/login'), {
      method: 'POST',
      body: formData,
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    })
    setTokens(tokenResponse)
    await fetchCurrentUser()
  }
  const register = async (payload: RegisterPayload) => {
    return await $fetch<UserRead>(useApiUrl('/auth/register'), {
      method: 'POST',
      body: payload,
    })
  }
  const logout = async () => {
    const tokenToRevoke = refreshToken.value
    if (tokenToRevoke) {
      try {
        await $fetch(useApiUrl('/auth/logout'), {
          method: 'POST',
          body: {
            refresh_token: tokenToRevoke,
          },
        })
      } catch {
        // Nawet jeśli backend odrzuci token,
        // frontend i tak czyści lokalną sesję.
      }
    }
    clearSession()
    return navigateTo('/login')
  }

  return {
    currentUser,
    initialized,
    accessToken,
    refreshToken,
    isAuthenticated,
    login,
    register,
    logout,
    fetchCurrentUser,
    refreshTokens,
    clearSession,
  }
}
