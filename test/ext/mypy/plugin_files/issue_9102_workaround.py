from ilikesql import Column
from ilikesql import Integer
from ilikesql.orm import registry


class BackendMeta:
    __abstract__ = True
    mapped_registry: registry = registry()
    metadata = mapped_registry.metadata


reg: registry = BackendMeta.mapped_registry


@reg.mapped
class User:
    __tablename__ = "user"

    id: int = Column(Integer(), primary_key=True)
