/**
 * Integration test of the whole app: real router, guards, session store
 * and interceptors. Only the network is mocked (axios adapter).
 */
import { render, screen } from "@testing-library/react"
import userEvent from "@testing-library/user-event"
import { describe, expect, it, vi } from "vitest"
import type { MockResponse } from "@/shared/lib/test"

const user = {
  id: "1",
  username: "ivan.ivanov",
  email: "ivan@example.com",
  avatarUrl: null,
}
const tokens = { accessToken: "access", permissions: [] }
const unauthorized: MockResponse = {
  status: 401,
  data: { detail: { type: "not_authenticated", msg: "" } },
}

// Each test gets fresh modules: the router and the store are singletons.
const renderApp = async (
  url: string,
  routes: Record<string, MockResponse | (() => MockResponse)>
) => {
  vi.resetModules()
  window.history.replaceState(null, "", url)

  const { apiClient, refreshClient } = await import("@/shared/api")
  const { createMockAdapter } = await import("@/shared/lib/test")
  const { App } = await import("@/app")

  const adapter = createMockAdapter(routes)
  apiClient.defaults.adapter = adapter
  refreshClient.defaults.adapter = adapter

  return render(<App />)
}

describe("App", () => {
  it("redirects to /login without a session and remembers where to return", async () => {
    await renderApp("/", { "POST /auth/refresh": unauthorized })

    expect(
      await screen.findByRole("heading", { level: 1, name: /sign in/i })
    ).toBeInTheDocument()
    expect(window.location.pathname).toBe("/login")
    expect(new URLSearchParams(window.location.search).get("redirect")).toBe(
      "/"
    )
  })

  it("shows validation errors without calling the API", async () => {
    const login = vi.fn(() => ({ status: 200, data: tokens }))
    await renderApp("/login", {
      "POST /auth/refresh": unauthorized,
      "POST /auth/login": login,
    })

    await userEvent.click(
      await screen.findByRole("button", { name: "Sign in" })
    )

    expect(await screen.findByText("Enter your username")).toBeInTheDocument()
    expect(login).not.toHaveBeenCalled()
  })

  it("opens the home page with the username after login", async () => {
    await renderApp("/login", {
      "POST /auth/refresh": unauthorized,
      "POST /auth/login": { status: 200, data: tokens },
      "GET /users/me": { status: 200, data: { data: user } },
    })

    await userEvent.type(
      await screen.findByLabelText("Username"),
      "ivan.ivanov"
    )
    await userEvent.type(screen.getByLabelText("Password"), "password123")
    await userEvent.click(screen.getByRole("button", { name: "Sign in" }))

    expect(
      await screen.findByRole("heading", { level: 1, name: "Home" })
    ).toBeInTheDocument()
    expect(screen.getByText(/Welcome, ivan.ivanov/)).toBeInTheDocument()
    expect(window.location.pathname).toBe("/")
  })

  it("restores the session via refresh without the login form", async () => {
    await renderApp("/", {
      "POST /auth/refresh": { status: 200, data: tokens },
      "GET /users/me": { status: 200, data: { data: user } },
    })

    expect(
      await screen.findByRole("heading", { level: 1, name: "Home" })
    ).toBeInTheDocument()
  })

  it("shows 404 for an unknown path", async () => {
    await renderApp("/does-not-exist", {
      "POST /auth/refresh": { status: 200, data: tokens },
      "GET /users/me": { status: 200, data: { data: user } },
    })

    expect(await screen.findByText("404")).toBeInTheDocument()
  })
})
