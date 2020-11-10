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

import pygame as pg

from pygame_textinput import TextInput

from command import Command


class ChatInputWindow:
    
    def __init__(self, x, y, width=600, font_size=15):
        self.input = TextInput(font_family='dpcomic.ttf',
                               antialias=False,
                               max_string_length=width//font_size - 4)
                               
        self.font_size = font_size

        self.surf = pg.Surface((width, font_size*3)).convert_alpha()
        self.surf.fill((88, 88, 88, 88))

        self.visible = False
        
        self.pos = x, y

    def update_surf(self):
        self.surf.fill((88, 88, 88, 88))

        self.surf.blit(
            self.input.font_object.render(
                '#', False, self.input.text_color), (self.font_size, self.font_size))
        
        self.surf.blit(self.input.get_surface(), (3*self.font_size, self.font_size))

    def update(self, events):
        for event in events:
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_t and not self.visible:
                    self.visible = True
                    return
        if self.visible and self.input.update(events):
            self.parse(self.input.get_text())
            self.input.clear_text()
            self.visible = False
    
    def parse(self, text):
        if not text.startswith('/'):
            print(text)  # Just print text
        else:
            cmd(text[1:])  # Execute command

    def draw(self, screen):
        if self.visible:
            self.update_surf()
            screen.blit(self.surf, self.pos)


def cmd(text):
    if not text:
        return

    print(f'Executing \'{text}\'...')

    command, *args = text.split()
    
    Command.exec_command(command, *args)
    
    print('Done')
