import { Link } from "@tanstack/react-router"
import { Button } from "@/shared/ui/button"

export const NotFoundPage = () => {
  return (
    <div className="flex min-h-full flex-1 flex-col items-center justify-center gap-4 p-8 text-center">
      <h1 className="text-5xl font-bold tracking-tighter">404</h1>
      <p className="max-w-sm text-muted-foreground">
        Page not found. It may have been removed, or you may have mistyped the
        address.
      </p>
      <Button nativeButton={false} render={<Link to="/" />}>
        Go home
      </Button>
    </div>
  )
}
