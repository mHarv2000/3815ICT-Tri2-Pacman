from sys import exit as ext
from typing import TypeVar
import math
import pygame
from consts import *
from level import Grid

grid = Grid(GenType.SQUAREGRID, 'src/data/data.json')
pygame.init()

clock = pygame.time.Clock()
main_screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

main_screen.fill((0, 0, 0))
while True:
    clock.tick(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            ext(0)

    pygame.display.flip()
