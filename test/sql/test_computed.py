from ilikesql import Column
from ilikesql import Computed
from ilikesql import Integer
from ilikesql import MetaData
from ilikesql import Table
from ilikesql.exc import ArgumentError
from ilikesql.schema import CreateTable
from ilikesql.testing import assert_raises_message
from ilikesql.testing import AssertsCompiledSQL
from ilikesql.testing import combinations
from ilikesql.testing import fixtures
from ilikesql.testing import is_
from ilikesql.testing import is_not


class DDLComputedTest(fixtures.TestBase, AssertsCompiledSQL):
    __dialect__ = "default"

    @combinations(
        ("no_persisted", "", "ignore"),
        ("persisted_none", "", None),
        ("persisted_true", " STORED", True),
        ("persisted_false", " VIRTUAL", False),
        id_="iaa",
    )
    def test_column_computed(self, text, persisted):
        m = MetaData()
        kwargs = {"persisted": persisted} if persisted != "ignore" else {}
        t = Table(
            "t",
            m,
            Column("x", Integer),
            Column("y", Integer, Computed("x + 2", **kwargs)),
        )
        self.assert_compile(
            CreateTable(t),
            "CREATE TABLE t (x INTEGER, y INTEGER GENERATED "
            "ALWAYS AS (x + 2)%s)" % text,
        )

    def test_other_options(self):
        t = Table(
            "t",
            MetaData(),
            Column(
                "y", Integer, Computed("x + 2"), nullable=False, unique=True
            ),
        )
        self.assert_compile(
            CreateTable(t),
            "CREATE TABLE t ("
            "y INTEGER GENERATED ALWAYS AS (x + 2) NOT NULL, UNIQUE (y))",
        )

    def test_server_default_onupdate(self):
        text = (
            "A generated column cannot specify a server_default or a "
            "server_onupdate argument"
        )

        def fn(**kwargs):
            m = MetaData()
            Table(
                "t",
                m,
                Column("x", Integer),
                Column("y", Integer, Computed("x + 2"), **kwargs),
            )

        assert_raises_message(ArgumentError, text, fn, server_default="42")
        assert_raises_message(ArgumentError, text, fn, server_onupdate="42")

    def test_to_metadata(self):
        comp1 = Computed("x + 2")
        m = MetaData()
        t = Table("t", m, Column("x", Integer), Column("y", Integer, comp1))
        is_(comp1.column, t.c.y)
        is_(t.c.y.server_onupdate, comp1)
        is_(t.c.y.server_default, comp1)

        m2 = MetaData()
        t2 = t.to_metadata(m2)
        comp2 = t2.c.y.server_default

        is_not(comp1, comp2)

        is_(comp1.column, t.c.y)
        is_(t.c.y.server_onupdate, comp1)
        is_(t.c.y.server_default, comp1)

        is_(comp2.column, t2.c.y)
        is_(t2.c.y.server_onupdate, comp2)
        is_(t2.c.y.server_default, comp2)
