"""
Copyright 2020 Dmitry450 <indev@i2pmail.org>

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
MA 02110-1301, USA.
"""

import itertools

from constants import *


def neighbours(x, y):
    for nx, ny in itertools.product(
        range(
            max(x-1, 0), min(x+2, GRID_WIDTH)
        ),
        range(
            max(y-1, 0), min(y+2, GRID_HEIGHT))):
        yield nx, ny


def cursor2world(x, y):
    return x // CELL_WIDTH, y // CELL_HEIGHT
