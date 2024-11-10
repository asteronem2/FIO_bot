import os
import re
from typing import NoReturn

from aiogram.types import InlineKeyboardButton as IButton, FSInputFile
from openpyxl import Workbook

import utils
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


class GetTable(TextMessageInterface):
    async def define(self) -> NoReturn | dict:
        if self.user.id == utils.ADMIN_ID:
            rres = re.fullmatch(r'таблица', self.text_low)
            if rres:
                return True

    async def process(self, *args, **kwargs) -> None:
        file_name = 'users_table.xlsx'

        wb = Workbook()
        ws = wb.active
        ws.title = 'Выгрузка базы данных'

        res = await self.user_core.find_all()

        ws.column_dimensions['A'].width = 3
        ws.column_dimensions['B'].width = 13
        ws.column_dimensions['C'].width = 20
        ws.column_dimensions['D'].width = 20
        ws.column_dimensions['E'].width = 30

        ws.cell(row=1, column=1, value='ID')
        ws.cell(row=1, column=2, value='USER_ID')
        ws.cell(row=1, column=3, value='USERNAME')
        ws.cell(row=1, column=4, value='FIRST_NAME')
        ws.cell(row=1, column=5, value='ФИО')

        row = 2

        for i in res:
            ws.cell(row=row, column=1, value=i.id)
            ws.cell(row=row, column=2, value=i.user_id)
            ws.cell(row=row, column=3, value=i.username or ' ')
            ws.cell(row=row, column=4, value=i.first_name or ' ')
            ws.cell(row=row, column=5, value=i.fio or ' ')
            row += 1

        wb.save(file_name)

        await self.bot.bot.send_document(self.chat.id, FSInputFile(file_name))
        os.remove(file_name)

class Distribution(TextMessageInterface):
    async def define(self) -> NoReturn | dict:
        if self.user.id == utils.ADMIN_ID:
            rres = re.fullmatch(r'рассылка', self.text_low)
            if rres:
                return True

    async def process(self, *args, **kwargs) -> None:
        await self.bot.send_message(MsgModel(
            chat_id=self.user.id,
            text=self.locale['DistributionTxt']
        ))
        await self.user_core.update({'id': self.db_user.id}, next_message_info='distribution')