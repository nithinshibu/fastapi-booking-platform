/*
 * Navbar.tsx — Application Navigation Bar
 *
 * The Navbar is a "smart" layout component — it reads auth state from context
 * to conditionally render logged-in vs. logged-out navigation options.
 *
 * Layout components (Navbar, Sidebar, Footer) are allowed to read context
 * directly because they are always aware of app-level state.
 * Pure UI components (Button, Input, Card) should never read context.
 *
 * STICKY POSITIONING:
 * The navbar stays at the top as you scroll down.
 * Tailwind: sticky top-0 z-40 keeps it above content but below modals.
 */

import { Link, NavLink } from "react-router-dom";
import { useAuth } from "../../features/auth/hooks/useAuth";
import { Button } from "../ui/Button";

export function Navbar() {
  const { user, logout } = useAuth();

  return (
    <header className="sticky top-0 z-40 bg-[--color-surface] border-b border-[--color-border]">
      <nav className="container-page h-16 flex items-center justify-between">
        {/* Brand logo */}
        <Link to="/" className="flex items-center gap-2 text-xl font-bold">
          {/* Film icon */}
          <span className="text-2xl">🎬</span>
          <span>
            <span className="text-[--color-brand]">Cine</span>
            <span className="text-[--color-text-primary]">Book</span>
          </span>
        </Link>

        {/* Navigation + auth */}
        <div className="flex items-center gap-2">
          {user ? (
            <>
              {/* Logged-in */}
              <NavLink
                to="/movies"
                className={({ isActive }) =>
                  `px-3 py-2 rounded-lg text-sm font-medium transition-colors ${
                    isActive
                      ? "text-[--color-brand] bg-[--color-surface-elevated]"
                      : "text-[--color-text-secondary] hover:text-[--color-text-primary] hover:bg-[--color-surface-elevated]"
                  }`
                }
              >
                Movies
              </NavLink>

              {/* User email */}
              <span className="hidden sm:block text-xs text-[--color-text-muted] px-3 py-1 bg-[--color-surface-elevated] rounded-full">
                {user.email}
              </span>

              <Button variant="ghost" size="sm" onClick={logout}>
                Sign out
              </Button>
            </>
          ) : (
            <>
              {/* Logged-out */}
              <Link
                to="/login"
                className="px-3 py-2 text-sm font-medium text-[--color-text-secondary] hover:text-[--color-text-primary] transition-colors"
              >
                Sign in
              </Link>

              <Button
                variant="primary"
                size="sm"
                onClick={() => {
                  window.location.href = "/register";
                }}
              >
                Get started
              </Button>
            </>
          )}
        </div>
      </nav>
    </header>
  );
}
