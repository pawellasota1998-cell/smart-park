import type { FetchOptions } from 'ofetch'

type ApiRequestOptions = {
  method?: 'GET' | 'POST' | 'PATCH' | 'PUT' | 'DELETE'
  body?: FetchOptions['body']
  headers?: HeadersInit
}

export function useApiUrl(path: string): string {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl

  return `${baseUrl}${path}`
}

export function useApiClient() {
  const accessToken = useCookie<string | null>('euro_park_access_token')

  const apiFetch = async <T>(path: string, options: ApiRequestOptions = {}) => {
    const headers = new Headers(options.headers)

    if (accessToken.value) {
      headers.set('Authorization', `Bearer ${accessToken.value}`)
    }

    return await $fetch<T>(useApiUrl(path), {
      method: options.method,
      body: options.body,
      headers,
    })
  }

  return {
    apiFetch,
  }
}
