import { Spinner } from "@/shared/ui/spinner"

// Shown by the router while a lazy route loads or beforeLoad runs.
export const PageLoader = () => {
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-background/80 backdrop-blur-sm">
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        <Spinner />
        Loading...
      </div>
    </div>
  )
}
