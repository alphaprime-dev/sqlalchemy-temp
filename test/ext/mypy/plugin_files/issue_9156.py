from typing import Any
from typing import Type

from ilikesql.sql.elements import ColumnElement
from ilikesql.sql.type_api import TypeEngine

col: ColumnElement[Any]
type_: Type[TypeEngine[Any]]
obj: TypeEngine[Any]

col.cast(type_)
col.cast(obj)
