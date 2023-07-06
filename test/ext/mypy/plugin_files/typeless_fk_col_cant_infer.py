from ilikesql import Column
from ilikesql import ForeignKey
from ilikesql import Integer
from ilikesql import String
from ilikesql.orm import registry

reg: registry = registry()


@reg.mapped
class User:
    __tablename__ = "user"

    id = Column(Integer(), primary_key=True)
    name = Column(String)


@reg.mapped
class Address:
    __tablename__ = "address"

    id = Column(Integer, primary_key=True)
    # EXPECTED: Can't infer type from ORM mapped expression assigned to attribute 'user_id';  # noqa: E501
    user_id = Column(ForeignKey("user.id"))
    email_address = Column(String)
