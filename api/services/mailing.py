from fastapi import Depends

from db.tables import Mailing
from api.repositories.mailing import MailingRepository
from api.repositories.bot import BotRepository
from api.schemas.mailing import MailingSchema
from api.schemas.mailing import MailingCreateSchema, MailingUpdateSchema


class MailingService:
    def __init__(
            self,
            mailing_repository: MailingRepository = Depends(),
            bot_repository: BotRepository = Depends()
    ):
        self.mailing_repository = mailing_repository
        self.bot_repository = bot_repository

    async def create(self, schema: MailingCreateSchema) -> MailingSchema:
        model = Mailing(**schema.model_dump() | {"gender": schema.gender.value if schema.gender else None})
        model = await self.mailing_repository.create(model)
        return MailingSchema.model_validate(model)

    async def list(self) -> list[MailingSchema]:
        models = await self.mailing_repository.list()
        return [
            MailingSchema.model_validate(model)
            for model in models
        ]

    async def get(self, mailing_id: int) -> MailingSchema:
        model = await self.mailing_repository.get(mailing_id)
        return MailingSchema.model_validate(model)

    async def update(self, mailing_id, schema: MailingUpdateSchema) -> MailingSchema:
        model = await self.mailing_repository.update(mailing_id, **schema.model_dump(exclude_none=True))
        return MailingSchema.model_validate(model)

    async def delete(self, mailing_id: int):
        await self.mailing_repository.delete(mailing_id)

    async def send(self, mailing_id: int):
        await self.bot_repository.send_mailing(mailing_id)

