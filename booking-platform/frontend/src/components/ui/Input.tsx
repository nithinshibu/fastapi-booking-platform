/* 

This Input component is a reusable, standardized form input wrapper designed for clean and scalable React apps.

It combines a label, input field, error message, and helper text into one reusable component.
Using forwardRef lets parent libraries like react-hook-form directly access the <input> for things like focusing invalid fields.
Extending InputHTMLAttributes means it supports all normal input props (type, placeholder, onChange, etc.) without redefining them.
It automatically links the label and input using id for better accessibility.
It conditionally shows an error message or helper text, keeping UI logic consistent across the app.
Accessibility is improved with aria-invalid and aria-describedby so screen readers understand input state.
It centralizes styling (input-base, input-error) to maintain a consistent design system.
It reduces duplication since all forms reuse this instead of rewriting input logic.
The component fits clean architecture by keeping UI elements modular, reusable, and independent.
Overall, it acts as a single source of truth for input behavior and styling in your frontend.

*/

import { forwardRef } from "react";
import type { InputHTMLAttributes } from "react";

interface InputProps extends InputHTMLAttributes<HTMLInputElement> {
  label: string;
  error?: string;
  helperText?: string;
}

// forwardRef: allows parent components to get a direct ref to the <input> element.
// react-hook-form needs this to focus invalid inputs on submission.
// .NET analogy: it's like passing an out parameter — the caller can get a handle
// to the internal element if they need direct access.
export const Input = forwardRef<HTMLInputElement, InputProps>(
  ({ label, error, helperText, id, className = "", ...rest }, ref) => {
    // Generate an id from the input name if not provided, for label association
    const inputId = id ?? rest.name;

    return (
      <div className="flex flex-col gap-1.5">
        {/* Label – the 'htmlFor' links it to the input by id (accessibility) */}
        <label
          htmlFor={inputId}
          className="text-sm font-medium text-[--color-text-secondary]"
        >
          {label}
        </label>

        {/* Input – applies error styling when an error message is present */}
        <input
          ref={ref}
          id={inputId}
          aria-invalid={!!error}
          aria-describedby={
            error
              ? `${inputId}-error`
              : helperText
                ? `${inputId}-helper`
                : undefined
          }
          className={`input-base ${error ? "input-error" : ""} ${className}`}
          {...rest}
        />

        {/* Error message – only shown when 'error' prop is provided */}
        {error && (
          <p
            id={`${inputId}-error`}
            className="text-xs text-[--color-error]"
            role="alert"
          >
            {error}
          </p>
        )}

        {/* Helper text – shown when no error */}
        {!error && helperText && (
          <p
            id={`${inputId}-helper`}
            className="text-xs text-[--color-text-muted]"
          >
            {helperText}
          </p>
        )}
      </div>
    );
  },
);

Input.displayName = "Input";
