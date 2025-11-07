"""Shared test fixtures for PostgreSQL Data API.

Provides database fixtures for unit and integration tests.
"""

import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from testcontainers.postgres import PostgresContainer

from src.models.base import Base
from src.core.config import settings


@pytest.fixture(scope="session")
def postgres_container():
    """Start PostgreSQL container for integration tests.

    Yields:
        PostgresContainer instance
    """
    with PostgresContainer("postgres:16") as postgres:
        yield postgres


@pytest.fixture(scope="session")
def database_url(postgres_container):
    """Get database URL from container.

    Args:
        postgres_container: PostgreSQL container fixture

    Returns:
        Async database URL (asyncpg)
    """
    # Get connection URL and convert to async
    url = postgres_container.get_connection_url()
    return url.replace("psycopg2", "asyncpg")


@pytest_asyncio.fixture(scope="function")
async def engine(database_url):
    """Create test database engine.

    Args:
        database_url: Database URL fixture

    Yields:
        Async engine instance

    Note:
        Uses NullPool for testing to avoid connection issues.
    """
    from sqlalchemy.pool import NullPool

    engine = create_async_engine(
        database_url,
        echo=False,
        poolclass=NullPool,
    )

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest_asyncio.fixture(scope="function")
async def session(engine):
    """Create test database session.

    Args:
        engine: Database engine fixture

    Yields:
        Async session instance

    Note:
        Session is rolled back after each test.
    """
    AsyncSessionLocal = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with AsyncSessionLocal() as session:
        yield session
        await session.rollback()


@pytest.fixture
def override_settings(monkeypatch):
    """Override settings for testing.

    Args:
        monkeypatch: Pytest monkeypatch fixture

    Example:
        >>> def test_with_custom_settings(override_settings):
        >>>     override_settings(TESTING=True, DEBUG=False)
        >>>     # Test code here
    """
    def _override(**kwargs):
        for key, value in kwargs.items():
            monkeypatch.setattr(settings, key, value)

    return _override
