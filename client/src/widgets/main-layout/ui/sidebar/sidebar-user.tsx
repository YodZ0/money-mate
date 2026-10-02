import { ChevronsUpDown } from "lucide-react"
import { UserAvatar, type User } from "@/entities/user"
import { LogoutMenuItem } from "@/features/auth"
import { ThemeSwitcherSubmenu } from "@/features/theme-switcher"
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/shared/ui/dropdown-menu"
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from "@/shared/ui/sidebar"

const UserInfo = ({ user }: { user: User }) => (
  <>
    <UserAvatar user={user} />
    <div className="grid flex-1 text-left text-sm leading-tight">
      <span className="truncate font-medium">{user.username}</span>
      {user.email && (
        <span className="truncate text-xs text-muted-foreground">
          {user.email}
        </span>
      )}
    </div>
  </>
)

export const SidebarUser = ({ user }: { user: User }) => {
  const { isMobile } = useSidebar()

  return (
    <SidebarMenu>
      <SidebarMenuItem>
        <DropdownMenu>
          <DropdownMenuTrigger
            render={<SidebarMenuButton size="lg" tooltip={user.username} />}
          >
            <UserInfo user={user} />
            <ChevronsUpDown className="ml-auto" />
          </DropdownMenuTrigger>

          <DropdownMenuContent
            className="min-w-56"
            side={isMobile ? "bottom" : "right"}
            align="end"
          >
            <DropdownMenuGroup>
              <DropdownMenuLabel className="flex items-center gap-2 font-normal text-foreground">
                <UserInfo user={user} />
              </DropdownMenuLabel>
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <DropdownMenuGroup>
              <ThemeSwitcherSubmenu />
            </DropdownMenuGroup>
            <DropdownMenuSeparator />
            <LogoutMenuItem />
          </DropdownMenuContent>
        </DropdownMenu>
      </SidebarMenuItem>
    </SidebarMenu>
  )
}
