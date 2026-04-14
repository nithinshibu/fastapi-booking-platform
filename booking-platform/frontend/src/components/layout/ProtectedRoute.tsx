/* 

ProtectedRoute.tsx - Auth Guard for Protected Pages

This component wraps any page that requires authentication.
If the user is not logged in, they are redirected to /login.
If the session restore still in progress , a spinner is shown.

Why the isLoading CHECK is CRITICAL : 

When the app first loads , AuthContext runs a useEffect to check localStorage
for an exisiting token and calls /users/me to validate it.
This takes a few milliseconds. During that time, user is null (the check hasn't finished yet).

Without the isLoading guard:

User has a valid token -> page loads -> user is null (check not done yet)
    -> ProtectedRoute redirects to /login -> 401 flash (wrong behavior)

With the isLoading guard:
    User has a valid token -> page loads -> isLoading is true -> show spinner
    -> check completes -> user is set -> render the actual page (correct behavior)

.NET equivalent is the [Authorize] attribute on a controller.
The attribute checks the current user and returns 401/redirect if not authenticated.
isLoading is the equivalent of waiting for the auth middleware to finish before the controller action runs.


The "replace" on <Navigate> means the /login URL replaces the current entry in the browser history.
So pressing Back after logging in doesn't go back to the protected page - it goes to whatever 
was before (good UX for auth redirects)

*/

import { Navigate } from "react-router-dom";
import type { ReactNode } from "react";
import { useAuth } from "../../features/auth/hooks/useAuth";
import { Spinner } from "../ui/Spinner";

interface ProtectedRouteProps {
  children: ReactNode;
}

export function ProtectedRoute({ children }: ProtectedRouteProps) {
  const { user, isLoading } = useAuth();

  //Session restore is progress - wait before making a redirect decision
  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-[--color-bg]">
        <Spinner size="lg" />
      </div>
    );
  }

  //Not authenticated - redirect to login
  if (!user) {
    return <Navigate to="/login" replace />;
  }

  //Authenticated - render the protected content
  return <>{children}</>;
}
