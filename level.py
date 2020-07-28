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

    map: list

    def __init__(self, genType, levelFile: str = None):
        self.genType = genType
        if levelFile is not None and os.path.exists(levelFile):
            with open(levelFile, 'r') as file:
                self.data = json.load(file)
        self.gen_map()
        self.correct_walls()

    def checkH(self, x, y):
        return self.map[x - 1][y].tileType == TileType.DBL_WALL and \
                self.map[x + 1][y].tileType == TileType.DBL_WALL

    def checkV(self, x, y):
        return self.map[x][y - 1].tileType == TileType.DBL_WALL and \
                self.map[x][y + 1].tileType == TileType.DBL_WALL

    def gen_map(self):
        if self.genType == GenType.SQUAREGRID:
            self.map = [[] for x in range(MAX_SCENE_TILE_WIDTH)]
            for y, column in enumerate(self.data['staticLevel']):
                for x, value in enumerate(column):
                    if value == ' ':
                        self.map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileId=TileID.BLANK))
                    elif value == '!':
                        self.map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileType=TileType.DBL_WALL, tileId=TileID.DBL_WALL_V))
                    elif value == '=':
                        self.map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileType=TileType.DBL_WALL, tileId=TileID.DBL_WALL_H))
                    elif value == 'o':
                        self.map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileType=TileType.DBL_CORNER))
                    elif value == '|':
                        self.map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileType=TileType.WALL, tileId=TileID.WALL_V))
                    elif value == '-':
                        self.map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileType=TileType.WALL, tileId=TileID.WALL_H))
                    elif value == '+':
                        self.map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileType=TileType.CORNER))
                    elif value == '.':
                        self.map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileId=TileID.FRUIT))
                    elif value == '*':
                        self.map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileId=TileID.ENERGIZER))
                    elif value == 'c':
                        self.map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileId=TileID.CHERRY))
                    elif value == 'd':
                        self.map[x].append(Tile(x, y, x * TILE_SIZE, y * TILE_SIZE, tileType=TileType.DOOR))

            self.width = len(self.map)
            self.height = len(self.map[0])

    def correct_walls(self):

        def update_corner_tl(x: int, y: int, tile_type: TileType):
            """
            Check if tile should become a top left corner
            :param x: x coordinate
            :param y: y coordinate
            :param tile_type: the generic type of the tile being compared to, only TileType formats are accepted
            """
            if self.map[x][y + 1].tileId == TileID.DBL_WALL_V and self.map[x + 1][y].tileId == TileID.DBL_WALL_H:
                self.map[x][y].tileId = TileID.DBL_WALL_TL
                self.map[x][y].rect = pygame.Rect(
                    (self.map[x][y].x + int(TILE_SIZE / 2), self.map[x][y].y + int(TILE_SIZE / 2)),
                    (TILE_SIZE, TILE_SIZE))

        def update_corner_tr(x: int, y: int, tile_type: TileType):
            """
            Check if tile should become a top right corner
            :param x: x coordinate
            :param y: y coordinate
            :param tile_type: the generic type of the tile being compared to, only TileType formats are accepted
            """
            if self.map[x][y + 1].tileId == TileID.DBL_WALL_V and self.map[x - 1][y].tileId == TileID.DBL_WALL_H:
                self.map[x][y].tileId = TileID.DBL_WALL_TR
                self.map[x][y].rect = pygame.Rect(
                    (self.map[x][y].x - int(TILE_SIZE / 2), self.map[x][y].y + int(TILE_SIZE / 2)),
                    (TILE_SIZE, TILE_SIZE))

        def update_corner_bl(x: int, y: int, tile_type: TileType):
            """
            Check if tile should become a bottom left corner
            :param x: x coordinate
            :param y: y coordinate
            :param tile_type: the generic type of the tile being compared to, only TileType formats are accepted
            """
            if self.map[x][y - 1].tileId == TileID.DBL_WALL_V and self.map[x + 1][y].tileId == TileID.DBL_WALL_H:
                self.map[x][y].tileId = TileID.DBL_WALL_BL
                self.map[x][y].rect = pygame.Rect(
                    (self.map[x][y].x + int(TILE_SIZE / 2), self.map[x][y].y - int(TILE_SIZE / 2)),
                    (TILE_SIZE, TILE_SIZE))

        def update_corner_br(x: int, y: int, tile_type: TileType):
            """
            Check if tile should become a bottom right corner and then update the tile's `tileId` to
            match the corner id and then add a physical boundary box
            :param x: x coordinate
            :param y: y coordinate
            :param tile_type: the generic type of the tile being compared to, only TileType formats are accepted
            """
            if self.map[x][y - 1].tileId == TileID.DBL_WALL_V and self.map[x - 1][y].tileId == TileID.DBL_WALL_H:
                self.map[x][y].tileId = TileID.DBL_WALL_BR
                self.map[x][y].rect = pygame.Rect(
                    (self.map[x][y].x - int(TILE_SIZE / 2), self.map[x][y].y - int(TILE_SIZE / 2)),
                    (TILE_SIZE, TILE_SIZE))

        def compareSides(x: int, y: int, tileType: TileType, includeTop: bool = False, includeLeft: bool = False,
                         includeBottom: bool = False, includeRight: bool = False):

            top = self.map[x][y - 1].tileId == TileID.DBL_WALL_V if includeTop else False
            left = self.map[x - 1][y].tileId == TileID.DBL_WALL_H if includeLeft else False
            bottom = self.map[x][y + 1].tileId == TileID.DBL_WALL_V if includeBottom else False
            right = self.map[x + 1][y].tileId == TileID.DBL_WALL_H if includeRight else False

            if top and left:
                update_corner_br(x, y, tileType)
            if top and right:
                update_corner_bl(x, y, tileType)
            if bottom and left:
                update_corner_tr(x, y, tileType)
            if bottom and right:
                update_corner_tl(x, y, tileType)

        for x, row in enumerate(self.map):
            for y, tile in enumerate(row):
                if tile == TileType.DBL_CORNER:

                    if x == 0:
                        if y == 0:
                            compareSides(x, y, TileType.DBL_WALL, includeTop=False, includeLeft=False)
                        if y == (self.height - 1):
                            compareSides(x, y, TileType.DBL_WALL, includeBottom=False, includeLeft=False)
                    elif x == (self.width - 1):
                        if y == 0:
                            compareSides(x, y, TileType.DBL_WALL, includeTop=False, includeRight=False)
                        if y == (self.height - 1):
                            compareSides(x, y, TileType.DBL_WALL, includeBottom=False, includeLeft=False)
                    elif y == 0:
                        if x == 0:
                            compareSides(x, y, TileType.DBL_WALL, includeTop=False, includeLeft=False)
                        if x == (self.width - 1):
                            compareSides(x, y, TileType.DBL_WALL, includeTop=False, includeRight=False)
                    elif y == (self.height - 1):
                        if x == 0:
                            compareSides(x, y, TileType.DBL_WALL, includeBottom=False, includeLeft=False)
                        if x == (self.width - 1):
                            compareSides(x, y, TileType.DBL_WALL, includeBottom=False, includeRight=False)
                    else:
                        compareSides(x, y, TileType.DBL_WALL, True, True, True, True)


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
print(*grid[0], sep='\n')
while True:
    clock.tick(5)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)

    for row in grid.map:
        for tile in row:


            if tile.tileId == TileID.DBL_WALL_TL:
                pygame.draw.arc(main_screen, BLUE, tile.rect, math.pi*.5, math.pi, 1)
                pygame.draw.rect(main_screen, RED, tile.rect, 1)
            elif tile.tileId == TileID.DBL_WALL_TR:
                pygame.draw.arc(main_screen, BLUE, tile.rect, 0, math.pi*.5, 1)
                pygame.draw.rect(main_screen, RED, tile.rect, 1)
            elif tile.tileId == TileID.DBL_WALL_BR:
                pygame.draw.arc(main_screen, BLUE, tile.rect, math.pi*1.5, math.pi*2, 1)
                pygame.draw.rect(main_screen, RED, tile.rect, 1)
            elif tile.tileId == TileID.DBL_WALL_BL:
                pygame.draw.arc(main_screen, BLUE, tile.rect, math.pi, math.pi*1.5, 1)
                pygame.draw.rect(main_screen, RED, tile.rect, 1)
            elif tile.tileId == TileID.DBL_WALL_H:
                pygame.draw.line(main_screen, BLUE,
                                 [tile.x, tile.y + int(TILE_SIZE / 2)],
                                 [tile.x + TILE_SIZE, tile.y + int(TILE_SIZE / 2)])
            elif tile.tileId == TileID.DBL_WALL_V:
                pygame.draw.line(main_screen, BLUE,
                                 [tile.x + int(TILE_SIZE / 2), tile.y],
                                 [tile.x + int(TILE_SIZE / 2), tile.y + TILE_SIZE])

    pygame.display.flip()
