"""
conftest.py — Shared Test Infrastructure

This file is pytest's equivalent of a base test class in xUnit.
Any fixture defined here is automatically available in EVERY test file
in this directory — no imports needed.

HOW PYTEST FIXTURES WORK:
A fixture is a function decorated with @pytest.fixture that sets up
(and optionally tears down) something a test needs.
When a test function declares a parameter with the same name as a fixture,
pytest automatically calls the fixture and injects the result.

.NET equivalent: IClassFixture<T> or [SetUp]/[TearDown] in NUnit/xUnit.
Fixtures are more powerful because they support dependency injection
(one fixture can depend on another) and scoping (session/module/function).

WHAT THIS FILE PROVIDES:
1. create_test_tables — creates DB tables once before all tests run
2. db_session         — a fresh database session per test (cleans up after)
3. client             — a TestClient with the test DB wired in
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base
from app.dependencies.db import get_db

# Import every model so SQLAlchemy registers them on Base.metadata.
# Without these imports, Base.metadata.create_all() won't know about the tables.
# This is the same reason alembic/env.py imports all models.
from app.models.user import User  # noqa: F401
from app.models.movie import Movie  # noqa: F401
from app.models.show import Show  # noqa: F401
from app.models.refresh_token import RefreshToken

from main import app


# --- Test Database Setup -------------------------------------------------------

# We use a SEPARATE database for tests — never the production database.
# Why? Tests create and delete real data. Running them against production
# would corrupt your data.

# We derive the test URL from the production URL by swapping the database name.
# Prerequisite: create the database in PostgreSQL once:
# CREATE DATABASE booking_platform_test;

# .NET equivalent: a separate connection string in appsettings.Test.json
TEST_DATABASE_URL = settings.DATABASE_URL.replace(
    "/booking_platform",
    "/booking_platform_test",
)

# Same setup as the production engine/session, but pointing at the test database.
# echo=False keeps test output clean (set to True temporarily to debug SQL queries).
engine = create_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# --- Fixture 1: create_test_tables --------------------------------------------

# scope="session"  → runs ONCE for the entire test run (not once per test)
# autouse=True     → automatically applied without being listed as a parameter

# Before all tests: create every table defined in our models.
# After all tests: drop every table (clean up the test database).


# .NET equivalent: [AssemblyInitialize] — setup that runs once before all tests.
@pytest.fixture(scope="session", autouse=True)
def create_test_tables():
    Base.metadata.create_all(bind=engine)
    yield  # ← all tests run here
    Base.metadata.drop_all(bind=engine)


# --- Fixture 2: db_session -----------------------------------------------------

# scope="function" (default) → a new session for EACH test function.

# After each test, we delete all rows from all tables.
# reversed(sorted_tables) deletes child tables (shows) before parent tables
# (movies, users) — this respects foreign key constraints.

# Why not just rollback the session?
# Our repository layer calls db.commit() which permanently writes to the DB.
# A session.rollback() can only undo uncommitted changes.
# Deleting all rows is simpler and works regardless of commit history.


# .NET equivalent: [TestCleanup] that calls dbContext.Database.EnsureDeleted()
@pytest.fixture()
def db_session():
    session = TestingSessionLocal()
    yield session
    session.close()

    # Clean all rows after each test so the next test starts fresh
    with engine.begin() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())


# --- Fixture 3: client ---------------------------------------------------------

# A TestClient is an in-process HTTP client — it sends real HTTP requests to your
# FastAPI app without needing a running server. Requests go directly through the
# ASGI interface in memory.

# .NET equivalent: WebApplicationFactory<TStartup>.CreateClient()

# DEPENDENCY OVERRIDE — the key technique:
# FastAPI's dependency_overrides lets you replace any Depends() function for the
# duration of a test. Here we replace get_db() so every route that calls
# Depends(get_db) receives our test session instead of the real one.

# .NET equivalent:
# builder.ConfigureTestServices(services => {
#     services.RemoveAll<IDbContext>();
#     services.AddScoped<IDbContext>(_ => testDbContext);
# })


@pytest.fixture()
def client(db_session):
    def override_get_db():
        """Replaces get_db() in all routes during this test."""
        yield db_session

    # Register the override — applies to the whole app
    app.dependency_overrides[get_db] = override_get_db

    # TestClient without context manager = no lifespan events triggered.
    # This avoids the startup health-check connecting to the production database.
    yield TestClient(app)

    # Always clean up overrides after the test so they don't leak between tests
    app.dependency_overrides.clear()
