import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import type { ReactNode } from "react";

/* 

@tanstack/react-query (commonly called React Query) is a library that helps your React app fetch, store,
and manage data from your backend API easily.
Instead of manually using fetch or axios and handling loading, errors, and caching yourself,
React Query does all of that for you.
It automatically caches data, so if you request the same data again, it doesn’t hit the server every time.
This makes your app faster, cleaner, and much easier to maintain.

QueryClient holds the cache for all server data fetched by React Query.

QueryClient is the main manager (brain) of React Query that stores and controls all your fetched data.
It keeps a cache of API responses, so your app can reuse data without refetching unnecessarily.
It also handles things like refetching, updating, and invalidating data when something changes.
You usually create one QueryClient and provide it to your whole app using QueryClientProvider.

Think of it as an in-memory store that keeps API responses so our components don't have to re-fetch data they already have.

defaultOptions config:
    retry:1     -> if a request fails , try once more before showing an error 
    staleTime   -> how long cached data is considered "fresh" before the React Query
                   refetches it in the background (5 minutes here)

/NET equivalent : configuring HttpClient caching policies or a memory cache.          

*/

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      staleTime: 1000 * 60 * 5, // 5 minutes
    },
  },
});

/* 

📦 AppProvidersProps

This defines the type (shape) of props that your AppProviders component will receive.
It says that this component expects a prop called children, and its type is ReactNode.
ReactNode means anything React can render (like JSX, components, text, etc.).
This helps TypeScript catch mistakes and ensures you pass valid content inside AppProviders.

*/

interface AppProvidersProps {
  children: ReactNode;
}

/* 
AppProviders wraps the entire app so every component has access to React Query's cache
via hooks (useQuery, useMutation, etc..)

We will add AuthProvider here later once the auth context is built.

*/

export function AppProviders({ children }: AppProvidersProps) {
  return (
    <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>
  );
}

/* 

🧩 QueryClientProvider

QueryClientProvider is like a wrapper that gives React Query access to your whole app.
It makes sure every component inside it can use React Query features like useQuery and useMutation.
Without this, your components won’t know where the data/cache is stored.
Think of it like Wi-Fi — without connecting to it, nothing works.

🧠 queryClient

queryClient is the actual storage + manager of your API data (cache).
It keeps track of all fetched data, errors, and loading states.
It also decides when to refetch or reuse existing data.
You create it once and give it to QueryClientProvider.

👶 children

children means all the components inside AppProviders.
Whatever you wrap inside <AppProviders>...</AppProviders> becomes children.
These components will automatically get access to React Query.
So basically, children = your entire app UI.

*/
