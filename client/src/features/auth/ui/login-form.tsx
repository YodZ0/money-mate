import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import { cn } from "@/shared/lib/utils"
import { Button } from "@/shared/ui/button"
import { Field, FieldError, FieldGroup, FieldLabel } from "@/shared/ui/field"
import { Input } from "@/shared/ui/input"
import { Spinner } from "@/shared/ui/spinner"
import { loginSchema, type LoginFormData } from "../model/login-schema"
import { useLogin } from "../model/use-login"

export function LoginForm({
  className,
  ...props
}: Omit<React.ComponentProps<"form">, "onSubmit">) {
  const { mutate: login, isPending } = useLogin()

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
    defaultValues: { username: "", password: "" },
  })

  return (
    <form
      className={cn("flex flex-col gap-6", className)}
      onSubmit={handleSubmit((data) => login(data))}
      noValidate
      {...props}
    >
      <FieldGroup>
        <Field data-invalid={!!errors.username || undefined}>
          <FieldLabel htmlFor="username">Username</FieldLabel>
          <Input
            id="username"
            autoComplete="username"
            placeholder="ivan.ivanov"
            disabled={isPending}
            aria-invalid={!!errors.username}
            {...register("username")}
          />
          <FieldError errors={[errors.username]} />
        </Field>
        <Field data-invalid={!!errors.password || undefined}>
          <FieldLabel htmlFor="password">Password</FieldLabel>
          <Input
            id="password"
            type="password"
            autoComplete="current-password"
            disabled={isPending}
            aria-invalid={!!errors.password}
            {...register("password")}
          />
          <FieldError errors={[errors.password]} />
        </Field>
        <Field>
          <Button type="submit" disabled={isPending}>
            {isPending && <Spinner data-icon="inline-start" />}
            {isPending ? "Signing in..." : "Sign in"}
          </Button>
        </Field>
      </FieldGroup>
    </form>
  )
}
