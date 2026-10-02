// Test-only utilities: never import from here in production code.
// setup.ts is loaded by Vitest directly (vite.config.ts → test.setupFiles).
export {
  createMockAdapter,
  type MockHandler,
  type MockResponse,
} from "./mock-adapter"
