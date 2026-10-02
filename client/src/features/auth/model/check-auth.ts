import { useSessionStore } from "@/entities/session"
import { getMe } from "@/entities/user"
import { logger } from "@/shared/lib/logger"
import { refreshTokenRequest } from "../api/auth-api"

/**
 * Checks whether there is an active session. If there is none in memory (e.g.
 * after a page reload), tries to restore it via the refresh cookie.
 * Used in route beforeLoad hooks.
 */
export const checkAuth = async (): Promise<boolean> => {
  const session = useSessionStore.getState()
  if (session.isAuth) return true

  try {
    session.setSession(await refreshTokenRequest())
    session.setUser(await getMe())
    return true
  } catch (error) {
    logger.debug("Session not restored:", error)
    session.clearSession()
    return false
  }
}
