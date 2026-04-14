/*
 * ShowsList.tsx — Shows List for a Movie
 */

import { useShows } from "../../shows/hooks/useShows";
import { Button } from "../../../components/ui/Button";
import { Spinner } from "../../../components/ui/Spinner";
import { formatShowTime } from "../../../utils/formatters";

interface ShowsListProps {
  movieId: number;
}

export function ShowsList({ movieId }: ShowsListProps) {
  const { data: shows, isLoading, isError } = useShows(movieId);

  // 🔄 Loading
  if (isLoading) {
    return (
      <div className="flex justify-center py-8">
        <Spinner size="md" />
      </div>
    );
  }

  // ❌ Error
  if (isError) {
    return (
      <p className="text-[--color-error] text-sm py-4">
        Could not load shows. Please try again.
      </p>
    );
  }

  // 📭 Empty state
  if (!shows || shows.length === 0) {
    return (
      <div className="rounded-lg bg-[--color-surface-elevated] p-6 text-center">
        <p className="text-[--color-text-muted]">No shows scheduled yet.</p>
      </div>
    );
  }

  // ✅ Data
  return (
    <div className="space-y-3">
      {shows.map((show) => {
        const isSoldOut = show.available_seats === 0;
        const isLowStock =
          show.available_seats > 0 && show.available_seats <= 5;

        return (
          <article
            key={show.id}
            className="flex items-center justify-between gap-4 rounded-lg bg-[--color-surface-elevated] p-4 border border-[--color-border]"
          >
            {/* 🎬 Show info */}
            <div className="min-w-0">
              <p className="font-medium text-[--color-text-primary] text-sm">
                {formatShowTime(show.show_time)}
              </p>
              <p className="text-xs text-[--color-text-secondary] mt-0.5">
                {show.hall_name}
              </p>
            </div>

            {/* 🎟️ Seats + CTA */}
            <div className="flex items-center gap-3 flex-shrink-0">
              {/* Seats indicator */}
              <div className="text-right">
                <p
                  className={`text-xs font-medium ${
                    isSoldOut
                      ? "text-[--color-error]"
                      : isLowStock
                        ? "text-[--color-warning]"
                        : "text-[--color-text-muted]"
                  }`}
                >
                  {isSoldOut
                    ? "Sold out"
                    : isLowStock
                      ? `Only ${show.available_seats} left!`
                      : `${show.available_seats} seats`}
                </p>
              </div>

              {/* CTA */}
              <Button
                variant="primary"
                size="sm"
                disabled={isSoldOut}
                title={isSoldOut ? "This show is sold out" : undefined}
              >
                {isSoldOut ? "Sold out" : "Book now"}
              </Button>
            </div>
          </article>
        );
      })}
    </div>
  );
}
