/* 

authService.ts - Auth API Layer

Pure async functions for auth endpoints. No React , no state , no hooks.

Refresh token is now an HttpOnly cookie - the browser sends it automatically.
logoutApi() no longer needs a token argument; the cookie is sent by the browser.



*/

import apiClient from "../../../services/apiClient";
import { ENDPOINTS } from "../../../services/endpoints";
import type {
  LoginRequest,
  RegisterRequest,
  TokenResponse,
  UserResponse,
} from "../types";

// ---- LOGIN ----

/* 

IMPORTANT - The FastAPI backend uses OAuth2PasswordRequestForm for login.
This means the request body must be form-encoded, NOT JSON.

Form-encoded looks like: "username=test@email.com&password=secret"

If we send JSON, FastAPI returns 422 Unprocessable Entity (silent failure)
that looks like a backend bug.

URLSearchParams automatically creates the correct form-encoded body.
We override Content-type just for this one call (the axios default is application/json).

*/

export async function login(credentials: LoginRequest): Promise<TokenResponse> {
  const formData = new URLSearchParams({
    username: credentials.username,
    password: credentials.password,
  });

  const response = await apiClient.post<TokenResponse>(
    ENDPOINTS.auth.login,
    formData,
    {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    },
  );

  return response.data;
}

// ---- REGISTER ----

/* 
Standard JSON POST - no special handling needed.
Returns the created user (NOT A TOKEN - the user must log in after registering).

*/

export async function register(data: RegisterRequest): Promise<UserResponse> {
  const response = await apiClient.post<UserResponse>(
    ENDPOINTS.auth.register,
    data,
  );
  return response.data;
}

// ---- getMe ----

/* 
Fetches the current user's profile using the stored JWT Token.
The token is automatically attached by the request interceptor in apiClient.ts

Called on app startup to restore a previous session from localStorage.

*/

export async function getMe(): Promise<UserResponse> {
  const response = await apiClient.get<UserResponse>(ENDPOINTS.auth.me);
  return response.data;
}

/* 



/* 

---- Logout ----

Revoke the refresh token server-side
The refresh_token cookie is sent automatically by the browser (withCredentials).
Called before clearing local storage so the server side session is ended.
Even if this request fails (network issues),the caller still clear the localStorage -
the user is logged out from the client's perspective.

*/

export async function logoutApi(): Promise<void> {
  await apiClient.post(ENDPOINTS.auth.logout);
}
