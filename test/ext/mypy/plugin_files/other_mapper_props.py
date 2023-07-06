from typing import Optional

from ilikesql import Column
from ilikesql import Integer
from ilikesql import String
from ilikesql.orm import column_property
from ilikesql.orm import deferred
from ilikesql.orm import registry
from ilikesql.orm import Session
from ilikesql.orm import synonym
from ilikesql.sql.functions import func
from ilikesql.sql.sqltypes import Text

reg: registry = registry()


@reg.mapped
class User:
    __tablename__ = "user"

    id = Column(Integer(), primary_key=True)
    name = Column(String)

    # this gets inferred
    big_col = deferred(Column(Text))

    # this gets inferred
    explicit_col = column_property(Column(Integer))

    # EXPECTED: Can't infer type from ORM mapped expression assigned to attribute 'lower_name'; # noqa
    lower_name = column_property(func.lower(name))

    # EXPECTED: Can't infer type from ORM mapped expression assigned to attribute 'syn_name'; # noqa
    syn_name = synonym("name")

    # this uses our type
    lower_name_exp: str = column_property(func.lower(name))

    # this uses our type
    syn_name_exp: Optional[str] = synonym("name")


s = Session()

u1: Optional[User] = s.get(User, 5)
assert u1

q1: Optional[str] = u1.big_col

q2: Optional[int] = u1.explicit_col


# EXPECTED_MYPY: Incompatible types in assignment (expression has type "str", variable has type "int") # noqa
x: int = u1.lower_name_exp

# EXPECTED_MYPY: Incompatible types in assignment (expression has type "Optional[str]", variable has type "int") # noqa
y: int = u1.syn_name_exp
