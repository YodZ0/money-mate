import { useSessionStore } from "./store"

/** Checks the current user's permissions for conditional rendering. */
export const usePermission = () => {
  const permissions = useSessionStore((state) => state.permissions)

  const can = (permission: string) => permissions.includes(permission)

  return { can }
}
