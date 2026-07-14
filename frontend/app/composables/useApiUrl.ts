export function useApiUrl(path: string): string {
  const config = useRuntimeConfig()
  const baseUrl = config.public.apiBaseUrl

  return `${baseUrl}${path}`
}
