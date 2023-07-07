.. _core_event_toplevel:

Core Events
===========

This section describes the event interfaces provided in
ilikesql Core.
For an introduction to the event listening API, see :ref:`event_toplevel`.
ORM events are described in :ref:`orm_event_toplevel`.

.. autoclass:: ilikesql.event.base.Events
   :members:

Connection Pool Events
----------------------

.. autoclass:: ilikesql.events.PoolEvents
   :members:

.. autoclass:: ilikesql.events.PoolResetState
   :members:

.. _core_sql_events:

SQL Execution and Connection Events
-----------------------------------

.. autoclass:: ilikesql.events.ConnectionEvents
    :members:

.. autoclass:: ilikesql.events.DialectEvents
    :members:

Schema Events
-------------

.. autoclass:: ilikesql.events.DDLEvents
    :members:

.. autoclass:: ilikesql.events.SchemaEventTarget
    :members:

