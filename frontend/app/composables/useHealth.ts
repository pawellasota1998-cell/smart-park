import type { HealthResponse, ReadinessResponse } from '~/types/api'
import { useApiUrl } from './useApiUrl'

export function useHealth() {
  const getHealth = () => {
    return useFetch<HealthResponse>(useApiUrl('/health'))
  }

  const getReadiness = () => {
    return useFetch<ReadinessResponse>(useApiUrl('/health/ready'))
  }

  return {
    getHealth,
    getReadiness,
  }
}
