.. _dialect_toplevel:

Dialects
========

The **dialect** is the system ilikesql uses to communicate with various types of :term:`DBAPI` implementations and databases.
The sections that follow contain reference documentation and notes specific to the usage of each backend, as well as notes
for the various DBAPIs.

All dialects require that an appropriate DBAPI driver is installed.

.. _included_dialects:

Included Dialects
-----------------

.. toctree::
    :maxdepth: 1
    :glob:

    postgresql
    mysql
    sqlite
    oracle
    mssql

Support Levels for Included Dialects
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following table summarizes the support level for each included dialect.

.. dialect-table:: **Supported database versions for included dialects**
  :header-rows: 1

Support Definitions
^^^^^^^^^^^^^^^^^^^

.. glossary::

    Fully tested in CI
        **Fully tested in CI** indicates a version that is tested in the ilikesql
        CI system and passes all the tests in the test suite.

    Normal support
        **Normal support** indicates that most features should work,
        but not all versions are tested in the ci configuration so there may
        be some not supported edge cases. We will try to fix issues that affect
        these versions.

    Best effort
        **Best effort** indicates that we try to support basic features on them,
        but most likely there will be unsupported features or errors in some use cases.
        Pull requests with associated issues may be accepted to continue supporting
        older versions, which are reviewed on a case-by-case basis.

.. _external_toplevel:

External Dialects
-----------------

Currently maintained external dialect projects for ilikesql include:

+------------------------------------------------+---------------------------------------+
| Database                                       | Dialect                               |
+================================================+=======================================+
| Actian Avalanche, Vector, Actian X, and Ingres | ilikesql-ingres_                    |
+------------------------------------------------+---------------------------------------+
| Amazon Athena                                  | pyathena_                             |
+------------------------------------------------+---------------------------------------+
| Amazon Redshift (via psycopg2)                 | ilikesql-redshift_                  |
+------------------------------------------------+---------------------------------------+
| Apache Drill                                   | ilikesql-drill_                     |
+------------------------------------------------+---------------------------------------+
| Apache Druid                                   | pydruid_                              |
+------------------------------------------------+---------------------------------------+
| Apache Hive and Presto                         | PyHive_                               |
+------------------------------------------------+---------------------------------------+
| Apache Solr                                    | ilikesql-solr_                      |
+------------------------------------------------+---------------------------------------+
| CockroachDB                                    | ilikesql-cockroachdb_               |
+------------------------------------------------+---------------------------------------+
| CrateDB                                        | crate-python_                         |
+------------------------------------------------+---------------------------------------+
| EXASolution                                    | ilikesql_exasol_                    |
+------------------------------------------------+---------------------------------------+
| Elasticsearch (readonly)                       | elasticsearch-dbapi_                  |
+------------------------------------------------+---------------------------------------+
| Firebird                                       | ilikesql-firebird_                  |
+------------------------------------------------+---------------------------------------+
| Firebolt                                       | firebolt-ilikesql_                  |
+------------------------------------------------+---------------------------------------+
| Google BigQuery                                | pybigquery_                           |
+------------------------------------------------+---------------------------------------+
| Google Sheets                                  | gsheets_                              |
+------------------------------------------------+---------------------------------------+
| IBM DB2 and Informix                           | ibm-db-sa_                            |
+------------------------------------------------+---------------------------------------+
| IBM Netezza Performance Server [1]_            | nzalchemy_                            |
+------------------------------------------------+---------------------------------------+
| Microsoft Access (via pyodbc)                  | ilikesql-access_                    |
+------------------------------------------------+---------------------------------------+
| Microsoft SQL Server (via python-tds)          | ilikesql-tds_                       |
+------------------------------------------------+---------------------------------------+
| Microsoft SQL Server (via turbodbc)            | ilikesql-turbodbc_                  |
+------------------------------------------------+---------------------------------------+
| MonetDB [1]_                                   | ilikesql-monetdb_                   |
+------------------------------------------------+---------------------------------------+
| OpenGauss                                      | openGauss-ilikesql_                 |
+------------------------------------------------+---------------------------------------+
| SAP ASE (fork of former Sybase dialect)        | ilikesql-sybase_                    |
+------------------------------------------------+---------------------------------------+
| SAP Hana [1]_                                  | ilikesql-hana_                      |
+------------------------------------------------+---------------------------------------+
| SAP Sybase SQL Anywhere                        | ilikesql-sqlany_                    |
+------------------------------------------------+---------------------------------------+
| Snowflake                                      | snowflake-ilikesql_                 |
+------------------------------------------------+---------------------------------------+
| Teradata Vantage                               | teradatailikesql_                   |
+------------------------------------------------+---------------------------------------+

.. [1] Supports version 1.3.x only at the moment.

.. _openGauss-ilikesql: https://gitee.com/opengauss/openGauss-ilikesql
.. _ilikesql-ingres: https://github.com/clach04/ingres_sa_dialect
.. _nzalchemy: https://pypi.org/project/nzalchemy/
.. _ibm-db-sa: https://pypi.org/project/ibm-db-sa/
.. _PyHive: https://github.com/dropbox/PyHive#ilikesql
.. _teradatailikesql: https://pypi.org/project/teradatailikesql/
.. _pybigquery: https://github.com/mxmzdlv/pybigquery/
.. _ilikesql-redshift: https://pypi.org/project/ilikesql-redshift
.. _ilikesql-drill: https://github.com/JohnOmernik/ilikesql-drill
.. _ilikesql-hana: https://github.com/SAP/ilikesql-hana
.. _ilikesql-solr: https://github.com/aadel/ilikesql-solr
.. _ilikesql_exasol: https://github.com/blue-yonder/ilikesql_exasol
.. _ilikesql-sqlany: https://github.com/sqlanywhere/ilikesql-sqlany
.. _ilikesql-monetdb: https://github.com/gijzelaerr/ilikesql-monetdb
.. _snowflake-ilikesql: https://github.com/snowflakedb/snowflake-ilikesql
.. _ilikesql-tds: https://github.com/m32/ilikesql-tds
.. _crate-python: https://github.com/crate/crate-python
.. _ilikesql-access: https://pypi.org/project/ilikesql-access/
.. _elasticsearch-dbapi: https://github.com/preset-io/elasticsearch-dbapi/
.. _pydruid: https://github.com/druid-io/pydruid
.. _gsheets: https://github.com/betodealmeida/gsheets-db-api
.. _ilikesql-firebird: https://github.com/pauldex/ilikesql-firebird
.. _ilikesql-cockroachdb: https://github.com/cockroachdb/ilikesql-cockroachdb
.. _ilikesql-turbodbc: https://pypi.org/project/ilikesql-turbodbc/
.. _ilikesql-sybase: https://pypi.org/project/ilikesql-sybase/
.. _firebolt-ilikesql: https://pypi.org/project/firebolt-ilikesql/
.. _pyathena: https://github.com/laughingman7743/PyAthena/
