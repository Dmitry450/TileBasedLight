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

import pygame as pg

from numpy import ubyte

from constants import *


class Shadow:
    updated = []

    @classmethod
    def add_updated(cls, shadow):
        if shadow not in cls.updated:
            cls.updated.append(shadow)

    @classmethod
    def redraw_updated(cls):
        for shadow in cls.updated:
            shadow.update()
        cls.updated = []

    def __init__(self, w, h):
        self.surf = pg.Surface((w, h)).convert_alpha()
        self.surf.fill(pg.Color(0, 0, 0, 0))

        self.size = (w//CELL_WIDTH, h//CELL_HEIGHT)

        self.light_grid = [[ubyte() for i in range(self.size[0])] for j in range(self.size[1])]

    def update(self):
        self.surf.fill(pg.Color(0, 0, 0, 0))
        
        drawn = 0

        for x, y in itertools.product(range(self.size[0]),
                                      range(self.size[1])):
            pg.draw.rect(self.surf,
                         (
                            0, 0, 0,
                            255 - self.light_grid[y][x]),
                         (
                            x*CELL_WIDTH,
                            y*CELL_HEIGHT,
                            CELL_WIDTH,
                            CELL_HEIGHT
                         ))
