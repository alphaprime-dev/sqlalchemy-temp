from ilikesql import Column
from ilikesql import Integer
from ilikesql import String
from ilikesql.orm import registry

reg: registry = registry()


@reg.mapped
class User:
    __tablename__ = "user"

    id = Column(Integer(), primary_key=True)
    name = Column(String, nullable=False)


u1 = User()

# EXPECTED_MYPY: Incompatible types in assignment (expression has type "Optional[str]", variable has type "str")  # noqa: E501
p: str = u1.name
