from db.tables import Mailing
from app.repositories.base import BaseRepository


class MailingRepository(BaseRepository):
    base_table = Mailing

    async def get(self, model_id: int) -> Mailing:
        return await self._get_one(id=model_id)

    async def create(self, model: Mailing) -> Mailing:
        return await self._create(model)

    async def list(self) -> list[Mailing]:
        return await self._get_many()
