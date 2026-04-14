/* 

loginSchema.ts - Login Form Validation Rules 

What is ZOD ?

Zod is a TypeScript first schema validation library.
We define the shape and rules of our data in one place and Zod gives
back us both:
    1. Runtime validation (checks the actual values at runtime).
    2. Static Typescript types (inferred automatically - no duplication)

.NET equivalent : FluentValidation - we define rules like RuleFor(x=>x.Email).NotEmpty().EmailAddress()
and it validates the  model and collects errors in the same way.

How it connects to the React Hook Form :
We pass the schema to the zodResolver() which brings zod and react-hook-form.
When the form is submitted , Zod runs the validation and react-hook-form puts any
errors into formState.errors - one error object per field.

*/

import { z } from "zod";

export const loginSchema = z.object({
  email: z
    .string()
    .min(1, "Email is required")
    .email("Please enter a valid email address"),

  password: z.string().min(1, "Password is required"),
});

//Typescript type inferred from the scheme - no need to define it separately.
// z.infer<typeof loginSchema> gives us : {email:string; password:string}

export type LoginFormData = z.infer<typeof loginSchema>;
