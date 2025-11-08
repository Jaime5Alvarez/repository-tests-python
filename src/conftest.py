import pytest_asyncio
from src.modules.shared.database.sql_alchemy_db import (
    Base,
    factory_session_manager,
)
from testcontainers.postgres import PostgresContainer


@pytest_asyncio.fixture(scope="session")
async def database_url():
    """Provides a PostgreSQL container for the entire test session"""
    # before all tests
    container = PostgresContainer("postgres:18-alpine")
    container.start()

    yield (container.get_connection_url(driver="asyncpg"))
    # after all tests
    container.stop()


# before each test
@pytest_asyncio.fixture(scope="function")
async def db_session(database_url):
    """Provides a clean database session for each test"""
    async with factory_session_manager(database_url).session() as session:
        # Clean database before test
        await session.run_sync(
            lambda sync_session: Base.metadata.drop_all(sync_session.get_bind())
        )
        await session.run_sync(
            lambda sync_session: Base.metadata.create_all(sync_session.get_bind())
        )
        yield session
