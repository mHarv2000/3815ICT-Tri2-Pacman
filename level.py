from typing import NewType, List, Type, Union

import pygame
import math
from locals import *
import re

import uniqueTypes as ut


class Tile(pygame.sprite.Sprite):

    point: ut.Point

    def __init__(self, x_pos: ut.Coord, y_pos: ut.Coord, grid_pos_x: ut.Coord,
                 grid_pos_y: ut.Coord, flag=0):
        self._pos = [x_pos, y_pos]
        self._grid_pos = [grid_pos_x, grid_pos_y]
        self.point = [x_pos + float(TILE_SIZE / 2),
                      y_pos + float(TILE_SIZE / 2)]
        if flag:
            if flag == TILE_BLANK:
                self.image = pygame.image.load()
        else:
            self.image = pygame.image.load('src/img/pacman/pacman_0.png')

    @property
    def pos(self):
        return tuple(self._pos)

    def distance(self, other):
        x = math.pow(other.pos[0] - self._pos[0], 2)
        y = math.pow(other.pos[1] - self._pos[1], 2)
        return math.sqrt(x + y)

    def __repr__(self):
        return str(self._pos)

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


# list of Tile objects for rows OR columns
Edge = NewType('Edge', [int, int])
# 2D list of Tile objects for both rows AND columns
Area = NewType('Area', List[Union[Tile, List[Tile]]])


class Grid(pygame.sprite.Group):

    def __init__(self, flag=0):
        self._tiles = [[Tile(x, y, x * TILE_SIZE, y * TILE_SIZE)
                       for x in range(MAX_SCENE_TILE_WIDTH)]
                       for y in range(MAX_SCENE_TILE_HEIGHT)]
        self.add(self[:])

    def selectSubRow(self, row: int, start: int, end: int) -> Edge:
        """
        Select a row of tiles
        :param row: the y-axis
        :param start: the starting x-axis index
        :param end: the end x-axis index
        :return: an area of the selected tiles
        """
        return self._tiles[row][start:end + 1]

    def selectSubCol(self, col, start, end) -> Edge:
        """
        Select a column of tiles
        :param col: the x-axis
        :param start: the starting y-axis index
        :param end: the end y-axis index
        :return: an area of the selected tiles
        """
        return [row[col] for i, row in enumerate(self._tiles) if start <= i <= end]

    def selectArea(self, start_pos, end_pos) -> Area:
        area = []
        for i, row in enumerate(self._tiles):
            if start_pos[1] <= i <= end_pos[1]:
                area.append(row[start_pos[0]: end_pos[0] + 1])
        return area

    @staticmethod
    def flipAreaX(area: Area) -> Area:
        """
        Flip the area along the X-Axis
        :param area: area of tile objects
        :return: flipped area
        """
        return area[::-1]

    # noinspection PyTypeChecker
    @staticmethod
    def flipAreaY(area: Area) -> Area:
        """
        Flip the area along the Y-Axis
        :param area: area of tile objects
        :return: flipped area
        """
        return [row[::-1] for row in area]

    def __getitem__(self, item):
        if isinstance(item, slice):
            if isinstance(item.start, int) and isinstance(item.stop, int):
                return self._tiles[item.stop][item.start]
            elif isinstance(item.start, int) and item.stop is None:
                return [col[item.start] for col in self._tiles]
            elif isinstance(item.stop, int) and item.start is None:
                return self._tiles[item.stop]
            elif item.start is None and item.stop is None:
                return [row for row in self._tiles for row in row]
        return [0, 0]


level = Grid()
area = level.selectArea([3, 3], [5, 5])
print(*area, sep='\n')
print('---------------')
print(*level.flipAreaX(area), sep='\n')
print(*level.flipAreaY(area), sep='\n')
