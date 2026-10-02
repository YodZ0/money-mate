import { AxiosHeaders } from "axios"
import { beforeEach, describe, expect, it, vi } from "vitest"
import { createMockAdapter } from "@/shared/lib/test"
import { apiClient, EXPIRED_TOKEN_ERROR, setupApiInterceptors } from "./client"

vi.mock("sonner", () => ({ toast: { error: vi.fn() } }))

const expired = {
  status: 401,
  data: { detail: { type: EXPIRED_TOKEN_ERROR, msg: "" } },
}

const authHeader = (config: { headers?: unknown }) =>
  new AxiosHeaders(config.headers as AxiosHeaders).get("Authorization")

describe("setupApiInterceptors", () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it("attaches the Bearer token", async () => {
    const seen: unknown[] = []
    apiClient.defaults.adapter = createMockAdapter({
      "GET /items": (config) => {
        seen.push(authHeader(config))
        return { status: 200 }
      },
    })
    setupApiInterceptors({
      getToken: () => "token",
      refreshToken: vi.fn(),
      onFail: vi.fn(),
    })

    await apiClient.get("/items")

    expect(seen).toEqual(["Bearer token"])
  })

  it("on expired_token refreshes the token once and retries all requests", async () => {
    let token = "old"
    apiClient.defaults.adapter = createMockAdapter({
      "GET /a": (config) =>
        authHeader(config) === "Bearer new" ? { status: 200 } : expired,
      "GET /b": (config) =>
        authHeader(config) === "Bearer new" ? { status: 200 } : expired,
    })
    const refreshToken = vi.fn(async () => {
      await new Promise((resolve) => setTimeout(resolve, 10))
      token = "new"
      return token
    })
    const onFail = vi.fn()
    setupApiInterceptors({ getToken: () => token, refreshToken, onFail })

    const responses = await Promise.all([
      apiClient.get("/a"),
      apiClient.get("/b"),
    ])

    expect(responses.map((r) => r.status)).toEqual([200, 200])
    expect(refreshToken).toHaveBeenCalledTimes(1)
    expect(onFail).not.toHaveBeenCalled()
  })

  it("calls onFail and rejects the request if refresh fails", async () => {
    apiClient.defaults.adapter = createMockAdapter({ "GET /a": expired })
    const onFail = vi.fn()
    setupApiInterceptors({
      getToken: () => "old",
      refreshToken: vi.fn().mockRejectedValue(new Error("refresh failed")),
      onFail,
    })

    await expect(apiClient.get("/a")).rejects.toThrow("refresh failed")
    expect(onFail).toHaveBeenCalledTimes(1)
  })

  it("does not call onFail on other 401s without a session (wrong password)", async () => {
    apiClient.defaults.adapter = createMockAdapter({
      "POST /auth/login": { status: 401, data: { detail: "bad" } },
    })
    const onFail = vi.fn()
    setupApiInterceptors({
      getToken: () => null,
      refreshToken: vi.fn(),
      onFail,
    })

    await expect(apiClient.post("/auth/login")).rejects.toMatchObject({
      response: { status: 401 },
    })
    expect(onFail).not.toHaveBeenCalled()
  })

  it("calls onFail on other 401s with an active session", async () => {
    apiClient.defaults.adapter = createMockAdapter({
      "GET /a": { status: 401, data: { detail: { type: "invalid_token" } } },
    })
    const refreshToken = vi.fn()
    const onFail = vi.fn()
    setupApiInterceptors({ getToken: () => "token", refreshToken, onFail })

    await expect(apiClient.get("/a")).rejects.toBeDefined()
    expect(onFail).toHaveBeenCalledTimes(1)
    expect(refreshToken).not.toHaveBeenCalled()
  })
})
