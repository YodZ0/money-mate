import { createRoute, redirect } from "@tanstack/react-router"
import { z } from "zod"
import { checkAuth } from "@/features/auth"
import { LoginPage } from "@/pages/login"
import { safeRedirect } from "@/shared/lib/safe-redirect"
import { rootRoute } from "./root"

export const loginRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/login",
  // Where to return the user after login (set by the authenticated area guard).
  validateSearch: z.object({ redirect: z.string().optional() }),
  beforeLoad: async ({ search }) => {
    if (await checkAuth()) {
      throw redirect({ href: safeRedirect(search.redirect) })
    }
  },
  component: LoginPage,
})
