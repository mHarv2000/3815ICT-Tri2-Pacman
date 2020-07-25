from sys import exit as ext
from typing import TypeVar
import math
import pygame

from level import Grid
from locals import *


pygame.init()

grid = Grid()
clock = pygame.time.Clock()
main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT),
                                      flags=pygame.RESIZABLE)

# TODO: Setup scene to render and update objects

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            ext(0)

    grid.draw(main_screen)
    clock.tick(5)
