import * as React from "react"
import { cn } from "@/shared/lib/utils"
import { ScrollArea } from "@/shared/ui/scroll-area"

// Page skeleton inside the authenticated layout: header + scrollable content.
// <Page.Title> is the page's only <h1>.

function PageRoot({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div
      className={cn("flex h-full flex-col overflow-hidden", className)}
      {...props}
    />
  )
}

function PageHeader({ className, ...props }: React.ComponentProps<"header">) {
  return (
    <header
      className={cn(
        "flex min-h-16 shrink-0 flex-wrap items-center justify-between gap-4 border-b bg-card px-4 py-3 md:px-6",
        className
      )}
      {...props}
    />
  )
}

function PageHeading({ className, ...props }: React.ComponentProps<"div">) {
  return (
    <div className={cn("flex min-w-0 flex-col gap-1", className)} {...props} />
  )
}

function PageTitle({ className, ...props }: React.ComponentProps<"h1">) {
  return (
    <h1
      className={cn("truncate text-xl font-semibold tracking-tight", className)}
      {...props}
    />
  )
}

function PageDescription({ className, ...props }: React.ComponentProps<"p">) {
  return (
    <p className={cn("text-sm text-muted-foreground", className)} {...props} />
  )
}

function PageActions({ className, ...props }: React.ComponentProps<"div">) {
  return <div className={cn("flex items-center gap-2", className)} {...props} />
}

function PageContent({
  className,
  children,
  ...props
}: React.ComponentProps<typeof ScrollArea>) {
  return (
    <ScrollArea
      className={cn("min-h-0 flex-1 bg-muted/50 dark:bg-background", className)}
      {...props}
    >
      <div className="mx-auto w-full max-w-7xl min-w-0 p-4 md:p-6">
        {children}
      </div>
    </ScrollArea>
  )
}

export const Page = Object.assign(PageRoot, {
  Header: PageHeader,
  Heading: PageHeading,
  Title: PageTitle,
  Description: PageDescription,
  Actions: PageActions,
  Content: PageContent,
})
