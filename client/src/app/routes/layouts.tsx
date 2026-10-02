import {
  createRoute,
  lazyRouteComponent,
  redirect,
} from "@tanstack/react-router"
import { checkAuth } from "@/features/auth"
import { rootRoute } from "./root"

/**
 * Pathless route of the authenticated area. All protected pages are attached
 * here (getParentRoute: () => authLayoutRoute) and get the guard and layout.
 */
export const authLayoutRoute = createRoute({
  getParentRoute: () => rootRoute,
  id: "authenticated",
  beforeLoad: async ({ location }) => {
    if (!(await checkAuth())) {
      throw redirect({ to: "/login", search: { redirect: location.href } })
    }
  },
  // The layout is lazy: the login screen doesn't need the sidebar and its primitives.
  component: lazyRouteComponent(
    () => import("@/widgets/main-layout"),
    "MainLayout"
  ),
})
