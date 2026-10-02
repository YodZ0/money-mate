import { describe, expect, it } from "vitest"
import { loginSchema } from "./login-schema"

const valid = { username: "ivan.ivanov", password: "password123" }

describe("loginSchema", () => {
  it("accepts valid data", () => {
    expect(loginSchema.safeParse(valid).success).toBe(true)
  })

  it("trims whitespace in the username", () => {
    expect(loginSchema.parse({ ...valid, username: "  ivan  " }).username).toBe(
      "ivan"
    )
  })

  it.each([
    ["empty username", { ...valid, username: "   " }],
    ["empty password", { ...valid, password: "" }],
    ["short password", { ...valid, password: "1234567" }],
  ])("rejects: %s", (_case, data) => {
    expect(loginSchema.safeParse(data).success).toBe(false)
  })
})
