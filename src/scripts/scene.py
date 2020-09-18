import json
import os
from typing import Tuple
import pygame
from src.scripts.ai import PacMan, Ghost
from src.scripts.consts import GenType, TileAttr, TileID


class Tile:
    """
    A cell representing a physical coordinate on the scene plane.

    Each tile has a tile type to identify it's generic type, an ID to identify it's specific type and an
    Attribute to help with AI pathfinding. The Tile represents a physical local coordinate on the grid that is either
    transversable (player can walk on) or non-transversable.
    """

    def __init__(self, lx: int, ly: int, gx: int, gy: int, tile_size: int, tile_type: TileType = None,
                 tile_id: TileID = None, tile_attr: TileAttr = None):
        """
        :param lx: x local coordinate
        :type lx: int
        :param ly: y local coordinate
        :type ly: int
        :param gx: x grid coordinate
        :type gx: int
        :param gy: y grid coordinate
        :type gy: int
        :param tile_size: size of the tile
        :type tile_size: int
        :param tile_type: type of tile
        :type tile_type: TileType
        :param tile_id: exact type of tile
        :type tile_id: TileID
        :param tile_attr: an attribute describing the tile
        :type tile_attr: TileAttr
        """
        self.__pos = lx, ly
        self.__grid_pos = gx, gy
        self.__tile_type = tile_type
        self.__tile_id = tile_id
        self.__tile_attr = tile_attr
        self.rect = pygame.Rect((gx, gy), (tile_size, tile_size))

    @property
    def lx(self) -> int:
        """ get current grid position's x coordinate """
        return self.__pos[0]

    @property
    def ly(self) -> int:
        """ get current grid position's y coordinate """
        return self.__pos[1]

    @property
    def pos(self) -> Tuple[ int, int ]:
        """ get current local position """
        return self.__pos

    @property
    def gx(self) -> int:
        """ get current grid position's x coordinate """
        return self.__grid_pos[0]

    @property
    def gy(self) -> int:
        """ get current grid position's y coordinate """
        return self.__grid_pos[1]

    @property
    def gpos(self) -> Tuple[int, int]:
        """ get current grid position """
        return self.__grid_pos

    @property
    def type(self) -> TileType:
        """ get tile type """
        return self.__tile_type

    @property
    def id(self) -> TileID:
        """ get tile ID """
        return self.__tile_id

    @property
    def attr(self) -> TileAttr:
        """ get tile attribute """
        return self.__tile_attr

    def compare_type(self, other) -> bool:
        """
        compare Tile type
        :param other: Tile object
        :type other: Tile
        :returns: True/False
        """
        if not isinstance(other, Tile):
            raise TypeError("other must be a Tile Object")
        return self.__tile_type == other.__tile_type

    def compare_id(self, other) -> bool:
        """
        compare Tile ID
        :param other: Tile object
        :type other: Tile
        :returns: True/False
        """
        if not isinstance(other, Tile):
            raise TypeError("other must be a Tile Object")
        return self.__tile_id == other.__tile_id

    def compare_attr(self, other) -> bool:
        """
        compare Tile attribute
        :param other: Tile object
        :type other: Tile
        :returns: True/False
        """
        if not isinstance(other, Tile):
            raise TypeError("other must be a Tile Object")
        return self.__tile_attr == other.__tile_attr

    def __repr__(self):
        """ representation of the object when called """
        return f"<{self.__tile_type} ({self.__tile_id}) at {self.__pos} ({self.__grid_pos})>"




