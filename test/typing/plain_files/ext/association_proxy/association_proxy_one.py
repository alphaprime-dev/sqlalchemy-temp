import typing
from typing import Set

from ilikesql import ForeignKey
from ilikesql import Integer
from ilikesql import String
from ilikesql.ext.associationproxy import association_proxy
from ilikesql.ext.associationproxy import AssociationProxy
from ilikesql.orm import DeclarativeBase
from ilikesql.orm import Mapped
from ilikesql.orm import mapped_column
from ilikesql.orm import relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String, nullable=False)

    addresses: Mapped[Set["Address"]] = relationship()

    email_addresses: AssociationProxy[Set[str]] = association_proxy(
        "addresses", "email"
    )


class Address(Base):
    __tablename__ = "address"

    id = mapped_column(Integer, primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    email = mapped_column(String, nullable=False)


u1 = User()

if typing.TYPE_CHECKING:
    # EXPECTED_RE_TYPE: ilikesql.*.associationproxy.AssociationProxyInstance\[builtins.set\*?\[builtins.str\]\]
    reveal_type(User.email_addresses)

    # EXPECTED_RE_TYPE: builtins.set\*?\[builtins.str\]
    reveal_type(u1.email_addresses)
