/* 

AuthContext.tsx - Global Authentication State

WHAT CHANGED FOR REFRESH TOKENS:
- login() now saves BOTH access_token and refresh_token to localStorage
- logout() calls the server first to revoke the refresh token, THEN clears
      local state (ensures the server side session is ended)
- Session restore : on page load, if the access token is expired the apiClient
  interceptor will automatically refresh it - no extra logic needed here

*/


import { createContext, useContext, useEffect, useState } from "react";
import type { ReactNode } from "react";
import * as authService from "../features/auth/services/authService";
import type { UserResponse, LoginRequest } from "../features/auth/types";
import { TOKEN_KEY,REFRESH_TOKEN_KEY, USER_KEY } from "../constants";

// ---- Type Definition ----

// This is the "shape" of what useAuth() returns.
// Every component that calls useAuth() gets exactly these fields.

export interface AuthContextType {
  // The currently logged-in user or null if not authenticated
  user: UserResponse | null;

  // The JWT Token or null. Mostly used internally - components use
  // 'user' to check auth state , not the raw token.
  token: string | null;

  // True during the initial session restore check on page load.
  // ProtectedRoute uses this to avoid redirecting before we know if the user is
  // logged in.
  isLoading: boolean;

  // Log in : calls the API, saves the token, fetches the user profile
  login: (credentials: LoginRequest) => Promise<void>;

  // Log out: clears stored data and resets state
  logout: () => Promise<void>;
}

// ---- Context Object ----

/* 

createContext(null) creates the context with null as the initial value.
The real value is set by the AuthProvider below.
Exported so the useAuth hook can read it.

*/

export const AuthContext = createContext<AuthContextType | null>(null);

// ---- AuthProvider ----

/* 
This component wraps the app (in providers.tsx) and makes the auth state
availbale to everything inside it via AuthContext.Provider.

Think of it as the implementation class of ICurrentUserService - it holds 
the state and exposes methods (login,logout) to interact with it.

*/

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true); // start true - we haven't checked yet.

  //---- Session Restore ----
  /* 
  What is useEffect ?
  - useEffect runs AFTER the component renders. The empty [] dependency array
  means "run once,after the first render"
  
  On every page load , we check if a token exists in localStorage.
  If it does, we call /users/me to verify it is still valid and get the user.
  This is what keeps users logged in across browser refreshes.
  
  -----Flow-----

  Page loads -> useEffect runs -> token found -> getMe() -> user set -> isLoading = false

  Page loads -> useEffect runs -> no token -> nothing -> isLoading = false  
  
  */

  useEffect(() => {
    const restoreSession = async () => {
      const storedToken = localStorage.getItem(TOKEN_KEY);
      if (!storedToken) {
        // No token - user hasn't logged in. Nothing to restore.
        setIsLoading(false);
        return;
      }
      try {
        // Token exists - verify it's still valid by fetching the user profile.
        // The appClient interceptor automatically attaches the token to this request.
        const currentUser = await authService.getMe();
        setToken(localStorage.getItem(TOKEN_KEY)); //may have been refreshed by interceptor
        setUser(currentUser);
      } catch {
        // Token is expired or invalid - clean up and start fresh.
        // The 401 interceptor in apiClient will also fire , but we handle it here too
        // to ensure clean state before isLoading becomes false
        localStorage.removeItem(TOKEN_KEY);
        localStorage.removeItem(REFRESH_TOKEN_KEY);
        localStorage.removeItem(USER_KEY);
      } finally {
        //Always set isLoading to false when done, whether success or failure.
        //This unblocks ProtectedRoute from making its redirect decision.
        setIsLoading(false);
      }
    };
    restoreSession();
  }, []); // empty array = run once on mount

  // ---- login ----
  /* 
  
  Called by LoginPage. NOW SAVED BOTH TOKENS
  Steps:
    1. Call the API to exchange credentials for a token.
    2. Save the token to localStorage (persists across refreshes)
    3. Call /users/me to get the user profile and save it
    4. Update React State - everything re-renders with the new user.

  Note: we throw on error so LoginPage can catch it and show the error message.
  This keeps error display logic in the UI Layer , not here.
  
  */

  const login = async (credentials: LoginRequest) => {
    const tokenResponse = await authService.login(credentials);
    localStorage.setItem(TOKEN_KEY, tokenResponse.access_token);
    localStorage.setItem(REFRESH_TOKEN_KEY, tokenResponse.refresh_token);

    const currentUser = await authService.getMe();
    localStorage.setItem(USER_KEY, JSON.stringify(currentUser));

    setToken(tokenResponse.access_token);
    setUser(currentUser);
  };

  // ---- Logout ----
  /* 
  Clears everything. The appClient interceptor redirects to /login on 401,
  but this is the explicit logout - called by the Navbar's Sign Out button.

  Two-step logout:
  1. Tell the server to revoke the refresh token (server side session ended)
  2. Clear local storage and reset React state.

  Step 1 can fail (network issue, token already expired) - we always 
  proceed to step 2 regardless , because the user's intent is to log out.
  Even a failed server call means the session will expire naturally.

  */
  const logout = async () => {

    const storedRefreshToken = localStorage.getItem(REFRESH_TOKEN_KEY)

    if(storedRefreshToken){
      try{
        await authService.logoutApi(storedRefreshToken)
      }catch{
        // Ignore errors - proceed to local clean up regardless
      }
    }

    localStorage.removeItem(TOKEN_KEY);
    localStorage.removeItem(REFRESH_TOKEN_KEY);
    localStorage.removeItem(USER_KEY);
    setToken(null);
    setUser(null);
    //Hard redirect - clears all React state and sends user to login page
    window.location.href = "/login";
  };

  // --Provide the value --
  /* Everything inside the <AuthProvider> can now access {user,token,isLoading,login,logout} via the useAuth() hook */
  return (
    <AuthContext.Provider value={{ user, token, isLoading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
}

// --- useAuth hook (convenience export)

/* 
Exported here as a convenience so imports can be:
import {useAuth} from "../context/AuthContext"
instead of importing from two files.

The canonical useAuth hook is in featurs/auth/hooks/useAuth.ts

*/

export function useAuth(): AuthContextType {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error(
      "useAuth must be used inside <AuthProviders>." +
        "Make sure your component is rendered inside AppProviders.",
    );
  }
  return context;
}
