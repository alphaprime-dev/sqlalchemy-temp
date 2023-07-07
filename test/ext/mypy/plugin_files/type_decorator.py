from typing import Any
from typing import Optional

from ilikesql import Column
from ilikesql import Integer
from ilikesql import String
from ilikesql import TypeDecorator
from ilikesql.ext.declarative import declarative_base

Base = declarative_base()


class IntToStr(TypeDecorator[int]):
    impl = String
    cache_ok = True

    def process_bind_param(
        self,
        value: Any,
        dialect: Any,
    ) -> Optional[str]:
        return str(value) if value is not None else value

    def process_result_value(
        self,
        value: Any,
        dialect: Any,
    ) -> Optional[int]:
        return int(value) if value is not None else value

    def copy(self, **kwargs: Any) -> "IntToStr":
        return IntToStr(self.impl.length)


class Thing(Base):
    __tablename__ = "things"

    id: int = Column(Integer, primary_key=True)
    intToStr: int = Column(IntToStr)


t1 = Thing(intToStr=5)

i5: int = t1.intToStr

t1.intToStr = 8
