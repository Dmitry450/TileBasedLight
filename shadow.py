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
