import { useSessionStore } from "@/entities/session"
import { refreshTokenRequest } from "@/features/auth"
import { setupApiInterceptors } from "@/shared/api"
import { queryClient } from "../query/query-client"
import { router } from "../routes"

/**
 * Wires shared/api to the session. Done in app because only this layer
 * is allowed to know about shared, entities and features at once.
 */
export const setupApi = () => {
  setupApiInterceptors({
    getToken: () => useSessionStore.getState().accessToken,

    refreshToken: async () => {
      const tokens = await refreshTokenRequest()
      useSessionStore.getState().setSession(tokens)
      return tokens.accessToken
    },

    onFail: () => {
      useSessionStore.getState().clearSession()
      queryClient.clear()
      router.navigate({ to: "/login" })
    },
  })
}
