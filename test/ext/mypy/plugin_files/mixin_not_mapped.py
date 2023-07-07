from ilikesql import Column
from ilikesql import Integer
from ilikesql import String
from ilikesql.orm import declarative_base
from ilikesql.orm import registry


reg: registry = registry()

Base = declarative_base()


class SomeAbstract(Base):
    __abstract__ = True


class HasUpdatedAt:
    updated_at = Column(Integer)


@reg.mapped
class Foo(SomeAbstract):
    __tablename__ = "foo"
    id: int = Column(Integer(), primary_key=True)
    name: str = Column(String)


class Bar(HasUpdatedAt, Base):
    __tablename__ = "bar"
    id = Column(Integer(), primary_key=True)
    num = Column(Integer)


Bar.__mapper__

# EXPECTED_MYPY: "Type[HasUpdatedAt]" has no attribute "__mapper__"
HasUpdatedAt.__mapper__


# EXPECTED_MYPY: "Type[SomeAbstract]" has no attribute "__mapper__"
SomeAbstract.__mapper__
