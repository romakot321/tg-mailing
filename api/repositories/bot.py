from fastapi import Depends
from app.controller import BotController


class BotRepository:
    def __init__(self, bot_controller: BotController = Depends()):
        self.bot_controller = bot_controller

    async def send_mailing(self, mailing_id: int):
        await self.bot_controller.send_mailing(mailing_id)

