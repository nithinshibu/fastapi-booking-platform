/*
 * RegisterPage.tsx — Registration Page (Smart Component)
 *
 * After a successful registration, we automatically log the user in.
 * This is a UX decision: users expect to be taken to the app immediately,
 * not asked to log in again right after creating their account.
 *
 * Flow:
 * 1. authService.register() → creates the account (returns UserResponse, not a token)
 * 2. login()               → exchanges credentials for a token, saves to localStorage
 * 3. navigate('/movies')   → user is now logged in and on the movies page
 *
 * If register fails (e.g. email already taken), we show the error.
 * If register succeeds but login fails somehow, we send to /login as a fallback.
 */

import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";
import { RegisterForm } from "../components/RegisterForm";
import * as authService from "../services/authService";
import { handleApiError } from "../../../utils/errorHandler";

import type { RegisterFormData } from "../schemas/registerSchema";

export function RegisterPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [apiError, setApiError] = useState<string | null>(null);

  const handleSubmit = async (data: RegisterFormData) => {
    try {
      setApiError(null);

      // Step 1: Create the account
      // { email, password } only — confirmPassword is stripped
      await authService.register({
        email: data.email,
        password: data.password,
      });

      // Step 2: Auto-login
      await login({
        username: data.email,
        password: data.password,
      });

      // Step 3: Redirect to movies page
      navigate("/movies");
    } catch (error) {
      setApiError(handleApiError(error));
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-[--color-bg] px-4">
      <div className="w-full max-w-md">
        {/* Brand header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-[--color-text-primary]">
            <span className="text-[--color-brand]">Cine</span>Book
          </h1>
          <p className="mt-2 text-[--color-text-secondary]">
            Create your account
          </p>
        </div>

        {/* Card */}
        <div className="card p-8">
          <RegisterForm onSubmit={handleSubmit} error={apiError} />
        </div>
      </div>
    </div>
  );
}
