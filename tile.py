import math
import pygame
from consts import TileType, TileID, TileAttr, TILE_SIZE


class Tile:

    def __init__(self, pos: tuple, grid_pos: tuple, tile_type: TileType = None,
                 tile_id: TileID = None, tile_attr: TileAttr = None):
        self.__pos = pos
        self.__grid_pos = grid_pos
        self.__center = [pos[0] + float(TILE_SIZE / 2),
                         pos[1] + float(TILE_SIZE / 2)]
        self.rect = pygame.Rect(pos, (TILE_SIZE, TILE_SIZE))
        self.tile_type = tile_type
        self.tile_id = tile_id
        self.tile_attr = tile_attr

    @property
    def x(self):
        return self.__grid_pos[0]

    @property
    def y(self):
        return self.__grid_pos[1]

    @property
    def pos(self):
        return self.__pos

    @property
    def center(self):
        return self.__center

    def distance(self, other):
        x = math.pow(other.center[0] - self.center[0], 2)
        y = math.pow(other.center[1] - self.center[1], 2)
        return math.sqrt(x + y)

    def __getitem__(self, item):
        if item == (0 or 1):
            return self.__pos[item]

    def __repr__(self):
        return f"<{self.tile_type} ({self.tile_id}) at {self.__pos} ({self.__grid_pos})>"

    def __eq__(self, other):
        return self.tile_type == other
