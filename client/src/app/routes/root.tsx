import { createRootRoute, Outlet } from "@tanstack/react-router"
import { lazy, Suspense } from "react"

// Devtools load only in dev: in the production build the branch is removed
// along with its imports, so the packages never reach the bundle.
const Devtools = import.meta.env.DEV
  ? lazy(() => import("./devtools"))
  : () => null

export const rootRoute = createRootRoute({
  component: () => (
    <>
      <Outlet />
      <Suspense>
        <Devtools />
      </Suspense>
    </>
  ),
})
