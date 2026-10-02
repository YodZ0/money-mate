import { cn } from "@/shared/lib/utils"
import { Avatar, AvatarFallback, AvatarImage } from "@/shared/ui/avatar"
import type { User } from "../model/types"

const getInitials = (username: string) =>
  username
    .split(/[\s._-]+/)
    .filter(Boolean)
    .slice(0, 2)
    .map((part) => part[0]!.toUpperCase())
    .join("")

export const UserAvatar = ({
  user,
  className,
}: {
  user: User
  className?: string
}) => {
  return (
    <Avatar className={cn("size-8 rounded-lg", className)}>
      {user.avatarUrl && (
        <AvatarImage src={user.avatarUrl} alt={user.username} />
      )}
      <AvatarFallback className="rounded-lg select-none">
        {getInitials(user.username)}
      </AvatarFallback>
    </Avatar>
  )
}
