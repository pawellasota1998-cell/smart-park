import type { FetchError } from 'ofetch'
import type { ApiErrorResponse } from '~/types/api'

export function useApiError() {
  const getErrorMessage = (error: unknown): string => {
    const fetchError = error as FetchError<ApiErrorResponse>

    return fetchError.data?.detail?.message ?? 'Wystąpił nieoczekiwany błąd.'
  }

  return {
    getErrorMessage,
  }
}
