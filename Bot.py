from dataclasses import dataclass
from typing import List, Literal

import aiogram
from aiogram import exceptions
from aiogram.types import InlineKeyboardMarkup as IMarkup, InlineKeyboardButton as IButton, Message, FSInputFile

from main import bot


@dataclass
class MsgModel:
    chat_id: int
    text: str | None = None
    markup: List[List[IButton]] | None = None
    photo: str | None = None
    photo_type: Literal['file_id', 'file_name'] = 'file_id'
    message_id: int | None = None

    disable_notifications: bool = False
    disable_web_page_preview: bool = True
    reply_to_message_id: int | None = None
    parse_mode: str | None = 'html'
    pin: bool = False

class BotInter:
    @staticmethod
    async def send_message(model: MsgModel) -> Message:
        if not model.photo:
            sent = await bot.send_message(
                chat_id=model.chat_id,
                text=model.text,
                reply_markup=IMarkup(inline_keyboard=model.markup) if model.markup else model.markup,
                reply_to_message_id=model.reply_to_message_id,
                disable_notification=model.disable_notifications,
                disable_web_page_preview=model.disable_web_page_preview,
                parse_mode=model.parse_mode
            )
            return sent
        else:
            sent = await bot.send_photo(
                chat_id=model.chat_id,
                caption=model.text,
                photo=model.photo if model.photo_type == 'file_id' else FSInputFile(model.photo),
                reply_markup=IMarkup(inline_keyboard=model.markup) if model.markup else model.markup,
                reply_to_message_id=model.reply_to_message_id,
                disable_notification=model.disable_notifications,
                parse_mode=model.parse_mode
            )
            return sent

    @staticmethod
    async def edit_message(model: MsgModel) -> None:
        try:
            if not model.photo:
                await bot.edit_message_text(
                    chat_id=model.chat_id,
                    text=model.text,
                    message_id=model.message_id,
                    reply_markup=IMarkup(inline_keyboard=model.markup) if model.markup else model.markup,
                    disable_web_page_preview=model.disable_web_page_preview,
                    parse_mode=model.parse_mode
                )
            else:
                try:
                    await BotInter.delete_message(model)
                except aiogram.exceptions.TelegramBadRequest:
                    pass
                await BotInter.send_message(model)
        except aiogram.exceptions.TelegramBadRequest:
            try:
                await BotInter.delete_message(model)
            except aiogram.exceptions.TelegramBadRequest:
                pass
            await BotInter.send_message(model)

    @staticmethod
    async def delete_message(model: MsgModel) -> bool:
        try:
            success = await bot.delete_message(chat_id=model.chat_id, message_id=model.message_id)
            return success
        except aiogram.exceptions.TelegramBadRequest:
            return False
