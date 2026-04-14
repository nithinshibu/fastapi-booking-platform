/* 
This code creates a custom hook called useMovie to fetch details of one specific movie.
It uses useQuery from TanStack React Query to handle fetching and caching.
The hook takes an id as input, which represents the movie you want.
queryKey: ["movies", id] uniquely identifies each movie in the cache.
This means each movie’s data is stored separately based on its ID.
queryFn: () => getMovie(id) is the function that actually fetches the movie data.
The arrow function ensures the correct id is used when fetching.
enabled: !!id && !isNaN(id) prevents the query from running if the ID is invalid.
So the API call only happens when a proper number ID is available.
When you use this hook, you get data, isLoading, and error for that specific movie.

*/

import { useQuery } from "@tanstack/react-query";
import { getMovie } from "../services/movieService";

export function useMovie(id: number) {
  return useQuery({
    queryKey: ["movies", id],
    queryFn: () => getMovie(id),
    enabled: !!id && !isNaN(id),
  });
}
