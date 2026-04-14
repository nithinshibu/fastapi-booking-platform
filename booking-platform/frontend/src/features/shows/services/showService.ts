/*
 * showService.ts — Shows API Layer
 */

import apiClient from "../../../services/apiClient";
import { ENDPOINTS } from "../../../services/endpoints";
import type { ShowResponse } from "../../movies/types";

// Type for creating a new show
export interface ShowCreate {
  movie_id: number;
  show_time: string; // ISO datetime: "2024-06-15T19:30:00"
  total_seats: number;
  hall_name: string;
}

// Get all shows for a movie
export async function getShowsForMovie(
  movieId: number,
): Promise<ShowResponse[]> {
  const response = await apiClient.get<ShowResponse[]>(
    ENDPOINTS.movies.shows(movieId),
  );
  return response.data;
}

// Create a new show
export async function createShow(data: ShowCreate): Promise<ShowResponse> {
  const response = await apiClient.post<ShowResponse>(
    ENDPOINTS.shows.create,
    data,
  );
  return response.data;
}
