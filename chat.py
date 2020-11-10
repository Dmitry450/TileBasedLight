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
