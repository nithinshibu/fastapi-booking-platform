/* 

Every API endpoint URL lives here - no URL strings anywhere else in the code base.

For static paths : ENDPOINTS.auth.login   --> "/auth/login"
For dynamic paths: ENDPOINTS.movies.detail(1)  --> "movies/1"

Using functions for dynamic URLs keep them type safe - Typescript
ensures we always pass the required parameters.

*/

export const ENDPOINTS = {
  auth: {
    register: "/auth/register",
    login: "/auth/login",
    refresh: "/auth/refresh",
    logout: "/auth/logout",
    me: "/users/me",
  },
  movies: {
    list: "/movies",
    detail: (id: number) => `/movies/${id}`,
    shows: (movieId: number) => `/movies/${movieId}/shows`,
  },
  shows: {
    create: "/shows",
  },
} as const;

/* 

React + TypeScript Endpoints (Simple Explanation)

Think of this file like a “menu” or “map” of all backend API URLs your
frontend can call.

Instead of writing URLs again and again everywhere, you store them in
one place.

------------------------------------------------------------------------

1.  export const ENDPOINTS

This creates a constant object that stores all your API routes.

“export” → allows other files to use it
“const” → cannot be changed later

------------------------------------------------------------------------

2.  auth section

auth: { register: “/auth/register”, login: “/auth/login”, me:
“/users/me”, }

These are API paths related to authentication:

-   register → used when creating a new account
-   login → used when logging in
-   me → used to get current logged-in user details

Example: frontend calls → POST /auth/login

------------------------------------------------------------------------

3.  movies section

movies: { list: “/movies”, detail: (id: number) => /movies/${id}, shows:
(movieId: number) => /movies/${movieId}/shows, }

-   list → get all movies
    → GET /movies

-   detail → get one movie using ID
    → example: /movies/5

-   shows → get shows for a movie
    → example: /movies/5/shows

Here, (id: number) means: “this function takes a number and builds a URL
dynamically”

------------------------------------------------------------------------

4.  shows section

shows: { create: “/shows”, }

Used to create a show: → POST /shows

------------------------------------------------------------------------

5.  What is as const?

This tells TypeScript:

“Do not change anything inside this object”

It also makes values more strict (readonly + exact values).

------------------------------------------------------------------------

6.  Why this pattern is useful?

Without this: You might write “/movies” everywhere → easy to make
mistakes

With this: You use: ENDPOINTS.movies.list

Benefits: - No typos - Easy to update - Clean code - Centralized API
management

------------------------------------------------------------------------

7.  How frontend uses it

Example:

fetch(ENDPOINTS.movies.detail(10))

This becomes: fetch(“/movies/10”)

------------------------------------------------------------------------

Final Idea:

This file is just a “central place to store all backend routes” so your
React app can talk to your FastAPI backend cleanly.



*/
