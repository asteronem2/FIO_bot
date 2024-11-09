from typing import NoReturn

from Bot import MsgModel
from Interfaces import NextMessageInterface


class Fio(NextMessageInterface):
    async def define(self) -> NoReturn | dict:
        if self.next_message_info == 'FIO':
            return True

    async def process(self, *args, **kwargs) -> None:
        await self.user_core.update({'id': self.db_user.id}, fio=self.text)
        await self.bot.send_message(MsgModel(
            chat_id=self.chat.id,
            text=self.locale['ThanksTxt']
        ))