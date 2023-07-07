from typing import TYPE_CHECKING

from ilikesql import Column
from ilikesql import Integer
from ilikesql.orm import as_declarative
from ilikesql.orm import declared_attr
from ilikesql.orm import Mapped
from .address import Address
from .user import User

if TYPE_CHECKING:
    from ilikesql.orm.decl_api import DeclarativeMeta


@as_declarative()
class Base:
    @declared_attr
    def __tablename__(self) -> Mapped[str]:
        return self.__name__.lower()

    id = Column(Integer, primary_key=True)


__all__ = ["User", "Address"]
