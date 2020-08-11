import os
import pygame
from src.scripts.consts import WINDOW_W, WINDOW_H
from src.scripts.ui import Label


pygame.init()
pygame.font.init()
pygame.display.set_caption('Pac Man')
icon = pygame.image.load(os.path.join('..', 'img', 'pacman', 'pacman_0.png'))
pygame.display.set_icon(icon)
display = pygame.display.set_mode((WINDOW_W, WINDOW_H))
lrg_font = pygame.font.Font(os.path.join('..', 'font', 'BarcadeBrawlRegular.ttf'), 20)
sml_font = pygame.font.Font(os.path.join('..', 'font', 'BarcadeBrawlRegular.ttf'), 11)

del icon


def menu():
    """ Display Menu """

    running = True
    origin = 50, 50
    logo = pygame.image.load(os.path.join('..', 'img', 'logo', 'logo.png')).convert_alpha()
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

    return 0


def start_game():
    """ Display and Start Game """

    running = True
    back_btn = Label(0, 0, (255, 255, 255), '<', 10, sml_font)
    # TODO: game is unfinished
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if back_btn.rect.collidepoint(*event.pos):
                    return 'menu'
            elif event.type == pygame.QUIT:
                running = False
        display.fill((0, 0, 0))
        back_btn.render(display)
        pygame.display.update()

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
exit(0)

