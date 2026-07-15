export type ApplicationStatus = 'PENDING' | 'APPROVED' | 'REJECTED' | 'NEEDS_CHANGES'

export type ParkingApplicationRead = {
  id: number
  user_id: number
  registration_number: string
  preferred_floor: number
  status: ApplicationStatus
  supervisor_comment: string | null
  reviewed_by_user_id: number | null
  reviewed_at: string | null
  created_at: string
  updated_at: string
}

export type ParkingApplicationCreatePayload = {
  registration_number: string
  preferred_floor: number
}

export type ParkingApplicationUpdatePayload = {
  registration_number?: string
  preferred_floor?: number
}

export const editableApplicationStatuses: ApplicationStatus[] = ['PENDING', 'NEEDS_CHANGES']

export function canEditApplication(application: ParkingApplicationRead): boolean {
  return editableApplicationStatuses.includes(application.status)
}
