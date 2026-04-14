/* 
This file creates a custom hook called useMovies to fetch movie data.
It uses useQuery from the TanStack React Query library.
useQuery helps you fetch, cache, and manage API data automatically.
The getMovies function is where the actual API call happens.
queryKey: ["movies"] is like a unique name to store and identify this data.
React Query uses this key to cache results and avoid repeated API calls.
queryFn: getMovies tells it which function to run to get the data.
When you call useMovies(), it triggers this whole process.
It returns useful values like data, isLoading, and error.
This makes your code simpler by removing manual fetching and state handling.

*/

import { useQuery } from "@tanstack/react-query";
import { getMovies } from "../services/movieService";

export function useMovies() {
  return useQuery({
    queryKey: ["movies"],
    queryFn: getMovies,
  });
}
