import json
import os
from enum import Enum, unique


@unique
class GenType(Enum):
    """
    Determines what type of tile-map the game will use
    SQUAREGRID  A grid full of square tiles with a simple coordinate system and requires keyboard support for basic
                up-down-left-right movement
    HEXGRID     Similar to the square grid but with hexagon tiles where every second coordinate on the x-axis is placed
                lower on the y-axis by half the size of the tile and vice-versa with the y-axis.
    RANDGRID    An arbitrary graph format where each path branches out in random directions and does not rely on tiles.
                The grid however extends a basic coordinate system and requires mouse support to move the PacMan object

    """
    SQUAREGRID = 0  # square grid
    HEXGRID = 1  # hexagonal grid
    RANDGRID = 2  # arbitrary grid


@unique
class TileType(Enum):
    """
    A generic label given to each tile to organise the tiles and help tell which tiles need a specific ID generated.
    """
    NONE = 0
    WALL = 1
    DBL_WALL = 2
    DOOR = 3
    OTHER = 4


@unique
class TileID(Enum):
    """
    A specific label given to each tile to tell the game exactly what the tile is.
    """
    BLANK = 0  # blank tile
    DBL_WALL_TL = 1  # double wall top-left tile
    DBL_WALL_TR = 2  # double wall top-right tile
    DBL_WALL_BR = 3  # double wall bottom_right tile
    DBL_WALL_BL = 4  # double wall bottom-left tile
    DBL_WALL_H = 5  # double wall horizontal tile
    DBL_WALL_V = 6  # double wall vertical tile
    WALL_TL = 7  # wall top-left tile
    WALL_TR = 8  # wall top-right tile
    WALL_BR = 9  # wall bottom-right tile
    WALL_BL = 10  # wall bottom-left tile
    WALL_H = 11  # wall horizontal tile
    WALL_V = 12  # wall vertical tile
    FRUIT = 13  # fruit tile
    ENERGIZER = 14  # energizer tile
    CHERRY = 15  # cherry tile
    DOOR_H = 16  # door horizontal tile
    DOOR_V = 17  # door vertical tile


@unique
class TileAttr(Enum):
    """
    An attribute given to tile objects to help with path-finding
    """
    PACMAN_SPAWN = 0
    GHOST_SPAWN = 1
    GHOST_FLEE = 2
