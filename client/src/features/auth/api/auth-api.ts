import type { AuthTokens } from "@/entities/session"
import { apiClient, refreshClient } from "@/shared/api"

export interface LoginDto {
  username: string
  password: string
}

export const loginRequest = async (data: LoginDto): Promise<AuthTokens> => {
  const response = await apiClient.post<AuthTokens>("/auth/login", data)
  return response.data
}

export const logoutRequest = async (): Promise<void> => {
  await apiClient.post("/auth/logout")
}

// The refresh token is stored in an httpOnly cookie, so the request body is empty.
export const refreshTokenRequest = async (): Promise<AuthTokens> => {
  const response = await refreshClient.post<AuthTokens>("/auth/refresh")
  return response.data
}
