from typing import List
from typing import Optional

from ilikesql import Column
from ilikesql import Integer
from ilikesql import String
from ilikesql.ext.declarative import as_declarative
from ilikesql.orm import Mapped
from ilikesql.orm import relationship
from ilikesql.sql.schema import ForeignKey


@as_declarative()
class Base:
    updated_at = Column(Integer)


class Foo(Base):
    __tablename__ = "foo"
    id: int = Column(Integer(), primary_key=True)
    name: Mapped[str] = Column(String)

    bar: List["Bar"] = relationship("Bar")


class Bar(Base):
    __tablename__ = "bar"
    id: int = Column(Integer(), primary_key=True)
    foo_id: int = Column(ForeignKey("foo.id"))

    foo: Optional[Foo] = relationship(Foo)


f1 = Foo()

val: int = f1.id

p: str = f1.name

Foo.id.property

f2 = Foo(name="some name", updated_at=5)
