from typing import Callable

from ilikesql import Column
from ilikesql import Integer
from ilikesql import String
from ilikesql.orm import deferred
from ilikesql.orm import Mapped
from ilikesql.orm.decl_api import declarative_mixin
from ilikesql.orm.decl_api import declared_attr
from ilikesql.orm.interfaces import MapperProperty


def some_other_decorator(fn: Callable[..., None]) -> Callable[..., None]:
    return fn


@declarative_mixin
class HasAMixin:
    x: Mapped[int] = Column(Integer)

    y = Column(String)

    @declared_attr
    def data(cls) -> Column[String]:
        return Column(String)

    @declared_attr
    def data2(cls) -> MapperProperty[str]:
        return deferred(Column(String))

    @some_other_decorator
    def q(cls) -> None:
        return None
