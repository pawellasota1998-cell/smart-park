export type HealthResponse = {
  status: 'ok'
  service: string
  version: string
}

export type ReadinessResponse = {
  status: 'ok'
  database: 'mssql'
}

export type ApiErrorDetail = {
  code: string
  message: string
  request_id?: string | null
  errors?: unknown[]
}

export type ApiErrorResponse = {
  detail: ApiErrorDetail
}
