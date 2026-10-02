import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "@tanstack/react-router"
import { useSessionStore } from "@/entities/session"
import { logoutRequest } from "../api/auth-api"

export const useLogout = () => {
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  return useMutation({
    mutationFn: logoutRequest,
    // onSettled: clear the local session even if the backend didn't respond.
    onSettled: () => {
      useSessionStore.getState().clearSession()
      queryClient.clear()
      navigate({ to: "/login" })
    },
  })
}
