/*
 * MovieCard.tsx — Movie List Card Component
 *
 * "Dumb" component — receives movie as props and renders UI.
 * No hooks, no API calls, no state.
 */

import { Link } from "react-router-dom";
import type { MovieResponse } from "../types";
import { formatDuration } from "../../../utils/formatters";

interface MovieCardProps {
  movie: MovieResponse;
}

export function MovieCard({ movie }: MovieCardProps) {
  const year = new Date(movie.release_date).getFullYear();

  return (
    <Link to={`/movies/${movie.id}`} className="group block">
      <article className="card overflow-hidden transition-transform duration-300 group-hover:scale-[1.02] group-hover:shadow-xl">
        {/* Poster area */}
        <div className="aspect-[2/3] bg-[--color-surface-elevated] flex flex-col items-center justify-center gap-3 relative overflow-hidden">
          {/* Gradient overlay */}
          <div className="absolute inset-0 bg-gradient-to-br from-[--color-brand]/5 to-transparent" />

          {/* Icon */}
          <span className="text-4xl opacity-30">🎬</span>

          {/* Title initials */}
          <span className="text-2xl font-bold text-[--color-text-muted] px-4 text-center leading-tight">
            {movie.title
              .split(" ")
              .slice(0, 2)
              .map((word) => word[0])
              .join("")
              .toUpperCase()}
          </span>
        </div>

        {/* Content */}
        <div className="p-4">
          <h3 className="font-semibold text-[--color-text-primary] truncate text-sm leading-tight">
            {movie.title}
          </h3>

          <p className="text-xs text-[--color-text-secondary] mt-1">
            {movie.language}
          </p>

          <div className="flex items-center justify-between mt-3">
            <span className="text-xs text-[--color-text-muted]">
              {formatDuration(movie.duration_minutes)}
            </span>

            {/* Year badge */}
            <span className="text-xs bg-[--color-brand] text-slate-900 font-semibold px-2 py-0.5 rounded-full">
              {year}
            </span>
          </div>
        </div>
      </article>
    </Link>
  );
}

/* ---------------- Skeleton ---------------- */

export function MovieCardSkeleton() {
  return (
    <div className="card overflow-hidden animate-pulse">
      <div className="aspect-[2/3] bg-[--color-surface-elevated]" />

      <div className="p-4 space-y-2">
        <div className="h-4 bg-[--color-surface-elevated] rounded w-3/4" />
        <div className="h-3 bg-[--color-surface-elevated] rounded w-1/2" />

        <div className="flex justify-between mt-3">
          <div className="h-3 bg-[--color-surface-elevated] rounded w-10" />
          <div className="h-5 bg-[--color-surface-elevated] rounded-full w-10" />
        </div>
      </div>
    </div>
  );
}
