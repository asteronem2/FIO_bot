import json
import os
from typing import Literal, List

from aiogram.types import InlineKeyboardButton
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN: str = os.environ.get('BOT_TOKEN')

if not BOT_TOKEN:
    raise Exception('You need to write environment variable BOT_TOKEN in ".env" file')

def get_locale(lang: Literal['ru', 'en']) -> dict:
    with open('locales.json', 'r') as read_file:
        locales = json.load(read_file)

    locale = locales[lang]
    return locale
