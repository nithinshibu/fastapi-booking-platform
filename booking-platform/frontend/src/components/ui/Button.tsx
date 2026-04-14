/*
 * Button.tsx – Reusable Button Component
 *
 * This is a “design system” component — one button that covers every use case
 * in the app through variants and sizes. Never write a raw <button> in a page
 * component; always use <Button> so styling stays consistent.
 *
 * PROPS DESIGN PATTERN: extends React.ButtonHTMLAttributes
 * This forwards ALL native button props (onClick, type, disabled, aria-label, etc.)
 * automatically. You don't need to redeclare them.
 *
 * .NET analogy: a base controller or helper that handles common concerns
 * (auth, logging) so each controller only adds its specific logic.
 * Extending the native props = inheriting from a base class.
 *
 * VARIANT PATTERN: a plain object maps variant names to Tailwind class strings.
 * This is cleaner than a switch statement and easy to extend — add a new
 * variant by adding one line to the object.
 */

import type { ButtonHTMLAttributes, ReactNode } from "react";
import { Spinner } from "./Spinner";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: "primary" | "secondary" | "danger" | "ghost";
  size?: "sm" | "md" | "lg";
  isLoading?: boolean;
  leftIcon?: ReactNode;
}

// Each variant defines the full set of color + hover + focus styles
// using Tailwind CSS with our custom color tokens from globals.css
const variantClasses: Record<NonNullable<ButtonProps["variant"]>, string> = {
  primary:
    "bg-[--color-brand] text-[--color-text-primary] font-semibold hover:bg-[--color-brand-dark] active:scale-[0.98]",
  secondary:
    "bg-[--color-surface-elevated] text-[--color-text-primary] border border-[--color-border] hover:bg-slate-600 hover:border-slate-500 active:scale-[0.98]",
  danger: "bg-red-600 text-white hover:bg-red-700 active:scale-[0.98]",
  ghost:
    "bg-transparent text-[--color-brand] hover:bg-[--color-surface] active:scale-[0.98]",
};

const sizeClasses: Record<NonNullable<ButtonProps["size"]>, string> = {
  sm: "px-3 py-1.5 text-sm rounded-md",
  md: "px-4 py-2.5 text-sm rounded-lg",
  lg: "px-6 py-3 text-base rounded-xl",
};

export function Button({
  variant = "primary",
  size = "md",
  isLoading = false,
  leftIcon,
  children,
  disabled,
  className = "",
  ...rest
}: ButtonProps) {
  return (
    <button
      disabled={disabled || isLoading}
      className={[
        "inline-flex items-center justify-center gap-2",
        "font-medium transition-all duration-150",
        "disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100",
        "cursor-pointer",
        variantClasses[variant],
        sizeClasses[size],
        className,
      ].join(" ")}
      {...rest}
    >
      {/* Show spinner on left side when loading, otherwise show the icon */}
      {isLoading ? (
        <Spinner size="sm" />
      ) : leftIcon ? (
        <span className="flex-shrink-0">{leftIcon}</span>
      ) : null}

      {children}
    </button>
  );
}
