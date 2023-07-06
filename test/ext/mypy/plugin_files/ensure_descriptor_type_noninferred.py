from typing import Optional

from ilikesql import Column
from ilikesql import Integer
from ilikesql import String
from ilikesql.orm import Mapped
from ilikesql.orm import registry

reg: registry = registry()


@reg.mapped
class User:
    __tablename__ = "user"

    id = Column(Integer(), primary_key=True)
    name: Mapped[Optional[str]] = Column(String)


u1 = User()

# EXPECTED_MYPY: Incompatible types in assignment (expression has type "Optional[str]", variable has type "Optional[int]") # noqa: E501
p: Optional[int] = u1.name
