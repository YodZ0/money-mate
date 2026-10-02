import fsd from "@feature-sliced/steiger-plugin"
import { defineConfig } from "steiger"

// FSD architecture linter: checks import direction between layers,
// slice public APIs, cross-imports and segment structure.
// Run: npm run lint:fsd
export default defineConfig([
  ...fsd.configs.recommended,
  {
    // In the template many slices have a single consumer so far. That is fine
    // for a start; the rule becomes meaningful as the project grows.
    rules: {
      "fsd/insignificant-slice": "off",
    },
  },
])
