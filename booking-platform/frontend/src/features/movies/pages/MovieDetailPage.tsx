/*
 * MovieDetailPage.tsx — Single Movie Detail Page
 */

import { useParams, useNavigate } from "react-router-dom";
import { useMovie } from "../hooks/useMovie";
import { ShowsList } from "../components/ShowsList";
import { Spinner } from "../../../components/ui/Spinner";
import { Button } from "../../../components/ui/Button";
import { formatDuration, formatReleaseDate } from "../../../utils/formatters";

export function MovieDetailPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  // Convert string → number
  const movieId = parseInt(id ?? "0", 10);

  const { data: movie, isLoading, isError } = useMovie(movieId);

  // Loading state
  if (isLoading) {
    return (
      <div className="flex justify-center py-20">
        <Spinner size="lg" />
      </div>
    );
  }

  // Error / not found
  if (isError || !movie) {
    return (
      <div className="text-center py-20">
        <p className="text-4xl mb-4">🎬</p>
        <p className="text-[--color-text-secondary] mb-4">Movie not found</p>
        <Button variant="secondary" onClick={() => navigate("/movies")}>
          Back to movies
        </Button>
      </div>
    );
  }

  return (
    <div>
      {/* Back button */}
      <button
        onClick={() => navigate(-1)}
        className="flex items-center gap-2 text-sm text-[--color-text-muted] hover:text-[--color-brand] transition-colors mb-6 cursor-pointer"
      >
        ← Back
      </button>

      {/* Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Poster */}
        <aside className="lg:col-span-1">
          <div className="aspect-[2/3] rounded-xl bg-[--color-surface-elevated] flex items-center justify-center relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-[--color-brand]/10 to-transparent" />

            {/* Placeholder initials */}
            <span className="text-4xl font-bold text-[--color-text-muted]">
              {movie.title
                .split(" ")
                .slice(0, 2)
                .map((w) => w[0])
                .join("")
                .toUpperCase()}
            </span>
          </div>
        </aside>

        {/* Info */}
        <div className="lg:col-span-2 space-y-6">
          <h1 className="text-3xl font-bold text-[--color-text-primary]">
            {movie.title}
          </h1>

          {/* Metadata */}
          <div className="flex flex-wrap gap-2">
            <span className="badge">
              ⏱ {formatDuration(movie.duration_minutes)}
            </span>

            <span className="badge">🌐 {movie.language}</span>

            <span className="badge">
              📅 {formatReleaseDate(movie.release_date)}
            </span>

            {movie.is_active && (
              <span className="badge-brand">Now Showing</span>
            )}
          </div>

          {/* Description */}
          {movie.description && (
            <div>
              <h2 className="text-lg font-semibold text-[--color-text-primary] mb-2">
                About
              </h2>
              <p className="text-[--color-text-secondary] leading-relaxed">
                {movie.description}
              </p>
            </div>
          )}

          {/* Shows */}
          <div>
            <h2 className="text-lg font-semibold text-[--color-text-primary] mb-4">
              Book Tickets
            </h2>

            <ShowsList movieId={movie.id} />
          </div>
        </div>
      </div>
    </div>
  );
}
