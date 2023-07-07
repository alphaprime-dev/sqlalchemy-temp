from __future__ import annotations

import typing

from ilikesql import ForeignKey
from ilikesql import select
from ilikesql.orm import DeclarativeBase
from ilikesql.orm import Mapped
from ilikesql.orm import mapped_column
from ilikesql.orm import relationship
from ilikesql.orm import Session
from ilikesql.orm import WriteOnlyMapped


class Base(DeclarativeBase):
    pass


class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    email_address: Mapped[str]


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    addresses: WriteOnlyMapped[Address] = relationship()


with Session() as session:
    u = User()
    session.add(u)
    session.commit()

    if typing.TYPE_CHECKING:
        # EXPECTED_TYPE: WriteOnlyCollection[Address]
        reveal_type(u.addresses)

    address = session.scalars(
        u.addresses.select().filter(Address.email_address.like("xyz"))
    ).one()

    if typing.TYPE_CHECKING:
        # EXPECTED_TYPE: Address
        reveal_type(address)

    u.addresses.add(Address())
    u.addresses.add_all([Address(), Address()])

    # this should emit an error, because __iter__ is NoReturn,
    # however typing tools don't pick up on that right now
    current_addresses = list(u.addresses)

    u.addresses.add(Address())

    session.commit()

    # test #9985
    stmt = select(User).join(User.addresses)
