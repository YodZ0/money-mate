/// <reference types="vitest/config" />
import { resolve } from "node:path"
import tailwindcss from "@tailwindcss/vite"
import react from "@vitejs/plugin-react"
import { defineConfig, loadEnv } from "vite"

// Vendor chunks: large libraries needed on the first screen are split
// into stable chunks for long-term caching.
// Entries are RegExp fragments matched against package names in node_modules.
const VENDOR_CHUNKS: Record<string, string[]> = {
  "vendor-react": ["react", "react-dom", "scheduler"],
  "vendor-tanstack": [
    "@tanstack/[^/]*router[^/]*",
    "@tanstack/[^/]*query[^/]*",
    "@tanstack/history",
  ],
  "vendor-forms": ["react-hook-form", "@hookform/resolvers", "zod"],
}

const vendorPattern = (packages: string[]) =>
  new RegExp(`[\\\\/]node_modules[\\\\/](${packages.join("|")})[\\\\/]`)

export default defineConfig(({ mode }) => {
  // The third argument "" also loads variables without the VITE_ prefix (they
  // are only used by the dev server and never reach the client bundle).
  const env = loadEnv(mode, process.cwd(), "")

  return {
    plugins: [react(), tailwindcss()],
    resolve: {
      alias: {
        "@": resolve(import.meta.dirname, "./src"),
      },
    },
    build: {
      rolldownOptions: {
        output: {
          // Strip console.* and debugger in production.
          minify: {
            compress: {
              dropConsole: mode === "production",
              dropDebugger: true,
            },
          },
          codeSplitting: {
            groups: Object.entries(VENDOR_CHUNKS).map(([name, packages]) => ({
              name,
              test: vendorPattern(packages),
            })),
          },
        },
      },
    },
    server: {
      port: 5173,
      // /api requests are proxied to the backend: no CORS in dev, and cookies
      // (refresh token) are set on the same origin as in production.
      proxy: {
        "/api": {
          target: env.API_PROXY_TARGET || "http://localhost:8000",
          changeOrigin: true,
        },
      },
    },
    test: {
      environment: "jsdom",
      setupFiles: ["./src/shared/lib/test/setup.ts"],
      css: false,
      coverage: {
        provider: "v8",
        reporter: ["text", "html"],
        include: ["src/**/*.{ts,tsx}"],
        // shadcn primitives are generated code and excluded from coverage.
        exclude: ["src/shared/ui/**", "src/**/*.test.{ts,tsx}", "src/main.tsx"],
      },
    },
  }
})
