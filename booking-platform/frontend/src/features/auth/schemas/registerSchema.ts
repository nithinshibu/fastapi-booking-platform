/* 
registerSchema.ts - Register Form Validation Rules 

Same concept as loginSchema.ts - a Zod schema for the register form.

New pattern here : z.refine() for cross field validation.

Standard validators check one field at a time.
refine() lets us write a custom check that sees the whole object - 
used here to ensure password and confirmPassword match.

confirmPassword is FRONTEND only.
The backend doesn't know about it - we strip it before sending the API request.
The form collects it to give the user a good UX; the API doesn't need it.

*/
import { z } from "zod";

export const registerSchema = z
  .object({
    email: z
      .string()
      .min(1, "Email is required")
      .email("Please enter a valid email address"),

    password: z.string().min(8, "Password must be atleast 8 characters"),

    confirmPassword: z.string().min(1, "Please confirm your password"),
  })
  .refine((data) => data.password === data.confirmPassword, {
    // the error message to show
    message: "Passwords do not match",
    //Which field to attach the error to (confirmPassword input shows the red border)
    path: ["confirmPassword"],
  });

export type RegisterFormData = z.infer<typeof registerSchema>;
