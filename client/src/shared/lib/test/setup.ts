import "@testing-library/jest-dom/vitest"
import { cleanup } from "@testing-library/react"
import { afterEach } from "vitest"

// Without unmounting, the DOM accumulates between tests and stale nodes
// leak into testing-library queries.
afterEach(() => {
  cleanup()
})

// jsdom doesn't implement matchMedia, which next-themes and useIsMobile rely on.
Object.defineProperty(window, "matchMedia", {
  writable: true,
  value: (query: string) => ({
    matches: false,
    media: query,
    onchange: null,
    addEventListener: () => {},
    removeEventListener: () => {},
    addListener: () => {},
    removeListener: () => {},
    dispatchEvent: () => false,
  }),
})

// The router scrolls to the top after navigation; jsdom can't do that.
window.scrollTo = () => {}
