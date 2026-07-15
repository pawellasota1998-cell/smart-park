import type {
  ParkingApplicationCreatePayload,
  ParkingApplicationRead,
  ParkingApplicationUpdatePayload,
} from '~/types/application'

export function useApplications() {
  const applications = useState<ParkingApplicationRead[]>('applications.myApplications', () => [])
  const pending = useState<boolean>('applications.pending', () => false)
  const errorMessage = useState<string | null>('applications.errorMessage', () => null)
  const { apiFetch } = useApiClient()
  const { getErrorMessage } = useApiError()

  const loadMyApplications = async () => {
    pending.value = true
    errorMessage.value = null

    try {
      applications.value = await apiFetch<ParkingApplicationRead[]>('/applications/me')
    } catch (error) {
      errorMessage.value = getErrorMessage(error)
      throw error
    } finally {
      pending.value = false
    }
  }

  const createApplication = async (payload: ParkingApplicationCreatePayload) => {
    pending.value = true
    errorMessage.value = null
    try {
      const application = await apiFetch<ParkingApplicationRead>('/applications', {
        method: 'POST',
        body: payload,
      })
      applications.value = [application, ...applications.value]
      return application
    } catch (error) {
      errorMessage.value = getErrorMessage(error)
      throw error
    } finally {
      pending.value = false
    }
  }

  const updateApplication = async (
    applicationId: number,
    payload: ParkingApplicationUpdatePayload,
  ) => {
    pending.value = true
    errorMessage.value = null

    try {
      const updatedApplication = await apiFetch<ParkingApplicationRead>(
        `/applications/${applicationId}`,
        {
          method: 'PATCH',
          body: payload,
        },
      )
      applications.value = applications.value.map((application) =>
        application.id === updatedApplication.id ? updatedApplication : application,
      )
      return updatedApplication
    } catch (error) {
      errorMessage.value = getErrorMessage(error)
      throw error
    } finally {
      pending.value = false
    }
  }
  return {
    applications,
    pending,
    errorMessage,
    loadMyApplications,
    createApplication,
    updateApplication,
  }
}
