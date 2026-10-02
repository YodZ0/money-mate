import { Link, type LinkProps } from "@tanstack/react-router"
import { House, type LucideIcon } from "lucide-react"
import { usePermission } from "@/entities/session"
import {
  SidebarGroup,
  SidebarGroupContent,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/shared/ui/sidebar"

interface NavItem {
  title: string
  to: LinkProps["to"]
  icon: LucideIcon
  /** The item is visible only if the user has this permission. */
  permission?: string
}

// Add new sections here after registering the route in app/routes.
const NAV_ITEMS: NavItem[] = [{ title: "Home", to: "/", icon: House }]

export const SidebarNav = () => {
  const { can } = usePermission()
  const items = NAV_ITEMS.filter(
    (item) => !item.permission || can(item.permission)
  )

  return (
    <SidebarGroup>
      <SidebarGroupContent>
        <SidebarMenu>
          {items.map((item) => (
            <SidebarMenuItem key={item.title}>
              <SidebarMenuButton
                tooltip={item.title}
                render={
                  <Link
                    to={item.to}
                    activeOptions={{ exact: true }}
                    activeProps={{ "data-active": true }}
                  />
                }
              >
                <item.icon />
                <span>{item.title}</span>
              </SidebarMenuButton>
            </SidebarMenuItem>
          ))}
        </SidebarMenu>
      </SidebarGroupContent>
    </SidebarGroup>
  )
}
