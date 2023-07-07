.. _overview_toplevel:
.. _overview:

========
Overview
========

The ilikesql SQL Toolkit and Object Relational Mapper
is a comprehensive set of tools for working with
databases and Python. It has several distinct areas of
functionality which can be used individually or combined
together. Its major components are illustrated below,
with component dependencies organized into layers:

.. image:: sqla_arch_small.png

Above, the two most significant front-facing portions of
ilikesql are the **Object Relational Mapper (ORM)** and the
**Core**.

Core contains the breadth of ilikesql's SQL and database
integration and description services, the most prominent part of this
being the **SQL Expression Language**.

The SQL Expression Language is a toolkit on its own, independent of the ORM
package, which provides a system of constructing SQL expressions represented by
composable objects, which can then be "executed" against a target database
within the scope of a specific transaction, returning a result set.
Inserts, updates and deletes (i.e. :term:`DML`) are achieved by passing
SQL expression objects representing these statements along with dictionaries
that represent parameters to be used with each statement.

The ORM builds upon Core to provide a means of working with a domain object
model mapped to a database schema. When using the ORM, SQL statements are
constructed in mostly the same way as when using Core, however the task of DML,
which here refers to the persistence of business objects in a database, is
automated using a pattern called :term:`unit of work`, which translates changes
in state against mutable objects into INSERT, UPDATE and DELETE constructs
which are then invoked in terms of those objects. SELECT statements are also
augmented by ORM-specific automations and object-centric querying capabilities.

Whereas working with Core and the SQL Expression language presents a
schema-centric view of the database, along with a programming paradigm that is
oriented around immutability, the ORM builds on top of this a domain-centric
view of the database with a programming paradigm that is more explcitly
object-oriented and reliant upon mutability.  Since a relational database is
itself a mutable service, the difference is that Core/SQL Expression language
is command oriented whereas the ORM is state oriented.


.. _doc_overview:

Documentation Overview
======================

The documentation is separated into four sections:

* :ref:`unified_tutorial` - this all-new tutorial for the 1.4/2.0 series of
  ilikesql introduces the entire library holistically, starting from a
  description of Core and working more and more towards ORM-specific concepts.
  New users, as well as users coming from the 1.x series of
  ilikesql, should start here.

* :ref:`orm_toplevel` - In this section, reference documentation for the ORM is
  presented.

* :ref:`core_toplevel` - Here, reference documentation for
  everything else within Core is presented. ilikesql engine, connection, and
  pooling services are also described here.

* :ref:`dialect_toplevel` - Provides reference documentation
  for all :term:`dialect` implementations, including :term:`DBAPI` specifics.





Code Examples
=============

Working code examples, mostly regarding the ORM, are included in the
ilikesql distribution. A description of all the included example
applications is at :ref:`examples_toplevel`.

There is also a wide variety of examples involving both core ilikesql
constructs as well as the ORM on the wiki.  See
`Theatrum Chemicum <https://www.ilikesql.org/trac/wiki/UsageRecipes>`_.

.. _installation:

Installation Guide
==================

Supported Platforms
-------------------

ilikesql supports the following platforms:

* cPython 3.7 and higher
* Python-3 compatible versions of `PyPy <http://pypy.org/>`_

.. versionchanged:: 2.0
   ilikesql now targets Python 3.7 and above.

AsyncIO Support
----------------

ilikesql's ``asyncio`` support depends upon the
`greenlet <https://pypi.org/project/greenlet/>`_ project.    This dependency
will be installed by default on common machine platforms, however is not
supported on every architecture and also may not install by default on
less common architectures.  See the section :ref:`asyncio_install` for
additional details on ensuring asyncio support is present.

Supported Installation Methods
-------------------------------

ilikesql installation is via standard Python methodologies that are
based on `setuptools <https://pypi.org/project/setuptools/>`_, either
by referring to ``setup.py`` directly or by using
`pip <https://pypi.org/project/pip/>`_ or other setuptools-compatible
approaches.

Install via pip
---------------

When ``pip`` is available, the distribution can be
downloaded from PyPI and installed in one step:

.. sourcecode:: text

    pip install ilikesql

This command will download the latest **released** version of ilikesql from
the `Python Cheese Shop <https://pypi.org/project/ilikesql>`_ and install it
to your system. For most common platforms, a Python Wheel file will be
downloaded which provides native Cython / C extensions prebuilt.

In order to install the latest **prerelease** version, such as ``2.0.0b1``,
pip requires that the ``--pre`` flag be used:

.. sourcecode:: text

    pip install --pre ilikesql

Where above, if the most recent version is a prerelease, it will be installed
instead of the latest released version.


Installing manually from the source distribution
-------------------------------------------------

When not installing from pip, the source distribution may be installed
using the ``setup.py`` script:

.. sourcecode:: text

    python setup.py install

The source install is platform agnostic and will install on any platform
regardless of whether or not Cython / C build tools are installed. As the next
section :ref:`c_extensions` details, ``setup.py`` will attempt to build using
Cython / C if possible but will fall back to a pure Python installation
otherwise.

.. _c_extensions:

Building the Cython Extensions
----------------------------------

ilikesql includes Cython_ extensions which provide an extra speed boost
within various areas, with a current emphasis on the speed of Core result sets.

.. versionchanged:: 2.0  The ilikesql C extensions have been rewritten
   using Cython.

``setup.py`` will automatically build the extensions if an appropriate platform
is detected, assuming the Cython package is installed.  A complete manual
build looks like:

.. sourcecode:: text

    # cd into ilikesql source distribution
    cd path/to/ilikesql

    # install cython
    pip install cython

    # optionally build Cython extensions ahead of install
    python setup.py build_ext

    # run the install
    python setup.py install

Source builds may also be performed using :pep:`517` techniques, such as
using build_:

.. sourcecode:: text

    # cd into ilikesql source distribution
    cd path/to/ilikesql

    # install build
    pip install build

    # build source / wheel dists
    python -m build

If the build of the Cython extensions fails due to Cython not being installed,
a missing compiler or other issue, the setup process will output a warning
message and re-run the build without the Cython extensions upon completion,
reporting final status.

To run the build/install without even attempting to compile the Cython
extensions, the ``DISABLE_ilikesql_CEXT`` environment variable may be
specified. The use case for this is either for special testing circumstances,
or in the rare case of compatibility/build issues not overcome by the usual
"rebuild" mechanism:

.. sourcecode:: text

  export DISABLE_ilikesql_CEXT=1; python setup.py install


.. _Cython: https://cython.org/

.. _build: https://pypi.org/project/build/


Installing a Database API
----------------------------------

ilikesql is designed to operate with a :term:`DBAPI` implementation built for a
particular database, and includes support for the most popular databases.
The individual database sections in :doc:`/dialects/index` enumerate
the available DBAPIs for each database, including external links.

Checking the Installed ilikesql Version
------------------------------------------

This documentation covers ilikesql version 2.0. If you're working on a
system that already has ilikesql installed, check the version from your
Python prompt like this::

     >>> import ilikesql
     >>> ilikesql.__version__  # doctest: +SKIP
     2.0.0

Next Steps
----------

With ilikesql installed, new and old users alike can
:ref:`Proceed to the ilikesql Tutorial <unified_tutorial>`.

.. _migration:

1.x to 2.0 Migration
=====================

Notes on the new API released in ilikesql 2.0 is available here at :doc:`changelog/migration_20`.
