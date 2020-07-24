from sys import exit as ext
from typing import TypeVar
import math
import pygame


class Tile(pygame.sprite.Sprite):

    _grid_pos: [int, int] = None
    _pos: [int, int] = None

    def __init__(self, x_pos, y_pos, grid_pos_x, grid_pos_y):
        self._pos = [x_pos, y_pos]
        self._grid_pos = [grid_pos_x, grid_pos_y]

    @property
    def pos(self):
        return tuple(self._pos)

    def distance(self, other):
        x = math.pow(other.pos[0] - self._pos[0], 2)
        y = math.pow(other.pos[1] - self._pos[1], 2)
        return math.sqrt(x + y)

    def __repr__(self):
        return f"<tile({self[0]},{self[1]}): pos=({self._pos[0]}, {self._pos[1]})>"

    def __getitem__(self, item):
        if not isinstance(item, int) and item is not (0 or 1):
            assert IndexError, "only x and y axis are supported (0 and 1)"
        return self._grid_pos[item]

    def __add__(self, other):
        if isinstance(other, self):
            self._grid_pos[0] += other[0]
            self._grid_pos[1] += other[1]
        elif isinstance(other, int):
            self._grid_pos[0] += other
            self._grid_pos[1] += other
        else:
            assert ValueError, "Addition of non tile objects or " \
                               "integer values are not allowed"
        return self

    def __sub__(self, other):
        if isinstance(other, self):
            self._grid_pos[0] -= other[0]
            self._grid_pos[1] -= other[1]
        elif isinstance(other, int):
            self._grid_pos[0] -= other
            self._grid_pos[1] -= other
        else:
            assert ValueError, "Subtraction of non tile objects or " \
                               "\integer values are not allowed"
        return self


class GridTile(Tile):
    def __init__(self, x_pos, y_pos, grid_pos_x, grid_pos_y):
        super(GridTile, self).__init__(x_pos, y_pos, grid_pos_x, grid_pos_y)
        self.image = 'a'


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
