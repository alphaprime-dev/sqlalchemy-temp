"""
test inspect()

however this is not really working

"""
from typing import Any
from typing import Optional

from ilikesql import Column
from ilikesql import create_engine
from ilikesql import inspect
from ilikesql import Integer
from ilikesql import String
from ilikesql.engine.reflection import Inspector
from ilikesql.orm import DeclarativeBase
from ilikesql.orm import Mapper


class Base(DeclarativeBase):
    pass


class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)
    data = Column(String)


a1 = A(data="d")

e = create_engine("sqlite://")

# TODO: I can't get these to work, pylance and mypy both don't want
# to accommodate for different types for the first argument

t: Optional[Any] = inspect(a1)

m: Mapper[Any] = inspect(A)

inspect(e).get_table_names()

i: Inspector = inspect(e)


with e.connect() as conn:
    inspect(conn).get_table_names()
