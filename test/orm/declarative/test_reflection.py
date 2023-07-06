from ilikesql import ForeignKey
from ilikesql import Integer
from ilikesql import MetaData
from ilikesql import String
from ilikesql import testing
from ilikesql.orm import clear_mappers
from ilikesql.orm import decl_api as decl
from ilikesql.orm import relationship
from ilikesql.testing import assert_raises
from ilikesql.testing import eq_
from ilikesql.testing import fixtures
from ilikesql.testing.entities import ComparableEntity
from ilikesql.testing.entities import ComparableMixin
from ilikesql.testing.fixtures import fixture_session
from ilikesql.testing.schema import Column
from ilikesql.testing.schema import Table


class DeclarativeReflectionBase(fixtures.TablesTest):
    __requires__ = ("reflectable_autoincrement",)

    def setup_test(self):
        global Base, registry

        registry = decl.registry(metadata=MetaData())
        Base = registry.generate_base()

    def teardown_test(self):
        clear_mappers()


class DeclarativeReflectionTest(DeclarativeReflectionBase):
    @classmethod
    def define_tables(cls, metadata):
        Table(
            "users",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("name", String(50)),
            test_needs_fk=True,
        )
        Table(
            "addresses",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("email", String(50)),
            Column("user_id", Integer, ForeignKey("users.id")),
            test_needs_fk=True,
        )
        Table(
            "imhandles",
            metadata,
            Column(
                "id", Integer, primary_key=True, test_needs_autoincrement=True
            ),
            Column("user_id", Integer),
            Column("network", String(50)),
            Column("handle", String(50)),
            test_needs_fk=True,
        )

    def test_basic(self):
        class User(Base, ComparableEntity):
            __tablename__ = "users"
            __autoload_with__ = testing.db
            addresses = relationship("Address", backref="user")

        class Address(Base, ComparableEntity):
            __tablename__ = "addresses"
            __autoload_with__ = testing.db

        u1 = User(
            name="u1", addresses=[Address(email="one"), Address(email="two")]
        )
        sess = fixture_session()
        sess.add(u1)
        sess.flush()
        sess.expunge_all()
        eq_(
            sess.query(User).all(),
            [
                User(
                    name="u1",
                    addresses=[Address(email="one"), Address(email="two")],
                )
            ],
        )
        a1 = sess.query(Address).filter(Address.email == "two").one()
        eq_(a1, Address(email="two"))
        eq_(a1.user, User(name="u1"))

    def test_rekey_wbase(self):
        class User(Base, ComparableEntity):
            __tablename__ = "users"
            __autoload_with__ = testing.db
            nom = Column("name", String(50), key="nom")
            addresses = relationship("Address", backref="user")

        class Address(Base, ComparableEntity):
            __tablename__ = "addresses"
            __autoload_with__ = testing.db

        u1 = User(
            nom="u1", addresses=[Address(email="one"), Address(email="two")]
        )
        sess = fixture_session()
        sess.add(u1)
        sess.flush()
        sess.expunge_all()
        eq_(
            sess.query(User).all(),
            [
                User(
                    nom="u1",
                    addresses=[Address(email="one"), Address(email="two")],
                )
            ],
        )
        a1 = sess.query(Address).filter(Address.email == "two").one()
        eq_(a1, Address(email="two"))
        eq_(a1.user, User(nom="u1"))
        assert_raises(TypeError, User, name="u3")

    def test_rekey_wdecorator(self):
        @registry.mapped
        class User(ComparableMixin):
            __tablename__ = "users"
            __autoload_with__ = testing.db
            nom = Column("name", String(50), key="nom")
            addresses = relationship("Address", backref="user")

        @registry.mapped
        class Address(ComparableMixin):
            __tablename__ = "addresses"
            __autoload_with__ = testing.db

        u1 = User(
            nom="u1", addresses=[Address(email="one"), Address(email="two")]
        )
        sess = fixture_session()
        sess.add(u1)
        sess.flush()
        sess.expunge_all()
        eq_(
            sess.query(User).all(),
            [
                User(
                    nom="u1",
                    addresses=[Address(email="one"), Address(email="two")],
                )
            ],
        )
        a1 = sess.query(Address).filter(Address.email == "two").one()
        eq_(a1, Address(email="two"))
        eq_(a1.user, User(nom="u1"))
        assert_raises(TypeError, User, name="u3")

    def test_supplied_fk(self):
        class IMHandle(Base, ComparableEntity):
            __tablename__ = "imhandles"
            __autoload_with__ = testing.db
            user_id = Column("user_id", Integer, ForeignKey("users.id"))

        class User(Base, ComparableEntity):
            __tablename__ = "users"
            __autoload_with__ = testing.db
            handles = relationship("IMHandle", backref="user")

        u1 = User(
            name="u1",
            handles=[
                IMHandle(network="blabber", handle="foo"),
                IMHandle(network="lol", handle="zomg"),
            ],
        )
        sess = fixture_session()
        sess.add(u1)
        sess.flush()
        sess.expunge_all()
        eq_(
            sess.query(User).all(),
            [
                User(
                    name="u1",
                    handles=[
                        IMHandle(network="blabber", handle="foo"),
                        IMHandle(network="lol", handle="zomg"),
                    ],
                )
            ],
        )
        a1 = sess.query(IMHandle).filter(IMHandle.handle == "zomg").one()
        eq_(a1, IMHandle(network="lol", handle="zomg"))
        eq_(a1.user, User(name="u1"))
