export type UserRole = 'USER' | 'SUPERVISOR' | 'ADMIN'

export type UserRead = {
  id: number
  email: string
  first_name: string
  last_name: string
  role: UserRole
  is_active: boolean
  created_at: string
}

export type TokenResponse = {
  access_token: string
  refresh_token: string
  token_type: 'bearer'
  expires_in: number
}

export type LoginCredentials = {
  email: string
  password: string
}

export type RegisterPayload = {
  email: string
  password: string
  first_name: string
  last_name: string
}
