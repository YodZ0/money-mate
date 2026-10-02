/**
 * Returns target only if it is an internal application path.
 * Otherwise ?redirect=https://evil.com becomes an open redirect.
 */
export const safeRedirect = (target: unknown, fallback = "/") =>
  typeof target === "string" &&
  target.startsWith("/") &&
  !target.startsWith("//") &&
  !target.startsWith("/\\")
    ? target
    : fallback
