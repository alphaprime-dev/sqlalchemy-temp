from typing import TYPE_CHECKING

from . import Base
from .user import HasUser

if TYPE_CHECKING:
    from ilikesql import Column  # noqa
    from ilikesql import Integer  # noqa
    from ilikesql.orm import RelationshipProperty  # noqa
    from .user import User  # noqa


class Address(Base, HasUser):
    pass
