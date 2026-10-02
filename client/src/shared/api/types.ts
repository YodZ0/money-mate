// API response wrappers. Adjust them to your backend's contract.
export interface ApiResponse<T> {
  data: T
  metadata: unknown | null
}

export interface ApiPaginatedResponse<T> {
  data: {
    objects: T[]
    count: number
  }
  metadata: unknown | null
}

export interface ApiErrorDetail {
  type: string
  msg: string
}

export interface ApiErrorResponse {
  detail: ApiErrorDetail | string
}
