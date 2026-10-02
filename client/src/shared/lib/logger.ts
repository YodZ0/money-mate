import { env } from "@/shared/config"

// console.* is stripped entirely from the production build (see vite.config.ts),
// so the IS_DEV check here only matters for tests and preview.
export const logger = {
  debug: (...args: unknown[]) => {
    if (env.IS_DEV && env.ENABLE_DEBUG) console.log("[DEBUG]:", ...args)
  },
  info: (...args: unknown[]) => {
    if (env.IS_DEV) console.info("[INFO]:", ...args)
  },
  error: (...args: unknown[]) => {
    if (env.IS_DEV) console.error("[ERROR]:", ...args)
  },
}
