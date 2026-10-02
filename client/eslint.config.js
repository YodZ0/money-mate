import js from "@eslint/js"
import globals from "globals"
import reactHooks from "eslint-plugin-react-hooks"
import reactRefresh from "eslint-plugin-react-refresh"
import tseslint from "typescript-eslint"
import { defineConfig, globalIgnores } from "eslint/config"

// FSD architecture rules (import direction, public API, cross-imports)
// are checked by steiger: see steiger.config.ts and `npm run lint:fsd`.
export default defineConfig([
  globalIgnores(["dist", "coverage"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      js.configs.recommended,
      tseslint.configs.recommended,
      reactHooks.configs.flat.recommended,
      reactRefresh.configs.vite,
    ],
    languageOptions: {
      globals: globals.browser,
    },
    rules: {
      "@typescript-eslint/no-unused-vars": [
        "error",
        {
          argsIgnorePattern: "^_",
          varsIgnorePattern: "^_",
          caughtErrorsIgnorePattern: "^_",
        },
      ],
      "@typescript-eslint/consistent-type-imports": [
        "error",
        { fixStyle: "inline-type-imports" },
      ],
      // Imports that bypass a slice's public API: @/features/auth/model/... instead
      // of @/features/auth. Inside a slice, use relative paths.
      "no-restricted-imports": [
        "error",
        {
          patterns: [
            {
              regex: "^@/(app|pages|widgets|features|entities)/[^/]+/(?!@x/).+",
              message:
                "Import a slice through its public API (index.ts); inside the slice, use a relative path.",
            },
          ],
        },
      ],
    },
  },
  {
    // shadcn primitives export variants (buttonVariants) alongside
    // components, which is acceptable for fast refresh.
    // Route files export route objects alongside components.
    files: ["src/shared/ui/**", "src/app/routes/**"],
    rules: {
      "react-refresh/only-export-components": "off",
    },
  },
])
