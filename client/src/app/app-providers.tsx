import { QueryClientProvider } from "@tanstack/react-query"
import { ThemeProvider } from "next-themes"
import type { ReactNode } from "react"
import { Toaster } from "@/shared/ui/sonner"
import { TooltipProvider } from "@/shared/ui/tooltip"
import { queryClient } from "./query/query-client"

export const AppProviders = ({ children }: { children: ReactNode }) => {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider
        attribute="class"
        defaultTheme="system"
        enableSystem
        disableTransitionOnChange
      >
        <TooltipProvider>
          {children}
          <Toaster position="bottom-right" richColors />
        </TooltipProvider>
      </ThemeProvider>
    </QueryClientProvider>
  )
}
