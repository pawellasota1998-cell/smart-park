import type { FetchError } from 'ofetch'
import type { ApiErrorResponse } from '~/types/api'

export function useApiError() {
  const getErrorMessage = (error: unknown): string => {
    const fetchError = error as FetchError<ApiErrorResponse>

    if (fetchError.statusCode === 429) {
      return fetchError.data?.detail?.message ?? 'Zbyt wiele prób. Spróbuj ponownie później.'
    }

    if (fetchError.statusCode === 401) {
      return fetchError.data?.detail?.message ?? 'Sesja wygasła albo brak autoryzacji.'
    }
    if (fetchError.statusCode === 403) {
      return fetchError.data?.detail?.message ?? 'Brak uprawnień do wykonania tej operacji.'
    }

    if (fetchError.statusCode === 422) {
      return fetchError.data?.detail?.message ?? 'Dane formularza są niepoprawne.'
    }

    return fetchError.data?.detail?.message ?? 'Wystąpił nieoczekiwany błąd.'
  }

  return {
    getErrorMessage,
  }
}
