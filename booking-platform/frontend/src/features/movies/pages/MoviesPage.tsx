/*
 * MoviesPage.tsx — Movies List Page
 *
 * Smart component — handles data fetching, state, filtering.
 */

import { useState } from "react";
import { useMovies } from "../hooks/useMovies";
import { MovieCard, MovieCardSkeleton } from "../components/MovieCard";

export function MoviesPage() {
  const { data: movies, isLoading, isError, refetch } = useMovies();
  const [search, setSearch] = useState("");

  // Client-side filter
  const filteredMovies = movies?.filter((movie) =>
    movie.title.toLowerCase().includes(search.toLowerCase()),
  );

  return (
    <div>
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-8">
        <div>
          <h1 className="text-2xl font-bold text-[--color-text-primary]">
            Now Showing
          </h1>

          <p className="text-sm text-[--color-text-secondary] mt-1">
            {isLoading
              ? "Loading movies..."
              : `${filteredMovies?.length ?? 0} movie${
                  (filteredMovies?.length ?? 0) === 1 ? "" : "s"
                }`}
          </p>
        </div>

        {/* Search */}
        {!isLoading && !isError && (
          <div className="relative">
            <span className="absolute left-3 top-1/2 -translate-y-1/2 text-[--color-text-muted] text-sm">
              🔍
            </span>
            <input
              type="search"
              placeholder="Search movies..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="input-base pl-9 w-full sm:w-64"
            />
          </div>
        )}
      </div>

      {/* Error */}
      {isError && (
        <div className="text-center py-16">
          <p className="text-[--color-error] text-lg mb-4">
            Failed to load movies
          </p>
          <button
            onClick={() => refetch()}
            className="text-[--color-brand] hover:underline text-sm cursor-pointer"
          >
            Try again
          </button>
        </div>
      )}

      {/* Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-4 sm:gap-6">
        {/* Loading */}
        {isLoading &&
          Array.from({ length: 10 }).map((_, i) => (
            <MovieCardSkeleton key={i} />
          ))}

        {/* Loaded */}
        {filteredMovies?.map((movie) => (
          <MovieCard key={movie.id} movie={movie} />
        ))}
      </div>

      {/* Empty state */}
      {!isLoading && !isError && filteredMovies?.length === 0 && (
        <div className="text-center py-16">
          <p className="text-4xl mb-4">🎬</p>

          <p className="text-[--color-text-secondary]">
            {search
              ? `No movies found for "${search}"`
              : "No movies available yet"}
          </p>

          {search && (
            <button
              onClick={() => setSearch("")}
              className="mt-3 text-[--color-brand] hover:underline text-sm cursor-pointer"
            >
              Clear search
            </button>
          )}
        </div>
      )}
    </div>
  );
}
