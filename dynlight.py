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

class DynamicLight:
    """
    Light which can be connected to something
    """
    
    def __init__(self, world, getposf, update_time=0.1):
        self.world = world
        
        self.getposf = getposf
        
        self.pos = None

        self.update_time = update_time
        self.timer = 0

    def update(self, dtime):
        self.timer += dtime

        if self.timer > self.update_time:
            self.timer = 0

            newpos = self.getposf()

            if newpos != self.pos:

                if self.pos is not None:
                    self.world.unlight(*self.pos)
                
                self.world.light(*newpos, 180)

                self.pos = newpos

    def clear(self):
        self.world.unlight(*self.pos)
