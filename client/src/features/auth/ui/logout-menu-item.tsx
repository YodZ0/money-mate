import { LogOut } from "lucide-react"
import { DropdownMenuItem } from "@/shared/ui/dropdown-menu"
import { useLogout } from "../model/use-logout"

export const LogoutMenuItem = () => {
  const { mutate: logout, isPending } = useLogout()

  return (
    <DropdownMenuItem
      variant="destructive"
      disabled={isPending}
      onClick={() => logout()}
    >
      <LogOut />
      {isPending ? "Logging out..." : "Log out"}
    </DropdownMenuItem>
  )
}
