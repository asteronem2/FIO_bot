from datetime import datetime
from typing import Literal, List

from sqlalchemy import func, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship
from typing import Annotated

from db import Base

lit_role = Literal['user']
lit_currency = Literal['rub', 'usdt']
lit_pay_method = Literal['bank_money', 'crypto']

id_pk = Annotated[int, mapped_column(primary_key=True)]
now_dtime = Annotated[datetime, mapped_column(default=func.now())]

class User(Base):
    __tablename__ = 'usertable'
    id: Mapped[id_pk]
    user_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str|None]
    first_name: Mapped[str|None]
    created_at: Mapped[now_dtime]
    role: Mapped[lit_role] = mapped_column(default='user')
    next_message_info: Mapped[str|None] = mapped_column(default=None)
    fio: Mapped[str|None]

    def __str__(self):
        return f'USER: id={self.id}, username={self.username or "NULL"}, role={self.role}'
