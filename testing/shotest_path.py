import json
import os
from collections import defaultdict
from queue import Queue

from src.scripts.consts import TileID, TileAttr
from src.scripts.misc import Direction


class Tile:
    """
    A cell representing a physical coordinate on the scene plane.

    Each tile has an ID to identify it's specific type and an Attribute to help with AI pathfinding.
    The Tile represents a physical local coordinate on the grid that is either transversable (player can walk on)
    or non-transversable.
    """
    def __init__(self, lx: int, ly: int, gx: int, gy: int, transversable: bool, tile_id: TileID = None,
                 tile_attr: TileAttr = None):
        self.__local_coords = lx, ly
        self.__global_coords = gx, gy
        self.__transverse = transversable
        self.__tile_id = tile_id
        self.__tile_attr = tile_attr

    def __repr__(self) -> str:
        return f'{self.__local_coords}, {self.__transverse}'

    def __int__(self) -> int:
        return 1

    def __radd__(self, other):
        return other + 1

    @property
    def lx(self) -> int:
        """ get local x-coordinate """
        return self.__local_coords[0]

    @property
    def ly(self) -> int:
        """ get local y-coordinate """
        return self.__local_coords[1]

    @property
    def lcoords(self) -> [int, int]:
        """ get local coordinates """
        return self.__local_coords

    @property
    def gx(self) -> int:
        """ get global x-coordinate """
        return self.__global_coords[0]

    @property
    def gy(self) -> int:
        """ get global y-coordinate """
        return self.__global_coords[1]

    @property
    def gcoords(self) -> [int, int]:
        """ get global scene coordinates """
        return self.__global_coords

    def is_transversible(self) -> bool:
        """ check whether tile can be walked on by pacman """
        return self.__transverse


class TileMap:
    """
    A coordinate system for the Pac Man scene containing a statically or dynamically generated
    square/hexagonal/random grid. Each tile is referencable through list indexing in the format
    [x, y] e.g. TileMap[0, 0]. Given a start and end coordinate, the map can find the shortest path
    between said points or find alternative tiles adjacent to a coordinate.

    The TileMap used local and global coordinates represented as lx, ly, gx, and gy.
    Global coordinates are physical coordinates within the window scene whereas local coordinates
    refer to a grid coordinate relative to the number of tiles in the grid. e.g. Tile 1, 2 is at 20, 40
    because the tile size is 20 therefore: lx = 1, ly = 2, gx = 20, gy = 40

    :param tile_size: size of each tile (width and height are the same)
    :type tile_size: int
    """
    def __init__(self, tile_size: int):
        self.tiles: [Tile] = []
        with open(os.path.abspath('../data/data.json'), 'r') as file:
            data = json.load(file)['staticLevel']
            for x, row in enumerate(data):
                self.tiles.append([])
                for y, tile in enumerate(row):
                    if tile == ' ':
                        self.tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, True, TileID.BLANK))
                    elif tile == '=':
                        self.tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, False, TileID.DBL_WALL))
                    elif tile == '-':
                        self.tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, False, TileID.WALL))
                    elif self.tiles == 'd':
                        self.tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, False, TileID.DOOR))
                    elif tile == '.':
                        self.tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, True, TileID.FRUIT))
                    elif tile == '*':
                        self.tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, True, TileID.ENERGIZER))
                    elif tile == 'p':
                        self.tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, True, TileID.BLANK,
                                                  TileAttr.PACMAN_SPAWN))
                    elif tile == 'c':
                        self.tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, True, TileID.CHERRY))
                    elif tile == 'g':
                        self.tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, True, TileID.BLANK,
                                                  TileAttr.GHOST_SPAWN))
        self.__lheight = len(self.tiles)
        self.__lwidth = len(self.tiles[0])
        self.__gheight = self.__lheight * tile_size
        self.__gwidth = self.__lwidth * tile_size

    def __getitem__(self, item: tuple):
        """ get tile at coordinates x, y """
        return self.tiles[item[1]][item[0]]

    def adjacent_tile(self, x: int, y: int, direction: Direction):
        if direction == 'n' and 0 < y < self.__lheight:
            return self[x, y - 1]
        elif direction == 's' and 0 <= y < (self.__lheight - 1):
            return self[x, y + 1]
        elif direction == 'e' and 0 <= x < (self.__lwidth - 1):
            return self[x + 1, y]
        elif direction == 'w' and 0 < x < self.__lwidth:
            return self[x - 1, y]
        else:
            return None

    def adjacent_tiles(self, x: int, y: int, exclude_direction: str = None):
        """
        Get adjacent tiles of a tile and return the tiles indexed by a compass character.
        :param x: x-local-coordinate of the initial tile
        :param y: y-local-coordinate of the initial tile
        :param exclude_direction: find all adjacent cells except in this direction
        :return:
        """

        directions = {'n', 's', 'e', 'w'}
        if exclude_direction is not None and exclude_direction in directions:
            directions.discard(exclude_direction)
        tiles = defaultdict()
        if 'n' in directions and 0 < y < self.__lheight:
            tile = self[x, y - 1]
            if tile.is_transversible():
                tiles['n'] = tile
        if 's' in directions and 0 <= y < (self.__lheight - 1):
            tile = self[x, y + 1]
            if tile.is_transversible():
                tiles['s'] = tile
        if 'e' in directions and 0 <= x < (self.__lwidth - 1):
            tile = self[x + 1, y]
            if tile.is_transversible():
                tiles['e'] = tile
        if 'w' in directions and 0 < x < self.__lwidth:
            tile = self[x - 1, y]
            if tile.is_transversible():
                tiles['w'] = tile

        return tiles

    def __gen_path(self, origin_x: int, origin_y: int, exclude_direction: str = None):
        """
        generate a singular path by finding a list of nodes along a path before it reaches an
        intersection i.e. the path ends once the final node/tile has more than one direction to travel in.
        :param origin_x: x-local-coordinate of the starting coordinate
        :param origin_y: y-local-coordinate of the starting coordinate
        :param exclude_direction:
        :return: yields tiles until end of path
        """
        origin = self[origin_x, origin_y]
        adjacent_tiles = self.adjacent_tiles(origin_x, origin_y, exclude_direction)
        for d, tile in adjacent_tiles.items():
            path = [origin, tile]
            while True:
                direction = Direction(d)
                next_tile = self.adjacent_tile(path[-1].lx, path[-1].ly, direction)

                if next_tile is not None and next_tile.is_transversible():
                    path.append(next_tile)

                    left_tile = self.adjacent_tile(path[-1].lx, path[-1].ly, direction - 1)
                    right_tile = self.adjacent_tile(path[-1].lx, path[-1].ly, direction + 1)
                    if left_tile is not None and left_tile.is_transversible():
                        path.append((direction - 2).orientation)
                        break
                    elif right_tile is not None and right_tile.is_transversible():
                        path.append((direction - 2).orientation)
                        break

                    continue
                path.append((direction - 2).orientation)
                break

            yield path

    def __gen_paths_to_target(self, start_coords: tuple, target_coords: tuple) -> [Tile]:
        """
        reorganise each available path on the grid to find the shortest path between
        the starting coordinate and target coordinate

        :param start_coords: starting coordinate
        :type start_coords: Tuple[int, int]
        :param target_coords: target coordinate
        :type target_coords: Tuple[int, int]
        :return: list of paths between the start and target point
        """
        start = self.__gen_path(*start_coords)
        paths = []
        temp_paths = Queue()
        for path in start:
            paths.append(path)
            temp_paths.put(path)

        target = self[target_coords[0], target_coords[1]]
        while not temp_paths.empty():
            prev_path = temp_paths.get()
            next_paths = self.__gen_path(prev_path[-2].lx, prev_path[-2].ly, prev_path[-1])
            for next_path in next_paths:
                paths.append(next_path)
                if target in next_path:
                    temp_paths = Queue()
                else:
                    temp_paths.put(next_path)

        return [i[:-1] for i in paths]

    def find_shortest_path(self, start_x: int, start_y: int, target_x: int, target_y: int):
        """
        Given a list of all the paths on the grid, finds the shortest path between the start
        and target position.
        :param start_x: starting local x-coordinate
        :param start_y: starting local y-coordinate
        :param target_x: target local x-coordinate
        :param target_y: target local y-coordinate
        :return: single path
        """
        start = self[start_x, start_y]
        target = self[target_x, target_y]
        if start == target:
            return None

        options = self.__gen_paths_to_target((start_x, start_y), (target_x, target_y))

        paths = []
        future_paths = Queue()
        future_paths.put([start])
        while not future_paths.empty():
            prev_path: [Tile] = future_paths.get()
            next_paths = (i for i in options if i[0] == prev_path[-1])
            for next_path in next_paths:
                while target in next_path and target != next_path[-1]:
                    next_path.pop(-1)
                if len(next_path) > 1:
                    combine_path = prev_path + next_path[1:]
                    future_paths.put(combine_path)
                    paths.append(combine_path)
        return min((i for i in paths if target in i), key=len)

    def render(self, display):
        """ render controller for rendering every thing on the scene

        :param display: current pygame display
        :type display: pygame.Surface
        :return:
        """
        # TODO: make render function
        ...

