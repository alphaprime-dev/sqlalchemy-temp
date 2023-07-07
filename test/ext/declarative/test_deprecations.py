import ilikesql as sa
from ilikesql import inspect
from ilikesql.ext import declarative as legacy_decl
from ilikesql.testing import eq_
from ilikesql.testing import expect_deprecated_20
from ilikesql.testing import fixtures
from ilikesql.testing import is_false
from ilikesql.testing import is_true


class DeprecatedImportsTest(fixtures.TestBase):
    def _expect_warning(self, name):
        return expect_deprecated_20(
            r"The ``%s\(\)`` function is now available as "
            r"ilikesql.orm.%s\(\)" % (name, name)
        )

    def test_declarative_base(self):
        with self._expect_warning("declarative_base"):
            Base = legacy_decl.declarative_base()

        class Foo(Base):
            __tablename__ = "foo"
            id = sa.Column(sa.Integer, primary_key=True)

        assert inspect(Foo).mapper

    def test_as_declarative(self):
        with self._expect_warning("as_declarative"):

            @legacy_decl.as_declarative()
            class Base:
                pass

        class Foo(Base):
            __tablename__ = "foo"
            id = sa.Column(sa.Integer, primary_key=True)

        assert inspect(Foo).mapper

    def test_has_inherited_table(self, registry):
        @registry.mapped
        class Foo:
            __tablename__ = "foo"
            id = sa.Column(sa.Integer, primary_key=True)

        @registry.mapped
        class Bar(Foo):
            __tablename__ = "bar"
            id = sa.Column(sa.ForeignKey("foo.id"), primary_key=True)

        with self._expect_warning("has_inherited_table"):
            is_true(legacy_decl.has_inherited_table(Bar))

        with self._expect_warning("has_inherited_table"):
            is_false(legacy_decl.has_inherited_table(Foo))

    def test_synonym_for(self, registry):
        with self._expect_warning("synonym_for"):

            @registry.mapped
            class Foo:
                __tablename__ = "foo"
                id = sa.Column(sa.Integer, primary_key=True)

                @legacy_decl.synonym_for("id")
                @property
                def id_prop(self):
                    return self.id

        f1 = Foo(id=5)
        eq_(f1.id_prop, 5)
