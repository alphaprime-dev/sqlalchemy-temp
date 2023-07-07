from typing import List
from typing import TYPE_CHECKING

from ilikesql import Column
from ilikesql import ForeignKey
from ilikesql import Integer
from ilikesql import String
from ilikesql.orm import Mapped
from ilikesql.orm import relationship
from ilikesql.orm.decl_api import declared_attr
from ilikesql.orm.relationships import RelationshipProperty
from . import Base

if TYPE_CHECKING:
    from .address import Address


class User(Base):
    name = Column(String)

    othername = Column(String)

    addresses: Mapped[List["Address"]] = relationship(
        "Address", back_populates="user"
    )


class HasUser:
    @declared_attr
    def user_id(self) -> "Column[Integer]":
        return Column(
            Integer,
            ForeignKey(User.id, ondelete="CASCADE", onupdate="CASCADE"),
            nullable=False,
        )

    @declared_attr
    def user(self) -> RelationshipProperty[User]:
        return relationship(User)
