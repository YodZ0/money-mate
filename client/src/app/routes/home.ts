import { createRoute, lazyRouteComponent } from "@tanstack/react-router"
import { authLayoutRoute } from "./layouts"

export const homeRoute = createRoute({
  getParentRoute: () => authLayoutRoute,
  path: "/",
  // Pages are lazy-loaded: each one goes into its own chunk.
  component: lazyRouteComponent(() => import("@/pages/home"), "HomePage"),
})
