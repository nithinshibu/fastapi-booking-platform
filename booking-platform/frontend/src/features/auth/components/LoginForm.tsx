/* 

LoginForm.tsx - Login Form UI component 

This is a dumb UI component - it receives data and callbacks as props
and renders the form. It knows NOTHING about the API or auth state.

REACT HOOK FORMS CONCEPTS :

useForm() initializes the form engine. It returns :
        register() - connects an input to the react-hook-form (tracks value + validation)
        handleSubmit - wraps our submit handler; only calls it if the validation passes
        formState - contains {errors , isSubmitting} and other state.

zodResolver (loginSchema) - the bridge between Zod and react-hook-form .
It tells react-hook-form to use the Zod schema as the validation engine.
When the handleSubmit runs , Zod validates the values and put any errors into
formState.errors - keyed by the field name.

Separation of Concerns :
The form component handles UI + Validation.
The page component handles what happens after submission (API call , navigation)
This way the form is resuable - we could embed it in a model later.

*/

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link } from "react-router-dom";
import { Input } from "../../../components/ui/Input";
import { Button } from "../../../components/ui/Button";
import { loginSchema } from "../schemas/loginSchema";
import type { LoginFormData } from "../schemas/loginSchema";

interface LoginFormProps {
  //Called with validated form data when the user submits
  onSubmit: (data: LoginFormData) => Promise<void>;
  //Optional API error to display (eg: Invalid credentials)
  error?: string | null;
}

export function LoginForm({ onSubmit, error }: LoginFormProps) {
  const [showPassword, setShowPassword] = useState(false);
  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginFormData>({
    resolver: zodResolver(loginSchema),
  });

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      noValidate
      className="flex flex-col gap-5"
    >
      {/* API error banner - shown when credentials are wrong */}
      {error && (
        <div className="rounded-lg bg-red-500/10 border border-red-500/30 p-3 text-sm text-[--color-error]">
          {error}
        </div>
      )}
      <Input
        label="Email Address"
        type="email"
        placeholder="you@example.com"
        autoComplete="email"
        {...register("email")}
        error={errors.email?.message}
      />

      <div className="flex flex-col gap-1.5">
        <Input
          label="Password"
          type={showPassword ? "text" : "password"}
          placeholder="Your password"
          autoComplete="current-password"
          {...register("password")}
          error={errors.password?.message}
        />
        {/* Show or hide password toggle */}
        <button
          type="button"
          onClick={() => setShowPassword((prev) => !prev)}
          className="self-end text-xs text-[--color-text-muted] hover:text-[--color-brand] transition-colors cursor-pointer"
        >
          {showPassword ? "Hide password" : "Show Password"}
        </button>
      </div>
      <Button type="submit" isLoading={isSubmitting} className="w-full mt-2">
        Sign in
      </Button>
      <p className="text-center text-sm text-[--color-text-secondary]">
        Don&apos;t have an account?{" "}
        <Link
          to="/register"
          className="text-[--color-brand] hover:text-[--color-brand-dark] font-medium"
        >
          Create one
        </Link>
      </p>
    </form>
  );
}
