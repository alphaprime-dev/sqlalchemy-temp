from __future__ import annotations

from typing import Any
from typing import Dict

from ilikesql import Column
from ilikesql import insert
from ilikesql import select
from ilikesql.orm import DeclarativeBase
from ilikesql.orm import Mapped
from ilikesql.orm import mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    data: Mapped[str]


# test #9376
d1: dict[str, Any] = {}
stmt1 = insert(User).values(d1)


d2: Dict[str, Any] = {}
stmt2 = insert(User).values(d2)


d3: Dict[Column[str], Any] = {}
stmt3 = insert(User).values(d3)

stmt4 = insert(User).from_select(
    [User.id, "name", User.__table__.c.data],
    select(User.id, User.name, User.data),
)
