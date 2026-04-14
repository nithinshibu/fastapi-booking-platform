/* App.tsx is the root component - top of the react component tree . Everything renders inside here. */

import { RouterProvider } from "react-router-dom";
import { router } from "./router";

function App() {
  return <RouterProvider router={router} />;
}

export default App;
