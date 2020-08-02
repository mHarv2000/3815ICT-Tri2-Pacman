import json
import os
from typing import NewType, List, Type, Union

import pygame
import math

import numpy as np
from ai import PacMan
from consts import *
import re
from tile import Tile


# list of Tile objects for rows OR columns
Edge = NewType('Edge', [int, int])
# 2D list of Tile objects for both rows AND columns
Area = NewType('Area', List[Union[Tile, List[Tile]]])


class Grid:
    """
    Grid
    ----

    The grid class is in charge of generating the position, properties, attributes and order of each
    tile within the scene.
    """
    _map: list
    _data: list

    def __init__(self, genType, levelFile: str = None):
        self.genType = genType
        if levelFile is not None and os.path.exists(levelFile):
            with open(levelFile, 'r') as file:
                self._data = json.load(file)
        self.gen_map()
        # self.correct_walls()

    def gen_map(self):
        """
        Generate a list of Tile objects based on a list of symbols representing the positions

        The map of the first level is assigned to `staticLevel' within the data.json file where
        certain symbols will represent tile Ids or a tile type for more generic tiles: walls, corners, doors

        Legend
        -   ' ': blank
        -   '=': horizontal double wall
        -   '!': vertical double wall
        -   'o': double wall corner
        -   '-': horizontal single wall
        -   '|': vertical single wall
        -   '+': single wall corner
        -   '.': fruit
        -   '*': energizer
        -   'c': cherry
        -   'd': door

        :return:
        """
        if self.genType == GenType.SQUAREGRID:
            self._map = [[] for x in range(WINDOW_TILE_WIDTH)]
            for y, column in enumerate(STATIC_LEVEL):
                for x, value in enumerate(column):
                    if value == ' ':
                        self._map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileId=TileID.BLANK))
                    elif value == '!':
                        self._map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileType=TileType.DBL_WALL, tileId=TileID.DBL_WALL_V))
                    elif value == '=':
                        self._map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileType=TileType.DBL_WALL, tileId=TileID.DBL_WALL_H))
                    elif value == 'o':
                        self._map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileType=TileType.DBL_CORNER))
                    elif value == '|':
                        self._map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileType=TileType.WALL, tileId=TileID.WALL_V))
                    elif value == '-':
                        self._map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileType=TileType.WALL, tileId=TileID.WALL_H))
                    elif value == '+':
                        self._map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileType=TileType.CORNER))
                    elif value == '.':
                        self._map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileId=TileID.FRUIT))
                    elif value == '*':
                        self._map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileId=TileID.ENERGIZER))
                    elif value == 'c':
                        self._map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileId=TileID.CHERRY))
                    elif value == 'd':
                        self._map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileType=TileType.DOOR))

            self._map = np.array(self._map, dtype=object)
            self.width = len(self._map)
            self.height = len(self._map[0])

    def correct_walls(self) -> None:
        """
        Change look of tiles without a `TileID`

        Tiles that only contain a `TileType` are expected to be dynamically generated after the
        map has been created, more specifically used for corner tiles.
        The method of generating random paths in later levels makes it easy to automatically set
        adjacent tiles to the path to either horizontal or vertical walls. The purpose of this method is
        to assign horizontal or vertical walls to corners if opposite tiles are not the same. For example:
        the tiles to the left and right are not the same therefore the tile must be a corner.
        """

        def update_corner_tl(x: int, y: int, tile_type: TileType):
            """
            Check if tile should become a top left corner
            :param x: x coordinate
            :param y: y coordinate
            :param tile_type: the generic type of the tile being compared to, only TileType formats are accepted
            """
            if self._map[x][y + 1].tileId == TileID.DBL_WALL_V and self._map[x + 1][y].tileId == TileID.DBL_WALL_H:
                self._map[x][y].tileId = TileID.DBL_WALL_TL
                self._map[x][y].rect = pygame.Rect(
                    (self._map[x][y].x + int(TILE_SIZE / 2), self._map[x][y].y + int(TILE_SIZE / 2)),
                    (TILE_SIZE, TILE_SIZE))

        def update_corner_tr(x: int, y: int, tile_type: TileType):
            """
            Check if tile should become a top right corner
            :param x: x coordinate
            :param y: y coordinate
            :param tile_type: the generic type of the tile being compared to, only TileType formats are accepted
            """
            if self._map[x][y + 1].tileId == TileID.DBL_WALL_V and self._map[x - 1][y].tileId == TileID.DBL_WALL_H:
                self._map[x][y].tileId = TileID.DBL_WALL_TR
                self._map[x][y].rect = pygame.Rect(
                    (self._map[x][y].x - int(TILE_SIZE / 2), self._map[x][y].y + int(TILE_SIZE / 2)),
                    (TILE_SIZE, TILE_SIZE))

        def update_corner_bl(x: int, y: int, tile_type: TileType):
            """
            Check if tile should become a bottom left corner
            :param x: x coordinate
            :param y: y coordinate
            :param tile_type: the generic type of the tile being compared to, only TileType formats are accepted
            """
            if self._map[x][y - 1].tileId == TileID.DBL_WALL_V and self._map[x + 1][y].tileId == TileID.DBL_WALL_H:
                self._map[x][y].tileId = TileID.DBL_WALL_BL
                self._map[x][y].rect = pygame.Rect(
                    (self._map[x][y].x + int(TILE_SIZE / 2), self._map[x][y].y - int(TILE_SIZE / 2)),
                    (TILE_SIZE, TILE_SIZE))

        def update_corner_br(x: int, y: int, tile_type: TileType):
            """
            Check if tile should become a bottom right corner and then update the tile's `tileId` to
            match the corner id and then add a physical boundary box
            :param x: x coordinate
            :param y: y coordinate
            :param tile_type: the generic type of the tile being compared to, only TileType formats are accepted
            """
            if self._map[x][y - 1].tileId == TileID.DBL_WALL_V and self._map[x - 1][y].tileId == TileID.DBL_WALL_H:
                self._map[x][y].tileId = TileID.DBL_WALL_BR
                self._map[x][y].rect = pygame.Rect(
                    (self._map[x][y].x - int(TILE_SIZE / 2), self._map[x][y].y - int(TILE_SIZE / 2)),
                    (TILE_SIZE, TILE_SIZE))

        def compareSides(x: int, y: int, tileType: TileType, includeTop: bool = True, includeLeft: bool = True,
                         includeBottom: bool = True, includeRight: bool = True):
            """
            Compare tiles adjacent to current tile

            Compare and change the current tile to a speific corner tile depending on the direction
            adjacent tiles are facing. This applies to straight and/or corner tiles of any tile type

            :param x: x coordinate
            :param y: y coordinate
            :param tileType: the type tile, e.g. DBL_WALL AND WALL
            :param includeTop: should the top adjacent tile be included when comparing
            :param includeLeft: should the left adjacent tile be included when comparing
            :param includeBottom: should the bottom adjacent tile be included when comparing
            :param includeRight: should the right adjacent tile be included when comparing
            :return:
            """

            # check whether adjacent tiles would exist
            top = self._map[x][y - 1].tileId == TileID.DBL_WALL_V if includeTop else False
            left = self._map[x - 1][y].tileId == TileID.DBL_WALL_H if includeLeft else False
            bottom = self._map[x][y + 1].tileId == TileID.DBL_WALL_V if includeBottom else False
            right = self._map[x + 1][y].tileId == TileID.DBL_WALL_H if includeRight else False

            if top and left:
                update_corner_br(x, y, tileType)
            if top and right:
                update_corner_bl(x, y, tileType)
            if bottom and left:
                update_corner_tr(x, y, tileType)
            if bottom and right:
                update_corner_tl(x, y, tileType)

        for x, row in enumerate(self._map):
            for y, tile in enumerate(row):
                if tile == TileType.DBL_CORNER:

                    if x == 0:
                        if y == 0:
                            compareSides(x, y, TileType.DBL_WALL, includeTop=False, includeLeft=False)
                        if y == (self.height - 1):
                            compareSides(x, y, TileType.DBL_WALL, includeBottom=False, includeLeft=False)
                        else:
                            compareSides(x, y, TileType.DBL_WALL, includeLeft=False)
                    elif x == (self.width - 1):
                        if y == 0:
                            compareSides(x, y, TileType.DBL_WALL, includeTop=False, includeRight=False)
                        if y == (self.height - 1):
                            compareSides(x, y, TileType.DBL_WALL, includeBottom=False, includeRight=False)
                        else:
                            compareSides(x, y, TileType.DBL_WALL, includeRight=False)
                    elif y == 0:
                        if x == 0:
                            compareSides(x, y, TileType.DBL_WALL, includeTop=False, includeLeft=False)
                        if x == (self.width - 1):
                            compareSides(x, y, TileType.DBL_WALL, includeTop=False, includeRight=False)
                        else:
                            compareSides(x, y, TileType.DBL_WALL, includeTop=False)
                    elif y == (self.height - 1):
                        if x == 0:
                            compareSides(x, y, TileType.DBL_WALL, includeBottom=False, includeLeft=False)
                        if x == (self.width - 1):
                            compareSides(x, y, TileType.DBL_WALL, includeBottom=False, includeRight=False)
                        else:
                            compareSides(x, y, TileType.DBL_WALL, includeBottom=False)
                    else:
                        compareSides(x, y, TileType.DBL_WALL)

    def __getitem__(self, item):
        return self._map[item]
