import { AxiosError, type AxiosAdapter, type AxiosResponse } from "axios"

export interface MockResponse {
  status: number
  data?: unknown
}

export type MockHandler = (
  config: Parameters<AxiosAdapter>[0]
) => MockResponse | Promise<MockResponse>

/**
 * Mocks the axios network: the key is "METHOD /url" (url without baseURL), the
 * value is a response or a function of the request config. Unmatched requests get 404.
 *
 * @example
 * apiClient.defaults.adapter = createMockAdapter({
 *   "GET /users/me": { status: 200, data: { data: user } },
 * })
 */
export const createMockAdapter = (
  routes: Record<string, MockResponse | MockHandler>
): AxiosAdapter => {
  return async (config) => {
    const key = `${config.method?.toUpperCase()} ${config.url}`
    const route = routes[key]
    const { status, data } = route
      ? typeof route === "function"
        ? await route(config)
        : route
      : { status: 404, data: { detail: `No mock for ${key}` } }

    const response: AxiosResponse = {
      data,
      status,
      statusText: String(status),
      headers: {},
      config,
    }

    if (status >= 400) {
      throw new AxiosError(
        `Request failed with status code ${status}`,
        undefined,
        config,
        null,
        response
      )
    }
    return response
  }
}
