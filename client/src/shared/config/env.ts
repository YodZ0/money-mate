// Single access point for environment variables. Components and API code
// never read import.meta.env directly: the variable list stays in one place
// and defaults aren't scattered around. Variables are described in .env.example.
export const env = {
  API_BASE_URL: import.meta.env.VITE_API_BASE_URL || "/api/v1",
  APP_NAME: import.meta.env.VITE_APP_NAME || "Money Mate",
  ENABLE_DEBUG: import.meta.env.VITE_ENABLE_DEBUG === "true",
  IS_DEV: import.meta.env.DEV,
} as const
