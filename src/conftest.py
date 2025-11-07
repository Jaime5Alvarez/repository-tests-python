import pytest_asyncio
from src.modules.shared.database.sql_alchemy_db import DatabaseSessionManager, Base


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Provides a clean database session for each test"""
    session_manager = DatabaseSessionManager(
        "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres",
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
