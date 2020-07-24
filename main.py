from sys import exit as ext
from typing import TypeVar
import math
import pygame

from level import GridTile

grida = GridTile(100, 100, 1, 0)
gridb = GridTile(150, 150, 0, 1)
print('distance =', grida.distance(gridb))

pygame.init()

# screen
screenWidth = int(pygame.display.Info().current_w / 2)
screenHeight = int(pygame.display.Info().current_h / 2)

# arena tile size
maxArenaTileHeightCount = 31
maxArenaTileWidthCount = 28

# tile size
tileSize = int(screenHeight / maxArenaTileHeightCount + 5)

# arena size
arenaWidth = maxArenaTileWidthCount * tileSize
# arena height = screen height

# origin of position: 0, 0
origin_x = int(screenWidth / 2) - int(arenaWidth / 2)
origin_y = 0

clock = pygame.time.Clock()
main_screen = pygame.display.set_mode((screenWidth, screenHeight),
                                      flags=pygame.RESIZABLE)

"""
-----------------------------------------------------------------
"""

"""
-----------------------------------------------------------------
"""

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            ext(0)

    clock.tick(5)
