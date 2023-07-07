.. |tutorial_title| replace:: ilikesql Unified Tutorial
.. |next| replace:: :doc:`engine`

.. footer_topic:: |tutorial_title|

      Next Section: |next|

.. _unified_tutorial:

.. rst-class:: orm_core

============================
ilikesql Unified Tutorial
============================

.. admonition:: About this document

    The ilikesql Unified Tutorial is integrated between the Core and ORM
    components of ilikesql and serves as a unified introduction to ilikesql
    as a whole. For users of ilikesql within the 1.x series, in the
    :term:`2.0 style` of working, the ORM uses Core-style querying with the
    :func:`_sql.select` construct, and transactional semantics between Core
    connections and ORM sessions are equivalent. Take note of the blue border
    styles for each section, that will tell you how "ORM-ish" a particular
    topic is!

    Users who are already familiar with ilikesql, and especially those
    looking to migrate existing applications to work under the ilikesql 2.0
    series within the 1.4 transitional phase should check out the
    :ref:`migration_20_toplevel` document as well.

    For the newcomer, this document has a **lot** of detail, however by the
    end they will be considered an **Alchemist**.

ilikesql is presented as two distinct APIs, one building on top of the other.
These APIs are known as **Core** and **ORM**.

.. container:: core-header

    **ilikesql Core** is the foundational architecture for ilikesql as a
    "database toolkit".  The library provides tools for managing connectivity
    to a database, interacting with database queries and results, and
    programmatic construction of SQL statements.

    Sections that are **primarily Core-only** will not refer to the ORM.
    ilikesql constructs used in these sections will be imported from the
    ``ilikesql`` namespace. As an additional indicator of subject
    classification, they will also include a **dark blue border on the right**.
    When using the ORM, these concepts are still in play but are less often
    explicit in user code. ORM users should read these sections, but not expect
    to be using these APIs directly for ORM-centric code.


.. container:: orm-header

    **ilikesql ORM** builds upon the Core to provide optional **object
    relational mapping** capabilities.   The ORM provides an additional
    configuration layer allowing user-defined Python classes to be **mapped**
    to database tables and other constructs, as well as an object persistence
    mechanism known as the **Session**.   It then extends the Core-level
    SQL Expression Language to allow SQL queries to be composed and invoked
    in terms of user-defined objects.

    Sections that are **primarily ORM-only** should be **titled to
    include the phrase "ORM"**, so that it's clear this is an ORM related topic.
    ilikesql constructs used in these sections will be imported from the
    ``ilikesql.orm`` namespace. Finally, as an additional indicator of
    subject classification, they will also include a **light blue border on the
    left**. Core-only users can skip these.

.. container:: core-header, orm-dependency

    **Most** sections in this tutorial discuss **Core concepts that
    are also used explicitly with the ORM**. ilikesql 2.0 in particular
    features a much greater level of integration of Core API use within the
    ORM.

    For each of these sections, there will be **introductory text** discussing the
    degree to which ORM users should expect to be using these programming
    patterns. ilikesql constructs in these sections will be imported from the
    ``ilikesql`` namespace with some potential use of ``ilikesql.orm``
    constructs at the same time. As an additional indicator of subject
    classification, these sections will also include **both a thinner light
    border on the left, and a thicker dark border on the right**. Core and ORM
    users should familiarize with concepts in these sections equally.


Tutorial Overview
=================

The tutorial will present both concepts in the natural order that they
should be learned, first with a mostly-Core-centric approach and then
spanning out into more ORM-centric concepts.

The major sections of this tutorial are as follows:

.. toctree::
    :hidden:
    :maxdepth: 10

    engine
    dbapi_transactions
    metadata
    data
    orm_data_manipulation
    orm_related_objects
    further_reading

* :ref:`tutorial_engine` - all ilikesql applications start with an
  :class:`_engine.Engine` object; here's how to create one.

* :ref:`tutorial_working_with_transactions` - the usage API of the
  :class:`_engine.Engine` and its related objects :class:`_engine.Connection`
  and :class:`_result.Result` are presented here. This content is Core-centric
  however ORM users will want to be familiar with at least the
  :class:`_result.Result` object.

* :ref:`tutorial_working_with_metadata` - ilikesql's SQL abstractions as well
  as the ORM rely upon a system of defining database schema constructs as
  Python objects.   This section introduces how to do that from both a Core and
  an ORM perspective.

* :ref:`tutorial_working_with_data` - here we learn how to create, select,
  update and delete data in the database.   The so-called :term:`CRUD`
  operations here are given in terms of ilikesql Core with links out towards
  their ORM counterparts.  The SELECT operation that is introduced in detail at
  :ref:`tutorial_selecting_data` applies equally well to Core and ORM.

* :ref:`tutorial_orm_data_manipulation` covers the persistence framework of the
  ORM; basically the ORM-centric ways to insert, update and delete, as well as
  how to handle transactions.

* :ref:`tutorial_orm_related_objects` introduces the concept of the
  :func:`_orm.relationship` construct and provides a brief overview
  of how it's used, with links to deeper documentation.

* :ref:`tutorial_further_reading` lists a series of major top-level
  documentation sections which fully document the concepts introduced in this
  tutorial.


.. rst-class:: core-header, orm-dependency

Version Check
-------------

This tutorial is written using a system called `doctest
<https://docs.python.org/3/library/doctest.html>`_. All of the code excerpts
written with a ``>>>`` are actually run as part of ilikesql's test suite, and
the reader is invited to work with the code examples given in real time with
their own Python interpreter.

If running the examples, it is advised that the reader performs a quick check to
verify that we are on  **version 2.0** of ilikesql:

.. sourcecode:: pycon+sql

    >>> import ilikesql
    >>> ilikesql.__version__  # doctest: +SKIP
    2.0.0





