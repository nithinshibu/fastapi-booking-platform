# Booking Platform

A modern full-stack web application for booking movies and shows, built with **FastAPI** (Python) for the backend and **React** (TypeScript) for the frontend. This project demonstrates best practices in API design, authentication, database management, and frontend development.

---

## Table of Contents
- [Booking Platform](#booking-platform)
  - [Table of Contents](#table-of-contents)
  - [Project Overview](#project-overview)
  - [Tech Stack](#tech-stack)
  - [Features](#features)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Backend Setup](#backend-setup)
    - [Frontend Setup](#frontend-setup)
  - [API Endpoints](#api-endpoints)
    - [Auth](#auth)
    - [Users](#users)
    - [Movies](#movies)
    - [Shows](#shows)
  - [Project Structure](#project-structure)
  - [Development Tools](#development-tools)
  - [License](#license)

---

## Project Overview
This platform allows users to register, authenticate, browse movies and shows, and make bookings. It is designed for scalability, maintainability, and ease of use, following industry standards for both backend and frontend development.

---

## Tech Stack
- **Backend:** FastAPI, SQLAlchemy, Alembic, JWT Authentication
- **Frontend:** React, TypeScript, Vite, Tailwind CSS
- **Database:** (Configurable, e.g., PostgreSQL, SQLite)
- **Testing:** Pytest (backend)

---

## Features
- User registration and authentication (JWT-based)
- Movie and show management
- Booking functionality
- Secure API endpoints
- Responsive frontend UI
- Environment-based configuration

---

## Getting Started

### Prerequisites
- Python 3.9+
- Node.js 16+
- (Recommended) PostgreSQL or SQLite

### Backend Setup
1. Navigate to `backend/`
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt  # or use pyproject.toml with poetry/pip
   ```
4. Set up environment variables (see `.env.example`)
5. Run database migrations:
   ```bash
   alembic upgrade head
   ```
6. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend Setup
1. Navigate to `frontend/`
2. Install dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```

---

## API Endpoints

### Auth
- `POST /api/v1/auth/register` — Register a new user
- `POST /api/v1/auth/login` — Login and receive JWT tokens
- `POST /api/v1/auth/refresh` — Refresh access token

### Users
- `GET /api/v1/users/me` — Get current user profile (auth required)

### Movies
- `GET /api/v1/movies/` — List all movies
- `GET /api/v1/movies/{movie_id}` — Get movie details
- `POST /api/v1/movies/` — Create a new movie (admin only)
- `PUT /api/v1/movies/{movie_id}` — Update a movie (admin only)
- `DELETE /api/v1/movies/{movie_id}` — Delete a movie (admin only)

### Shows
- `GET /api/v1/shows/` — List all shows
- `GET /api/v1/shows/{show_id}` — Get show details
- `POST /api/v1/shows/` — Create a new show (admin only)
- `PUT /api/v1/shows/{show_id}` — Update a show (admin only)
- `DELETE /api/v1/shows/{show_id}` — Delete a show (admin only)

> **Note:** All endpoints are prefixed with `/api/v1/` and may require authentication.

---

## Project Structure
```
backend/
  app/
    api/v1/routes/      # FastAPI route definitions
    core/               # Config, security, settings
    db/                 # Database models and session
    dependencies/       # Dependency injection
    models/             # SQLAlchemy models
    repositories/       # Data access logic
    schemas/            # Pydantic schemas
    services/           # Business logic
  tests/                # Pytest test cases
frontend/
  src/
    app/                # App entry and providers
    components/         # Reusable UI components
    features/           # Feature modules (auth, movies, shows)
    services/           # API client and endpoints
    utils/              # Utility functions
```

---

## Development Tools
- **Backend:**
  - FastAPI
  - SQLAlchemy
  - Alembic
  - Pytest
  - Uvicorn
- **Frontend:**
  - React
  - Vite
  - Tailwind CSS
  - TypeScript
  - ESLint, Prettier

---

## License
This project is licensed under the MIT License.
