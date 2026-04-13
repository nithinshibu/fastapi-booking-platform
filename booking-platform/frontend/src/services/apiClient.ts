import axios from "axios";
import { API_URL } from "../config/env";
import { TOKEN_KEY, USER_KEY } from "../constants";

// Create a single shared Axios instance for the entire app.

/* 

.NET equivalent : a named HttpClient registered in DI with a base address and a custom
DelegatingHandler that attaches the auth header.

Every single file (authService,movieService,etc) imports THIS client - 
never the raw 'axios' object. That way, all the HTTP calls automatically get:
1. The correct base URL
2. The JWT Token attached
3. Global 401 handling 
*/

const apiClient = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// ---------- Request Interceptor ----------

/* 

Runs before every outgoing request - reads the token from localStorage and attaches it to the Authorization header.

Why localStorage ?
It persists across browser refreshes, unlike in-memory state.
Trade-off : less secure than httpOnly cookies (vulnerable to XSS) , but simpler for a learning project.

*/

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// ---------- Response Interceptor ----------

/* 

Runs after EVERY response - the first function handles success, the second handles errors.

On 401 Unauthorized : the token has expired or is invalid.
We clear localStorage and force a redirect to /login.

.NET equivalent: middleware that checks the response status and redirects to the login page when the authentication fails.

Why window.location.href instead of React Router's navigate() ?

Interceptors live outside the React components , so hooks (including useNavigate) can't be used here.

window.location.href is a hard browser redirect - it also clears all React state, which is exactly what we want on logout.


*/

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status == 401) {
      localStorage.removeItem(TOKEN_KEY);
      localStorage.removeItem(USER_KEY);
      window.location.href = "/login";
    }
    return Promise.reject(error);
  },
);

export default apiClient;
