import { createRouter } from "@tanstack/react-router"
import { NotFoundPage } from "@/pages/not-found"
import { PageLoader } from "@/shared/ui/page-loader"
import { authLayoutRoute } from "./layouts"
import { rootRoute } from "./root"
import { homeRoute } from "./home"
import { loginRoute } from "./login"

const routeTree = rootRoute.addChildren([
  loginRoute,
  authLayoutRoute.addChildren([homeRoute]),
])

export const router = createRouter({
  routeTree,
  defaultNotFoundComponent: NotFoundPage,
  defaultPendingComponent: PageLoader,
  // The loader appears only if loading takes longer than 300 ms and stays
  // for at least 300 ms, so fast navigations don't flicker.
  defaultPendingMs: 300,
  defaultPendingMinMs: 300,
  defaultPreload: "intent",
})

declare module "@tanstack/react-router" {
  interface Register {
    router: typeof router
  }
}
