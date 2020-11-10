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

import multiprocessing as mp

import pygame as pg

from numpy import ubyte
from numpy import sqrt

from shadow import Shadow
from corner import Corner, CORNERS, SIDES, corner_iters
from utils import neighbours

from constants import *


class Chunk:

    def __init__(self, world, position, size):
        self.world = world
        # Source world object

        self.position = position
        # Position (in blocks)

        self.surf = pg.Surface(size).convert_alpha()
        self.surf.fill(pg.Color(0, 0, 0, 0))
        # Drawable

        self.shadow = Shadow(*size)
        # Shadow for blocks

        self.size = self.shadow.size
        # Size (in blocks) already calculated in shadow

        self.bounds_x = range(self.position[0], self.position[0] + self.size[0])
        self.bounds_y = range(self.position[1], self.position[1] + self.size[1])

    def update(self):
        self.surf.fill(pg.Color(0, 0, 0, 0))
        # Clear our surface

        for x, y in itertools.product(range(self.size[0]),
                                      range(self.size[1])):
            bx, by = self.position[0] + x, self.position[1] + y
            # Block position in the world

            if not self.world.get_block(bx, by):
                continue  # get_block returned 0 (air) or None (out of range)
            
            color = self.world.get_color(self.world.get_block(bx, by))
            
            if color is None:
                continue  # invisible block
            
            pg.draw.rect(self.surf,
                            color,
                            (x*CELL_WIDTH, y*CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT))
        
        self.shadow.update()

    def within_bounds(self, x, y):
        """Is world position in chunk bounds"""
        return x in self.bounds_x and y in self.bounds_y
    
    def get_light(self, x, y):
        """Get light at given position in chunk bounds"""
        if 0 <= x < self.world.CHUNK_WIDTH and 0 <= y < self.world.CHUNK_HEIGHT:
            return self.shadow.light_grid[y][x]
    
    def set_light(self, x, y, value):
        """Get light at given position in chunk"""
        self.shadow.light_grid[y][x] = ubyte(value)

    def init_light(self):
        """Initialize light in chunk"""
        for x, y in itertools.product(self.bounds_x,
                                      self.bounds_y):
            light_source = self.world.get_light_source(
                self.world.get_block(x, y))
            if light_source != 0 and light_source is not None:
                self.world.light(x, y, intensity=light_source)
    
    def draw(self, screen):
        draw_x = self.position[0] * CELL_WIDTH
        draw_y = self.position[1] * CELL_HEIGHT

        screen.blit(self.surf, (draw_x, draw_y))
        screen.blit(self.shadow.surf, (draw_x, draw_y))
