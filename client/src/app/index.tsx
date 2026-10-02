import { RouterProvider } from "@tanstack/react-router"
import { setupApi } from "./api/setup-api"
import { AppProviders } from "./app-providers"
import { router } from "./routes"
import "./styles/index.css"

setupApi()

export const App = () => {
  return (
    <AppProviders>
      <RouterProvider router={router} />
    </AppProviders>
  )
}
