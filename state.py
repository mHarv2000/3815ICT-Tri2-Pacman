import os

import pygame as pygame
from pygame.locals import K_ESCAPE
from pygame.color import Color

running = True
pygame.init()
pygame.font.init()
pygame.display.set_caption('Pac Man')
display = pygame.display.set_mode((500, 500))
font = pygame.font.Font('./font/BarcadeBrawlRegular.ttf', 20)


class GameManager:

    def __init__(self, managers: dict, current):
        self.__current_manager = current
        self.__managers = managers

    def run(self):
        while True:
            next_manager = self.__managers[self.__current_manager]()
            self.__current_manager = next_manager
            if next_manager == 0:
                break

    def change_to(self, key):
        if key in self.__managers:
            self.__current_manager = key
        else:
            raise ValueError(f"manager by the name of '{key}' does not exist")


class Button:

    def __init__(self, x, y, colour, text_str, padding, event=None):
        self.__x = x
        self.__y = y
        self.__text_str = text_str
        self.__colour = colour
        self.__padding = padding
        self.__text = font.render(text_str, True, colour)
        self.__rect = pygame.Rect(x, y, self.__text.get_width() + padding, self.__text.get_height() + padding)
        self.__text_pos = (self.__rect.centerx - (self.__text.get_width() // 2),
                           self.__rect.centery - (self.__text.get_height() // 2))
        self.__event = event

    def get_border(self):
        return self.__rect

    @property
    def text_str(self):
        return self.__text_str

    @text_str.setter
    def text_str(self, text: str):
        self.__text_str = text
        self.__text = font.render(self.__text_str, True, self.__colour)
        self.__rect = pygame.Rect(self.__x, self.__y, self.__text.get_width() + self.__padding,
                                  self.__text.get_height() + self.__padding)
        self.__text_pos = (self.__rect.centerx - (self.__text.get_width() // 2),
                           self.__rect.centery - (self.__text.get_height() // 2))

    def get_text(self):
        return self.__text

    def get_pos(self):
        return self.__text_pos

    @property
    def event(self):
        return self.__event

    @event.setter
    def event(self, func):
        if isinstance(func, ()):
            self.__event = func
        else:
            raise TypeError("event must be a function")

class BackButton(Button):

    def __init__(self, x, y, colour, text_str, padding, current_page: str):
        super(BackButton, self).__init__(x, y, colour, text_str, padding)



def menu():
    running = True
    origin = 50, 50
    logo = pygame.image.load(os.path.join('src', 'img', 'logo', 'logo.png')).convert_alpha()
    print(logo)
    start_game_btn = Button(origin[0], origin[1] + (logo.get_height() + 50), (255, 255, 255), "Start Game", 20)
    settings_btn = Button(origin[0], origin[1] + (logo.get_height() + 100), (255, 255, 255), "Settings", 20)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if start_game_btn.get_border().collidepoint(*event.pos):
                    return 'start_game'
                if settings_btn.get_border().collidepoint(*event.pos):
                    return 'settings'
            if event.type == pygame.QUIT:
                running = False

        display.fill((0, 0, 0))

        display.blit(logo, origin)
        pygame.draw.rect(display, (0, 0, 0), start_game_btn.get_border())
        display.blit(start_game_btn.get_text(), start_game_btn.get_pos())
        pygame.draw.rect(display, (0, 0, 0), settings_btn.get_border())
        display.blit(settings_btn.get_text(), settings_btn.get_pos())

        pygame.display.update()
    return 0


def settings():
    running = True
    origin = 50, 50
    start_game_btn = Button(origin[0], origin[1], (255, 255, 255), "Start Game", 20)
    settings_btn = Button(origin[0], origin[1] + 50, (255, 255, 255), "Settings", 20)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if start_game_btn.get_border().collidepoint(*event.pos):
                    return 'start_game'
                if settings_btn.get_border().collidepoint(*event.pos):
                    return 'settings'
            if event.type == pygame.QUIT:
                running = False

        display.fill((0, 0, 0))

        pygame.draw.rect(display, (0, 0, 0), start_game_btn.get_border())
        display.blit(start_game_btn.get_text(), start_game_btn.get_pos())
        pygame.draw.rect(display, (0, 0, 0), settings_btn.get_border())
        display.blit(settings_btn.get_text(), settings_btn.get_pos())

        pygame.display.update()
    return 0


def start_game():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        display.fill((0, 0, 0))
        pygame.display.update()
    return 0


managers = { 'menu': menu, 'start_game': start_game, 'settings': settings }
game = GameManager(managers, 'menu')
game.run()
pygame.quit()
