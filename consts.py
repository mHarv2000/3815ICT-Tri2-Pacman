import json
from enum import Enum, unique
from typing import NewType

data = []

with open('src/data/data.json', 'r') as file:
    data = json.load(file)

# Unique data types
# X and Y Axis Coordinate [x, y]
Coord = NewType('Coord', [int, int])
# more precise coordinate [x.00..., y.00...]
Point = NewType('Point', [float, float])

IS_FULLSCREEN = data['fullscreen']
DIFFICULTY_STEP = data['levelDifficultyStep']
SIZE_SCALE_PER_STEP = data['levelSizeScalePerStep']
STATIC_LEVEL = data['staticLevel']

# vars
WINDOW_WIDTH = 500   # window width in pixels
WINDOW_HEIGHT = 500      # window height in pixels
WINDOW_TILE_WIDTH = data['tileWidth']
WINDOW_TILE_HEIGHT = data['tileHeight']

TILE_SIZE = WINDOW_HEIGHT // (WINDOW_TILE_HEIGHT + 5)
SCENE_WIDTH = int(TILE_SIZE * WINDOW_TILE_WIDTH)
# scene height = SCREEN_HEIGHT

ORIGIN = (int(SCENE_WIDTH / 2) - int(SCENE_WIDTH / 2), 0)
FPS = 15

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


@unique
class GenType(Enum):

    SQUAREGRID = 0  # square grid
    HEXGRID = 1  # hexagonal grid
    RANDGRID = 2  # arbitrary grid


@unique
class TileType(Enum):

    DBL_WALL = 0
    WALL = 1
    CORNER = 2
    DBL_CORNER = 3
    DOOR = 4


@unique
class TileID(Enum):

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
    CHERRY = 15
    DOOR_H = 16  # door tile
    DOOR_V = 17


@unique
class TileAttr(Enum):

    GHOST_SPAWN = 0
    GHOST_FLEE = 1


@unique
class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

