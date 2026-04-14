/*
 * RegisterForm.tsx — Registration Form UI Component
 *
 * Same patterns as LoginForm.tsx. Additional points:
 *
 * - confirmPassword field: frontend-only validation — not sent to the API.
 *   The page strips it before calling register().
 *
 * - The Zod schema uses .refine() to compare two fields.
 *   Errors on a refine() attach to the path you specified in the schema
 *   (["confirmPassword"]) so errors.confirmPassword?.message works normally.
 *
 * - For comments on useForm, register, handleSubmit, zodResolver — see LoginForm.tsx.
 */

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Link } from "react-router-dom";

import { Input } from "../../../components/ui/Input";
import { Button } from "../../../components/ui/Button";

import { registerSchema } from "../schemas/registerSchema";
import type { RegisterFormData } from "../schemas/registerSchema";

interface RegisterFormProps {
  onSubmit: (data: RegisterFormData) => Promise<void>;
  error?: string | null;
}

export function RegisterForm({ onSubmit, error }: RegisterFormProps) {
  const [showPassword, setShowPassword] = useState(false);

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterFormData>({
    resolver: zodResolver(registerSchema),
  });

  return (
    <form
      onSubmit={handleSubmit(onSubmit)}
      noValidate
      className="flex flex-col gap-5"
    >
      {error && (
        <div className="rounded-lg bg-red-500/10 border border-red-500/30 p-3 text-sm text-[--color-error]">
          {error}
        </div>
      )}

      <Input
        label="Email address"
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
          placeholder="Minimum 8 characters"
          autoComplete="new-password"
          helperText="Must be at least 8 characters"
          {...register("password")}
          error={errors.password?.message}
        />

        <button
          type="button"
          onClick={() => setShowPassword((prev) => !prev)}
          className="self-end text-xs text-[--color-text-muted] hover:text-[--color-brand] transition-colors cursor-pointer"
        >
          {showPassword ? "Hide password" : "Show password"}
        </button>
      </div>

      <Input
        label="Confirm password"
        type={showPassword ? "text" : "password"}
        placeholder="Repeat your password"
        autoComplete="new-password"
        {...register("confirmPassword")}
        error={errors.confirmPassword?.message}
      />

      <Button type="submit" isLoading={isSubmitting} className="w-full mt-2">
        Create account
      </Button>

      <p className="text-center text-sm text-[--color-text-secondary]">
        Already have an account?{" "}
        <Link
          to="/login"
          className="text-[--color-brand] hover:text-[--color-brand-dark] font-medium"
        >
          Sign in
        </Link>
      </p>
    </form>
  );
}
