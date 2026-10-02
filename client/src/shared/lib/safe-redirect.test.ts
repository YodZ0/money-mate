import { describe, expect, it } from "vitest"
import { safeRedirect } from "./safe-redirect"

describe("safeRedirect", () => {
  it.each(["/", "/users", "/users/1?tab=info#top"])(
    "allows internal path %s",
    (path) => {
      expect(safeRedirect(path)).toBe(path)
    }
  )

  it.each([
    "https://evil.com",
    "//evil.com",
    "/\\evil.com",
    "javascript:alert(1)",
    "",
    undefined,
    42,
  ])("replaces %s with fallback", (target) => {
    expect(safeRedirect(target)).toBe("/")
  })
})
