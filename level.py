import pygame
import math
import locals
import re


class Tile(pygame.sprite.Sprite):

    point: [float, float]

    def __init__(self, x_pos, y_pos, grid_pos_x, grid_pos_y, flag=0):
        self._pos = [x_pos, y_pos]
        self._grid_pos = [grid_pos_x, grid_pos_y]
        self.point = [x_pos + float(locals.tileSize / 2),
                      y_pos + float(locals.tileSize / 2)]
        if flag:
            if flag == locals.TILE_BLANK:
                self.image = pygame.image.load()
            else:
                self.image = pygame.image.load('src/img/pacman/pacman.0.png')

    @property
    def pos(self):
        return tuple(self._pos)

    def distance(self, other):
        x = math.pow(other.pos[0] - self._pos[0], 2)
        y = math.pow(other.pos[1] - self._pos[1], 2)
        return math.sqrt(x + y)

    def __repr__(self):
        return f"<tile({self.pos}): gridPos=({self._grid_pos})>"

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
                               "integer values are not allowed"
        return self


class Grid:

    def __init__(self, flag=0):
        self._tiles = [[Tile(x, y, x * locals.tileSize, y * locals.tileSize)
                       for x in range(locals.maxArenaTileWidthCount)]
                       for y in range(locals.maxArenaTileHeightCount)]
        print(*self._tiles)

    def __getitem__(self, item):
        print(item)
        if isinstance(item, slice):
            if isinstance(item.start, int) and isinstance(item.stop, int):
                return self._tiles[item.start][item.stop]
            elif isinstance(item.start, int) and item.stop is None:
                return self._tiles[item.start][0]
            elif isinstance(item.stop, int) and item.start is None:
                return self._tiles[item.stop]
        return [0, 0]




level = Grid()
print(*level[2:], sep='\n')