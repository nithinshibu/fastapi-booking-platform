/*
 * router.tsx — Application Routing Configuration
 *
 * Defines every URL route and which component renders at that URL.
 *
 * React Router v7 (createBrowserRouter):
 * - Config-based routing (not JSX <Route>)
 * - Better TypeScript support
 * - Route-level lazy loading (code splitting)
 * - Nested routes (Layout → child pages)
 *
 * Lazy loading:
 * - Pages are loaded only when visited
 * - Improves initial load performance
 */

import { lazy, Suspense } from "react";
import { createBrowserRouter, Navigate } from "react-router-dom";

import { Layout } from "../components/layout/Layout";
import { ProtectedRoute } from "../components/layout/ProtectedRoute";
import { Spinner } from "../components/ui/Spinner";

/* ---------------- Lazy pages ---------------- */

const LoginPage = lazy(() =>
  import("../features/auth/pages/LoginPage").then((m) => ({
    default: m.LoginPage,
  })),
);

const RegisterPage = lazy(() =>
  import("../features/auth/pages/RegisterPage").then((m) => ({
    default: m.RegisterPage,
  })),
);

const MoviesPage = lazy(() =>
  import("../features/movies/pages/MoviesPage").then((m) => ({
    default: m.MoviesPage,
  })),
);

const MovieDetailPage = lazy(() =>
  import("../features/movies/pages/MovieDetailPage").then((m) => ({
    default: m.MovieDetailPage,
  })),
);

/* ---------------- Loader ---------------- */

function PageLoader() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-[--color-bg]">
      <Spinner size="lg" />
    </div>
  );
}

/* ---------------- Router ---------------- */

export const router = createBrowserRouter([
  /* ---------- Public routes ---------- */
  {
    path: "/login",
    element: (
      <Suspense fallback={<PageLoader />}>
        <LoginPage />
      </Suspense>
    ),
  },
  {
    path: "/register",
    element: (
      <Suspense fallback={<PageLoader />}>
        <RegisterPage />
      </Suspense>
    ),
  },

  /* ---------- Protected routes ---------- */
  {
    path: "/",
    element: (
      <ProtectedRoute>
        <Layout />
      </ProtectedRoute>
    ),
    children: [
      {
        index: true,
        element: <Navigate to="/movies" replace />,
      },
      {
        path: "movies",
        element: (
          <Suspense fallback={<PageLoader />}>
            <MoviesPage />
          </Suspense>
        ),
      },
      {
        path: "movies/:id",
        element: (
          <Suspense fallback={<PageLoader />}>
            <MovieDetailPage />
          </Suspense>
        ),
      },
    ],
  },

  /* ---------- Catch-all ---------- */
  {
    path: "*",
    element: <Navigate to="/" replace />,
  },
]);
