import re
from typing import NoReturn

from aiogram.types import InlineKeyboardButton as IButton

from Bot import MsgModel
from Interfaces import TextMessageInterface


class StartMsg(TextMessageInterface):
    async def define(self) -> NoReturn | dict:
        rres = re.fullmatch(r'/start.*', self.text_low)
        if rres:
            return True

    async def process(self, *args, **kwargs) -> None:
        await self.bot.send_message(MsgModel(
            chat_id=self.chat.id,
            text=self.locale['StartTxt'],
            markup=[[IButton(text='Принять участие', callback_data='take_part')]]
        ))

        await self.user_core.update({'id': self.db_user.id}, next_message_info=None)