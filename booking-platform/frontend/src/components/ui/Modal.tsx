/* 

This Modal component is a popup dialog box that appears on top of the page when needed.

It shows the modal only when isOpen is true; otherwise it renders nothing.
It uses createPortal (from React) to render the modal outside the normal component tree, directly into document.body.
When the modal opens, it disables background scrolling so the user can’t scroll the page behind it.
It listens for the Escape key and closes the modal when pressed, improving usability.
The dark backdrop covers the screen, and clicking on it will close the modal.
Clicking inside the modal content won’t close it because of stopPropagation().
It supports different sizes (sm, md, lg) to control how wide the modal appears.
The header contains a title and a close button for easy interaction.
children allows you to pass any custom content inside the modal (forms, text, etc.).
Accessibility is handled using attributes like role="dialog" and aria-modal so screen readers


*/

import { useEffect } from "react";
import { createPortal } from "react-dom";
import type { ReactNode } from "react";
import { Button } from "./Button";

interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: ReactNode;
  size?: "sm" | "md" | "lg";
}

const sizeClasses = {
  sm: "max-w-sm",
  md: "max-w-md",
  lg: "max-w-2xl",
};

export function Modal({
  isOpen,
  onClose,
  title,
  children,
  size = "md",
}: ModalProps) {
  // Prevent background scrolling while modal is open
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = "hidden";
    }

    return () => {
      document.body.style.overflow = "";
    };
  }, [isOpen]);

  // Close on Escape key – important for keyboard accessibility
  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };

    if (isOpen) {
      document.addEventListener("keydown", handleEscape);
    }

    return () => document.removeEventListener("keydown", handleEscape);
  }, [isOpen, onClose]);

  if (!isOpen) return null;

  return createPortal(
    // Backdrop – the dark overlay behind the modal panel
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4"
      style={{ backgroundColor: "rgba(0, 0, 0, 0.7)" }}
      onClick={onClose} // clicking backdrop closes the modal
    >
      {/* Modal panel – stopPropagation prevents closing when clicking inside */}
      <div
        className={[
          "relative w-full rounded-xl bg-[--color-surface] p-6",
          "shadow-[--shadow-modal] border border-[--color-border]",
          sizeClasses[size],
        ].join(" ")}
        onClick={(e) => e.stopPropagation()}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
      >
        {/* Header */}
        <div className="flex items-center justify-between mb-4">
          <h2
            id="modal-title"
            className="text-lg font-semibold text-[--color-text-primary]"
          >
            {title}
          </h2>

          <Button
            variant="ghost"
            size="sm"
            onClick={onClose}
            aria-label="Close modal"
            className="text-[--color-text-muted] hover:text-[--color-text-primary]"
          >
            ×
          </Button>
        </div>

        {/* Content */}
        {children}
      </div>
    </div>,
    document.body, // portal target – renders outside the React tree
  );
}
