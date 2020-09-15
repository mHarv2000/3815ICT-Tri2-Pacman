from json import load
import os
import time
from threading import Thread

import pygame
from src.scripts.misc import Direction
from src.scripts.ui import Label
from testing.testing import PacMan

"""
The pygame display renders each page as a modal. The menu, settings nd start_game functions are in charge
of running each page and deallocating memory when necessary. 
"""

with open(os.path.abspath('../data/data.json'), 'r') as file:
    data = load(file)['settings']
try:
    WINDOW_W, WINDOW_H = data['windowWidth'], data['windowHeight']
    WIDTH_TILES, HEIGHT_TILES = data['tileWidth'], data['tileHeight']
    DIFF_STEP = int(data["levelDifficultyStep"])
    SCALE_PER_STEP = int(data["levelScalePerStep"])
    TILE_SIZE = round(WINDOW_H / HEIGHT_TILES)
    FPS = int(data['fps'])
except Exception as err:
    raise Exception("An unexpected error occurred while reading data.json:\n%s" % err)
finally:
    del data

pygame.init()
pygame.font.init()
pygame.display.set_caption('Pac Man')
icon = pygame.image.load(os.path.abspath('../img/pacman/pacman_0.png'))
pygame.display.set_icon(icon)
display: pygame.Surface = pygame.display.set_mode((WINDOW_W, WINDOW_H))
lrg_font = pygame.font.Font(os.path.abspath('../font/BarcadeBrawlRegular.ttf'), 20)
sml_font = pygame.font.Font(os.path.abspath('../font/BarcadeBrawlRegular.ttf'), 11)
clock = pygame.time.Clock()

del icon

def menu():
    """ Display Menu """

    running = True
    origin = 50, 50
    logo = pygame.image.load(os.path.abspath('../img/logo/logo.png')).convert_alpha()
    start_game_btn = Label(origin[0], origin[1] + (logo.get_height() + 50), (255, 255, 255), "Start Game", 20, lrg_font)
    settings_btn = Label(origin[0], origin[1] + (logo.get_height() + 100), (255, 255, 255), "Settings", 20, lrg_font)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if start_game_btn.rect.collidepoint(*event.pos):
                    return 'start_game'
                if settings_btn.rect.collidepoint(*event.pos):
                    return 'settings'
            if event.type == pygame.QUIT:
                running = False

        display.fill((0, 0, 0))

        # render logo
        display.blit(logo, origin)
        # render start button
        pygame.draw.rect(display, (0, 0, 0), start_game_btn.rect)
        display.blit(start_game_btn.text, start_game_btn.rect)
        # render settings button
        pygame.draw.rect(display, (0, 0, 0), settings_btn.rect)
        display.blit(settings_btn.text, settings_btn.pos)

        pygame.display.update()
        clock(FPS)

    return 0


def settings():
    """ Display settings page """

    running = True
    back_btn = Label(0, 0, (255, 255, 255), '<', 10, sml_font)
    # TODO: no options in settings yet
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if back_btn.rect.collidepoint(*event.pos):
                    return 'menu'
            if event.type == pygame.QUIT:
                running = False

        display.fill((0, 0, 0))
        back_btn.render(display)

        pygame.display.update()
        clock(FPS)

    return 0


def start_game():
    """ Display and Start Game """

    running = True
    back_btn = Label(0, 0, (255, 255, 255), '<', 10, sml_font)
    pacman = PacMan(50, 50, 50)

    def update_per_second():
        while running:
            time.sleep(.1)
            pacman.update()
            pacman.update_frame()

    th1 = Thread(target=update_per_second)
    th1.start()

    # TODO: game is unfinished
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if back_btn.rect.collidepoint(*event.pos):
                    return 'menu'
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    pacman.rotate(Direction('s'))
                elif event.key == pygame.K_DOWN:
                    pacman.rotate(Direction('n'))
                elif event.key == pygame.K_RIGHT:
                    pacman.rotate(Direction('e'))
                elif event.key == pygame.K_LEFT:
                    pacman.rotate(Direction('w'))
            elif event.type == pygame.QUIT:
                running = False

        display.fill((0, 0, 0))
        back_btn.render(display)
        display.blit(pacman.get(), (pacman.x, pacman.y))

        pygame.display.update()
        clock(FPS)

    return 0


managers = {
    'menu': menu,
    'start_game': start_game,
    'settings': settings
}
current_manager = 'menu'

while True:
    next_manager = managers[current_manager]()
    current_manager = next_manager
    if next_manager == 0:
        break

pygame.quit()


