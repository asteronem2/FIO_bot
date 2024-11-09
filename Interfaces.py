from abc import abstractmethod
from typing import NoReturn

from aiogram.types.callback_query import CallbackQuery
from aiogram.types.inline_query import InlineQuery
from aiogram.types.message import Message
from aiogram.types.message_reaction_updated import MessageReactionUpdated

import Bot
from core import UserCore
from models import User
from utils import get_locale


class TextMessageInterface:
    db_user: User

    def __init__(self, message: Message):
        self.message = message
        self.chat = message.chat
        self.user = message.from_user
        self.text = message.text if message.text else (message.caption if message.caption else '')
        self.text_low = self.text.lower().strip()

        self.user_core = UserCore

        self.locale = get_locale('ru')

        self.bot = Bot.BotInter()

    async def async_init(self):
        await self._get_addition_from_db()

    @abstractmethod
    async def define(self) -> NoReturn | dict:
        """
        :return: True if these processors define and None if not define
        """
        pass

    @abstractmethod
    async def process(self, *args, **kwargs) -> None:
        pass

    async def generate_send_message(self, *args, **kwargs):
        pass

    async def generate_error_message(self, *args, **kwargs):
        pass

    async def generate_edit_message(self, *args, **kwargs):
        pass

    async def _get_addition_from_db(self):
        self.db_user = await self.user_core.find_one(user_id=self.user.id)

        if self.db_user is None:
            await self.user_core.add(
                user_id=self.user.id,
                username=self.user.username,
                first_name=self.user.first_name
            )

        self.db_user = await self.user_core.find_one(user_id=self.user.id)


class CallbackQueryInterface:
    db_user: User

    def __init__(self, callback: CallbackQuery):
        self.callback = callback
        self.chat = callback.message.chat
        self.user = callback.from_user
        self.message = callback.message
        self.sent_message_id = callback.message.message_id
        self.topic = 0 if callback.message.message_thread_id is None else callback.message.message_thread_id
        self.cdata = callback.data

        self.user_core = UserCore

        self.locale = get_locale('ru')

        self.bot = Bot.BotInter()

    async def async_init(self):
        await self._get_addition_from_db()

    @abstractmethod
    async def define(self) -> NoReturn | dict:
        """
        :return: True if these processors define and None if not define
        """
        pass

    @abstractmethod
    async def process(self, *args, **kwargs) -> None:
        pass

    async def generate_send_message(self, *args, **kwargs):
        pass

    async def generate_edit_message(self, *args, **kwargs):
        pass

    async def generate_error_message(self, *args, **kwargs):
        pass

    async def _get_addition_from_db(self):
        self.db_user = await self.user_core.find_one(user_id=self.user.id)

        if self.db_user is None:
            await self.user_core.add(
                user_id=self.user.id,
                username=self.user.username,
                first_name=self.user.first_name
            )

        self.db_user = await self.user_core.find_one(user_id=self.user.id)


class NextMessageInterface:
    cdata: str

    def __init__(self, message: Message):
        self.message = message
        self.chat = message.chat
        self.user = message.from_user
        self.text = message.text or message.caption or ''
        self.text_low = self.text.lower().strip()
        self.topic = 0 if message.message_thread_id is None else message.message_thread_id

        self.user_core = UserCore

        self.locale = get_locale('ru')

        self.bot = Bot.BotInter()

    async def async_init(self):
        await self._get_addition_from_db()

    @abstractmethod
    async def define(self) -> NoReturn | dict:
        pass

    @abstractmethod
    async def process(self, *args, **kwargs) -> None:
        pass

    async def generate_send_message(self, *args, **kwargs):
        pass

    async def generate_edit_message(self, *args, **kwargs):
        pass

    async def generate_error_message(self, *args, **kwargs):
        pass

    async def _get_addition_from_db(self):
        self.db_user = await self.user_core.find_one(user_id=self.user.id)

        if self.db_user is None:
            await self.user_core.add(
                user_id=self.user.id,
                username=self.user.username,
                first_name=self.user.first_name
            )

        self.db_user = await self.user_core.find_one(user_id=self.user.id)
        self.next_message_info = self.db_user.next_message_info

class ReactionInterface:
    def __init__(self, reaction: MessageReactionUpdated):
        self.reaction = reaction
        self.chat = reaction.chat
        self.user = reaction.user
        self.new = False
        self.old = False

        if reaction.new_reaction:
            self.new = True
        else:
            self.old = True

        self.emoji = reaction.new_reaction[-1].emoji if self.new else reaction.old_reaction[-1].emoji

        self.user_core = UserCore

        self.locale = get_locale('ru')

        self.bot = Bot.BotInter()

        self.message_id = reaction.message_id

    async def async_init(self):
        await self._get_addition_from_db()

    @abstractmethod
    async def define(self) -> NoReturn | dict:
        pass

    @abstractmethod
    async def process(self, *args, **kwargs) -> None:
        pass

    async def generate_send_message(self, *args, **kwargs):
        pass

    async def _get_addition_from_db(self):
        self.db_user = await self.user_core.find_one(user_id=self.user.id)

        if self.db_user is None:
            await self.user_core.add(
                user_id=self.user.id,
                username=self.user.username,
                first_name=self.user.first_name
            )

        self.db_user = await self.user_core.find_one(user_id=self.user.id)


class InlineQueryInterface:
    def __init__(self, inline: InlineQuery):
        self.inline = inline
        self.query = inline.query
        self.bot = Bot.BotInter()
        self.user_core = UserCore

        self.locale = get_locale('ru')

    async def async_init(self):
        pass

    @abstractmethod
    async def define(self) -> NoReturn | dict:
        pass

    @abstractmethod
    async def process(self, *args, **kwargs):
        pass

    @abstractmethod
    async def generate_results(self, *args, **kwargs):
        pass
