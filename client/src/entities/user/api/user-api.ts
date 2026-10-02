import { apiClient, type ApiResponse } from "@/shared/api"
import type { User } from "../model/types"

export const getMe = async (): Promise<User> => {
  const response = await apiClient.get<ApiResponse<User>>("/users/me")
  return response.data.data
}
