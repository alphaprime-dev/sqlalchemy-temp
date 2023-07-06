import operator
from typing import cast

from ilikesql import Column
from ilikesql.testing import eq_
from ilikesql.testing import fixtures


class TestGenerics(fixtures.TestBase):
    def test_traversible_is_generic(self):
        """test #6759"""
        col = Column[int]

        # looked in the source for typing._GenericAlias.
        # col.__origin__ is Column, but it's not public API.
        # __reduce__ could change too but seems good enough for now
        eq_(cast(object, col).__reduce__(), (operator.getitem, (Column, int)))
