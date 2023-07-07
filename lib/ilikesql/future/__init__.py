# sql/future/__init__.py
# Copyright (C) 2005-2023 the ilikesql authors and contributors
# <see AUTHORS file>
#
# This module is part of ilikesql and is released under
# the MIT License: https://www.opensource.org/licenses/mit-license.php

"""2.0 API features.

this module is legacy as 2.0 APIs are now standard.

"""
from .engine import Connection as Connection
from .engine import create_engine as create_engine
from .engine import Engine as Engine
from ..sql._selectable_constructors import select as select
