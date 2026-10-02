import { z } from "zod"

export const loginSchema = z.object({
  username: z.string().trim().min(1, "Enter your username"),
  password: z
    .string()
    .min(1, "Enter your password")
    .min(8, "Password must be at least 8 characters"),
})

export type LoginFormData = z.infer<typeof loginSchema>
