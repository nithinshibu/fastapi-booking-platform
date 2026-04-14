/*
 * LoginPage.tsx — Login Page (Smart Component)
 *
 * This is a "smart" component — it handles business logic and side effects.
 * It knows about auth state (useAuth), routing (useNavigate), and error handling.
 * The LoginForm component above is "dumb" — it just renders UI.
 *
 * SEPARATION OF CONCERNS in practice:
 * LoginForm   → WHAT the form looks like + client validation
 * LoginPage   → WHAT HAPPENS when the form is submitted (API + navigation)
 *
 * .NET analogy:
 * LoginForm = Razor partial view (pure HTML/binding)
 * LoginPage = Controller action (handles the HTTP request, calls service, redirects)
 *
 * IMPORTANT — the username/email mapping:
 * The form field is named 'email' (user-friendly label).
 * The backend's OAuth2 endpoint expects a field named 'username'.
 * We transform data.email → username here before calling login().
 */

import { useState } from "react";
import { useNavigate } from "react-router-dom";

import { useAuth } from "../hooks/useAuth";
import { LoginForm } from "../components/LoginForm";
import { handleApiError } from "../../../utils/errorHandler";

import type { LoginFormData } from "../schemas/loginSchema";

export function LoginPage() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [apiError, setApiError] = useState<string | null>(null);

  const handleSubmit = async (data: LoginFormData) => {
    try {
      setApiError(null);

      // Map the form's 'email' field to the OAuth2-required 'username' field
      await login({
        username: data.email,
        password: data.password,
      });

      navigate("/movies");
    } catch (error) {
      // Extract 'detail' field from FastAPI error response
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
            Sign in to your account
          </p>
        </div>

        {/* Card */}
        <div className="card p-8">
          <LoginForm onSubmit={handleSubmit} error={apiError} />
        </div>
      </div>
    </div>
  );
}
