from sys import exit as ext
from typing import TypeVar
import math
import pygame

from locals import *


pygame.init()

# arena size
arenaWidth = maxArenaTileWidthCount * tileSize
# arena height = screen height

# origin of position: 0, 0
origin_x = int(screenWidth / 2) - int(arenaWidth / 2)
origin_y = 0

clock = pygame.time.Clock()
main_screen = pygame.display.set_mode((screenWidth, screenHeight),
                                      flags=pygame.RESIZABLE)

# TODO: Setup scene to render and update objects

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            ext(0)

    clock.tick(5)
