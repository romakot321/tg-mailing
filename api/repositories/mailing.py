from .base import BaseRepository
from db.tables import Mailing


class MailingRepository(BaseRepository):
    base_table = Mailing

    async def create(self, model: Mailing) -> Mailing:
        return await self._create(model)

    async def list(self) -> list[Mailing]:
        return await self._get_many()

    async def delete(self, model_id: int):
        await self._delete(model_id)

    async def update(self, model_id: int, **fields) -> Mailing:
        return await self._update(model_id, **fields)

