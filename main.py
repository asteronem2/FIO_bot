import asyncio
import traceback
from typing import Any, Union, Dict

from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineQuery, MessageReactionUpdated

import core
import utils
import Interfaces

bot = Bot(token=utils.BOT_TOKEN)
disp = Dispatcher()

CallbackQueryClasses = []
InlineQueryClasses = []
NextMessageClasses = []
ReactionClasses = []
TextMessageClasses = []


def init_event_classes():
    from processors import (CallbackQuery, InlineQuery, NextMessage, Reaction, TextMessage)
    import inspect

    list_to_pyfile = (
        (CallbackQueryClasses, CallbackQuery),
        (InlineQueryClasses, InlineQuery),
        (NextMessageClasses, NextMessage),
        (ReactionClasses, Reaction),
        (TextMessageClasses, TextMessage)
    )

    for x in list_to_pyfile:
        for i in inspect.getmembers(x[1], inspect.isclass):
            if i[1].__dict__['__module__'] == x[1].__dict__['__name__']:
                x[0].append(i[1])

async def check_define(event_obj, list_classes, interface_class):
    interface = interface_class(event_obj)
    await interface.async_init()
    for cls in list_classes:
        define = await cls.define(interface)
        if define:
            return cls
    return None

@disp.message()
async def message_handler(message: Message):
    try:
        if message.content_type != 'text':
            return
        elif message.via_bot:
            return

        print(f'\n\n\033[1;36mMESSAGE {message.from_user.username}: \033[1;32m{message.text}\033[0;0m')

        db_user = await core.UserCore.find_one(user_id=message.from_user.id)
        if db_user and db_user.next_message_info:
            defined_cls = await check_define(message, NextMessageClasses, Interfaces.NextMessageInterface)
        else:
            defined_cls = await check_define(message, TextMessageClasses, Interfaces.TextMessageInterface)

        init_cls = defined_cls(message)
        await init_cls.async_init()

        defining = await init_cls.define()
        if defining:
            if type(defining) == dict:
                await init_cls.process(**defining)
            else:
                await init_cls.process()

    except Exception as err:
        traceback.print_exc()

@disp.callback_query()
async def message_handler(callback: CallbackQuery):
    try:
        print(f'\n\n\033[1;36mCALLBACK {callback.from_user.username}: \033[1;32m{callback.data}\033[0;0m')

        defined_cls = await check_define(callback, CallbackQueryClasses, Interfaces.CallbackQueryInterface)

        init_cls = defined_cls(callback)
        await init_cls.async_init()

        defining = await init_cls.define()
        if defining:
            if type(defining) == dict:
                await init_cls.process(**defining)
            else:
                await init_cls.process()
    except Exception as err:
        traceback.print_exc()

@disp.inline_query()
async def message_handler(inline: InlineQuery):
    try:
        defined_cls = await check_define(inline, InlineQueryClasses, Interfaces.InlineQueryInterface)

        init_cls = defined_cls(inline)
        await init_cls.async_init()

        defining = await init_cls.define()
        if defining:
            if type(defining) == dict:
                await init_cls.process(**defining)
            else:
                await init_cls.process()
    except Exception as err:
        traceback.print_exc()

@disp.message_reaction()
async def message_handler(reaction: MessageReactionUpdated):
    try:
        defined_cls = await check_define(reaction, ReactionClasses, Interfaces.ReactionInterface)

        init_cls = defined_cls(reaction)
        await init_cls.async_init()

        defining = await init_cls.define()
        if defining:
            if type(defining) == dict:
                await init_cls.process(**defining)
            else:
                await init_cls.process()
    except Exception as err:
        traceback.print_exc()

async def main():
    init_event_classes()
    print('BOT STARTED')
    await disp.start_polling(
        bot,
        allowed_updates=['message', 'message_reaction', 'inline_query', 'callback_query'],
        handle_signals=False
    )

if __name__ == '__main__':
    asyncio.run(main())