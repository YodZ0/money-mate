import { useSessionStore } from "@/entities/session"
import { Card, CardDescription, CardHeader, CardTitle } from "@/shared/ui/card"
import { Page } from "@/shared/ui/page"

export const HomePage = () => {
  const user = useSessionStore((state) => state.user)

  return (
    <Page>
      <Page.Header>
        <Page.Heading>
          <Page.Title>Home</Page.Title>
          <Page.Description>Application start page</Page.Description>
        </Page.Heading>
      </Page.Header>
      <Page.Content>
        <Card>
          <CardHeader>
            <CardTitle>Welcome, {user?.username}!</CardTitle>
            <CardDescription>
              Start with a new page in src/pages and a route in src/app/routes.
            </CardDescription>
          </CardHeader>
        </Card>
      </Page.Content>
    </Page>
  )
}
