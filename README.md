# 🎬 Cinema & Show Booking Platform

A production-grade, full-stack Cinema & Event Booking Platform built with **FastAPI (Python)** on the backend and **React 19 (TypeScript + Vite)** on the frontend. 

Both applications are engineered strictly according to **Clean Architecture** and **Domain-Driven Modular** principles, ensuring high maintainability, strict separation of concerns, comprehensive testability, and seamless scalability.

---

## 📑 Table of Contents

1. [Application Overview](#-application-overview)
2. [Tech Stack](#-tech-stack)
3. [Architecture Philosophy (Clean Architecture)](#-architecture-philosophy-clean-architecture)
   - [The Dependency Rule](#the-dependency-rule)
   - [Backend Mental Model (.NET / Spring Boot → FastAPI)](#backend-mental-model-net--spring-boot--fastapi)
   - [Frontend Mental Model (Feature-Sliced Architecture)](#frontend-mental-model-feature-sliced-architecture)
4. [Backend Deep Dive (FastAPI)](#-backend-deep-dive-fastapi)
   - [Directory Structure](#backend-directory-structure)
   - [Folder-by-Folder Guide & Responsibilities](#backend-folder-by-folder-guide)
   - [Data Flow Architecture](#backend-data-flow-architecture)
5. [Frontend Deep Dive (React + TypeScript)](#-frontend-deep-dive-react--typescript)
   - [Directory Structure](#frontend-directory-structure)
   - [Folder-by-Folder Guide & Responsibilities](#frontend-folder-by-folder-guide)
   - [Design Token Palette (Cinema Dark Theme)](#design-token-palette-cinema-dark-theme)
6. [Authentication & Security Deep Dive](#-authentication--security-deep-dive)
   - [Dual-Token Architecture (Access Token + Refresh Token)](#dual-token-architecture)
   - [Why Opaque Cryptographic Strings for Refresh Tokens?](#why-opaque-cryptographic-strings-for-refresh-tokens)
   - [Why SHA-256 Hash Refresh Tokens in the Database?](#why-sha-256-hash-refresh-tokens-in-the-database)
   - [Token Rotation & Reuse Detection](#token-rotation--reuse-detection)
   - [Silent Refresh & Preventing "Refresh Storms" in React](#silent-refresh--preventing-refresh-storms-in-react)
   - [Complete Authentication Lifecycle Diagram](#complete-authentication-lifecycle-diagram)
7. [Database Schema & Data Models](#-database-schema--data-models)
   - [Entity-Relationship Diagram](#entity-relationship-diagram)
   - [Table Definitions & Relationships](#table-definitions--relationships)
8. [Complete API Reference](#-complete-api-reference)
   - [Health Check](#health-check)
   - [Authentication Endpoints](#authentication-endpoints)
   - [User Endpoints](#user-endpoints)
   - [Movie Endpoints](#movie-endpoints)
   - [Show Endpoints](#show-endpoints)
9. [Step-by-Step Installation & Setup Guide](#-step-by-step-installation--setup-guide)
   - [Prerequisites](#prerequisites)
   - [Database Setup (PostgreSQL)](#1-database-setup-postgresql)
   - [Backend Setup & Migrations](#2-backend-setup--migrations)
   - [Frontend Setup & Environment](#3-frontend-setup--environment)
   - [Running the Complete Application](#4-running-the-complete-application)
   - [Running Automated Tests](#5-running-automated-tests)
   - [Troubleshooting & Common Pitfalls](#6-troubleshooting--common-pitfalls)
10. [Development Guidelines & Architectural Invariants](#-development-guidelines--architectural-invariants)

---

## 🌟 Application Overview

The **Booking Platform** is an end-to-end entertainment ticketing solution designed for cinemas and live event venues. 

### Core Capabilities
* **User Authentication & Session Management**: Secure user onboarding, login, session persistence, automatic silent token refresh, and server-side token revocation on logout.
* **Movie Catalog Management**: Browsing active and upcoming movie listings with rich metadata (duration, release date, language, synopsis), plus administrative capabilities to create, edit, and soft-delete/deactivate titles.
* **Show & Screening Scheduling**: Multi-hall screening management tied to movies, tracking showtime datetime, total venue capacity, and real-time remaining seat inventory.
* **Dynamic Client-Side Experience**: Instant client-side search and filtering, lazy-loaded route views, responsive cinema-inspired dark UI, and optimistic caching via TanStack Query.

---

## 🛠 Tech Stack

### Backend
| Technology | Version / Purpose |
| :--- | :--- |
| **FastAPI** | High-performance modern ASGI web framework with automated OpenAPI (Swagger) documentation |
| **Python** | 3.10+ (compatible with Python 3.14 with specific bcrypt/passlib pinning) |
| **SQLAlchemy** | 2.0+ Declarative ORM mapping and expressive database queries |
| **Alembic** | Lightweight database migration tool for schema evolution |
| **PostgreSQL** | Relational primary data store for production and testing |
| **Pydantic v2 & Pydantic-Settings** | Type validation, DTO transformation, and typed environment configuration |
| **python-jose** | Cryptographic JSON Web Signature (JWS / JWT) signing and verification |
| **Passlib & BCrypt** | Salted password hashing with constant-time verification |
| **Pytest & HTTPX** | In-memory integration testing suite with transactional test DB isolation |

### Frontend
| Technology | Version / Purpose |
| :--- | :--- |
| **React** | 19+ Modern Component UI library |
| **TypeScript** | Strict static type verification |
| **Vite** | Blazing-fast frontend build tooling and development server |
| **Tailwind CSS & PostCSS** | Utility-first styling configured with custom design tokens |
| **TanStack React Query** | Asynchronous server-state management, automated query caching, and invalidation |
| **React Router** | v7 Config-based declarative client-side routing with code splitting |
| **React Hook Form & Zod** | Form state management paired with runtime schema validation |
| **Axios** | HTTP client augmented with request and response interceptors |

---

## 🏛 Architecture Philosophy (Clean Architecture)

Both the backend and frontend are intentionally structured around **Clean Architecture** (also known as Hexagonal or Onion Architecture). 

### The Dependency Rule
> **Source code dependencies must only point inwards, toward higher-level policies.**

```
       [ HTTP / Presentation Layer ]
                    ↓
        [ Business / Service Layer ]
                    ↓
      [ Data Access / Repository Layer ]
                    ↓
         [ Database / Infrastructure ]
```

* **The Database does not know about the API.**
* **The Business Logic (Services) does not know about HTTP requests, cookies, or status codes.**
* **The HTTP Controllers (Routes) do not write SQL or talk directly to the database.**
* **The Domain Entities (SQLAlchemy Models) never leak unvalidated data to the client.**

---

### Backend Mental Model (.NET / Spring Boot → FastAPI)

If you come from an enterprise .NET (C#) or Spring Boot (Java) background, FastAPI maps cleanly to the same enterprise design patterns:

| Enterprise .NET / Spring Pattern | FastAPI Equivalent in this Project | Project Path |
| :--- | :--- | :--- |
| **Controller** (`[ApiController]`) | `APIRouter` route definitions | `app/api/v1/routes/` |
| **Service Layer** (`IUserService`) | Plain Python classes / business modules | `app/services/` |
| **Repository Layer** (`IUserRepository`) | Pure SQLAlchemy data access functions | `app/repositories/` |
| **DbContext / EntityManager** | `SessionLocal` from SQLAlchemy | `app/db/session.py` |
| **Entity / DB Model** | SQLAlchemy Declarative Base ORM classes | `app/models/` |
| **DTOs (Request / Response ViewModels)** | Pydantic `BaseModel` classes | `app/schemas/` |
| **Dependency Injection Container** (`AddScoped`) | FastAPI `Depends(get_db)` parameter injection | `app/dependencies/db.py` |
| **`[Authorize]` Filter Attribute** | FastAPI `Depends(get_current_user)` | `app/dependencies/auth.py` |
| **`appsettings.json` / `IOptions<T>`** | `pydantic-settings` `BaseSettings` reading `.env` | `app/core/config.py` |
| **`Program.cs` / `Startup.cs`** | `FastAPI()` app initialization + CORS + router mounting | `main.py` |
| **EF Core Migrations** | Alembic migration scripts | `alembic/versions/` |
| **`packages.config` / `.csproj`** | `pyproject.toml` | `pyproject.toml` |

---

### Frontend Mental Model (Feature-Sliced Architecture)

In the frontend, rather than grouping files by technical type (all components in one folder, all hooks in another), code is structured **by business domain (features)**:

```
Components (UI only) ──► Custom Hooks (React Query) ──► Services (API Calls) ──► apiClient (Axios) ──► Backend
```

1. **Pages** render the route layout and orchestrate feature components.
2. **Components** only receive props and fire events; they do not perform raw `fetch` calls.
3. **Hooks** encapsulate caching, loading, error states, and mutations via React Query.
4. **Services** are pure async functions that return typed data; they contain zero React code.
5. **apiClient** is the centralized HTTP engine that injects tokens and orchestrates silent refresh.

---

## 🐍 Backend Deep Dive (FastAPI)

### Backend Directory Structure

```
backend/
├── alembic/                          # Alembic database migration environment
│   ├── versions/                     # Auto-generated and manual migration scripts
│   │   ├── 6fed83e5f8c8_create_users_table.py
│   │   ├── b912e66371ed_create_movies_table.py
│   │   ├── ffc73bb596a4_create_shows_table.py
│   │   └── fdb1fa44b2d3_add_refresh_tokens_table.py
│   ├── env.py                        # Alembic runner configuration (imports all models)
│   ├── README
│   └── script.py.mako                # Template for generating migration revisions
├── app/
│   ├── api/                          # HTTP Presentation Layer
│   │   └── v1/
│   │       └── routes/               # API endpoint routers grouped by domain
│   │           ├── auth.py           # /api/v1/auth (register, login, refresh, logout)
│   │           ├── users.py          # /api/v1/users (current user profile /me)
│   │           ├── movies.py         # /api/v1/movies (CRUD for movies)
│   │           └── shows.py          # /api/v1/shows & /api/v1/movies/{id}/shows
│   ├── core/                         # Core infrastructure & configuration
│   │   ├── config.py                 # Pydantic Settings (reads .env variables)
│   │   └── security.py               # Password hashing (bcrypt) & JWT / token crypto
│   ├── db/                           # Database engine & session setup
│   │   ├── base.py                   # DeclarativeBase setup
│   │   └── session.py                # SQLAlchemy engine & SessionLocal sessionmaker
│   ├── dependencies/                 # FastAPI dependency injection callables
│   │   ├── auth.py                   # get_current_user (Bearer JWT extraction & validation)
│   │   └── db.py                     # get_db (Scoped session generator with auto-close)
│   ├── models/                       # SQLAlchemy ORM database entities
│   │   ├── base.py                   # Abstract BaseModel (id, created_at, updated_at)
│   │   ├── user.py                   # User entity
│   │   ├── movie.py                  # Movie entity
│   │   ├── show.py                   # Show entity (linked to Movie via FK)
│   │   └── refresh_token.py          # RefreshToken entity (hashed token session store)
│   ├── repositories/                 # Data Access Layer (DAL) - pure SQLAlchemy queries
│   │   ├── user_repository.py        # User queries (get_by_email, create)
│   │   ├── movie_repository.py       # Movie queries (get_all, get_by_id, create, update, delete)
│   │   ├── show_repository.py        # Show queries (get_by_movie, create)
│   │   └── refresh_token_repository.py # Refresh token queries (create, get_by_hash, revoke)
│   ├── schemas/                      # Pydantic DTOs (Request / Response validation)
│   │   ├── auth.py                   # RegisterRequest, LoginRequest, TokenResponse, etc.
│   │   ├── movie.py                  # MovieCreate, MovieUpdate, MovieResponse
│   │   └── show.py                   # ShowCreate, ShowResponse
│   └── services/                     # Business Logic Layer - application rules
│       ├── auth_service.py           # User registration, credential checks, token rotation
│       ├── movie_service.py          # Movie domain validation, partial updates
│       └── show_service.py           # Show scheduling, available seat derivation
├── tests/                            # Automated test suite
│   ├── conftest.py                   # Pytest fixtures, test DB creation, dependency overrides
│   ├── test_auth.py                  # Unit tests for password hashing & JWT generation
│   └── test_routes_auth.py           # Integration tests for auth API routes
├── .env                              # Environment secret configuration (gitignored)
├── .env.example                      # Template for environment variables
├── alembic.ini                       # Alembic CLI configuration file
├── main.py                           # Application factory, middleware & router registration
└── pyproject.toml                    # Package dependencies and project metadata
```

---

### Backend Folder-by-Folder Guide

#### 1. `app/api/v1/routes/` (Controllers)
* **What belongs here:** FastAPI route decorators (`@router.get`, `@router.post`), extracting request bodies, path parameters, query parameters, injecting dependencies via `Depends()`, and translating service exceptions into HTTP exceptions (`HTTPException(400)`, `HTTPException(404)`).
* **What DOES NOT belong here:** Direct SQL statements, password hashing logic, or direct database mutations. Routes delegate immediately to the service layer.

#### 2. `app/services/` (Business Logic Layer)
* **What belongs here:** Pure business logic and domain rules:
  - Validating that an email is not duplicate before registering.
  - Ensuring password plaintext is hashed before persisting.
  - Initializing `available_seats = total_seats` when scheduling a show.
  - Revoking old tokens and generating new token pairs on refresh.
  - Raising domain exceptions (`AuthError`, `MovieNotFoundError`).
* **What DOES NOT belong here:** HTTP concepts. Services never import `Request`, `Response`, `HTTPException`, or status codes. This keeps business logic completely testable without mocking web servers.

#### 3. `app/repositories/` (Data Access Layer)
* **What belongs here:** Direct SQLAlchemy queries using modern 2.0 `select(...)` syntax, adding models to sessions, committing, refreshing, and deleting rows.
* **Stateless Design:** Every function in this layer takes `db: Session` as its first parameter. Repositories do not maintain state or manage their own connections.

#### 4. `app/models/` (Database Entities)
* **What belongs here:** SQLAlchemy declarative ORM models mapping directly to PostgreSQL tables.
* **`BaseModel`:** An abstract model (`__abstract__ = True`) defining standard audit columns (`id`, `created_at`, `updated_at`) inherited by all tables.
* **Relationships:** Configures foreign key constraints (`ForeignKey("movies.id", ondelete="CASCADE")`) and bi-directional ORM navigation (`relationship("Show", back_populates="movie")`).

#### 5. `app/schemas/` (Data Transfer Objects - DTOs)
* **What belongs here:** Pydantic models that strictly validate data coming into the API (request payloads) and format data exiting the API (response payloads).
* **Security Whitelist:** Response schemas ensure internal or sensitive fields (such as `hashed_password` or internal database hashes) are **never** serialized into JSON.
* **`from_attributes = True`:** Enables Pydantic schemas to read attributes directly from SQLAlchemy ORM entity objects.

#### 6. `app/dependencies/` (Dependency Injection)
* **`db.py` (`get_db`)**: Creates a scoped SQLAlchemy session per HTTP request and guarantees that `db.close()` runs in a `finally` block when the request finishes.
* **`auth.py` (`get_current_user`)**: Plugs into FastAPI's `OAuth2PasswordBearer`, inspects the `Authorization: Bearer <token>` header, validates the JWT signature and expiration, retrieves the user from the database, and injects the authenticated `User` object into protected route parameters.

#### 7. `app/core/` (Core Configuration & Security)
* **`config.py`**: Typed configuration powered by `pydantic-settings`. Fails immediately on application startup if required environment variables (like `DATABASE_URL` or `SECRET_KEY`) are missing.
* **`security.py`**: Low-level cryptographic utilities: passlib bcrypt password hashing, JWT encoding/decoding via `python-jose`, opaque cryptographic refresh token generation using `secrets.token_urlsafe(64)`, and SHA-256 token hashing.

---

### Backend Data Flow Architecture

```
HTTP Request (e.g. POST /api/v1/auth/login)
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 1. main.py (CORSMiddleware checks origins)          │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 2. routes/auth.py (Parses OAuth2PasswordRequestForm)│
│    Injects: db Session via Depends(get_db)          │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 3. services/auth_service.py (login_user)            │
│    - Calls user_repository.get_by_email(db, email)  │
│    - Calls security.verify_password(pass, hash)     │
│    - Generates Access Token (JWT, 30m)              │
│    - Generates Opaque Refresh Token (64 bytes)      │
│    - Hashes Refresh Token with SHA-256              │
│    - Calls refresh_token_repository.create(...)     │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 4. repositories/ (Executes SQL against PostgreSQL)  │
└──────────────────┬──────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────┐
│ 5. schemas/auth.py (TokenResponse)                  │
│    Serializes JSON: access_token, refresh_token     │
└─────────────────────────────────────────────────────┘
```

---

## ⚛ Frontend Deep Dive (React + TypeScript)

### Frontend Directory Structure

```
frontend/
├── public/                           # Static public assets (favicons, SVG sprite icons)
│   ├── favicon.svg
│   └── icons.svg
├── src/
│   ├── app/                          # Top-level application setup & wrappers
│   │   ├── App.tsx                   # Root component rendering RouterProvider
│   │   ├── providers.tsx             # Global providers (QueryClientProvider, AuthProvider)
│   │   └── router.tsx                # React Router v7 routes with code-splitting (lazy)
│   ├── assets/                       # Bundled static assets & imagery
│   │   └── hero.png
│   ├── components/                   # Shared UI component library
│   │   ├── layout/                   # Structural layout components
│   │   │   ├── Layout.tsx            # Main layout wrapper (Navbar + main outlet)
│   │   │   ├── Navbar.tsx            # Navigation header with user profile & logout
│   │   │   └── ProtectedRoute.tsx    # Auth guard protecting authenticated routes
│   │   └── ui/                       # Design system atoms
│   │       ├── Button.tsx            # Variant-styled button (primary, secondary, danger)
│   │       ├── Input.tsx             # Accessible labeled input with validation error states
│   │       ├── Modal.tsx             # Accessible dialog overlay
│   │       └── Spinner.tsx           # Configurable loading spinner
│   ├── config/                       # Application runtime configuration
│   │   └── env.ts                    # Exports typed API_URL from import.meta.env
│   ├── constants/                    # Constant definitions
│   │   └── index.ts                  # LocalStorage keys (TOKEN_KEY, REFRESH_TOKEN_KEY, USER_KEY)
│   ├── context/                      # React Context providers
│   │   └── AuthContext.tsx           # Global auth state, session restore, login & logout
│   ├── features/                     # Domain modules (Feature-Sliced structure)
│   │   ├── auth/                     # Authentication feature
│   │   │   ├── components/           # Feature UI (LoginForm.tsx, RegisterForm.tsx)
│   │   │   ├── hooks/                # useAuth hook wrapper
│   │   │   ├── pages/                # Route pages (LoginPage.tsx, RegisterPage.tsx)
│   │   │   ├── schemas/              # Zod validation schemas (loginSchema, registerSchema)
│   │   │   ├── services/             # authService.ts (API calls for login, register, me, logout)
│   │   │   └── types.ts              # TypeScript interfaces for authentication
│   │   ├── movies/                   # Movie browsing & catalog feature
│   │   │   ├── components/           # MovieCard.tsx, MovieCardSkeleton, ShowsList.tsx
│   │   │   ├── hooks/                # useMovies, useMovie, useCreateMovie (React Query)
│   │   │   ├── pages/                # MoviesPage.tsx, MovieDetailPage.tsx
│   │   │   ├── services/             # movieService.ts (CRUD API calls)
│   │   │   └── types.ts              # Movie and show domain models
│   │   └── shows/                    # Screening & scheduling feature
│   │       ├── hooks/                # useShows custom hook
│   │       └── services/             # showService.ts (getShowsForMovie, createShow)
│   ├── services/                     # Core HTTP client infrastructure
│   │   ├── apiClient.ts              # Axios singleton with auth & silent refresh interceptors
│   │   └── endpoints.ts              # Centralized type-safe API route dictionary
│   ├── utils/                        # Formatting and utility functions
│   │   └── formatters.ts             # Time duration & release date formatters
│   ├── index.css                     # Tailwind CSS imports & theme CSS variables
│   └── main.tsx                      # Vite React entry point (DOM mount)
├── index.html                        # Single Page Application HTML entry point
├── package.json                      # NPM package manifest & scripts
├── postcss.config.cjs                # PostCSS configuration for Tailwind
└── vite.config.ts                    # Vite build tool configuration
```

---

### Frontend Folder-by-Folder Guide

#### 1. `src/features/` (Domain-Driven Modules)
Each business feature encapsulates its own user interface, state hooks, validation rules, and network calls:
* **`components/`**: UI components specific to that feature (e.g., `MovieCard.tsx`, `LoginForm.tsx`).
* **`hooks/`**: React Query wrappers (e.g., `useMovies.ts`). These handle background caching, automatic refetching, and provide simple `{ data, isLoading, isError }` bindings to components.
* **`services/`**: Pure functions executing network calls via `apiClient`. Never call React hooks or modify state here.
* **`schemas/`**: Runtime validation schemas powered by Zod, enforcing valid input format before requests leave the browser.
* **`pages/`**: Route components wired into `router.tsx`.

#### 2. `src/services/` (HTTP Client & Endpoints)
* **`endpoints.ts`**: A centralized, strictly-typed dictionary defining all backend paths (`as const`). Dynamic endpoints are typed helper functions (e.g., `ENDPOINTS.movies.detail(id)`). This eliminates raw URL strings and typos across the app.
* **`apiClient.ts`**: The application's custom Axios instance. Configures the base URL, sets `Content-Type: application/json`, attaches the JWT Bearer token on every outgoing request via a **Request Interceptor**, and performs automatic silent token renewal via a **Response Interceptor**.

#### 3. `src/context/` (Global State)
* **`AuthContext.tsx`**: Provides application-wide authentication state. On mount, it restores existing sessions by checking `localStorage` and calling `/users/me`. It exposes `login()`, `logout()`, `user`, `token`, and `isLoading`.

#### 4. `src/components/layout/` (Application Shell)
* **`Layout.tsx`**: Common shell featuring the persistent header/navigation bar and an `<Outlet />` for child page rendering.
* **`ProtectedRoute.tsx`**: An authorization barrier. If `isLoading` is true, it displays a loading spinner; if the user is unauthenticated, it redirects to `/login` with the attempted route preserved.

---

### Design Token Palette (Cinema Dark Theme)

The UI is styled with a sleek, cinematic dark aesthetic using custom CSS properties integrated with Tailwind CSS:

| Token Name | Hex Code | Purpose |
| :--- | :--- | :--- |
| **Brand Primary** | `#F59E0B` | Amber / Gold accent (CTA buttons, active highlights) |
| **Brand Dark** | `#D97706` | Hover state for brand actions |
| **Background** | `#0F172A` | Deep slate canvas background |
| **Surface** | `#1E293B` | Movie cards, navigation headers, containers |
| **Surface Elevated**| `#334155` | Modal overlays, text inputs, hoverable cards |
| **Border** | `#475569` | Card borders, input outlines, dividers |
| **Text Primary** | `#F8FAFC` | Main headings, prominent titles |
| **Text Secondary** | `#94A3B8` | Subtext, metadata badges, synopsis text |
| **Success** | `#10B981` | Positive feedback, confirmation badges |
| **Error** | `#EF4444` | Validation error alerts, destructive buttons |

---

## 🔐 Authentication & Security Deep Dive

This platform implements an enterprise-grade **Dual-Token Authentication Strategy** with **Token Rotation** and **Silent Refresh**.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             TOKEN STRATEGY                                  │
├──────────────────────────────────────┬──────────────────────────────────────┤
│          ACCESS TOKEN (JWT)          │         REFRESH TOKEN (OPAQUE)       │
├──────────────────────────────────────┼──────────────────────────────────────┤
│ • Lifespan: Short (15–30 minutes)    │ • Lifespan: Long (7 days)            │
│ • Storage: In-memory / localStorage  │ • Storage: Secure localStorage / DB  │
│ • Format: JSON Web Token (HS256)     │ • Format: 64-byte URL-Safe String    │
│ • Verification: Stateless (Signature)│ • Verification: Stateful (DB Lookup) │
│ • Purpose: Authorize API requests    │ • Purpose: Obtain new token pair     │
└──────────────────────────────────────┴──────────────────────────────────────┘
```

---

### Dual-Token Architecture

1. **Access Token (JWT)**:
   - Contains claims such as `"sub": user.email` and `"exp": <expiration_timestamp>`.
   - Signed using the server's `SECRET_KEY` with the `HS256` HMAC algorithm.
   - **Stateless:** When a request arrives at a protected endpoint, the backend validates the cryptographic signature and expiration timestamp **without querying the database**. This ensures high performance for high-traffic endpoints.
   - Kept short-lived so that if a token is intercepted, an attacker has a very limited window of opportunity.

2. **Refresh Token (Opaque Cryptographic String)**:
   - Issued upon successful login.
   - Used exclusively at the `/api/v1/auth/refresh` endpoint to obtain a new Access Token when the old one expires.

---

### Why Opaque Cryptographic Strings for Refresh Tokens?

Why not use a JWT for the refresh token?
* **Instant Revocation:** A JWT is self-contained and valid until its expiration timestamp, making it impossible to invalidate without maintaining a complex distributed blocklist (e.g., in Redis).
* **Stateful Control:** An opaque token (`secrets.token_urlsafe(64)`) is stored in the database. When a user logs out or rotates tokens, the server sets `is_revoked = True`. Any subsequent attempt to use that token is instantly denied.

---

### Why SHA-256 Hash Refresh Tokens in the Database?

Following the principle of **Defense in Depth**:
* We never store plaintext passwords, and we **never store plaintext refresh tokens**.
* If an attacker compromises the database (via a SQL injection vulnerability or a compromised database backup), they only obtain SHA-256 hashes.
* Because the original token is a random 64-byte string with ~512 bits of entropy, it **cannot be reversed or brute-forced**. The attacker cannot use the hash to authenticate.

---

### Token Rotation & Reuse Detection

Every time `/api/v1/auth/refresh` is called:
1. The submitted refresh token is looked up by its SHA-256 hash.
2. The server verifies:
   - Does the hash exist?
   - Is `is_revoked == False`?
   - Is `expires_at > now(UTC)`?
3. **The old refresh token is immediately marked `is_revoked = True`.**
4. A brand new Access Token and a brand new Refresh Token are generated and persisted.
5. **Token Reuse Detection:** If an attacker and a legitimate user both attempt to use the same token, the second attempt will encounter a revoked token. This alerts the system that a token compromise occurred.

---

### Silent Refresh & Preventing "Refresh Storms" in React

In `src/services/apiClient.ts`, Axios interceptors handle token expiration completely behind the scenes so the user is never interrupted.

#### The "Refresh Storm" Problem
Imagine a user opens a dashboard that makes 4 parallel API requests:
1. `GET /api/v1/movies`
2. `GET /api/v1/users/me`
3. `GET /api/v1/shows`
4. `GET /api/v1/notifications`

If the Access Token has expired, all 4 requests return `401 Unauthorized` at the exact same millisecond. Without coordination, the frontend would fire **4 simultaneous refresh requests**. Because of token rotation, the first refresh request revokes the token, causing the other 3 to fail and log the user out!

#### The Project's Solution (Queueing & Mutex)
* `apiClient.ts` maintains a boolean flag `_isRefreshing` and a callback queue `_waitingQueue`.
* When the first 401 arrives:
  1. `_isRefreshing` is set to `true`.
  2. The remaining 3 requests are paused and pushed into `_waitingQueue`.
  3. A single `POST /api/v1/auth/refresh` is executed using **raw Axios** (skipping the interceptor to prevent infinite recursion).
  4. Once the new tokens arrive, `apiClient` saves them, updates default headers, drains the queue by retrying all waiting requests with the new token, and resets `_isRefreshing = false`.
* The user experiences zero interruption or logout prompts.

---

### Complete Authentication Lifecycle Diagram

```
User               Browser / React              FastAPI Backend             PostgreSQL
 │                       │                             │                        │
 ├── 1. Enter Email/Pass ┤                             │                        │
 │                       ├── 2. POST /auth/login ─────►│                        │
 │                       │      (Form-Encoded)         ├── 3. Verify bcrypt ───►│
 │                       │                             ├── 4. Gen JWT + Opaque ─►│ (Store Hash)
 │                       │◄── 5. Return Tokens ────────┤                        │
 │                       │      (access + refresh)     │                        │
 │                       │                             │                        │
 │── 6. Browse /movies ──┤                             │                        │
 │                       ├── 7. GET /movies ──────────►│                        │
 │                       │      (Bearer JWT)           ├── 8. Verify Sig (Fast) │
 │                       │◄── 9. Return Movie List ────┤                        │
 │                       │                             │                        │
 │      ~ 30 Minutes Later (Access Token Expires) ~    │                        │
 │                       │                             │                        │
 │── 10. Click Movie ────┤                             │                        │
 │                       ├── 11. GET /movies/42 ──────►│                        │
 │                       │◄── 12. HTTP 401 Expired ────┤                        │
 │                       │                             │                        │
 │                       │── [ Interceptor Catches 401 ]                        │
 │                       ├── 13. POST /auth/refresh ──►│                        │
 │                       │       (with refresh_token)  ├── 14. Check Hash ─────►│
 │                       │                             ├── 15. Revoke Old ─────►│
 │                       │                             ├── 16. Store New Hash ─►│
 │                       │◄── 17. Return New Pair ─────┤                        │
 │                       │                             │                        │
 │                       │── [ Retry Original Request ]                         │
 │                       ├── 18. GET /movies/42 ──────►│                        │
 │                       │       (New Bearer JWT)      │                        │
 │                       │◄── 19. Return Movie Detail ─┤                        │
 │◄── 20. View Movie ────┤                             │                        │
```

---

## 🗄 Database Schema & Data Models

### Entity-Relationship Diagram

```mermaid
erDiagram
    USERS ||--o{ REFRESH_TOKENS : "has many sessions"
    MOVIES ||--o{ SHOWS : "has many screenings"

    USERS {
        int id PK
        string email UK "Indexed"
        string hashed_password
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    REFRESH_TOKENS {
        int id PK
        int user_id FK "Cascade Delete"
        string token_hash UK "SHA-256, 64-char"
        datetime expires_at
        boolean is_revoked "Default: false"
        datetime created_at
        datetime updated_at
    }

    MOVIES {
        int id PK
        string title "Indexed"
        string description "Nullable"
        int duration_minutes
        string language
        date release_date
        boolean is_active "Default: true"
        datetime created_at
        datetime updated_at
    }

    SHOWS {
        int id PK
        int movie_id FK "Cascade Delete"
        datetime show_time "Indexed"
        int total_seats
        int available_seats "Denormalized for speed"
        string hall_name
        datetime created_at
        datetime updated_at
    }
```

### Table Definitions & Relationships

1. **`users`**:
   - Stores account credentials.
   - Enforces unique email constraint.
   - Passwords stored strictly as bcrypt hashes.

2. **`refresh_tokens`**:
   - Represents active user login sessions across devices.
   - `ondelete="CASCADE"` on `user_id` ensures user deletion cleanly purges all active sessions.
   - `is_revoked` enables instant session cancellation and reuse detection.

3. **`movies`**:
   - Represents film records.
   - Includes `is_active` for soft-disabling movies without breaking foreign key history.
   - Direct one-to-many relationship with `shows`.

4. **`shows`**:
   - Represents specific film screenings at a scheduled datetime in a specified cinema hall.
   - Contains denormalized `available_seats` initialized to `total_seats` on creation, avoiding heavy `COUNT()` queries during booking spikes.

---

## 📡 Complete API Reference

All API routes (except `/health`) are prefixed with `/api/v1`. Interactive OpenAPI documentation is accessible at `http://localhost:8000/docs`.

### Health Check
| Method | Endpoint | Auth Required | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | No | Returns `{"status": "ok"}` when the API server is alive. |

---

### Authentication Endpoints
Tag: `Auth`

#### 1. Register User
- **Method / Path:** `POST /api/v1/auth/register`
- **Auth Required:** No
- **Request Body (`application/json`):**
  ```json
  {
    "email": "jane.doe@example.com",
    "password": "securepassword123"
  }
  ```
- **Response (`201 Created`):**
  ```json
  {
    "id": 1,
    "email": "jane.doe@example.com"
  }
  ```
- **Error Codes:** `400 Bad Request` (Email already registered), `422 Unprocessable Entity` (Password < 8 characters or invalid email format).

#### 2. Login User
- **Method / Path:** `POST /api/v1/auth/login`
- **Auth Required:** No
- **Request Body (`application/x-www-form-urlencoded`):**
  ```
  username=jane.doe@example.com&password=securepassword123
  ```
- **Response (`200 OK`):**
  ```json
  {
    "access_token": "eyJhbGciOiJIUzI1NiIsIn...",
    "refresh_token": "4vK9eZ3m...",
    "token_type": "bearer"
  }
  ```
- **Error Codes:** `401 Unauthorized` (Invalid email or password).

#### 3. Refresh Token Pair
- **Method / Path:** `POST /api/v1/auth/refresh`
- **Auth Required:** No
- **Request Body (`application/json`):**
  ```json
  {
    "refresh_token": "4vK9eZ3m..."
  }
  ```
- **Response (`200 OK`):** Returns brand new `access_token` and rotated `refresh_token`.
- **Error Codes:** `401 Unauthorized` (Token invalid, expired, or revoked).

#### 4. Logout User
- **Method / Path:** `POST /api/v1/auth/logout`
- **Auth Required:** No
- **Request Body (`application/json`):**
  ```json
  {
    "refresh_token": "4vK9eZ3m..."
  }
  ```
- **Response (`204 No Content`):** Token is revoked server-side.

---

### User Endpoints
Tag: `Users`

#### 1. Get Current User Profile
- **Method / Path:** `GET /api/v1/users/me`
- **Auth Required:** Yes (`Bearer <access_token>`)
- **Response (`200 OK`):**
  ```json
  {
    "id": 1,
    "email": "jane.doe@example.com"
  }
  ```
- **Error Codes:** `401 Unauthorized`.

---

### Movie Endpoints
Tag: `Movies`

#### 1. List All Movies
- **Method / Path:** `GET /api/v1/movies`
- **Auth Required:** No
- **Response (`200 OK`):** Array of `MovieResponse` objects ordered by release date descending.

#### 2. Get Movie By ID
- **Method / Path:** `GET /api/v1/movies/{movie_id}`
- **Auth Required:** No
- **Response (`200 OK`):** Single `MovieResponse`.
- **Error Codes:** `404 Not Found`.

#### 3. Create Movie
- **Method / Path:** `POST /api/v1/movies`
- **Auth Required:** Yes (`Bearer <access_token>`)
- **Request Body (`application/json`):**
  ```json
  {
    "title": "Interstellar",
    "description": "A team of explorers travel through a wormhole in space.",
    "duration_minutes": 169,
    "language": "English",
    "release_date": "2014-11-07"
  }
  ```
- **Response (`201 Created`):** Created `MovieResponse`.

#### 4. Update Movie
- **Method / Path:** `PUT /api/v1/movies/{movie_id}`
- **Auth Required:** Yes (`Bearer <access_token>`)
- **Request Body:** Partial `MovieUpdate` object (only supplied fields are updated).
- **Response (`200 OK`):** Updated `MovieResponse`.

#### 5. Delete Movie
- **Method / Path:** `DELETE /api/v1/movies/{movie_id}`
- **Auth Required:** Yes (`Bearer <access_token>`)
- **Response (`204 No Content`):** Movie and its associated shows are removed.

---

### Show Endpoints
Tag: `Shows`

#### 1. List Shows for a Movie
- **Method / Path:** `GET /api/v1/movies/{movie_id}/shows`
- **Auth Required:** No
- **Response (`200 OK`):** Array of `ShowResponse` objects ordered by `show_time` ascending.

#### 2. Create Show
- **Method / Path:** `POST /api/v1/shows`
- **Auth Required:** Yes (`Bearer <access_token>`)
- **Request Body (`application/json`):**
  ```json
  {
    "movie_id": 1,
    "show_time": "2026-10-15T19:30:00Z",
    "total_seats": 120,
    "hall_name": "IMAX Screen 1"
  }
  ```
- **Response (`201 Created`):** Created `ShowResponse` with `available_seats` automatically initialized to `120`.

---

## 🚀 Step-by-Step Installation & Setup Guide

### Prerequisites
* **Python**: 3.10 to 3.14
* **Node.js**: v18.0+ or v22.x (with npm 10+)
* **PostgreSQL**: Server running locally on port `5432`

---

### 1. Database Setup (PostgreSQL)

Open your terminal or `psql` command prompt and verify your PostgreSQL service is running:
```powershell
pg_isready
```

Create both the **development** and **test** databases:
```sql
psql -U postgres -c "CREATE DATABASE booking_platform;"
psql -U postgres -c "CREATE DATABASE booking_platform_test;"
```

---

### 2. Backend Setup & Migrations

#### A. Navigate to backend and create `.env`
```powershell
cd D:\fastapi\booking-platform\backend
copy .env.example .env
```

Ensure your `.env` contains valid credentials:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/booking_platform
SECRET_KEY=generate-a-strong-random-secret-key-here-minimum-32-chars
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

#### B. Create & activate Python virtual environment
```powershell
python -m venv .venv
.venv\Scripts\activate
```

#### C. Install Python dependencies
```powershell
pip install -e ".[dev]"
pip install email-validator httpx
```

> [!TIP]
> **Python 3.14 Compatibility Note:**
> If you encounter an error when importing `passlib` or `bcrypt` on newer Python releases, pin the versions as follows:
> ```powershell
> pip uninstall bcrypt passlib -y
> pip install passlib==1.7.4 bcrypt==3.2.2
> ```

#### D. Run Alembic database migrations
Apply the existing migration chain to build all database tables:
```powershell
alembic upgrade head
```

Verify the tables were created:
```powershell
psql -U postgres -d booking_platform -c "\dt"
```
*(You should see `users`, `refresh_tokens`, `movies`, `shows`, and `alembic_version`)*.

---

### 3. Frontend Setup & Environment

#### A. Navigate to frontend
```powershell
cd D:\fastapi\booking-platform\frontend
```

#### B. Setup environment variables
Create a `.env` file in `frontend/`:
```env
VITE_API_URL=http://localhost:8000/api/v1
```

#### C. Install Node dependencies
```powershell
npm install
```

> [!NOTE]
> **Tailwind CSS PostCSS Plugin:**
> If you experience styling build errors related to `@tailwindcss/postcss`, install the dedicated PostCSS plugin:
> ```powershell
> npm install -D @tailwindcss/postcss
> ```

---

### 4. Running the Complete Application

#### Start Backend Server:
```powershell
cd D:\fastapi\booking-platform\backend
.venv\Scripts\activate
uvicorn main:app --reload --port 8000
```
* API Server: `http://localhost:8000`
* Swagger Documentation: `http://localhost:8000/docs`
* Health Check: `http://localhost:8000/health`

#### Start Frontend Development Server:
```powershell
cd D:\fastapi\booking-platform\frontend
npm run dev
```
* Web Application: `http://localhost:5173`

---

### 5. Running Automated Tests

The backend includes test suites with isolated database lifecycle management via `pytest` and `conftest.py`.

```powershell
cd D:\fastapi\booking-platform\backend
.venv\Scripts\activate

# Run authentication unit tests
pytest tests/test_auth.py -v

# Run API integration tests
pytest tests/test_routes_auth.py -v

# Run entire test suite
pytest -v
```

---

### 6. Troubleshooting & Common Pitfalls

| Issue / Symptom | Root Cause | Solution |
| :--- | :--- | :--- |
| **CORS error in browser console** | Frontend origin (`http://localhost:5173`) not allowed in backend CORS configuration. | Ensure `main.py` has `allow_origins=["http://localhost:5173"]` and `allow_credentials=True`. |
| **Login returns `422 Unprocessable Entity`** | Sending JSON to `/api/v1/auth/login`. | `OAuth2PasswordRequestForm` requires `application/x-www-form-urlencoded`. Ensure `URLSearchParams` is used in `authService.ts`. |
| **Alembic table creation fails** | Missing database or wrong connection string. | Verify `DATABASE_URL` in `.env` and verify database exists using `psql -l`. |
| **Infinite refresh loop on 401** | Calling `apiClient` inside `refreshToken()` instead of raw `axios`. | Use un-intercepted `axios.post()` inside `refreshToken()` to break the interceptor cycle. |
| **Tests fail with DB errors** | Test DB `booking_platform_test` was not created. | Run `psql -U postgres -c "CREATE DATABASE booking_platform_test;"`. |

---

## 📐 Development Guidelines & Architectural Invariants

To preserve the clean architecture of this codebase as you add new features (e.g., Seat Selection, Payment Gateways, Booking Reservations), adhere to these non-negotiable rules:

### 🛑 Backend Rules
1. **Never import database sessions inside services directly.** Sessions are injected via `Depends(get_db)` into routes and passed as arguments down to repositories.
2. **Never return SQLAlchemy model instances directly from routes.** Always specify `response_model=YourSchemaResponse` to prevent data leakage and enforce strict schemas.
3. **Never write raw SQL queries in routes or services.** All SQL/ORM logic belongs exclusively inside `app/repositories/`.
4. **Never store plain text secrets or passwords.** Always use `security.hash_password()` and `security.hash_refresh_token()`.

### 🛑 Frontend Rules
1. **Components must never make direct `axios` or `fetch` calls.** Components invoke custom hooks, which call feature services.
2. **Never store hardcoded endpoint strings in components.** Always reference the centralized `ENDPOINTS` dictionary in `src/services/endpoints.ts`.
3. **Always use Zod for form validation.** Validate user input on the client before submitting payloads to the backend.
4. **Use React Query for server data.** Avoid storing server API data in local `useState` variables; let React Query manage caching, refetching, and cache invalidation.

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
