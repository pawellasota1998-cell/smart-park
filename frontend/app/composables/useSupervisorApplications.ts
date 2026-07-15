import type {
  ApplicationStatus,
  ParkingApplicationPage,
  ParkingApplicationRead,
  SupervisorApplicationsFilters,
  SupervisorDecisionPayload,
  SupervisorRequestChangesPayload,
} from '~/types/application'

import type { FetchOptions } from 'ofetch'

export function useSupervisorApplications() {
  const applications = useState<ParkingApplicationRead[]>('supervisor.applications', () => [])

  const pagination = useState<ParkingApplicationPage['pagination']>(
    'supervisor.pagination',
    () => ({
      page: 1,
      page_size: 20,
      total_items: 0,
      total_pages: 0,
    }),
  )

  const filters = useState<SupervisorApplicationsFilters>('supervisor.filters', () => ({
    status: '',
    registration_number: '',
    page: 1,
    page_size: 20,
    sort_by: 'created_at',
    sort_order: 'desc',
  }))

  const pending = useState<boolean>('supervisor.pending', () => false)

  const errorMessage = useState<string | null>('supervisor.errorMessage', () => null)

  const { apiFetch } = useApiClient()
  const { getErrorMessage } = useApiError()

  function buildQueryString(): string {
    const params = new URLSearchParams()
    if (filters.value.status) {
      params.set('status', filters.value.status)
    }
    if (filters.value.registration_number) {
      params.set('registration_number', filters.value.registration_number)
    }

    params.set('page', String(filters.value.page))
    params.set('page_size', String(filters.value.page_size))
    params.set('sort_by', filters.value.sort_by)
    params.set('sort_order', filters.value.sort_order)

    return params.toString()
  }

  async function loadApplications() {
    pending.value = true
    errorMessage.value = null

    try {
      const queryString = buildQueryString()
      const response = await apiFetch<ParkingApplicationPage>(
        `/supervisor/applications?${queryString}`,
      )
      applications.value = response.items
      pagination.value = response.pagination
    } catch (error) {
      errorMessage.value = getErrorMessage(error)
      throw error
    } finally {
      pending.value = false
    }
  }

  async function updateApplicationStatus(
    applicationId: number,
    path: string,
    options: {
      method: 'PATCH'
      body?: FetchOptions['body']
    },
  ) {
    pending.value = true
    errorMessage.value = null
    try {
      const updatedApplication = await apiFetch<ParkingApplicationRead>(path, options)

      applications.value = applications.value.map((application) =>
        application.id === applicationId ? updatedApplication : application,
      )

      return updatedApplication
    } catch (error) {
      errorMessage.value = getErrorMessage(error)
      throw error
    } finally {
      pending.value = false
    }
  }

  async function approveApplication(applicationId: number) {
    return updateApplicationStatus(
      applicationId,
      `/supervisor/applications/${applicationId}/approve`,
      {
        method: 'PATCH',
      },
    )
  }

  async function rejectApplication(applicationId: number, payload: SupervisorDecisionPayload) {
    return updateApplicationStatus(
      applicationId,
      `/supervisor/applications/${applicationId}/reject`,
      {
        method: 'PATCH',
        body: payload,
      },
    )
  }

  async function requestChanges(applicationId: number, payload: SupervisorRequestChangesPayload) {
    return updateApplicationStatus(
      applicationId,
      `/supervisor/applications/${applicationId}/request-changes`,
      {
        method: 'PATCH',
        body: payload,
      },
    )
  }

  function setStatusFilter(status: ApplicationStatus | '') {
    filters.value.status = status
    filters.value.page = 1
  }
  function setRegistrationNumberFilter(registrationNumber: string) {
    filters.value.registration_number = registrationNumber
    filters.value.page = 1
  }
  function setPage(page: number) {
    filters.value.page = page
  }

  return {
    applications,
    pagination,
    filters,
    pending,
    errorMessage,
    loadApplications,
    approveApplication,
    rejectApplication,
    requestChanges,
    setStatusFilter,
    setRegistrationNumberFilter,
    setPage,
  }
}
