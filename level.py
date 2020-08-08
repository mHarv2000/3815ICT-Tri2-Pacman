import numpy as np

from consts import *
from tile import Tile


class Grid:

    def __init__(self):
        self.__xAxis = np.linspace(0, WINDOW_TILE_WIDTH - 1, WINDOW_TILE_HEIGHT, dtype=np.int16)
        self.__yAxis = np.linspace(0, WINDOW_TILE_WIDTH - 1, WINDOW_TILE_WIDTH, dtype=np.int16)
        self.__coords = [[(y, x) for x in self.__xAxis] for y in self.__yAxis]

    def __iter__(self):
        return iter(self.__coords)

    def __getitem__(self, item):
        if isinstance(item, int):
            if item <= (WINDOW_TILE_WIDTH - 1):
                return self.__coords[item]
            else:
                assert IndexError, f"coordinate of {item} is out of range, x must be between " \
                                   f"0-{self.__width} and y 0-{self.__height}"
        elif isinstance(item, slice):
            if item.stop <= (WINDOW_TILE_WIDTH - 1):
                return self.__coords[item]
        else:
            assert TypeError, "coordinate index must be an int in the form: coord[int] or coord[int][int]"


class TileMap:
    """
    Grid
    ----

    The grid class is in charge of generating the position, properties, attributes and order of each
    tile within the scene.
    """

    def __init__(self, genType):
        self.__genType = genType
        self.__data = STATIC_LEVEL

        self.__grid = Grid()
        self.__tiles = [[Tile(pos, (pos[0] * TILE_SIZE, pos[1] * TILE_SIZE)) for pos in row] for row in self.__grid]

        self.__gen_map()
        self.__correct_walls()

    def __gen_map(self):
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
        if self.__genType == GenType.SQUAREGRID:
            for y, column in enumerate(STATIC_LEVEL):
                for x, value in enumerate(column):
                    if value == ' ':
                        self.__tiles[x][y].tile_id = TileID.BLANK
                    elif value == '!':
                        self.__tiles[x][y].tile_type = TileType.DBL_WALL
                        self.__tiles[x][y].tile_id = TileID.DBL_WALL_V
                    elif value == '=':
                        self.__tiles[x][y].tile_type = TileType.DBL_WALL
                        self.__tiles[x][y].tile_id = TileID.DBL_WALL_H
                    elif value == 'o':
                        self.__tiles[x][y].tile_type = TileType.DBL_CORNER
                    elif value == '|':
                        self.__tiles[x][y].tile_type = TileType.WALL
                        self.__tiles[x][y].tile_id = TileID.WALL_V
                    elif value == '-':
                        self.__tiles[x][y].tile_type = TileType.WALL
                        self.__tiles[x][y].tile_id = TileID.WALL_H
                    elif value == '+':
                        self.__tiles[x][y].tile_type = TileType.DBL_CORNER
                    elif value == '.':
                        self.__tiles[x][y].tile_id = TileID.FRUIT
                    elif value == '*':
                        self.__tiles[x][y].tile_id = TileID.ENERGIZER
                    elif value == 'c':
                        self.__tiles[x][y].tile_id = TileID.CHERRY
                    elif value == 'd':
                        self.__tiles[x][y].tile_type = TileType.DOOR

            self.width = len(self.__tiles)
            self.height = len(self.__tiles[0])

    def index_range(func):
        """
        Check if adjacent tiles to the current coordinate are out of range of the
        index

        If so, append a bitwise flag for up to 4 bits (0-15) to determine
        which sides should/should not be included.

            NSEW
            ----
            0000 - None
            0001 - W
            0010 - E
            0011 - EW
            0100 - S
            0101 - SW
            0110 - SE
            0111 - SEW
            1000 - N
            1001 - NW
            1010 - NE
            1011 - NEW
            1100 - NS
            1101 - NSW
            1110 - NSE
            1111 - ALL

        :return: wrapper function
        """

        def wrapper(self, tile, *args, **kwargs):

            coord = tile.pos if tile else None
            if not coord:
                assert ValueError, "'include_direction' key word not in function parameters"

            include_adjacent = 0b1111

            if coord[0] == 0:
                if coord[1] == 0:
                    include_adjacent = 0b0110
                elif coord[1] == (WINDOW_TILE_HEIGHT - 1):
                    include_adjacent = 0b1010
                else:
                    include_adjacent = 0b0111
            elif coord[1] == 0:
                if coord[0] == 0:
                    include_adjacent = 0b0110
                elif coord[0] == (WINDOW_TILE_HEIGHT - 1):
                    include_adjacent = 0b0101
                else:
                    include_adjacent = 0b1110
            elif coord[0] == (WINDOW_TILE_WIDTH - 1):
                if coord[1] == 0:
                    include_adjacent = 0b0101
                elif coord[1] == (WINDOW_TILE_HEIGHT - 1):
                    include_adjacent = 0b1001
                else:
                    include_adjacent = 0b1101
            elif coord[1] == (WINDOW_TILE_WIDTH - 1):
                if coord[0] == 0:
                    include_adjacent = 0b1010
                elif coord[0] == (WINDOW_TILE_HEIGHT - 1):
                    include_adjacent = 0b1001
                else:
                    include_adjacent = 0b1011
            else:
                assert Exception, "tile is invalid, coordinates do not match any grid value"

            func(include_adjacent=include_adjacent)

        return wrapper

    @index_range
    def __correct_dbl_wall(self, tile, include_adjacent=None):

        x = tile[0]
        y = tile[1]

        if include_adjacent == 0b1111:  # ALL
            # TODO: fix
            pass
        elif include_adjacent == 0b0011:  # EW
            tile.tile_id = TileID.DBL_WALL_H
        elif include_adjacent == 0b0101:  # SW
            tile.tile_id = TileID.DBL_WALL_BL
        elif include_adjacent == 0b0110:  # SE
            tile.tile_id = TileID.DBL_WALL_BR
        elif include_adjacent == 0b0111:  # SEW
            if self.__tiles[x - 1][y].tile_type == TileType.DBL_WALL \
                    and self.__tiles[x][y + 1].tile_type == TileType.DBL_WALL:
                tile.tile_id = TileID.DBL_WALL_TR
            elif self.__tiles[x + 1][y].tile_type == TileType.DBL_WALL \
                    and self.__tiles[x][y + 1].tile_type == TileType.DBL_WALL:
                tile.tile_id = TileID.DBL_WALL_TL
            elif self.__tiles[x + 1][y].tile_type == TileType.DBL_WALL \
                    and self.__tiles[x - 1][y].tile_type == TileType.DBL_WALL:
                tile.tile_id = TileID.DBL_WALL_H
        elif include_adjacent == 0b1001:  # NW
            tile.tile_id = TileID.DBL_WALL_TL
        elif include_adjacent == 0b1010:  # NE
            tile.tile_id = TileID.DBL_WALL_TR
        elif include_adjacent == 0b1011:  # NEW
            if self.__tiles[x - 1][y].tile_type == TileType.DBL_WALL \
                    and self.__tiles[x][y - 1].tile_type == TileType.DBL_WALL:
                tile.tile_id = TileID.DBL_WALL_BR
            elif self.__tiles[x + 1][y].tile_type == TileType.DBL_WALL \
                    and self.__tiles[x][y - 1].tile_type == TileType.DBL_WALL:
                tile.tile_id = TileID.DBL_WALL_BL
            elif self.__tiles[x + 1][y].tile_type == TileType.DBL_WALL \
                    and self.__tiles[x - 1][y].tile_type == TileType.DBL_WALL:
                tile.tile_id = TileID.DBL_WALL_H
        elif include_adjacent == 0b1100:  # NS
            tile.tile_id = TileID.DBL_WALL_V
        elif include_adjacent == 0b1101:  # NSW
            if self.__tiles[x - 1][y].tile_type == TileType.DBL_WALL \
                    and self.__tiles[x][y - 1].tile_type == TileType.DBL_WALL:
                tile.tile_id = TileID.DBL_WALL_BR
            elif self.__tiles[x - 1][y].tile_type == TileType.DBL_WALL \
                    and self.__tiles[x][y + 1].tile_type == TileType.DBL_WALL:
                tile.tile_id = TileID.DBL_WALL_TR
            elif self.__tiles[x][y + 1].tile_type == TileType.DBL_WALL \
                    and self.__tiles[x][y - 1].tile_type == TileType.DBL_WALL:
                tile.tile_id = TileID.DBL_WALL_V
        elif include_adjacent == 0b1110:  # NSE
            if self.__tiles[x + 1][y].tile_type == TileType.DBL_WALL \
                    and self.__tiles[x][y - 1].tile_type == TileType.DBL_WALL:
                tile.tile_id = TileID.DBL_WALL_TL
            elif self.__tiles[x - 1][y].tile_type == TileType.DBL_WALL \
                    and self.__tiles[x][y + 1].tile_type == TileType.DBL_WALL:
                tile.tile_id = TileID.DBL_WALL_TR
            elif self.__tiles[x][y + 1].tile_type == TileType.DBL_WALL \
                    and self.__tiles[x][y - 1].tile_type == TileType.DBL_WALL:
                tile.tile_id = TileID.DBL_WALL_V

        return tile

    def __gen_tile_ids(self):
        """
        Generate tile IDs for each tile based on the elements of the map and how each tile
        is positioned against each other.
        :return:
        """
        for y, rows in self.__tiles:
            for x, tile in rows:
                if tile.tile_type == TileType.DBL_WALL:
                    self.__tiles[x][y] = self.__correct_dbl_wall(tile)

    def __iter__(self):
        return iter(self.__tiles)

    def __getitem__(self, item):
        if isinstance(item, int):
            if item <= (WINDOW_TILE_WIDTH - 1):
                return self.__tiles[item]
            else:
                assert IndexError, f"coordinate of {item} is out of range, x must be between " \
                                   f"0-{WINDOW_TILE_WIDTH} and y 0-{WINDOW_TILE_HEIGHT}"
        elif isinstance(item, slice):
            if item.stop <= (WINDOW_TILE_WIDTH - 1):
                return self.__tiles[item]
            else:
                assert IndexError, f"coordinate of {item} is out of range, x must be between " \
                                   f"0-{WINDOW_TILE_WIDTH} and y 0-{WINDOW_TILE_HEIGHT}"
        else:
            assert TypeError, "coordinate index must be an int in the form: coord[int] or coord[int][int]"



x = None
def setX(func: ()):
    global x
    x = func

setX(lambda x: x * 10)
print(x(10))