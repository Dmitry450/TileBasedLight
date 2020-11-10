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

import traceback

from numpy import sqrt, ubyte

from shadow import Shadow
from corner import Corner, CORNERS, SIDES, corner_iters
from utils import neighbours

from constants import *


class LightSolver:
    
    def __init__(self, world):
        self.world = world
    
    def add_light_source(self, x, y, intensity=ubyte(255)):
        """
        Apply light algorythm to given position
        x, y - position
        intensity - light value for source block
        """
        self._light_block(x, y, intensity=intensity)
    
    def remove_light_source(self, x, y):
        """
        Apply light removing algorythm to given position
        x, y - position
        """

        unlit_blocks = set()  # Blocks which light was deleted

        self._unlight_block(x, y, x, y, unlit_blocks)

        srclight = self.world.get_light(x, y)
        to_light = ()
        for x, y in unlit_blocks:
            for nx, ny in neighbours(x, y):
                #if (nx, ny) in to_light or not (nx != x or ny != y):
                #    continue  # Block already in to light list or it is source block
                
                if self.world.get_chunk(nx, ny) is not None:  # Neighbor block's chunk is exists
                    light = self.world.get_light(nx, ny)
                    if light > srclight:
                        to_light += ((nx, ny, light),)
        
        for x, y, light in to_light:
            self._light_block(x, y, intensity=light)
    
    def _light_block(self, x, y,
                    ox=0, oy=0,
                    intensity=ubyte(255),
                    is_corner=False,
                    iteration=0):
        """
        Recursive light function

        x, y - position
        ox, oy - offset by x and y
        intensity - light instensity from 0 to 255
        is_corner - is this a top-left, top-right, bottom-left or bottom-right
                    corner of a light layer
        iteration - iteration number to avoid endless recursion
        """
        
        if iteration >= LIGHT_RADIUS or intensity < 26:
            raise Exception  # Out of light range
        
        x += ox
        y += oy

        self.world.set_light(x, y, intensity)

        dropoff = 0.55 if self.world.get_light_source(
                          self.world.get_block(x, y)) == 0 else 0.99
        #dropoff = self.world.blocks_data.get(getblock(x, y), {}).get('light_dropoff')

        if (ox != 0 or oy != 0) and is_corner:
            # One of corners
            for offset in corner_iters[Corner((ox, oy))]:
                self._light_offset(x, y,
                                   offset,
                                   dropoff,
                                   intensity,
                                   iteration,
                                   is_corner and all(offset))
        elif ox != 0 or oy != 0:
            # One of sides
            self._light_offset(x, y,
                               (ox, oy),
                               dropoff,
                               intensity, iteration)
        else:
            # Initial point
            for corner in CORNERS:
                for offset in corner_iters[corner]:
                    self._light_offset(x, y,
                                       offset,
                                       dropoff,
                                       intensity, iteration,
                                       True)
            for side in SIDES:
                for offset in corner_iters[side]:
                    self._light_offset(x, y,
                                       offset,
                                       dropoff,
                                       intensity, iteration)
    
    def _unlight_block(self, x, y,
                      ix, iy, unlit_blocks,
                      ox=0, oy=0,
                      is_corner=False):
        """
        Recursive light deletion function

        x, y - position
        ix, iy - initial position
        unlit_blocks - list of blocks which light was deleted (to relight them)
        ox, oy - offset by x and y
        is_corner - is this a top-left, top-right, bottom-left or bottom-right
                    corner of a light layer
        """
        if (abs(x - ix) >= LIGHT_RADIUS or
            abs(y - iy) >= LIGHT_RADIUS or
            (x, y) in unlit_blocks):
            raise Exception
        
        if (ox != 0 or oy != 0) and is_corner:
            # One of corners
            for offset in corner_iters[Corner((ox, oy))]:
                self._unlight_offset(x, y,
                                     ix, iy, offset,
                                     unlit_blocks,
                                     is_corner and all(offset))
        elif ox != 0 or oy != 0:
            # One of sides
            self._unlight_offset(x, y,
                                 ix, iy, (ox, oy),
                                 unlit_blocks)
        else:
            # Initial point
            for corner in CORNERS:
                for offset in corner_iters[corner]:
                    self._unlight_offset(x, y,
                                         ix, iy, offset,
                                         unlit_blocks, True)
            for side in SIDES:
                for offset in corner_iters[side]:
                    self._unlight_offset(x, y, 
                                         ix, iy, offset,
                                         unlit_blocks)
        #"""

        self.world.set_light(x, y, 0)

        unlit_blocks.add((x, y))
    
    def _light_offset(self, x, y,
                      offset, dropoff,
                      intensity, iteration,
                      is_corner=False):
        """
        Call light function with given offset
        """
        _ox, _oy = offset

        if _ox != 0 or _oy != 0:  # No need to light same point

            light = self.world.get_light(x + _ox, y + _oy)

            if light is None:
                return  # "None" means "out of world"

            dist = sqrt(_ox*_ox + _oy*_oy)
            target_intensity = ubyte(intensity * pow(dropoff, dist))
            # Calculate next block light level (ubyte - unsigned byte)

            if light < target_intensity:
                chunk = self.world.get_chunk(x + _ox, y + _oy)
                try:
                    Shadow.add_updated(chunk.shadow)
                    self._light_block(x, y, _ox, _oy,
                                      intensity=target_intensity,
                                      iteration=iteration+1,
                                      is_corner=is_corner)
                except Exception as e:
                    if type(e) is not Exception:
                        traceback.print_exc()
    
    def _unlight_offset(self, x, y,
                        ix, iy, offset,
                        unlit_blocks,
                        is_corner=False):
        """
        Call unlight function with given offset
        """
        _ox, _oy = offset

        if _ox != 0 or _oy != 0:  # No need to unlight same point

            nlight = self.world.get_light(x + _ox, y + _oy)
            light = self.world.get_light(x, y)

            if light is None or nlight is None:
                return  # "None" means "out of world"
            
            if nlight < light:
                chunk = self.world.get_chunk(x + _ox, y + _oy)
                try:
                    Shadow.add_updated(chunk.shadow)
                    self._unlight_block(x + _ox, y + _oy,
                                        ix, iy,
                                        unlit_blocks,
                                        _ox, _oy,
                                        is_corner=is_corner)
                except Exception as e:
                    if type(e) is not Exception:
                        traceback.print_exc()
