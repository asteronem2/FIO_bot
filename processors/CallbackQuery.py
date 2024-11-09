import re
from typing import NoReturn

from Bot import MsgModel
from Interfaces import CallbackQueryInterface


class TakePart(CallbackQueryInterface):
    async def define(self) -> NoReturn | dict:
        rres = re.fullmatch(r'take_part', self.cdata)
        if rres:
            return True

    async def process(self, *args, **kwargs) -> None:
        await self.bot.edit_message(MsgModel(
            chat_id=self.chat.id,
            text=self.locale['TakePartTxt'],
            message_id=self.sent_message_id
        ))

        await self.user_core.update({'id': self.db_user.id}, next_message_info='FIO')