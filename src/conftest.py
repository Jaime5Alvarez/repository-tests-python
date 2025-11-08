import pytest_asyncio
from src.modules.shared.database.sql_alchemy_db import DatabaseSessionManager, Base
from testcontainers.postgres import PostgresContainer

@pytest_asyncio.fixture(scope="session")
async def database_url():
    """Provides a PostgreSQL container for the entire test session"""
    # before all tests
    container = PostgresContainer("postgres:18-alpine")
    container.start()

    # Replace the connection URL to use asyncpg instead of psycopg2, only if needed
    yield (
        container.get_connection_url()
        .replace("postgresql://", "postgresql+asyncpg://")
        .replace("postgresql+psycopg2://", "postgresql+asyncpg://")
    )
    # after all tests
    container.stop()


# before each test
@pytest_asyncio.fixture(scope="function")
async def db_session(database_url):
    """Provides a clean database session for each test"""
    session_manager = DatabaseSessionManager(
        database_url,
        {"echo": False},
    )

    async with session_manager.session() as session:
        # Clean database before test
        await session.run_sync(
            lambda sync_session: Base.metadata.drop_all(sync_session.get_bind())
        )
        await session.run_sync(
            lambda sync_session: Base.metadata.create_all(sync_session.get_bind())
        )

        yield session

        await session.commit()

    await session_manager.close()
