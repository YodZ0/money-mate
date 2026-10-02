import { useSessionStore } from "@/entities/session"
import { env } from "@/shared/config"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarRail,
} from "@/shared/ui/sidebar"
import { SidebarNav } from "./sidebar-nav"
import { SidebarUser } from "./sidebar-user"

export const AppSidebar = () => {
  const user = useSessionStore((state) => state.user)

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader>
        <div className="flex h-10 items-center gap-2 overflow-hidden px-1">
          <div className="flex size-8 shrink-0 items-center justify-center rounded-md bg-primary text-sm font-semibold text-primary-foreground select-none">
            {env.APP_NAME[0]}
          </div>
          <span className="truncate font-semibold group-data-[collapsible=icon]:hidden">
            {env.APP_NAME}
          </span>
        </div>
      </SidebarHeader>

      <SidebarContent>
        <SidebarNav />
      </SidebarContent>

      <SidebarFooter>{user && <SidebarUser user={user} />}</SidebarFooter>
      <SidebarRail />
    </Sidebar>
  )
}
