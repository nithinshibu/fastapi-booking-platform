# Mental Model (.NET → FastAPI Mapping)

| .NET Concept             | FastAPI Equivalent                          |
| ------------------------ | ------------------------------------------- |
| Controllers              | app/api/v1/routes/ (FastAPI APIRouter)      |
| Service / IService       | app/services/ (plain Python classes)        |
| Repository / IRepository | app/repositories/ (plain Python classes)    |
| DbContext                | app/db/session.py (SQLAlchemy SessionLocal) |
| Entity / Model           | app/models/ (SQLAlchemy ORM classes)        |
| DTOs (Request/Response)  | app/schemas/ (Pydantic BaseModel)           |
| appsettings.json         | app/core/config.py + .env                   |
| Program.cs / Startup.cs  | main.py + app/core/                         |
| DI Container / AddScoped | FastAPI Depends() in route signatures       |
| [Authorize] attribute    | Depends(get_current_user) in route args     |
| EF Core Migrations       | Alembic (alembic/versions/)                 |
| IOptions                 | pydantic-settings BaseSettings              |
| NuGet / .csproj          | pyproject.toml + pip                        |

# 📁 Booking Platform - Project Structure (FastAPI + React)

## Backend

```
backend/
├── alembic/                      # DB migrations (EF Core equivalent)
│   └── versions/
│
├── app/
│   ├── api/v1/routes/            # HTTP endpoints – one file per resource
│   │   ├── auth.py
│   │   ├── movies.py
│   │   └── shows.py
│   │
│   ├── core/
│   │   ├── config.py             # pydantic-settings – reads .env
│   │   └── security.py           # JWT create/verify + password hashing
│   │
│   ├── db/
│   │   ├── base.py               # declarative_base() + imports all models
│   │   └── session.py            # engine + SessionLocal factory
│   │
│   ├── models/                   # SQLAlchemy ORM table definitions
│   │   ├── base.py               # shared columns: id, created_at, updated_at
│   │   ├── user.py
│   │   ├── movie.py
│   │   └── show.py
│   │
│   ├── schemas/                  # Pydantic DTOs (Request + Response)
│   │   ├── auth.py               # RegisterRequest, LoginRequest, TokenResponse
│   │   ├── movie.py              # MovieCreate, MovieUpdate, MovieResponse
│   │   └── show.py
│   │
│   ├── services/                 # Business logic layer
│   │   ├── auth_service.py
│   │   ├── movie_service.py
│   │   └── show_service.py
│   │
│   ├── repositories/             # DB query layer – only SQLAlchemy here
│   │   ├── user_repository.py
│   │   ├── movie_repository.py
│   │   └── show_repository.py
│   │
│   └── dependencies/             # FastAPI Depends() callables
│       ├── auth.py               # get_current_user()
│       └── db.py                 # get_db() – yields Session per request
│
├── tests/
│   ├── conftest.py               # shared pytest fixtures
│   ├── test_auth.py
│   └── test_movies.py
│
├── .env                          # NEVER commit
├── .env.example
├── alembic.ini
├── main.py                       # FastAPI app factory + router registration
└── pyproject.toml                # dependency manifest
```

---

## Frontend (booking-platform/frontend/)

```
frontend/
├── src/
│   ├── assets/
│   │
│   ├── components/
│   │   ├── common/               # Button, Input, LoadingSpinner, ErrorMessage
│   │   ├── layout/               # Navbar, PageLayout
│   │   └── movies/               # MovieCard, MovieList
│   │
│   ├── pages/                   # One file per route
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   ├── MoviesPage.jsx
│   │   └── MovieDetailPage.jsx
│   │
│   ├── hooks/                   # Custom hooks (React Query wrappers)
│   │   ├── useMovies.js
│   │   ├── useMovie.js
│   │   └── useAuth.js
│   │
│   ├── services/                # Axios API call functions
│   │   ├── api.js               # Axios instance + auth interceptor
│   │   ├── authService.js
│   │   └── movieService.js
│   │
│   ├── context/
│   │   └── AuthContext.jsx      # Global auth state (user, token, login/logout)
│   │
│   ├── utils/
│   │   └── formatters.js
│   │
│   ├── App.jsx                  # React Router route definitions
│   └── main.jsx                 # Vite entry point
│
├── .env
├── .env.example
├── index.html
├── package.json
└── vite.config.js

# VITE_API_URL=http://localhost:8000
```
