import axios, { type AxiosError, type InternalAxiosRequestConfig } from "axios"
import { toast } from "sonner"
import { env } from "@/shared/config"
import { logger } from "@/shared/lib/logger"
import type { ApiErrorResponse } from "./types"

interface RetryableRequestConfig extends InternalAxiosRequestConfig {
  _retry?: boolean
}

export interface InterceptorOptions {
  /** Current access token, or null if there is no session. */
  getToken: () => string | null
  /** Refreshes the session and returns a new access token. */
  refreshToken: () => Promise<string>
  /** Called when the session cannot be restored: logout and redirect. */
  onFail: () => void
}

/** Error code the backend uses to report an expired access token. */
export const EXPIRED_TOKEN_ERROR = "expired_token"

let isRefreshing = false
let failedQueue: Array<{
  resolve: (token: string) => void
  reject: (error: unknown) => void
}> = []

const processQueue = (error: unknown, token: string | null = null) => {
  failedQueue.forEach((promise) => {
    if (error) promise.reject(error)
    else promise.resolve(token as string)
  })
  failedQueue = []
}

const getErrorType = (error: AxiosError<ApiErrorResponse>) => {
  const detail = error.response?.data?.detail
  return typeof detail === "object" && detail !== null ? detail.type : ""
}

// Separate client without interceptors: refresh must not intercept itself.
export const refreshClient = axios.create({
  baseURL: env.API_BASE_URL,
  withCredentials: true,
  timeout: 5000,
})

export const apiClient = axios.create({
  baseURL: env.API_BASE_URL,
  headers: { "Content-Type": "application/json" },
  withCredentials: true,
  timeout: 10000,
})

/**
 * Attaches authorization to apiClient. Called once from the app layer:
 * shared knows nothing about the session, so the token source and the logout
 * handler are passed in from outside (dependency inversion).
 */
export const setupApiInterceptors = (options: InterceptorOptions) => {
  apiClient.interceptors.request.clear()
  apiClient.interceptors.response.clear()

  apiClient.interceptors.request.use((config) => {
    const token = options.getToken()
    if (token) config.headers.Authorization = `Bearer ${token}`
    return config
  })

  apiClient.interceptors.response.use(
    (response) => response,
    async (error: AxiosError<ApiErrorResponse>) => {
      const originalRequest = error.config as RetryableRequestConfig | undefined
      const status = error.response?.status

      if (status === 401 && originalRequest && !originalRequest._retry) {
        if (getErrorType(error) !== EXPIRED_TOKEN_ERROR) {
          // Without a token there is nothing to tear down, e.g. a wrong password on /login.
          // The calling code handles such errors itself.
          if (options.getToken()) options.onFail()
          return Promise.reject(error)
        }

        // Refresh is already in progress: queue the request and retry with the new token.
        if (isRefreshing) {
          return new Promise<string>((resolve, reject) => {
            failedQueue.push({ resolve, reject })
          }).then((token) => {
            originalRequest.headers.Authorization = `Bearer ${token}`
            return apiClient(originalRequest)
          })
        }

        originalRequest._retry = true
        isRefreshing = true

        try {
          const newToken = await options.refreshToken()
          processQueue(null, newToken)
          originalRequest.headers.Authorization = `Bearer ${newToken}`
          return apiClient(originalRequest)
        } catch (refreshError) {
          processQueue(refreshError)
          options.onFail()
          return Promise.reject(refreshError)
        } finally {
          isRefreshing = false
        }
      }

      if (status === 403) {
        logger.debug("403:", error.response?.data?.detail)
        toast.error("Access denied")
      }

      if (status === 429) {
        toast.error("Too many requests", {
          description: "Please wait a moment and try again.",
        })
      }

      if (status && status >= 500) {
        logger.debug("Server error:", error.response?.data?.detail)
        toast.error("Server error", {
          description: "Something went wrong. Please try again later.",
        })
      }

      return Promise.reject(error)
    }
  )
}
