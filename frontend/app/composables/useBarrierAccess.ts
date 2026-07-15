import type { BarrierAccessRequest, BarrierAccessResponse } from '~/types/barrier'

export function useBarrierAccess() {
  const result = useState<BarrierAccessResponse | null>('barrier.result', () => null)
  const pending = useState<boolean>('barrier.pending', () => false)
  const errorMessage = useState<string | null>('barrier.errorMessage', () => null)

  const { apiFetch } = useApiClient()
  const { getErrorMessage } = useApiError()

  const checkAccess = async (payload: BarrierAccessRequest) => {
    pending.value = true
    errorMessage.value = null
    result.value = null

    try {
      result.value = await apiFetch<BarrierAccessResponse>('/barrier/check-access', {
        method: 'POST',
        body: payload,
      })

      return result.value
    } catch (error) {
      errorMessage.value = getErrorMessage(error)
      throw error
    } finally {
      pending.value = false
    }
  }

  const clearResult = () => {
    result.value = null
    errorMessage.value = null
  }
  return {
    result,
    pending,
    errorMessage,
    checkAccess,
    clearResult,
  }
}
