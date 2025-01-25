from db.tables import User
from app.repositories.base import BaseRepository


class UserRepository(BaseRepository):
    base_table = User

    async def create(self, model: User) -> User:
        return await self._create(model)

    async def list(self) -> list[User]:
        return list(await self._get_many())

