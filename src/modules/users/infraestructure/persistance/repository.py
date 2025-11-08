from typing import override
from src.modules.users.domain.interfaces import IUserRepository
from src.modules.users.domain.entities import User as UserEntity
from src.modules.users.infraestructure.persistance.models import User as UserModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class SqlAlchemyUserRepository(IUserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    @override
    async def create(self, user: UserEntity) -> UserEntity:
        user_model = UserModel(
            name=user.name,
            email=user.email,
            is_admin=user.is_admin,
        )
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        return UserEntity(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            is_admin=user_model.is_admin,
        )

    @override
    async def update(self, user: UserEntity) -> UserEntity:
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user.id)
        )
        user_model = result.scalar_one_or_none()

        if not user_model:
            raise ValueError(f"User with id {user.id} not found")

        user_model.name = user.name
        user_model.email = user.email
        user_model.is_admin = user.is_admin
        await self.session.commit()
        await self.session.refresh(user_model)
        return UserEntity(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            is_admin=user_model.is_admin,
        )

    @override
    async def get_by_id(self, id: int) -> UserEntity | None:
        result = await self.session.execute(select(UserModel).where(UserModel.id == id))
        user_model = (
            result.scalar_one_or_none()
        )  # gives us the first row of the result or None if no row is found
        if not user_model:
            return None
        return UserEntity(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            is_admin=user_model.is_admin,
        )

    @override
    async def get_all(self) -> list[UserEntity]:
        result = await self.session.execute(select(UserModel).order_by(UserModel.id))
        user_models = result.scalars().all()
        return [
            UserEntity(
                id=user_model.id,
                name=user_model.name,
                email=user_model.email,
                is_admin=user_model.is_admin,
            )
            for user_model in user_models
        ]
