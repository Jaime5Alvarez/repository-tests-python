from typing import override
from src.modules.users.domain.interfaces import UserRepository
from src.modules.users.domain.entities import User as UserEntity
from src.modules.users.infraestructure.persistance.models import User as UserModel
from sqlalchemy.ext.asyncio import AsyncSession


class SqlAlchemyUserRepository(UserRepository):
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
    async def get_by_id(self, id: int) -> UserEntity | None:
        user_model = await self.session.get(UserModel, id)
        if not user_model:
            return None
        return UserEntity(
            id=user_model.id,
            name=user_model.name,
            email=user_model.email,
            is_admin=user_model.is_admin,
        )
