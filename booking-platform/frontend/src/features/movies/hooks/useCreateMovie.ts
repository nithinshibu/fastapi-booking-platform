/* 

This code creates a custom hook called useCreateMovie to add a new movie.
It uses useMutation from TanStack React Query, which is used for creating/updating/deleting data.
createMovie is the function that sends the new movie data to the backend.
useQueryClient() gives access to React Query’s cache system.
The mutationFn: createMovie tells it which function to run when creating a movie.
When you call this hook, it returns a function you can use to trigger the creation.
onSuccess runs only after the movie is successfully created.
Inside it, invalidateQueries({ queryKey: ["movies"] }) clears the old movie list cache.
This forces React Query to refetch the updated movie list automatically.
So overall, it creates a movie and ensures your UI shows the latest data without manual refresh.

*/

import { useMutation, useQueryClient } from "@tanstack/react-query";
import { createMovie } from "../services/movieService";

export function useCreateMovie() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: createMovie,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["movies"] });
    },
  });
}
