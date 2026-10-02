import type { User } from "@/entities/user/@x/session"

/** Backend response to login/refresh. */
export interface AuthTokens {
  accessToken: string
  permissions: string[]
}

export interface SessionState {
  accessToken: string | null
  permissions: string[]
  user: User | null
  isAuth: boolean
}
