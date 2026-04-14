/*
 * formatters.ts — Display Formatting Utilities
 *
 * Pure functions that convert raw data into user-friendly strings.
 * No React, no state, no side effects.
 *
 * Uses Intl API (built-in browser support for localization).
 */

/* ---------------- Show time ---------------- */
// Input:  "2024-06-15T19:30:00"
// Output: "Sat, 15 Jun - 19:30"

export function formatShowTime(isoString: string): string {
  try {
    return new Intl.DateTimeFormat("en-GB", {
      weekday: "short",
      day: "numeric",
      month: "short",
      hour: "2-digit",
      minute: "2-digit",
    }).format(new Date(isoString));
  } catch {
    return isoString;
  }
}

/* ---------------- Release date ---------------- */
// Input:  "2024-06-15"
// Output: "15 Jun 2024"

export function formatReleaseDate(isoDate: string): string {
  try {
    return new Intl.DateTimeFormat("en-GB", {
      day: "numeric",
      month: "short",
      year: "numeric",
    }).format(new Date(isoDate));
  } catch {
    return isoDate;
  }
}

/* ---------------- Duration ---------------- */
// Input:  150
// Output: "2h 30m"

export function formatDuration(minutes: number): string {
  const h = Math.floor(minutes / 60);
  const m = minutes % 60;

  if (h === 0) return `${m}m`;
  if (m === 0) return `${h}h`;

  return `${h}h ${m}m`;
}
