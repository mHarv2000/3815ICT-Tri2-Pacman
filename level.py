import json
import os
from typing import NewType, List, Type, Union

import pygame
import math
from consts import *
import re
from tile import Tile


# list of Tile objects for rows OR columns
Edge = NewType('Edge', [int, int])
# 2D list of Tile objects for both rows AND columns
Area = NewType('Area', List[Union[Tile, List[Tile]]])


class Grid:
    map: list = [[]]

    def __init__(self, genType, levelFile: str = None):
        self.genType = genType
        if levelFile is not None and os.path.exists(levelFile):
            with open(levelFile, 'r') as file:
                self.data = json.load(file)
        self.genGrid()
        self.correctWalls()

    def genGrid(self, levelNo=0):
        if self.genType == GenType.SQUAREGRID:
            if levelNo == 0:
                for ri, row in enumerate(self.data['staticLevel']):
                    self.map.append([])
                    for ci, val in enumerate(row):
                        if val == '.':
                            self.map[ri].append(Tile(
                                ri, ci, ri * TILE_SIZE, ci * TILE_SIZE,
                                TileType.TILE_BLANK
                            ))
                        elif val == '0':
                            self.map[ri].append(Tile(
                                ri, ci, ri * TILE_SIZE, ci * TILE_SIZE,
                                TileType.TILE_DBL_WALL
                            ))
                        elif val == '1':
                            self.map[ri].append(Tile(
                                ri, ci, ri * TILE_SIZE, ci * TILE_SIZE,
                                TileType.TILE_WALL
                            ))
                        elif val == '-':
                            self.map[ri].append(Tile(
                                ri, ci, ri * TILE_SIZE, ci * TILE_SIZE,
                                TileType.TILE_FRUIT
                            ))

    def correctWalls(self):

        def checkTR(x, y):
            if self.map[x][y - 1].tileType == TileType.TILE_DBL_WALL and \
                    self.map[x + 1][y].tileType == TileType.TILE_DBL_WALL:
                return TileType.TILE_DBL_WALL_BL
            else:
                assert ValueError, f"something wrong with coordinate ({x}, {y})"

        def checkTL(x, y):
            if self.map[x][y - 1].tileType == TileType.TILE_DBL_WALL and \
                    self.map[x - 1][y].tileType == TileType.TILE_DBL_WALL:
                return TileType.TILE_DBL_WALL_BR
            else:
                assert ValueError, f"something wrong with coordinate ({x}, {y})"

        def checkBR(x, y):
            print(f"vals are {x}, {y}")
            if self.map[x][y + 1].tileType == TileType.TILE_DBL_WALL and \
                    self.map[x + 1][y].tileType == TileType.TILE_DBL_WALL:
                return TileType.TILE_DBL_WALL_TL
            else:
                assert ValueError, f"something wrong with coordinate ({x}, {y})"

        def checkBL(x, y):
            if self.map[x][y + 1].tileType == TileType.TILE_DBL_WALL and \
                    self.map[x - 1][y].tileType == TileType.TILE_DBL_WALL:
                return TileType.TILE_DBL_WALL_TR
            else:
                assert ValueError, f"something wrong with coordinate ({x}, {y})"

        def checkH(x, y):
            if self.map[x - 1][y].tileType == TileType.TILE_DBL_WALL and \
                    self.map[x + 1][y].tileType == TileType.TILE_DBL_WALL:
                return TileType.TILE_DBL_WALL_H
            else:
                assert ValueError, f"something wrong with coordinate ({x}, {y})"

        def checkV(x, y):
            if self.map[x][y-1].tileType == TileType.TILE_DBL_WALL and \
                    self.map[x][y+1].tileType == TileType.TILE_DBL_WALL:
                return TileType.TILE_DBL_WALL_V
            else:
                assert ValueError, f"something wrong with coordinate ({x}, {y})"

        MW = MAX_SCENE_TILE_HEIGHT - 6
        MH = MAX_SCENE_TILE_WIDTH - 1
        print(MW, MH)
        for x, row in enumerate(self.map):
            for y, tile in enumerate(self.map[x]):
                if x == 0:
                    if y == 0:
                        checkBR(x, y)
                    if y == MH:
                        checkTR(x, y)
                    if y != 0 and y != MH:
                        checkBR(x, y)
                        checkTR(x, y)
                        checkV(x, y)
                if x == MW:
                    if y == 0:
                        checkBL(x, y)
                    if y == MH:
                        checkTL(x, y)
                    if y != 0 and y != MH:
                        checkBL(x, y)
                        checkTL(x, y)
                        checkV(x, y)
                if x != 0 and x != MW:
                    if y == 0:
                        checkBR(x, y)
                        checkBL(x, y)
                        checkH(x, y)
                    if y == MH:
                        checkTR(x, y)
                        checkTL(x, y)
                        checkH(x, y)
                    if y != 0 and y != MH:
                        checkTR(x, y)
                        checkTL(x, y)
                        checkBR(x, y)
                        checkBL(x, y)
                        checkH(x, y)
                        checkV(x, y)

    def selectSubRow(self, row: int, start: int, end: int) -> Edge:
        """
        Select a row of tiles
        :param row: the y-axis
        :param start: the starting x-axis index
        :param end: the end x-axis index
        :return: an area of the selected tiles
        """
        return self.map[row][start:end + 1]

    def selectSubCol(self, col: int, start: int, end: int) -> Edge:
        """
        Select a column of tiles
        :param col: the x-axis
        :param start: the starting y-axis index
        :param end: the end y-axis index
        :return: an area of the selected tiles
        """
        return [row[col] for i, row in enumerate(self.map) if start <= i <= end]

    def selectArea(self, start_pos, end_pos) -> Area:
        area = []
        for i, row in enumerate(self.map):
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
        return self.map[item]


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
            quit(0)

    pygame.display.flip()
