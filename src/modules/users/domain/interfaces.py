from abc import ABC, abstractmethod

from src.modules.users.domain.entities import User


class UserRepository(ABC):
    @abstractmethod
    async def create(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_by_id(self, id: int) -> User | None:
        pass
