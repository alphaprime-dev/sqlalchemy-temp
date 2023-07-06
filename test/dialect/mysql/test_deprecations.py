from ilikesql import select
from ilikesql import table
from ilikesql.dialects.mysql import base as mysql
from ilikesql.testing import AssertsCompiledSQL
from ilikesql.testing import expect_deprecated
from ilikesql.testing import fixtures


class CompileTest(AssertsCompiledSQL, fixtures.TestBase):
    __dialect__ = mysql.dialect()

    def test_distinct_string(self):
        s = select("*").select_from(table("foo"))
        s._distinct = "foo"

        with expect_deprecated(
            "Sending string values for 'distinct' is deprecated in the MySQL "
            "dialect and will be removed in a future release"
        ):
            self.assert_compile(s, "SELECT FOO * FROM foo")
