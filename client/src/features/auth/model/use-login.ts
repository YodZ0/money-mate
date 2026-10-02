import { useMutation } from "@tanstack/react-query"
import { useNavigate, useSearch } from "@tanstack/react-router"
import { isAxiosError } from "axios"
import { toast } from "sonner"
import { useSessionStore } from "@/entities/session"
import { getMe } from "@/entities/user"
import { safeRedirect } from "@/shared/lib/safe-redirect"
import { loginRequest, type LoginDto } from "../api/auth-api"

export const useLogin = () => {
  const navigate = useNavigate()
  // strict: false, since the feature isn't bound to a specific route.
  const search: { redirect?: unknown } = useSearch({ strict: false })

  return useMutation({
    mutationFn: async (data: LoginDto) => {
      const { setSession, setUser } = useSessionStore.getState()
      setSession(await loginRequest(data))
      setUser(await getMe())
    },
    onSuccess: () => {
      navigate({ href: safeRedirect(search.redirect) })
    },
    onError: (error) => {
      useSessionStore.getState().clearSession()
      if (isAxiosError(error) && error.response?.status === 401) {
        toast.error("Invalid username or password")
      } else if (!isAxiosError(error) || !error.response) {
        // Responses with a status (403, 429, 5xx) are already reported by the apiClient interceptor.
        toast.error("Failed to sign in", {
          description: "The server is unavailable. Please try again later.",
        })
      }
    },
  })
}
