import uuid

from ilikesql import Column
from ilikesql import String
from ilikesql.orm import declarative_base

Base = declarative_base()


class MyClass(Base):
    id = Column(String, default=lambda: uuid.uuid4(), primary_key=True)
