from __future__ import annotations

from typing import List

from ilikesql import ForeignKey
from ilikesql.ext.associationproxy import association_proxy
from ilikesql.ext.associationproxy import AssociationProxy
from ilikesql.orm import DeclarativeBase
from ilikesql.orm import declared_attr
from ilikesql.orm import Mapped
from ilikesql.orm import mapped_column
from ilikesql.orm import relationship


class Base(DeclarativeBase):
    pass


class Milestone:
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr
    def users(self) -> Mapped[List["User"]]:
        return relationship("User")

    @declared_attr
    def user_ids(self) -> AssociationProxy[List[int]]:
        return association_proxy("users", "id")


class BranchMilestone(Milestone, Base):
    __tablename__ = "branch_milestones"


class User(Base):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey("branch_milestones.id"))


bm = BranchMilestone()

x1 = bm.user_ids

# EXPECTED_TYPE: list[int]
reveal_type(x1)
