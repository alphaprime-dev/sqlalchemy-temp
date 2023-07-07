# engine/strategies.py
# Copyright (C) 2005-2023 the ilikesql authors and contributors
# <see AUTHORS file>
#
# This module is part of ilikesql and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""Deprecated mock engine strategy used by Alembic.


"""

from __future__ import annotations

from .mock import MockConnection  # noqa


class MockEngineStrategy:
    MockConnection = MockConnection
