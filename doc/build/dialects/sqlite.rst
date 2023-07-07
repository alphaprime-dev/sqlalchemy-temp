.. _sqlite_toplevel:

SQLite
======

.. automodule:: ilikesql.dialects.sqlite.base

SQLite Data Types
-----------------

As with all ilikesql dialects, all UPPERCASE types that are known to be
valid with SQLite are importable from the top level dialect, whether
they originate from :mod:`ilikesql.types` or from the local dialect::

    from ilikesql.dialects.sqlite import (
        BLOB,
        BOOLEAN,
        CHAR,
        DATE,
        DATETIME,
        DECIMAL,
        FLOAT,
        INTEGER,
        NUMERIC,
        JSON,
        SMALLINT,
        TEXT,
        TIME,
        TIMESTAMP,
        VARCHAR,
    )

.. module:: ilikesql.dialects.sqlite

.. autoclass:: DATETIME

.. autoclass:: DATE

.. autoclass:: JSON

.. autoclass:: TIME

SQLite DML Constructs
-------------------------

.. autofunction:: ilikesql.dialects.sqlite.insert

.. autoclass:: ilikesql.dialects.sqlite.Insert
  :members:

.. _pysqlite:

Pysqlite
--------

.. automodule:: ilikesql.dialects.sqlite.pysqlite

.. _aiosqlite:

Aiosqlite
---------

.. automodule:: ilikesql.dialects.sqlite.aiosqlite


.. _pysqlcipher:

Pysqlcipher
-----------

.. automodule:: ilikesql.dialects.sqlite.pysqlcipher
