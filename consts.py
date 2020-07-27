from enum import Enum, unique
from typing import NewType

# Unique data types
# X and Y Axis Coordinate [x, y]
Coord = NewType('Coord', [int, int])
# more precise coordinate [x.00..., y.00...]
Point = NewType('Point', [float, float])

# vars
SCREEN_WIDTH = 500   # window width in pixels
SCREEN_HEIGHT = 500      # window height in pixels
MAX_SCENE_TILE_WIDTH = 28    # height of scene in tiles
MAX_SCENE_TILE_HEIGHT = 36     # width of scene in tiles

TILE_SIZE = int(SCREEN_WIDTH / (MAX_SCENE_TILE_HEIGHT - 5))
SCENE_WIDTH = MAX_SCENE_TILE_WIDTH * TILE_SIZE
# scene height = SCREEN_HEIGHT

ORIGIN = (int(SCREEN_WIDTH / 2) - int(SCENE_WIDTH / 2), 0)

BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

@unique
class GenType(Enum):
    SQUAREGRID = 0  # square grid
    HEXGRID = 1  # hexagonal grid
    RANDGRID = 2  # arbitrary grid


@unique
class TileType(Enum):
    TILE_BLANK = 0   # blank tile
    TILE_DBL_WALL = 1
    TILE_WALL = 2
    TILE_DOOR = 3

    TILE_DBL_WALL_TL = 4     # double wall top-left tile
    TILE_DBL_WALL_TR = 5     # double wall top-right tile
    TILE_DBL_WALL_BR = 6     # double wall bottom_right tile
    TILE_DBL_WALL_BL = 7     # double wall bottom-left tile
    TILE_DBL_WALL_H = 8  # double wall horizontal tile
    TILE_DBL_WALL_V = 9  # double wall vertical tile
    TILE_WALL_TL = 10     # wall top-left tile
    TILE_WALL_TR = 11     # wall top-right tile
    TILE_WALL_BR = 12     # wall bottom-right tile
    TILE_WALL_BL = 13     # wall bottom-left tile
    TILE_WALL_H = 14  # wall horizontal tile
    TILE_WALL_V = 15  # wall vertical tile
    TILE_FRUIT = 16   # fruit tile
    TILE_ENERGIZER = 17   # energizer tile
    TILE_CHERRY = 18
    TILE_DOOR_H = 19    # door tile
    TILE_DOOR_V = 20

    TILE_CORNER = 21
    TILE_GHOST_SPAWN = 22



@unique
class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3
