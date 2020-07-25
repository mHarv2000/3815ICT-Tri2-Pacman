# vars
SCREEN_WIDTH = 500   # window width in pixels
SCREEN_HEIGHT = 500      # window height in pixels
MAX_SCENE_TILE_WIDTH = 28    # height of scene in tiles
MAX_SCENE_TILE_HEIGHT = 36     # width of scene in tiles

TILE_SIZE = int(SCREEN_WIDTH / (MAX_SCENE_TILE_HEIGHT - 5))
SCENE_WIDTH = MAX_SCENE_TILE_WIDTH * TILE_SIZE
# scene height = SCREEN_HEIGHT

ORIGIN = (int(SCREEN_WIDTH / 2) - int(SCENE_WIDTH / 2), 0)

# flags
SQUAREGRID = 0x00   # square grid
HEXGRID = 0x01  # hexagonal grid
RANDGRID = 0x02     # arbitrary grid
TILE_BLANK = 0x03   # blank tile
TILE_DBL_WALL_TL = 0x04     # double wall top-left tile
TILE_DBL_WALL_TR = 0x05     # double wall top-right tile
TILE_DBL_WALL_BR = 0x06     # double wall bottom_right tile
TILE_DBL_WALL_BL = 0x07     # double wall bottom-left tile
TILE_DBL_WALL_H = 0x08  # double wall horizontal tile
TILE_DBL_WALL_V = 0x09  # double wall vertical tile
TILE_WALL_TL = 0x0a     # wall top-left tile
TILE_WALL_TR = 0x0b     # wall top-right tile
TILE_WALL_BR = 0x0c     # wall bottom-right tile
TILE_WALL_BL = 0x0d     # wall bottom-left tile
TILE_WALL_H = 0x0e  # wall horizontal tile
TILE_WALL_V = 0x0f  # wall vertical tile
TILE_FRUIT = 0x10   # fruit tile
TILE_ENERGIZER = 0x11   # energizer tile
TILE_DOOR = 0x12    # door tile
