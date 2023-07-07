.. _mysql_toplevel:

MySQL and MariaDB
=================

.. automodule:: ilikesql.dialects.mysql.base

MySQL SQL Constructs
--------------------

.. currentmodule:: ilikesql.dialects.mysql

.. autoclass:: match
    :members:

MySQL Data Types
----------------

As with all ilikesql dialects, all UPPERCASE types that are known to be
valid with MySQL are importable from the top level dialect::

    from ilikesql.dialects.mysql import (
        BIGINT,
        BINARY,
        BIT,
        BLOB,
        BOOLEAN,
        CHAR,
        DATE,
        DATETIME,
        DECIMAL,
        DECIMAL,
        DOUBLE,
        ENUM,
        FLOAT,
        INTEGER,
        LONGBLOB,
        LONGTEXT,
        MEDIUMBLOB,
        MEDIUMINT,
        MEDIUMTEXT,
        NCHAR,
        NUMERIC,
        NVARCHAR,
        REAL,
        SET,
        SMALLINT,
        TEXT,
        TIME,
        TIMESTAMP,
        TINYBLOB,
        TINYINT,
        TINYTEXT,
        VARBINARY,
        VARCHAR,
        YEAR,
    )

Types which are specific to MySQL, or have MySQL-specific
construction arguments, are as follows:

.. note: where :noindex: is used, indicates a type that is not redefined
   in the dialect module, just imported from sqltypes.  this avoids warnings
   in the sphinx build

.. currentmodule:: ilikesql.dialects.mysql

.. autoclass:: BIGINT
    :members: __init__


.. autoclass:: BINARY
    :noindex:
    :members: __init__


.. autoclass:: BIT
    :members: __init__


.. autoclass:: BLOB
    :members: __init__
    :noindex:


.. autoclass:: BOOLEAN
    :members: __init__
    :noindex:


.. autoclass:: CHAR
    :members: __init__


.. autoclass:: DATE
    :members: __init__
    :noindex:


.. autoclass:: DATETIME
    :members: __init__


.. autoclass:: DECIMAL
    :members: __init__


.. autoclass:: DOUBLE
    :members: __init__
    :noindex:

.. autoclass:: ENUM
    :members: __init__


.. autoclass:: FLOAT
    :members: __init__


.. autoclass:: INTEGER
    :members: __init__

.. autoclass:: JSON
    :members:

.. autoclass:: LONGBLOB
    :members: __init__


.. autoclass:: LONGTEXT
    :members: __init__


.. autoclass:: MEDIUMBLOB
    :members: __init__


.. autoclass:: MEDIUMINT
    :members: __init__


.. autoclass:: MEDIUMTEXT
    :members: __init__


.. autoclass:: NCHAR
    :members: __init__


.. autoclass:: NUMERIC
    :members: __init__


.. autoclass:: NVARCHAR
    :members: __init__


.. autoclass:: REAL
    :members: __init__


.. autoclass:: SET
    :members: __init__


.. autoclass:: SMALLINT
    :members: __init__


.. autoclass:: TEXT
    :members: __init__
    :noindex:


.. autoclass:: TIME
    :members: __init__


.. autoclass:: TIMESTAMP
    :members: __init__


.. autoclass:: TINYBLOB
    :members: __init__


.. autoclass:: TINYINT
    :members: __init__


.. autoclass:: TINYTEXT
    :members: __init__


.. autoclass:: VARBINARY
    :members: __init__
    :noindex:


.. autoclass:: VARCHAR
    :members: __init__


.. autoclass:: YEAR
    :members: __init__

MySQL DML Constructs
-------------------------

.. autofunction:: ilikesql.dialects.mysql.insert

.. autoclass:: ilikesql.dialects.mysql.Insert
  :members:



mysqlclient (fork of MySQL-Python)
----------------------------------

.. automodule:: ilikesql.dialects.mysql.mysqldb

PyMySQL
-------

.. automodule:: ilikesql.dialects.mysql.pymysql

MariaDB-Connector
------------------

.. automodule:: ilikesql.dialects.mysql.mariadbconnector

MySQL-Connector
---------------

.. automodule:: ilikesql.dialects.mysql.mysqlconnector

.. _asyncmy:

asyncmy
-------

.. automodule:: ilikesql.dialects.mysql.asyncmy


.. _aiomysql:

aiomysql
--------

.. automodule:: ilikesql.dialects.mysql.aiomysql

cymysql
-------

.. automodule:: ilikesql.dialects.mysql.cymysql

pyodbc
------

.. automodule:: ilikesql.dialects.mysql.pyodbc
