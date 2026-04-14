import axios from "axios";
import type { AxiosError } from "axios";
import { API_URL } from "../config/env";
import { TOKEN_KEY, REFRESH_TOKEN_KEY, USER_KEY } from "../constants";

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

WHAT CHANGED:
On a 401 , we now attempt a silent token refresh BEFORE giving up.

SILENT REFRESH FLOW:

        Request => 401 (access token expired)
        ↓
        Read refresh_token from localStorage
        ↓
        POST /auth/refresh {refresh_token}
        ↓
        Success => save new access token + refresh token => Retry original request
        Failure => clear storage => redirect to /login (session truly ended)

The user never sees a login prompt - from their perspective the API call 
just succeeded, slightly slower than usual.

is_Refreshing FLAG:
Prevents a "refresh storm". If 3 requests fire simulataneously and all get 401,
only the first one triggers a real  /auth/refresh  call.
The others wait for it.
Without this flag, we would see 3 refresh requests - wasteful and potentially 
causes race conditions where rotation revokes one before the others use it.
*/

let _isRefreshing = false;

// Queue of {resolve,reject} callbacks from requests waiting during a refresh.
// When the refresh completes, all waiting requests are retried.

let _waitingQueue: Array<{
  resolve: (token: string) => void;
  reject: (error: unknown) => void;
}> = [];

function processQueue(error: unknown, newToken: string | null) {
  _waitingQueue.forEach((item) => {
    if (error) {
      item.reject(error);
    } else {
      item.resolve(newToken!);
    }
  });
  _waitingQueue = [];
}

function clearAuthAndRedirect() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
  window.location.href = "/login";
}

apiClient.interceptors.response.use(
  //Success path - pass the response through unchanged
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as typeof error.config & {
      _retried?: boolean;
    };

    //Only handle 401 errors. Also check _retired to avoid infinite loops:
    // if the retried request ALSO gets a 401, we give up instead of looping.
    if (error.response?.status !== 401 || originalRequest._retried) {
      return Promise.reject(error);
    }

    const storedRefreshToken = localStorage.getItem(REFRESH_TOKEN_KEY);

    // No refresh toke in storage - can't refresh , must log in
    if (!storedRefreshToken) {
      clearAuthAndRedirect();
      return Promise.reject(error);
    }

    // If a refresh is already in flight , queue this request to wait for it
    if (_isRefreshing) {
      return new Promise((resolve, reject) => {
        _waitingQueue.push({
          resolve: (newToken: string) => {
            originalRequest!.headers!["Authorization"] = `Bearer ${newToken}`;
            resolve(apiClient(originalRequest));
          },
          reject,
        });
      });
    }

    // This is the FIRST 401 - start the refresh process
    originalRequest._retried = true
    _isRefreshing = true

    try {
      //Use raw axios (not apiClient) to avoid trigerring this interceptor again.
      const response = await axios.post<{
        access_token: string;
        refresh_token: string;
      }>(`${API_URL}/auth/refresh`, {
        refresh_token: storedRefreshToken,
      });

      const { access_token, refresh_token: newRefreshToken } = response.data

      // Save the new tokens
      localStorage.setItem(TOKEN_KEY, access_token)
      localStorage.setItem(REFRESH_TOKEN_KEY, newRefreshToken)

      // Update the default header so future requests use the new token
      apiClient.defaults.headers.common["Authorization"] = `Bearer ${access_token}`

      // Unblock all waiting requests with the new token
      processQueue(null, access_token)

      // Retry the original request that triggered the 401.
      originalRequest!.headers!["Authorization"] = `Bearer ${access_token}`
      return apiClient(originalRequest)

    } catch (refreshError) {
      // Refresh failed - the session is truly over
      processQueue(refreshError, null)
      clearAuthAndRedirect()
      return Promise.reject(refreshError)
    } finally {
      _isRefreshing = false
    }



  },
);

export default apiClient;
