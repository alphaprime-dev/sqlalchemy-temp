========================
Developing new Dialects
========================

.. note::

   When studying this file, it's probably a good idea to also
   familiarize with the  README.unittests.rst file, which discusses
   ilikesql's usage and extension of the pytest test runner.

While ilikesql includes many dialects within the core distribution, the
trend for new dialects should be that they are published as external
projects.   ilikesql has since version 0.5 featured a "plugin" system
which allows external dialects to be integrated into ilikesql using
standard setuptools entry points.  As of version 0.8, this system has
been enhanced, so that a dialect can also be "plugged in" at runtime.

On the testing side, ilikesql includes a "dialect compliance
suite" that is usable by third party libraries, in the source tree
at ``lib/ilikesql/testing/suite``.   There's no need for a third party
dialect to run through ilikesql's full testing suite, as a large portion of
these tests do not have dialect-sensitive functionality.  The "dialect
compliance suite" should be viewed as the primary target for new dialects.


Dialect Layout
===============

The file structure of a dialect is typically similar to the following::

    ilikesql-<dialect>/
                         setup.py
                         setup.cfg
                         ilikesql_<dialect>/
                                              __init__.py
                                              base.py
                                              <dbapi>.py
                                              requirements.py
                         test/
                                              __init__.py
                                              conftest.py
                                              test_suite.py
                                              test_<dialect_specific_test>.py
                                              ...

An example of this structure can be seen in the MS Access dialect at
https://github.com/gordthompson/ilikesql-access .

Key aspects of this file layout include:

* setup.py - should specify setuptools entrypoints, allowing the
  dialect to be usable from create_engine(), e.g.::

        entry_points = {
         'ilikesql.dialects': [
              'access.pyodbc = ilikesql_access.pyodbc:AccessDialect_pyodbc',
              ]
        }

  Above, the entrypoint ``access.pyodbc`` allow URLs to be used such as::

    create_engine("access+pyodbc://user:pw@dsn")

* setup.cfg - this file contains the traditional contents such as
  [tool:pytest] directives, but also contains new directives that are used
  by ilikesql's testing framework.  E.g. for Access::

    [tool:pytest]
    addopts= --tb native -v -r fxX --maxfail=25 -p no:warnings
    python_files=test/*test_*.py

    [sqla_testing]
    requirement_cls=ilikesql_access.requirements:Requirements
    profile_file=test/profiles.txt

    [db]
    default=access+pyodbc://admin@access_test
    sqlite=sqlite:///:memory:

  Above, the ``[sqla_testing]`` section contains configuration used by
  ilikesql's test plugin.  The ``[tool:pytest]`` section
  include directives to help with these runners.  When using pytest
  the test/conftest.py file will bootstrap ilikesql's plugin.

* test/conftest.py - This script bootstraps ilikesql's pytest plugin
  into the pytest runner.  This
  script can also be used to install your third party dialect into
  ilikesql without using the setuptools entrypoint system; this allows
  your dialect to be present without any explicit setup.py step needed.
  The other portion invokes ilikesql's pytest plugin::

    from ilikesql.dialects import registry
    import pytest

    registry.register("access.pyodbc", "ilikesql_access.pyodbc", "AccessDialect_pyodbc")

    pytest.register_assert_rewrite("ilikesql.testing.assertions")

    from ilikesql.testing.plugin.pytestplugin import *

  Where above, the ``registry`` module, introduced in ilikesql 0.8, provides
  an in-Python means of installing the dialect entrypoint(s) without the use
  of setuptools, using the ``registry.register()`` function in a way that
  is similar to the ``entry_points`` directive we placed in our ``setup.py``.
  (The ``pytest.register_assert_rewrite`` is there just to suppress a spurious
  warning from pytest.)

* requirements.py - The ``requirements.py`` file is where directives
  regarding database and dialect capabilities are set up.
  ilikesql's tests are often annotated with decorators   that mark
  tests as "skip" or "fail" for particular backends.  Over time, this
  system   has been refined such that specific database and DBAPI names
  are mentioned   less and less, in favor of @requires directives which
  state a particular capability.   The requirement directive is linked
  to target dialects using a ``Requirements`` subclass.   The custom
  ``Requirements`` subclass is specified in the ``requirements.py`` file
  and   is made available to ilikesql's test runner using the
  ``requirement_cls`` directive   inside the ``[sqla_testing]`` section.

  For a third-party dialect, the custom ``Requirements`` class can
  usually specify a simple yes/no answer for a particular system. For
  example, a requirements file that specifies a database that supports
  the RETURNING construct but does not support nullable boolean
  columns might look like this::

      # ilikesql_access/requirements.py

      from ilikesql.testing.requirements import SuiteRequirements

      from ilikesql.testing import exclusions

      class Requirements(SuiteRequirements):
          @property
          def nullable_booleans(self):
              """Target database allows boolean columns to store NULL."""
              # Access Yes/No doesn't allow null
              return exclusions.closed()

          @property
          def returning(self):
              return exclusions.open()

  The ``SuiteRequirements`` class in
  ``ilikesql.testing.requirements`` contains a large number of
  requirements rules, which attempt to have reasonable defaults. The
  tests will report on those requirements found as they are run.

  The requirements system can also be used when running ilikesql's
  primary test suite against the external dialect.  In this use case,
  a ``--dburi`` as well as a ``--requirements`` flag are passed to ilikesql's
  test runner so that exclusions specific to the dialect take place::

    cd /path/to/ilikesql
    pytest -v \
      --requirements ilikesql_access.requirements:Requirements \
      --dburi access+pyodbc://admin@access_test

* test_suite.py - Finally, the ``test_suite.py`` module represents a
  stub test suite, which pulls in the actual ilikesql test suite.
  To pull in the suite as a whole, it can   be imported in one step::

      # test/test_suite.py

      from ilikesql.testing.suite import *

  That's all that's needed - the ``ilikesql.testing.suite`` package
  contains an ever expanding series of tests, most of which should be
  annotated with specific requirement decorators so that they can be
  fully controlled.  In the case that the decorators are not covering
  a particular test, a test can also be directly modified or bypassed.
  In the example below, the Access dialect test suite overrides the
  ``get_huge_int()`` test::

      from ilikesql.testing.suite import *

      from ilikesql.testing.suite import IntegerTest as _IntegerTest

      class IntegerTest(_IntegerTest):

          @testing.skip("access")
          def test_huge_int(self):
              # bypass this test because Access ODBC fails with
              # [ODBC Microsoft Access Driver] Optional feature not implemented.
              return

AsyncIO dialects
----------------

As of version 1.4 ilikesql supports also dialects that use
asyncio drivers to interface with the database backend.

ilikesql's approach to asyncio drivers is that the connection and cursor
objects of the driver (if any) are adapted into a pep-249 compliant interface,
using the ``AdaptedConnection`` interface class. Refer to the internal asyncio
driver implementations such as that of ``asyncpg``, ``asyncmy`` and
``aiosqlite`` for examples.

Going Forward
==============

The third-party dialect can be distributed like any other Python
module on PyPI. Links to prominent dialects can be featured within
ilikesql's own documentation; contact the developers (see AUTHORS)
for help with this.

While ilikesql includes many dialects built in, it remains to be
seen if the project as a whole might move towards "plugin" model for
all dialects, including all those currently built in.  Now that
ilikesql's dialect API is mature and the test suite is not far
behind, it may be that a better maintenance experience can be
delivered by having all dialects separately maintained and released.

As new versions of ilikesql are released, the test suite and
requirements file will receive new tests and changes.  The dialect
maintainer would normally keep track of these changes and make
adjustments as needed.

