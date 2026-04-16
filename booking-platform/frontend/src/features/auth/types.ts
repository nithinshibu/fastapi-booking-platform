/* These mirror the Pydantic schemas in the FastAPI backend exactly */

export interface RegisterRequest {
  email: string;
  password: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  token_type: string;
  /* 
  refresh token is no longer need in the response body as it is delivered as an
  HttpOnly cookie (Set-Cookie header) and managed entirely by the browser.
  */
}

export interface UserResponse {
  id: number;
  email: string;
}
