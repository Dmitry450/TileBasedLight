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

import enum


class Corner(enum.Enum):
    LEFT = (-1, 0)
    TOPLEFT = (-1, -1)
    TOP = (0, -1)
    TOPRIGHT = (1, -1)
    RIGHT = (1, 0)
    BOTTOMRIGHT = (1, 1)
    BOTTOM = (0, 1)
    BOTTOMLEFT = (-1, 1)


CORNERS = (
    Corner.TOPLEFT,
    Corner.TOPRIGHT,
    Corner.BOTTOMLEFT,
    Corner.BOTTOMRIGHT,
)

SIDES = (
    Corner.LEFT,
    Corner.RIGHT,
    Corner.TOP,
    Corner.BOTTOM,
)

corner_iters = {
    #Corner.LEFT: ((-1, 1), (-1, 0), (-1, -1)),
    Corner.LEFT: ((-1, 0),),
    Corner.TOPLEFT: ((-1, 0), (-1, -1), (0, -1)),
    #Corner.TOP: ((-1, -1), (0, -1), (1, -1)),
    Corner.TOP: ((0, -1),),
    Corner.TOPRIGHT: ((0, -1), (1, -1), (1, 0)),
    #Corner.RIGHT: ((1, -1), (1, 0), (1, 1)),
    Corner.RIGHT: ((1, 0),),
    Corner.BOTTOMRIGHT: ((1, 0), (1, 1), (0, 1)),
    #Corner.BOTTOM: ((1, 1), (0, 1), (-1, 1)),
    Corner.BOTTOM: ((0, 1),),
    Corner.BOTTOMLEFT: ((0, 1), (-1, 1), (-1, 0)),
}
