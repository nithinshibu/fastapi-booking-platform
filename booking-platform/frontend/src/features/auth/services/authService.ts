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
