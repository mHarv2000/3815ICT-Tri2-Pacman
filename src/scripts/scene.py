import json
import os
from typing import Tuple
import pygame
from src.scripts.ai import PacMan, Ghost
from src.scripts.consts import GenType, TileAttr, TileID, TileType


class Grid:
    """
    Basic coordinate system for the game scene

    The grid relies on two types of coordinates; grid coordinates and local coordinates. Grid coordinates are the
    literal scene coordinates on the screen where as the local coordinates refer to the index of the tiles. for example:
    assuming the tile size is 20, the grid position of the tile at local position (1, 3) is (20, 60). The origin (0, 0)
    is placed at the grid position equal to (TILE_SIZE, TILESIZE * 3) to save room for displaying the score above the
    grid and a back button to the left.
    """

    def __init__(self, window_h: int, scene_tile_w: int, scene_tile_h: int, gen_type: GenType):
        """
        :param window_h: window height, should equal WINDOW_H
        :type window_h: int
        :param scene_tile_w: width of the scene in the number of tiles
        :type scene_tile_w: int
        :param scene_tile_h: height of the scene in the number of tiles
        :type scene_tile_h: int
        :param gen_type: generation type
        :type gen_type: GenType
        """
        if gen_type == GenType.SQUAREGRID:
            self._scene_tile_w = scene_tile_w
            self._scene_tile_h = scene_tile_h
            # size of the tiles (for both width and height)
            self._tile_size = (window_h // scene_tile_h)
            # width of the scene
            self._scene_w = (scene_tile_w + 1) * self._tile_size
            # height of the scene
            self._scene_h = scene_tile_h * self._tile_size
            # first grid position on the game scene
            self._origin = self._tile_size, 3 * self._tile_size
            # 2D list of coordinatess (position relative to the indexes of this list)
            self._local_coords = [[(x, y) for x in range(scene_tile_w)] for y in range(scene_tile_h)]
            # 2D list of grid coordinates (position on the screen)
            self._grid_coords = [[((x * self._tile_size) + self._origin[0], (y * self._tile_size) + self._origin[1])
                                  for x in range(scene_tile_w)] for y in range(scene_tile_h)]

    def lpos(self, x: int = None, y: int = None):
        """
        get grid position from full or partial local coordinate
        :param x: x local coordinate (not grid coordinate)
        :param y: y local coordinate (not grid coordinate)
        :return: all grid coordinates, row of grid coordinates or a single coordinate
        """
        if x is not None and y is None:
            if not 0 <= x <= self._scene_tile_w:
                raise IndexError("x local coordinate is out of range, must be between 0 and %s"
                                 % (self._scene_tile_w - 1))
            return self._grid_coords[x]
        elif y is not None and x is None:
            if not 0 <= x <= self._scene_tile_h:
                raise IndexError("y local coordinate is out of range, must be between 0 and %s"
                                 % (self._scene_tile_h - 1))
            return [_[y] for _ in self._grid_coords]
        elif x is not None and y is not None:
            if not 0 <= x <= self._scene_tile_h:
                raise IndexError("x or y local coordinate are out of range, must be between (0, 0) and (%s, %s)"
                                 % ((self._scene_tile_w - 1), (self._scene_tile_h - 1)))
            return self._grid_coords[x][y]

    def gpos(self, x: int = None, y: int = None):
        """
        get grid position from full or partial local coordinate
        :param x: x local coordinate (not grid coordinate)
        :param y: y local coordinate (not grid coordinate)
        :return: all grid coordinates, row of grid coordinates or a single coordinate
        """
        if x is not None and y is None:
            if not 0 <= x <= self._scene_tile_w:
                raise IndexError("x local coordinate is out of range, must be between 0 and %s"
                                 % (self._scene_tile_w - 1))
            return self._grid_coords[x]
        elif y is not None and x is None:
            if not 0 <= x <= self._scene_tile_h:
                raise IndexError("y local coordinate is out of range, must be between 0 and %s"
                                 % (self._scene_tile_h - 1))
            return [_[y] for _ in self._grid_coords]
        elif x is not None and y is not None:
            if not 0 <= x <= self._scene_tile_h:
                raise IndexError("x or y local coordinate are out of range, must be between (0, 0) and (%s, %s)"
                                 % ((self._scene_tile_w - 1), (self._scene_tile_h - 1)))
            return self._grid_coords[x][y]


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


class TileMap(Grid):
    """
    Grid Container and Manager of Game Elements

    Generates a grid of tiles based on the coords in the grid superclass and then creates pacman, the ghosts and
    the scoreboards. The TileMap takes care of ghost pathfinding and pacman events that may trigger events outside the
    class.
    """
    def __init__(self, width_in_tiles, height_in_tiles):
        """
        :param width_in_tiles: How many tiles wide the game scene is
        :type width_in_tiles: int
        :param height_in_tiles: How many tiles high the game scene is
        :type height_in_tiles: int
        """
        super(TileMap, self).__init__(width_in_tiles, height_in_tiles)
        self.__tiles = ((Tile(lx, ly, *gpos, self._tile_size) for lx, gpos in enumerate(row))
                        for ly, row in enumerate(self._grid_coords))
        self.__pacman = PacMan(0, 0, 1.1, os.path.join('..', 'img', 'pacman', '*.png'))
        self.__blinky = Ghost(0, 0, 1, os.path.join('..', 'img', 'ghost', 'blinky', '*.png'))
        self.__inky = Ghost(0, 0, 1, os.path.join('..', 'img', 'ghost', 'inky', '*.png'))
        self.__pinky = Ghost(0, 0, 1, os.path.join('..', 'img', 'ghost', 'pinky', '*.png'))
        self.__clyde = Ghost(0, 0, 1, os.path.join('..', 'img', 'ghost', 'clyde', '*.png'))

    def __load_level_one(self, setttings_path: str) -> None:
        """
        load the first level of the game so that further levels made expand and scale based on this design.
        The map shown in data.json contains multiple letters that represent tile types, ids and attributes
        which can be read and used to generate the tiles

        Legend
        ' ' | id: BLANK
        'o' | type: DBL_CORNER
        '=' | type: DBL_WALL | id: DBL_WALL_H
        '!' | type: DBL_WALL | id: DBL_WALL_V
        '+' | type: CORNER
        '-' | type: WALL | id: WALL_H
        '|' | type: WALL | id: WALL_V
        '.' | id: FRUIT
        'd' | type: DOOR
        '^' | type: TELEPORT
        'E' | id: ENERGISER
        'C' | id: CHERRY
        'P' | id: BLANK | attr: PACMAN_SPAWN
        'S' | id: BLANK | attr: GHOST_SPAWN
        'F' | id: FRUIT | attr: GHOST_FLEE
        """
        with open(setttings_path, 'r') as file:
            grid_map = json.load(file)['staticLevel']
        # TODO: assign values to self.__tiles

    def right_of(self, x: int, y: int) -> Tile:
        """
        get tile to the right of the active tile
        :param x: x local coordinate
        :param y: y local coordinate
        :return: the tile object
        """
        if x < self._scene_tile_w:
            return self.__tiles[x + 1][y]
        return self.__tiles[x][y]

    def left_of(self, x: int, y: int) -> Tile:
        """
        get tile to the left of the active tile
        :param x: x local coordinate
        :param y: y local coordinate
        :return: the tile object
        """
        if x >= 0:
            return self.__tiles[x - 1][y]
        return self.__tiles[x][y]

    def above(self, x: int, y: int) -> Tile:
        """
        get tile above the active tile
        :param x: x local coordinate
        :param y: y local coordinate
        :return: the tile object
        """
        if y >= 0:
            return self.__tiles[x][y - 1]
        return self.__tiles[x][y]

    def below(self, x: int, y: int) -> Tile:
        """
        get tile below the active tile
        :param x: x local coordinate
        :param y: y local coordinate
        :return: the tile object
        """
        if x < self._scene_tile_h:
            return self.__tiles[x][y + 1]
        return self.__tiles[x][y]

    def render(self, display):
        """
        render controller for rendering every thing on the scene
        :param display: current pygame display
        :type display: pygame.Surface
        :return:
        """
        # TODO: make render function
        ...

    def __getitem__(self, item):
        if not isinstance(item, int):
            raise TypeError("index/s must be an integer")
        return self.__tiles[item]
