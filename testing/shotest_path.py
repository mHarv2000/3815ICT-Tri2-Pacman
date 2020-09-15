import json
import os
from collections import defaultdict
from queue import Queue

from src.scripts.consts import TileType, TileID
from src.scripts.misc import Direction


class Tile:

    def __init__(self, lx: int, ly: int, gx: int, gy: int, tile_type: TileType = None, tile_id: TileID = None):
        self.__local_coords = lx, ly
        self.__global_coords = gx, gy
        self.__transverse = True if tile_type == TileType.NONE or tile_type == TileType.OTHER else False
        self.__tile_type = tile_type
        self.__tile_id = tile_id

    def __repr__(self):
        return f'{self.__local_coords}, {self.__transverse}'

    def __int__(self):
        return 1

    def __radd__(self, other):
        return other + 1

    @property
    def lx(self):
        return self.__local_coords[0]

    @property
    def ly(self):
        return self.__local_coords[1]

    @property
    def lcoords(self):
        return self.__local_coords

    @property
    def gx(self):
        return self.__global_coords[0]

    @property
    def gy(self):
        return self.__global_coords[1]

    @property
    def gcoords(self):
        return self.__global_coords

    def is_transversible(self):
        return self.__transverse


class TileMap:

    def __init__(self, tile_size: int):
        self.tiles = []
        with open(os.path.abspath('../src/data/data.json'), 'r') as file:
            data = json.load(file)['staticLevel']
            for x, row in enumerate(data):
                self.tiles.append([])
                for y, tile in enumerate(row):
                    if tile == ' ':
                        self.tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, tile_type=TileType.BLANK))
                    elif tile == '=':
                        self.tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, tile_type=TileType.DBL_WALL))
                    elif tile == '-':
                        self.tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, tile_type=TileType.WALL))
                    elif tile == '.':
                        self.tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, tile_id=TileID.FRUIT))
                    elif tile == '.':
                        self.tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, tile_id=TileID.FRUIT))

    def __getitem__(self, item: tuple):
        return self.tiles[item[1]][item[0]]

    def adjacent_tile(self, x: int, y: int, direction: Direction):
        if direction == 'n' and 0 < y < height:
            return self[x, y - 1]
        elif direction == 's' and 0 <= y < (height - 1):
            return self[x, y + 1]
        elif direction == 'e' and 0 <= x < (width - 1):
            return self[x + 1, y]
        elif direction == 'w' and 0 < x < width:
            return self[x - 1, y]
        else:
            return None

    def adjacent_tiles(self, x: int, y: int, exclude_direction: str = None):
        directions = {'n', 's', 'e', 'w'}
        if exclude_direction is not None and exclude_direction in directions:
            directions.discard(exclude_direction)
        tiles = defaultdict()
        if 'n' in directions and 0 < y < height:
            tile = self[x, y - 1]
            if tile.is_transversible():
                tiles['n'] = tile
        if 's' in directions and 0 <= y < (height - 1):
            tile = self[x, y + 1]
            if tile.is_transversible():
                tiles['s'] = tile
        if 'e' in directions and 0 <= x < (width - 1):
            tile = self[x + 1, y]
            if tile.is_transversible():
                tiles['e'] = tile
        if 'w' in directions and 0 < x < width:
            tile = self[x - 1, y]
            if tile.is_transversible():
                tiles['w'] = tile
        return tiles

    def __gen_path(self, origin_x: int, origin_y: int, exclude_direction: str = None):
        origin = self[origin_x, origin_y]
        adjacent_tiles = self.adjacent_tiles(origin_x, origin_y, exclude_direction)
        for d, tile in adjacent_tiles.items():
            path = [origin, tile]
            while True:
                direction = Direction(d)
                next_tile = self.adjacent_tile(path[-1].x, path[-1].y, direction)

                if next_tile is not None and next_tile.is_transversible():
                    path.append(next_tile)

                    left_tile = self.adjacent_tile(path[-1].x, path[-1].y, direction - 1)
                    right_tile = self.adjacent_tile(path[-1].x, path[-1].y, direction + 1)
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

    @staticmethod
    def __gen_paths_to_target(start_coords: tuple, target_coords: tuple):
        start = tile_map.__gen_path(*start_coords)
        paths = []
        temp_paths = Queue()
        for path in start:
            paths.append(path)
            temp_paths.put(path)

        target = tile_map[target_coords[0], target_coords[1]]
        while not temp_paths.empty():
            prev_path = temp_paths.get()
            next_paths = tile_map.__gen_path(prev_path[-2].x, prev_path[-2].y, prev_path[-1])
            for next_path in next_paths:
                paths.append(next_path)
                if target in next_path:
                    temp_paths = Queue()
                else:
                    temp_paths.put(next_path)

        return [i[:-1] for i in paths]

    def find_shortest_path(self, start_x: int, start_y: int, target_x: int, target_y: int):
        """
        :param start_x:
        :param start_y:
        :param target_x:
        :param target_y:
        :return: single path
        """
        start = self[start_x, start_y]
        target = self[target_x, target_y]
        if start == target:
            return None

        options = tile_map.__gen_paths_to_target((start_x, start_y), (target_x, target_y))

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


tile_map = TileMap()
shortest_path = tile_map.find_shortest_path(0, 0, 5, 4)
print(shortest_path)
