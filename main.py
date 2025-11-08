import asyncio

from src.modules.users.infraestructure.persistance.repository import (
    SqlAlchemyUserRepository,
)
from src.modules.shared.database.sql_alchemy_db import (
    DatabaseSessionManager,
    Base,
    get_db_session,
)
from src.modules.users.domain.entities import User as UserEntity
from testcontainers.postgres import PostgresContainer


async def main():
    container = PostgresContainer("postgres:18-alpine")
    container.start()

    database_url = container.get_connection_url(driver="asyncpg")
    session_manager = DatabaseSessionManager(database_url, {"echo": False})

    async with get_db_session(session_manager) as db_session:
        # Create tables
        await db_session.run_sync(
            lambda sync_session: Base.metadata.create_all(sync_session.get_bind())
        )

        # Use repository
        repository = SqlAlchemyUserRepository(db_session)
        await repository.create(
            UserEntity(
                id=0, name="John Doe", email="john.doe@example.com", is_admin=False
            )
        )
        user = await repository.get_by_id(1)
        print(user)

    container.stop()


if __name__ == "__main__":
    asyncio.run(main())
