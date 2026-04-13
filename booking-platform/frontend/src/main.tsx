import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import App from "./app/App.tsx";
import { AppProviders } from "./app/providers.tsx";

/* 
AppProviders wraps App so every component in the tree has access to React Query's cache
and auth context.

Order matters - providers wrap outside in , so the outermost provider is available
to everything inside it.

*/

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AppProviders>
      <App />
    </AppProviders>
  </StrictMode>,
);
