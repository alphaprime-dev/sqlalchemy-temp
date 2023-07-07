from typing import Optional
from typing import Set

from ilikesql import Column
from ilikesql import ForeignKey
from ilikesql import Integer
from ilikesql import String
from ilikesql.ext.declarative import declarative_base
from ilikesql.orm import relationship

Base = declarative_base()


class B(Base):
    __tablename__ = "b"
    id = Column(Integer, primary_key=True)
    a_id: int = Column(ForeignKey("a.id"))
    data = Column(String)
    a: Optional["A"] = relationship("A", back_populates="bs")


class A(Base):
    __tablename__ = "a"

    id = Column(Integer, primary_key=True)
    data = Column(String)

    bs: Set[B] = relationship(B, uselist=True, back_populates="a")

    # EXPECTED: Left hand assignment 'another_bs: "Set[B]"' not compatible with ORM mapped expression of type "Mapped[B]" # noqa
    another_bs: Set[B] = relationship(B, viewonly=True)


# EXPECTED_MYPY: Argument "a" to "B" has incompatible type "str"; expected "Optional[A]" # noqa
b1 = B(a="not an a")
