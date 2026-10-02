import { Outlet } from "@tanstack/react-router"
import { env } from "@/shared/config"
import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/shared/ui/sidebar"
import { AppSidebar } from "./sidebar/app-sidebar"

/** Shell of the authenticated area: sidebar + page area. */
export const MainLayout = () => {
  return (
    <SidebarProvider className="h-svh">
      <AppSidebar />
      <SidebarInset className="min-w-0 overflow-hidden">
        {/* On mobile the sidebar is a Sheet, and there is no other way to open it. */}
        <div className="flex h-12 shrink-0 items-center gap-2 border-b px-2 md:hidden">
          <SidebarTrigger />
          <span className="truncate text-sm font-semibold">{env.APP_NAME}</span>
        </div>
        <Outlet />
      </SidebarInset>
    </SidebarProvider>
  )
}
