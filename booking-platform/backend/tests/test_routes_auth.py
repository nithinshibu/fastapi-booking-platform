"""
test_routes_auth.py — Integration Tests for Auth Routes

WHAT IS AN INTEGRATION TEST?
Unlike unit tests (which test one function in isolation), integration tests
send a real HTTP request through the full stack:

Test → TestClient → FastAPI route → service → repository → test database

This catches problems that unit tests miss:
- Route doesn't wire the right dependency
- Service raises wrong exception type
- Pydantic schema rejects valid input
- SQL query has a mistake

.NET equivalent: WebApplicationFactory + HttpClient-based tests that
hit actual controller endpoints (not mocked units).

HOW TESTCLIENT WORKS:
client.post("/api/v1/auth/register", json={...}) is equivalent to sending
an HTTP POST request. The response object has .status_code and .json().
No server needs to be running — it's all in-process.

FIXTURE INJECTION:
The `client` parameter in each test function is NOT imported.
pytest sees it, looks for a fixture named `client` in conftest.py, calls it,
and injects the result. Same for any other fixture (db_session, etc.).
"""

# --- Helpers ------------------------------------------------------------------

def register_user(client, email="test@example.com", password="password123"):
    """Helper to register a user. Returns the response."""
    return client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": password},
    )


def login_user(client, email="test@example.com", password="password123"):
    """Helper to log in. Returns the response."""
    # Note: login uses form-encoded data (OAuth2PasswordRequestForm), not JSON.
    # That's why we use data= here instead of json=.
    return client.post(
        "/api/v1/auth/login",
        data={"username": email, "password": password},
    )


# --- Tests --------------------------------------------------------------------

class TestRegister:
    """Tests for POST /api/v1/auth/register"""

    def test_register_new_user_returns_201(self, client):
        """
        Happy path: registering with valid email + password creates a user.

        We check:
        - HTTP 201 Created (not 200 — creation returns 201)
        - Response contains the user's id and email
        - Password is NOT in the response (never expose it)
        """
        response = register_user(client)

        assert response.status_code == 201
        body = response.json()
        assert body["email"] == "test@example.com"
        assert "id" in body
        assert "password" not in body
        assert "hashed_password" not in body

    def test_register_duplicate_email_returns_400(self, client):
        """
        Registering the same email twice should fail with 400 Bad Request.
        This tests our AuthError → HTTP 400 mapping in the route.
        """
        register_user(client)  # first registration
        response = register_user(client)  # duplicate

        assert response.status_code == 400
        # FastAPI returns errors in {"detail": "..."} format
        assert "already registered" in response.json()["detail"].lower()

    def test_register_short_password_returns_422(self, client):
        """
        Pydantic validates the request body before it reaches the route.
        A password shorter than 8 characters should be rejected with 422
        Unprocessable Entity — FastAPI's standard validation error code.

        422 means: "I understood the request but the data is invalid."
        .NET equivalent: ModelState.IsValid returning false → 400 in MVC.
        """
        response = client.post(
            "/api/v1/auth/register",
            json={"email": "test@example.com", "password": "short"},
        )

        assert response.status_code == 422


class TestLogin:
    """Tests for POST /api/v1/auth/login"""

    def test_login_valid_credentials_returns_token(self, client):
        """
        Happy path: correct email + password returns a JWT access token.

        We verify the token structure (3 dot-separated parts) rather than
        decoding it — we're testing the HTTP layer, not the JWT library.
        """
        register_user(client)
        response = login_user(client)

        assert response.status_code == 200
        body = response.json()
        assert "access_token" in body
        assert body["token_type"] == "bearer"

        # A JWT always has exactly 3 parts: header.payload.signature
        assert len(body["access_token"].split(".")) == 3

    def test_login_wrong_password_returns_401(self, client):
        """
        Wrong credentials must return 401 Unauthorized.
        The error message should be generic — it must NOT say whether
        the email doesn't exist or whether the password is wrong.
        (Specific messages enable user enumeration attacks.)
        """
        register_user(client)
        response = login_user(client, password="wrongpassword")

        assert response.status_code == 401

    def test_login_nonexistent_email_returns_401(self, client):
        """
        Logging in with an email that was never registered also returns 401.
        Same status code as wrong password — no enumeration.
        """
        response = login_user(client, email="nobody@example.com")

        assert response.status_code == 401


class TestProtectedRoute:
    """Tests for GET /api/v1/users/me — requires a valid JWT"""

    def test_get_me_with_valid_token_returns_user(self, client):
        """
        Happy path: a valid Bearer token lets you access the protected route.
        This tests the full auth flow end-to-end:
        register → login → use token → get user profile
        """
        register_user(client)
        login_response = login_user(client)
        token = login_response.json()["access_token"]

        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": f"Bearer {token}"},
        )

        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"

    def test_get_me_without_token_returns_401(self, client):
        """
        Accessing a protected route with no Authorization header must return 401.
        This verifies our get_current_user dependency is actually protecting the route.
        """
        response = client.get("/api/v1/users/me")

        assert response.status_code == 401

    def test_get_me_with_invalid_token_returns_401(self, client):
        """
        A garbage token should be rejected — not crash the server.
        Tests that decode_access_token() handles bad input gracefully.
        """
        response = client.get(
            "/api/v1/users/me",
            headers={"Authorization": "Bearer this.is.garbage"},
        )

        assert response.status_code == 401