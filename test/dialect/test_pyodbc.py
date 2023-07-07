from ilikesql.connectors import pyodbc
from ilikesql.testing import eq_
from ilikesql.testing import fixtures


class PyODBCTest(fixtures.TestBase):
    def test_pyodbc_version(self):
        connector = pyodbc.PyODBCConnector()
        for vers, expected in [
            ("2.1.8", (2, 1, 8)),
            ("py3-3.0.1-beta4", (3, 0, 1, "beta4")),
            ("10.15.17", (10, 15, 17)),
            ("crap.crap.crap", ()),
        ]:
            eq_(connector._parse_dbapi_version(vers), expected)
