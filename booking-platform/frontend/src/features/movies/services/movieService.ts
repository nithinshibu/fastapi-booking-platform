import apiClient from "../../../services/apiClient";
import { ENDPOINTS } from "../../../services/endpoints";

import type { MovieResponse, MovieCreate, MovieUpdate } from "../types";

/* ---------------- Get all movies ---------------- */

export async function getMovies(): Promise<MovieResponse[]> {
  const response = await apiClient.get<MovieResponse[]>(ENDPOINTS.movies.list);
  return response.data;
}

/* ---------------- Get single movie ---------------- */

export async function getMovie(id: number): Promise<MovieResponse> {
  const response = await apiClient.get<MovieResponse>(
    ENDPOINTS.movies.detail(id),
  );
  return response.data;
}

/* ---------------- Create movie ---------------- */

export async function createMovie(data: MovieCreate): Promise<MovieResponse> {
  const response = await apiClient.post<MovieResponse>(
    ENDPOINTS.movies.list,
    data,
  );
  return response.data;
}

/* ---------------- Update movie ---------------- */

export async function updateMovie(
  id: number,
  data: MovieUpdate,
): Promise<MovieResponse> {
  const response = await apiClient.put<MovieResponse>(
    ENDPOINTS.movies.detail(id),
    data,
  );
  return response.data;
}

/* ---------------- Delete movie ---------------- */
// DELETE returns 204 No Content → no response body

export async function deleteMovie(id: number): Promise<void> {
  await apiClient.delete(ENDPOINTS.movies.detail(id));
}
