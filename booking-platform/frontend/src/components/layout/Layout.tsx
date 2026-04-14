/* 

Layout.tsx - Page Shell / Application Layout

Wraps all authenticated Pages with the Navbar at the top and a content area below it.
The <Outlet /> renders the current page's content.

What is <Outlet /> ?

In React Router v6 , when we nest routes , the parent route renders its
component and the child route's component is placed where <Outlet /> appears.

The Navbar and footer stay consistent; only the <Outlet /> content changes.


*/

import { Outlet } from "react-router-dom";
import { Navbar } from "./Navbar";

export function Layout() {
  return (
    <div className="min-h-screen flex flex-col bg-[--color-bg]">
      <Navbar />
      {/* Main content area - flex-1 makes it grow to fill remaining height */}
      <main className="flex-1 container-page py-8">
        <Outlet />
      </main>
      {/* Footer */}
      <footer className="border-t border-[--color-border] py-6 text-center text-sm text-[--color-text-muted]">
        <p>
          CineBook &copy; {new Date().getFullYear()} - Built with FastAPI &amp;
          React
        </p>
      </footer>
    </div>
  );
}
