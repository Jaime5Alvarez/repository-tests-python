import pytest
import pytest_asyncio

from src.modules.users.infraestructure.persistance.repository import (
    SqlAlchemyUserRepository,
)
from src.modules.users.domain.entities import User as UserEntity
from sqlalchemy.ext.asyncio import AsyncSession


@pytest_asyncio.fixture
async def repository(db_session: AsyncSession) -> SqlAlchemyUserRepository:
    """Provides a repository instance with a clean database session"""
    return SqlAlchemyUserRepository(db_session)


class TestSqlAlchemyUserRepository:
    @pytest.mark.asyncio
    async def test_create_user(self, repository: SqlAlchemyUserRepository):
        """Test creating a new user"""
        # Arrange
        user_data = UserEntity(
            id=0,  # Will be ignored, database will assign the ID
            name="John Doe",
            email="john.doe@example.com",
            is_admin=False,
        )

        # Act
        created_user = await repository.create(user_data)

        # Assert
        assert created_user.id is not None
        assert created_user.name == "John Doe"
        assert created_user.email == "john.doe@example.com"
        assert created_user.is_admin is False

    @pytest.mark.asyncio
    async def test_create_admin_user(self, repository: SqlAlchemyUserRepository):
        """Test creating an admin user"""
        # Arrange
        admin_data = UserEntity(
            id=0, name="Admin User", email="admin@example.com", is_admin=True
        )

        # Act
        created_admin = await repository.create(admin_data)

        # Assert
        assert created_admin.id is not None
        assert created_admin.is_admin is True

    @pytest.mark.asyncio
    async def test_get_by_id_existing_user(self, repository: SqlAlchemyUserRepository):
        """Test retrieving an existing user by ID"""
        # Arrange - Create a user first
        user_data = UserEntity(
            id=0, name="Jane Smith", email="jane.smith@example.com", is_admin=False
        )
        created_user = await repository.create(user_data)

        # Act
        retrieved_user = await repository.get_by_id(created_user.id)

        # Assert
        assert retrieved_user is not None
        assert retrieved_user.id == created_user.id
        assert retrieved_user.name == "Jane Smith"
        assert retrieved_user.email == "jane.smith@example.com"
        assert retrieved_user.is_admin is False

    @pytest.mark.asyncio
    async def test_get_by_id_non_existing_user(
        self, repository: SqlAlchemyUserRepository
    ):
        """Test retrieving a non-existing user by ID"""
        # Act
        retrieved_user = await repository.get_by_id(999)

        # Assert
        assert retrieved_user is None

    @pytest.mark.asyncio
    async def test_create_multiple_users(self, repository: SqlAlchemyUserRepository):
        """Test creating multiple users"""
        # Arrange
        users_data = [
            UserEntity(id=0, name="User 1", email="user1@example.com", is_admin=False),
            UserEntity(id=0, name="User 2", email="user2@example.com", is_admin=True),
            UserEntity(id=0, name="User 3", email="user3@example.com", is_admin=False),
        ]

        # Act
        created_users = []
        for user_data in users_data:
            created_user = await repository.create(user_data)
            created_users.append(created_user)

        # Assert
        assert len(created_users) == 3
        assert all(user.id is not None for user in created_users)
        assert created_users[0].name == "User 1"
        assert created_users[1].is_admin is True
        assert created_users[2].email == "user3@example.com"

    @pytest.mark.asyncio
    async def test_get_all_created_users(self, repository: SqlAlchemyUserRepository):
        """Test that we can retrieve all created users"""
        # Arrange - Create multiple users
        user1 = await repository.create(
            UserEntity(id=0, name="Alice", email="alice@example.com", is_admin=False)
        )
        user2 = await repository.create(
            UserEntity(id=0, name="Bob", email="bob@example.com", is_admin=True)
        )

        # Act
        retrieved_user1 = await repository.get_by_id(user1.id)
        retrieved_user2 = await repository.get_by_id(user2.id)

        # Assert
        assert retrieved_user1 is not None
        assert retrieved_user1.name == "Alice"
        assert retrieved_user2 is not None
        assert retrieved_user2.name == "Bob"
