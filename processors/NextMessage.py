from typing import NoReturn

import aiogram.exceptions

from Bot import MsgModel
from Interfaces import NextMessageInterface


class Fio(NextMessageInterface):
    async def define(self) -> NoReturn | dict:
        if self.next_message_info == 'FIO':
            return True

    async def process(self, *args, **kwargs) -> None:
        await self.user_core.update({'id': self.db_user.id}, fio=self.text, next_message_info=None)
        await self.bot.send_message(MsgModel(
            chat_id=self.chat.id,
            text=self.locale['ThanksTxt']
        ))


class Distribution(NextMessageInterface):
    async def define(self) -> NoReturn | dict:
        if self.nmi == 'distribution':
            return True

    async def process(self, *args, **kwargs) -> None:
        await self.user_core.update({'id': self.db_user.id}, next_message_info=None)

        if self.text_low == 'отмена':
            return

        all_users = await self.user_core.find_all()

        count = 0

        for user in all_users:
            try:
                await self.bot.send_message(MsgModel(
                    chat_id=user.user_id,
                    text=self.text,
                    photo=None if not self.message.photo else self.message.photo[-1].file_id,
                    photo_type='file_id'
                ))
                count += 1
            except aiogram.exceptions.TelegramBadRequest:
                continue
            except aiogram.exceptions.TelegramForbiddenError:
                continue

        await self.bot.send_message(MsgModel(
            chat_id=self.user.id,
            text=f'Успешно разослано {count} сообщений'
        ))