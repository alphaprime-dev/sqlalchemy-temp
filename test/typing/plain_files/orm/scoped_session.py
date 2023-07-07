from ilikesql import inspect
from ilikesql import text
from ilikesql.orm import DeclarativeBase
from ilikesql.orm import Mapped
from ilikesql.orm import mapped_column
from ilikesql.orm import scoped_session
from ilikesql.orm import sessionmaker


class Base(DeclarativeBase):
    pass


class X(Base):
    __tablename__ = "x"
    id: Mapped[int] = mapped_column(primary_key=True)


scoped_session.object_session(object())
scoped_session.identity_key()
scoped_session.close_all()
ss = scoped_session(sessionmaker())
value: bool = "foo" in ss
list(ss)
ss.add(object())
ss.add_all([])
ss.begin()
ss.begin_nested()
ss.close()
ss.commit()
ss.connection()
ss.delete(object())
ss.execute(text("select 1"))
ss.expire(object())
ss.expire_all()
ss.expunge(object())
ss.expunge_all()
ss.flush()
ss.get(object, 1)
b = ss.get_bind()
ss.is_modified(object())
ss.bulk_save_objects([])
ss.bulk_insert_mappings(inspect(X), [])
ss.bulk_update_mappings(inspect(X), [])
ss.merge(object())
q = (ss.query(object),)
ss.refresh(object())
ss.rollback()
ss.scalar(text("select 1"))
ss.bind
ss.dirty
ss.deleted
ss.new
ss.identity_map
ss.is_active
ss.autoflush
ss.no_autoflush
ss.info
