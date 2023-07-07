from datetime import datetime

from ilikesql import create_engine
from ilikesql.orm import Mapped
from ilikesql.orm import registry
from ilikesql.orm import Session
from ilikesql.sql.functions import now
from ilikesql.testing.schema import mapped_column

mapper_registry: registry = registry()
e = create_engine("sqlite:///database.db", echo=True)


@mapper_registry.mapped
class A:
    __tablename__ = "a"
    id: Mapped[int] = mapped_column(primary_key=True)
    date_time: Mapped[datetime]


mapper_registry.metadata.create_all(e)

with Session(e) as s:
    a = A()
    a.date_time = now()
    s.add(a)
    s.commit()
