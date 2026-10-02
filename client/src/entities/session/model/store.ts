import { create } from "zustand"
import type { User } from "@/entities/user/@x/session"
import type { AuthTokens, SessionState } from "./types"

interface SessionActions {
  setSession: (tokens: AuthTokens) => void
  setUser: (user: User) => void
  clearSession: () => void
}

const initialState: SessionState = {
  accessToken: null,
  permissions: [],
  user: null,
  isAuth: false,
}

// The access token lives only in memory: after a reload the session
// is restored via the refresh cookie (see features/auth/check-auth).
export const useSessionStore = create<SessionState & SessionActions>()(
  (set) => ({
    ...initialState,

    setSession: ({ accessToken, permissions }) =>
      set({ accessToken, permissions, isAuth: true }),

    setUser: (user) => set({ user }),

    clearSession: () => set(initialState),
  })
)
