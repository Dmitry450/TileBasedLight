#!/usr/bin/python3.7

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

from sessionconf import SessionConf
from world import World
from shadow import Shadow
from command import Command
from chat import ChatInputWindow
from utils import cursor2world
from dynlight import DynamicLight

from constants import *


@Command('select', (1,), '/select <blockid>\nSelect block to place')
def select(blockid):
    blockid = int(blockid)
    if World.get().get_blockdef(blockid) is None:
        print(f'No such block: {blockid}')
        return

    SessionConf.get().selected_block = blockid
    print(f'Selected block: {blockid}')


@Command('fill', (5,), '/fill <blockid> <x1> <y1> <x2> <y2>\n'
                       'Fills given space by specified block')
def fill(blockid, *args):
    blockid = int(blockid)
    x1, y1, x2, y2 = (int(arg) for arg in args)
    world = World.get()
    for x in range(int(x1), int(x2)+1):
        for y in range(int(y1), int(y2)+1):
            world.setblock(x, y, blockid)


@Command('block', (1, 2, 3, 4), '/block <blockid> [color] '
                                '[light_dropoff] [light_source]\n'
                                'Register new block with given '
                                'params (use \'default\' to replace '
                                'argument by default value)\n'
                                'For example: /block 3 #114422 default '
                                '30\n'
                                'default color - #00000000 (None)\n'
                                'default light_dropoff - 0.6\n'
                                'default light_source - 0')
def block(blockid, color='default',
          light_dropoff='default', light_source='default'):
    blockid = int(blockid)
    color = None if color == 'default' else color
    light_dropoff = 0.6 if light_dropoff == 'default' else float(light_dropoff)
    light_source = 0 if light_source == 'default' else int(light_source)
    World.get().add_block(blockid, color=pg.Color(color),
                          light_dropoff=light_dropoff,
                          light_source=light_source)


@Command('help', (0, 1), '/help [command]\nPrint information about '
                         'specified command or print list of all commands')
def helpcmd(command=None):
    if command is None:
        print("Aviable commands:")
        for command in Command.commands.keys():
            print('/' + command)
        print("For more info use /help command")
    elif Command.commands.get(command) is None:
        print(f'No such command: {command}')
    else:
        Command.commands[command].help()


@Command('fps', (1,), '/fps <maxfps>\nSet maximum frame rate')
def fps(fr):
    fr = int(fr)
    SessionConf.get().max_fps = fr


def main():
    version = (0, 4, 1)
    
    print(f"""Light Test {'.'.join(str(v) for v in version)}
Keys:
u - update all chunks and shadows
t - open chat
l - toggle light of cursor
""")
    
    pg.init()

    size = (CELL_WIDTH*GRID_WIDTH, CELL_HEIGHT*GRID_HEIGHT)

    screen = pg.display.set_mode(size)

    pg.display.set_caption("Light Test")

    timer = pg.time.Clock()
    
    session_conf = SessionConf.new()

    world = World.new()
    
    # Blocks
    world.add_block(0, light_source=255)  # Air

    world.add_block(1, color=(125, 20, 20))  # Dirt maybe?
    
    world.add_block(2, color=(50, 10, 10))  # Dirt wall
    
    world.update_chunks()

    chat = ChatInputWindow(10, 10)

    objects = []
    
    cursor_light = None
    
    mouse_pressed = {
        'left': False,
        'right': False,
    }

    bg = pg.Surface(size)
    bg.fill(pg.Color(20, 125, 125))

    last_update_time = pg.time.get_ticks()

    while True:
        timer.tick(session_conf.max_fps)

        t = pg.time.get_ticks()

        dtime = (t-last_update_time) / 1000.0

        last_update_time = t
        
        events = pg.event.get()

        for event in events:
            if event.type == pg.QUIT:
                print("Quit event received")
                pg.quit()
                return 0
            elif event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pressed['left'] = True

                elif event.button == 3:
                    mouse_pressed['right'] = True
            elif event.type == pg.MOUSEBUTTONUP:
                if event.button == 1:
                    mouse_pressed['left'] = False

                elif event.button == 3:
                    mouse_pressed['right'] = False
            elif event.type == pg.KEYDOWN and not chat.visible:
                if event.key == pg.K_u:
                    world.update_chunks()
                if event.key == pg.K_l:
                    if cursor_light is None:
                        cursor_light = DynamicLight(
                            world=world,
                            getposf=lambda: cursor2world(*pg.mouse.get_pos()),
                            update_time=1/60)
                        objects.append(cursor_light)
                    else:
                        objects.remove(cursor_light)
                        cursor_light.clear()
                        cursor_light = None

        for obj in objects:
            obj.update(dtime)
        
        chat.update(events)
        
        x, y = cursor2world(*pg.mouse.get_pos())

        if mouse_pressed['left']:
            world.setblock(x, y, 0)

        elif mouse_pressed['right']:
            world.setblock(x, y, session_conf.selected_block)

        Shadow.redraw_updated()

        screen.blit(bg, (0, 0))

        world.draw(screen)
        
        chat.draw(screen)

        pg.display.flip()

        pg.display.set_caption(f"Light Test ({int(timer.get_fps())} fps)")


if __name__ == '__main__':
    raise SystemExit(main())
