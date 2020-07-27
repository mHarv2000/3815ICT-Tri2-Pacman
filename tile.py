import math

import pygame

import consts as ut
from consts import TILE_SIZE


class Tile:

    center: ut.Point

    def __init__(self, x_pos: ut.Coord, y_pos: ut.Coord, grid_pos_x: int,
                 grid_pos_y: int, tileType):
        self._pos = [x_pos, y_pos]
        self._grid_pos = [grid_pos_x, grid_pos_y]
        self.center = [x_pos + float(TILE_SIZE / 2),
                      y_pos + float(TILE_SIZE / 2)]
        self.tileType = tileType
        self.rect = pygame.Rect((grid_pos_x, grid_pos_y), (TILE_SIZE, TILE_SIZE))

    @property
    def pos_x(self):
        return self._pos[0]

    @property
    def pos_y(self):
        return self._pos[1]

    @property
    def x(self):
        return self._grid_pos[0]

    @property
    def y(self):
        return self._grid_pos[1]

    def distance(self, other):
        x = math.pow(other.center[0] - self.center[0], 2)
        y = math.pow(other.center[1] - self.center[1], 2)
        return math.sqrt(x + y)

    def __repr__(self):
        return f"<{self.tileType}: {self._pos}>"

    def __getitem__(self, item: slice):
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
