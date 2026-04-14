/* 

authService.ts - Auth API Layer

This file contains pure async functions that make HTTP calls to the authentication endpoints.
No React, no hooks, no state - just data in , data out.

ARCHITECTURE RULE : 
- API calls live ONLY in service files.

Components -> Hooks -> Services -> apiClient -> Backend

Functions throw an error and let the caller (hook/component) decide 
how to handle it - same as how a .NET repository throws exceptions and the service layer 
catches / handles them.

WHAT CHANGED FOR REFRESH TOKENS:
- login() now returns {access_token,refresh_token,token_type}
- refreshToken() exchanges a refresh token for a new pair
- logoutApi() revokes the refresh token server-side

IMPORTANT - refreshToken() uses a raw axios call, NOT apiClient.
Why? apiClient has an interceptor that catches 401 errors and calls
refreshToken().
If refreshToken() also used apiClient, a failed refresh would call refreshToken() again
-> infinite loop occurs.
Using raw axios breaks the cycle.



*/

import axios from "axios";
import apiClient from "../../../services/apiClient";
import { ENDPOINTS } from "../../../services/endpoints";
import { API_URL } from "../../../config/env";
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

---- refreshToken ----

Exchange the stored refresh token for a new access token + refresh token pair.

Why raw axios (not apiClient) ?

apiClient has a response interceptor that catches 401 errors and calls This
function. If we again used apiClient here ,a failed refresh would trigger the interceptor
again which calls refreshToken() again which leads to a infinite loop.

Raw axios skips the interceptor entirely , breaking the cycle.

*/

export async function refreshToken(
  storedRefreshToken: string,
): Promise<TokenResponse> {
  const response = await axios.post<TokenResponse>(
    `${API_URL}${ENDPOINTS.auth.refresh}`,
    { refresh_token: storedRefreshToken },
  );
  return response.data;
}

/* 

---- Logout ----

Revoke the refresh token server-side
Called before clearing local storage so the server side session is ended.
Even if this request fails (network issues) we still clear the localStorage -
the user is logged out from the client's perspective.

*/

export async function logoutApi(storedRefreshToken: string): Promise<void> {
  await apiClient.post(ENDPOINTS.auth.logout, {
    refresh_token: storedRefreshToken,
  });
}
