import { ReactQueryDevtools } from "@tanstack/react-query-devtools"
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools"

// Both buttons sit in the bottom-right corner: the bottom-left holds the sidebar profile.
export default function Devtools() {
  return (
    <>
      <div className="fixed right-44 bottom-2 z-99999">
        <ReactQueryDevtools buttonPosition="relative" />
      </div>
      <TanStackRouterDevtools position="bottom-right" />
    </>
  )
}
