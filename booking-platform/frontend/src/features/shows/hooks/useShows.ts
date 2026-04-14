/*
 * useShows.ts — Shows List Hook
 */

import { useQuery } from "@tanstack/react-query";
import { getShowsForMovie } from "../services/showService";

export function useShows(movieId: number) {
  return useQuery({
    queryKey: ["shows", movieId],
    queryFn: () => getShowsForMovie(movieId),

    // Prevent invalid calls
    enabled: !!movieId && !isNaN(movieId),

    // Optional but recommended
    staleTime: 1000 * 60 * 5, // 5 minutes cache
  });
}
