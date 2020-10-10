import os
from threading import Thread
import pygame
import glob
import time
from enum import Enum, unique
import json
from collections import defaultdict
from queue import Queue
from typing import Tuple

class Label:
	"""
	Label/Button UI Element

	A pygame label displaying text which can be used for events.
	"""

	def __init__(self, x, y, colour, text_str, padding, font):
		"""
		:param x: x-Axis coordinate
		:type x: int
		:param y: y-Axis coordinate
		:type y: int
		:param text_str: the text string
		:type text_str: str
		:param colour: colour of the text
		:type colour: Colour
		:param font: type of font
		:type font: pygame.font.Font
		:param padding: the space between the edges of the label and the text
		:type padding: int
		"""

		self.__x = x
		self.__y = y
		self.__text_str = text_str
		self.__colour = colour
		self.__font = font
		self.__padding = padding
		self.__text = font.render(text_str, True, colour)
		self.__rect = pygame.Rect(x, y, self.__text.get_width() + padding, self.__text.get_height() + padding)
		self.__text_pos = (self.__rect.centerx - (self.__text.get_width() // 2),
		                   self.__rect.centery - (self.__text.get_height() // 2))

	@property
	def rect(self) -> pygame.Rect:
		""" get label box """
		return self.__rect

	@property
	def text_str(self) -> str:
		""" get text string """
		return self.__text_str

	@text_str.setter
	def text_str(self, text: str) -> None:
		""" set text string """
		if not isinstance(text, str):
			raise TypeError("text must be string")
		self.__text_str = text
		self.__text = self.__font.render(self.__text_str, True, self.__colour)
		self.__rect = pygame.Rect(self.__x, self.__y, self.__text.get_width() + self.__padding,
		                          self.__text.get_height() + self.__padding)
		self.__text_pos = (self.__rect.centerx - (self.__text.get_width() // 2),
		                   self.__rect.centery - (self.__text.get_height() // 2))

	@property
	def text(self) -> pygame.Surface:
		""" get text object """
		return self.__text

	@property
	def pos(self) -> Tuple[int, int]:
		""" get x and y position """
		return self.__text_pos

	def render(self, display) -> None:
		"""
		display the elements to the screen
		:param display: the current pygame display
		:type display: pygame.Surface
		"""
		pygame.draw.rect(display, (0, 0, 0), self.__rect)
		display.blit(self.__text, self.__text_pos)


class Spinner:
	"""
	Spinner Input UI Element

	A UI Integer input with arrows to increase/decrease the value by a given step amount
	"""

	def __init__(self, x, y, value, font, minimum=0, maximum=1, step=1):
		"""
		:param x: x coordinte
		:type x: int
		:param y: y coordinte
		:type y: int
		:param value: integer value of the text
		:type value: int
		:param font: font object
		:type value: pygame.font.Font
		:param minimum: the minimum value the value can go to
		:type minimum: int
		:param maximum: the maximum value the value can go to
		:type maximum: int
		:param step: the amount to increase the value by
		:type step: int
		"""
		self.__x = x
		self.__y = y
		self.__value = value
		self.__font = font
		self.__minimum = minimum
		self.__maximum == maximum
		self.__step = step
		self.__text = font.render(str(value), True, (255, 255, 255))
		self.__rect = pygame.Rect(self.__x, self.__y, self.__text.get_width() + 5,
		                          self.__text.get_height() + 5)
		self.__text_pos = (self.__rect.centerx - (self.__text.get_width() // 2),
		                   self.__rect.centery - (self.__text.get_height() // 2))

	def add_step(self, is_positive=True) -> None:
		"""
		increase/decrease value by step
		:param is_positive: should the value be increased (False means decrease)
		:type is_positive: bool
		"""
		self.__value += self.__step

	@property
	def rect(self) -> pygame.Rect:
		""" get rectangle """
		return self.__rect

	@property
	def value(self) -> None:
		""" get value """
		return self.__value

	@value.setter
	def value(self, new_value: int) -> None:
		""" set value and update spinner elements """
		self.__value = new_value if self.__minimum <= new_value <= self.__maximum else self.__value
		self.__recreate()

	@property
	def pos(self):
		return self.__x, self.__y

	def set_step(self, value: int) -> None:
		""" set step amount """
		if not isinstance(value, int) and value <= self.__maximum:
			raise ValueError("step size exceeds the maximum amount")
		self.__step = value

	def set_font(self, new_font: pygame.font.Font) -> None:
		""" set font """
		if not isinstance(new_font, pygame.font.Font):
			raise ValueError("new font must be a pygame Font object")
		self.__font = new_font
		self.__recreate()

	def __recreate(self) -> None:
		""" recreate spinner object by reinitialising it's elements """
		self.__text = self.__font.render(str(self.__value), True, (255, 255, 255))
		self.__rect = pygame.Rect(self.__x, self.__y, self.__text.get_width() + 5,
		                          self.__text.get_height() + 5)
		self.__text_pos = (self.__rect.centerx - (self.__text.get_width() // 2),
		                   self.__rect.centery - (self.__text.get_height() // 2))

	def render(self, display) -> None:
		"""
		display the elements to the screen
		:param display: the current pygame display
		:type display: pygame.Surface
		:return:
		"""
		# TODO: make render function


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
class TileID(Enum):
    """
    A specific label given to each tile to tell the game exactly what the tile is.
    """
    BLANK = 0  # blank tile
    DBL_WALL = 1  # generic double wall
    DBL_WALL_TL = 2  # double wall top-left tile
    DBL_WALL_TR = 3  # double wall top-right tile
    DBL_WALL_BR = 4  # double wall bottom_right tile
    DBL_WALL_BL = 5  # double wall bottom-left tile
    DBL_WALL_H = 6  # double wall horizontal tile
    DBL_WALL_V = 7  # double wall vertical tile
    WALL = 8  # generic wall
    WALL_TL = 9  # wall top-left tile
    WALL_TR = 10  # wall top-right tile
    WALL_BR = 11  # wall bottom-right tile
    WALL_BL = 12  # wall bottom-left tile
    WALL_H = 13  # wall horizontal tile
    WALL_V = 14  # wall vertical tile
    FRUIT = 15  # fruit tile
    ENERGIZER = 16  # energizer tile
    CHERRY = 17  # cherry tile
    DOOR = 18  # generic door
    DOOR_H = 19  # door horizontal tile
    DOOR_V = 20  # door vertical tile


@unique
class TileAttr(Enum):
    """
    An attribute given to tile objects to help with path-finding
    """
    PACMAN_SPAWN = 0
    GHOST_SPAWN = 1
    GHOST_FLEE = 2

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


class Direction:
    """ A clock-wise lateral dynamically incremental compass used to tell the direction relative to the grid.

    Each direction Is iterable and can be iterated over infinitely to return a string based
    representation of each compass direction (orientation) or a number representing the orientation (digit);
    'n' | 0 (North), 'e' | 1 (East), 's' | 2 (South) and 'w' | 3 (West)

    :param value: string character (n, s, e, w) or 0-3
    :type value: str | int
    """
    def __init__(self, value):
        if isinstance(value, str):
            self.__orientation = value
            self.__digit = self.convert(value)
        elif isinstance(value, int):
            self.__digit = value
            self.__orientation = self.convert(value)

    @property
    def orientation(self):
        """ get direction

        :return: string representation of direction """
        return self.__orientation

    @orientation.setter
    def orientation(self, value):
        """ set direction by string

        :param value: string character (n, s, e, w) """
        self.__orientation = value
        self.__digit = self.convert(value)

    @property
    def digit(self) -> int:
        """ get digit

        :return: digit representing the direction """
        return self.__digit

    @digit.setter
    def digit(self, value) -> None:
        """ set digit

        :param value: digit (0-3)
        """
        self.__digit = value
        self.__orientation = self.convert(value)

    @staticmethod
    def convert(value):
        """ set orientation equivalent to the digit and vice versa

        :param value: orientation or digit
        :return: return the opposite value of the one passed in through value,
                 e.g. passing in orientation will return the digit
        """
        if isinstance(value, int):
            if value == 0:
                return 'n'
            elif value == 1:
                return 'e'
            elif value == 2:
                return 's'
            elif value == 3:
                return 'w'
            else:
                raise ValueError('digit must be in the range 0-3')
        elif isinstance(value, str):
            if value == 'n':
                return 0
            elif value == 'e':
                return 1
            elif value == 's':
                return 2
            elif value == 'w':
                return 3
            else:
                raise ValueError(f'character \'{value}\' does not exist')
        else:
            raise TypeError('only accepts the characters n, s, e, w and integers 0-3')

    def is_north_or_south(self):
        """ check if direction is north or south

        :return: True/False """
        return True if self.__digit == 0 \
                       or self.__digit == 2 else False

    def __repr__(self):
        return self.__orientation.upper()

    def __str__(self):
        """ when cast to a string, return the orientation """
        return self.__orientation

    def __int__(self):
        """ when cast to an integer, return the digit """
        return self.__digit

    def __add__(self, other):
        """ allow direction objects to be incremental

        The RHS can allow for integers but also other directions to be incremented, however,
        digit is reset to 0 after exceeding 3 and resumes incrementing. e.g. 0 + 5 = 1

        :return: the sum of both digits"""
        return Direction((self.__digit + other) % 4)

    def __eq__(self, other):
        """ check if orientation or digit is equal to RHS """
        if isinstance(other, str):
            return self.__orientation == other
        elif isinstance(other, int):
            return self.__digit == other
        return False

    def __sub__(self, other):
        """ allow direction objects to be decremental

        digit is reset to 3 after subceeding 0 and resumes decrementing. e.g. 3 - 5 = 2

        :param other: integer value or Direction
        :return: the sum of subtracted digits"""
        return Direction((self.__digit - other) % 4)

    def __iadd__(self, other):
        """ adds and sets digit and orientation with the += operator

        :param other: orientation or digit
        :returns self:
        """
        self.__digit += other
        if self.__digit < 0 or self.__digit > 3:
            self.__digit %= abs(4)
        self.__orientation = self.convert(self.__digit)
        return self

    def __isub__(self, other):
        """ subtracts and sets digit and orientation with the -= operator

        :param other: orientation or digit
        :returns self:
        """
        self.__digit -= other
        if self.__digit < 0:
            self.__digit %= 4
        self.__orientation = self.convert(self.__digit)
        return self

    def __reversed__(self):
        """ subtracts 2 from the digit to get the opposite direction

        example: inverting north will be south (n -> s), (0 -> 2)
        """
        return Direction((self.__digit - 2) % 4)

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
        self.__tiles: [Tile] = []
        with open(os.path.abspath('./data/data.json'), 'r') as file:
            data = json.load(file)['staticLevel']
            for x, row in enumerate(data):
                self.__tiles.append([])
                for y, tile in enumerate(row):
                    if tile == ' ':
                        self.__tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, True, TileID.BLANK))
                    elif tile == '=':
                        self.__tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, False, TileID.DBL_WALL))
                    elif tile == '-':
                        self.__tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, False, TileID.WALL))
                    elif self.__tiles == 'd':
                        self.__tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, False, TileID.DOOR))
                    elif tile == '.':
                        self.__tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, True, TileID.FRUIT))
                    elif tile == '*':
                        self.__tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, True, TileID.ENERGIZER))
                    elif tile == 'p':
                        self.__tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, True, TileID.BLANK,
                                                    TileAttr.PACMAN_SPAWN))
                    elif tile == 'c':
                        self.__tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, True, TileID.CHERRY))
                    elif tile == 'g':
                        self.__tiles[x].append(Tile(y, x, y * tile_size, x * tile_size, True, TileID.BLANK,
                                                    TileAttr.GHOST_SPAWN))
        self.__lheight = len(self.__tiles)
        self.__lwidth = len(self.__tiles[0])
        self.__gheight = self.__lheight * tile_size
        self.__gwidth = self.__lwidth * tile_size

    def __getitem__(self, item: tuple):
        """ get tile at coordinates x, y """
        return self.__tiles[item[1]][item[0]]

    def adjacent_tile(self, lx: int, ly: int, direction: Direction):
        if direction == 'n' and 0 < ly < self.__lheight:
            return self[lx, ly - 1]
        elif direction == 's' and 0 <= ly < (self.__lheight - 1):
            return self[lx, ly + 1]
        elif direction == 'e' and 0 <= lx < (self.__lwidth - 1):
            return self[lx + 1, ly]
        elif direction == 'w' and 0 < lx < self.__lwidth:
            return self[lx - 1, ly]
        else:
            return None

    def adjacent_tiles(self, lx: int, ly: int, exclude_direction: str = None):
        """
        Get adjacent tiles of a tile and return the tiles indexed by a compass character.
        :param lx: x-local-coordinate of the initial tile
        :param ly: y-local-coordinate of the initial tile
        :param exclude_direction: find all adjacent cells except in this direction
        :return:
        """

        directions = {'n', 's', 'e', 'w'}
        if exclude_direction is not None and exclude_direction in directions:
            directions.discard(exclude_direction)
        tiles = defaultdict()
        if 'n' in directions and 0 < ly < self.__lheight:
            tile = self[lx, ly - 1]
            if tile.is_transversible():
                tiles['n'] = tile
        if 's' in directions and 0 <= ly < (self.__lheight - 1):
            tile = self[lx, ly + 1]
            if tile.is_transversible():
                tiles['s'] = tile
        if 'e' in directions and 0 <= lx < (self.__lwidth - 1):
            tile = self[lx + 1, ly]
            if tile.is_transversible():
                tiles['e'] = tile
        if 'w' in directions and 0 < lx < self.__lwidth:
            tile = self[lx - 1, ly]
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

class Character:
    """ Generic Character for AI or PLayer control

    AI or player controlled sprite with path finding, animation and transform control. Used with an external pygame
    display to render and update the character each frame

    :param lx: local x-coordinate on the tile_map
    :type lx: int
    :param ly: local y-coordinate on the tile_map
    :type lx: int
    :param speed: how many tiles are travelled per second
    :type speed: int
    :param size: should be equal to tile_size
    :type size: int
    """

    def __init__(self, lx: int, ly: int, speed: int, size: int):
        self._lx = lx
        self._ly = ly
        self._gx = lx * size
        self._gy = ly * size

        self._current_direction = Direction('e')
        self._speed = speed
        self._frame = None

    @property
    def lx(self):
        """ get the local x-coordinate relative to the grid """
        return self._lx

    @property
    def ly(self):
        """ get the local y-coordinate relative to the grid """
        return self._ly

    @property
    def gx(self):
        """ get the global x-coordinate """
        return self._gx

    @property
    def gy(self):
        """ get the global y-coordinate """
        return self._gy

    def get_frame(self):
        """ get current frame of animation """
        return self._frame

    def resume_animation(self):
        """ update frame in animation """
        ...

    def move(self):
        """ move in the current direction """

    def rotate(self, new_direction: Direction):
        """ rotate to face the current direction """


class PacMan(Character):
    """ The PacMan Character Controller

    The PacMan class controls the animation, direction, events and state of the character
    controlled through pygame key-events externally.
    -   sprite animation relies on a group of image icons to animate each frame.
    -   pacman movement is updated constantly and may only change direction when an arrow key event is triggered

    :param lx: local x-coordinate on the tile_map
    :type lx: int
    :param ly: local y-coordinate on the tile_map
    :type lx: int
    :param speed: how many tiles are travelled per second
    :type speed: int
    :param size: should be equal to tile_size
    :type size: int
    :param highscore: copy of highscore value from storage
    :type highscore: int
    """

    def __init__(self, lx: int, ly: int, speed: int, size: int, highscore: int):
        super(PacMan, self).__init__(lx, ly, speed, size)
        try:
            url = glob.glob('./img/pacman/*.png')
            self.__animation_seq = [pygame.transform.scale(pygame.image.load(img), (size, size)) for img in url]
        except FileNotFoundError as err:
            raise FileExistsError("file path to directory: '%s' does not exist" % err)

        self.__frame_index = 0
        self.__animation_playback = 1
        self._frame = self.__animation_seq[0]

        # score information
        self.__score = 0
        self.__highscore = highscore
        self.__lives = 3

    def resume_animation(self):
        """ update frame in animation """
        if self.__frame_index == len(self.__animation_seq) - 1:
            self.__animation_playback = -1
        elif self.__frame_index == 0:
            self.__animation_playback = 1
        self.__frame_index += self.__animation_playback
        self._frame = self.__animation_seq[self.__frame_index]

    def move(self):
        """ move in the current direction """
        if self._current_direction == 0:
            self._gy += self._speed
        elif self._current_direction == 1:
            self._gx += self._speed
        elif self._current_direction == 2:
            self._gy -= self._speed
        elif self._current_direction == 3:
            self._gx -= self._speed

    def rotate(self, new_direction):
        """ rotate to face the current direction """
        old_angle = int(self._current_direction) * 90
        new_angle = int(new_direction) * 90
        self._current_direction = new_direction
        for i, frame in enumerate(self.__animation_seq):
            self.__animation_seq[i] = pygame.transform.rotate(self.__animation_seq[i], -old_angle)
            self.__animation_seq[i] = pygame.transform.rotate(self.__animation_seq[i], new_angle)

    def update_score(self, base_score, is_cherry: bool, is_ghost: bool) -> dict:
        """
        Update the current score based on the item eaten by PacMan
        :param base_score: the base score depending on the game session's time
        :param is_cherry: item eaten was a cherry
        :param is_ghost: item eaten was a ghost
        :return: current score
        """
        if is_cherry:
            self.__score += int(base_score * 3)
        elif is_ghost:
            self.__score += int(base_score * 2)
        else:
            self.__score += base_score // 5
        return self.get_score()

    def get_score(self):
        """ get current score """
        return {
            'score': self.__score,
            'highscore': self.__highscore,
            'lives': self.__lives
        }

    def remove_life(self):
        """ remove a life and return the new amount left """
        self.__lives -= 1
        return self.__lives


class Ghost(Character):
    """
    The Ghost Character Controller

    The Ghost class controls the animation, direction, events and state of the character
    controlled through game events.
    -   sprite animation relies on a group of image icons to animate each frame depending on the direction.
    -   ghost movement is updated constantly and may only change when the the route to the pacman's position changes
        or because of game events

    :param lx: local x-coordinate on the tile_map
    :type lx: int
    :param ly: local y-coordinate on the tile_map
    :type lx: int
    :param speed: how many tiles are travelled per second
    :type speed: int
    :param size: should be equal to tile_size
    :type size: int
    """

    def __init__(self, lx: int, ly: int, speed: int, size: int, ghost_name: str):
        super(Ghost, self).__init__(lx, ly, speed, size)
        try:
            url = glob.glob(f'./img/ghost/{ghost_name}/*.png')
            vuln_url = glob.glob('./img/ghost/vulnerable/*.png')
            self.__animation_seq = [pygame.transform.scale(pygame.image.load(img), (size, size)) for img in url]
            self.__vuln_animation_seq = [pygame.transform.scale(
                pygame.image.load(img), (size, size)) for img in vuln_url]
        except FileNotFoundError as err:
            raise FileExistsError("file path to directory: '%s' does not exist" % err)

        self.__name = ghost_name

        self.__animation_playback = 1
        self._frame = self.__animation_seq[0]

        self._current_direction = Direction(0)
        self._speed = speed
        self.__vulnerable = False
        self.__semi_vulnerable = False
        self__path = []

    def resume_animation(self):
        """ update frame in animation """
        if self.__animation_playback == 1:
            self.__animation_playback = 0
        else:
            self.__animation_playback = 1

    def move(self) -> None:
        """ move in the current direction """
        if self._current_direction == 0:
            self._gy += self._speed
        elif self._current_direction == 1:
            self._gx += self._speed
        elif self._current_direction == 2:
            self._gy -= self._speed
        elif self._current_direction == 3:
            self._gx -= self._speed

    def rotate(self, new_direction):
        """ rotate to face the current direction """
        # TODO: make rotate method
        ...

    def retreat(self, sec: int):
        """ convert the ghost into vulnerable state for a limited number of seconds.

        With 4 seconds remaining, the ghost will go into semi-vulnerable state where it will
        begin flashing white/blue before finally returning to it's normal state.

        :param sec: number of seconds the ghost is vulnerable
        :type sec: int
        """

        def __timer():
            """  """
            vulnerability_timer = 10
            while vulnerability_timer != 0:
                time.sleep(1)
                vulnerability_timer -= 1
                if vulnerability_timer == 4:
                    self.__semi_vulnerable = True
            self.__semi_vulnerable = False

        self.__vulnerable = True
        timer = Thread(target=__timer, args=(sec,))
        timer.start()
        timer.join()
        self.__vulnerable = False

    def follow(self, new_path):
        """ set the current path to allow the Ghost to follow along
        a set of Tiles until it reaches the end point

        :param new_path: list of tiles in order representing the path from the
                         current coordinate to the end-point
        :type new_path: [(int, int)]
        """
        ...

"""
The pygame display renders each page as a modal. The menu, settings nd start_game functions are in charge
of running each page and deallocating memory when necessary. 
"""

with open(os.path.abspath('./data/data.json'), 'r') as file:
    data = json.load(file)['settings']
try:
    WINDOW_W, WINDOW_H = data['windowWidth'], data['windowHeight']
    WIDTH_TILES, HEIGHT_TILES = data['tileWidth'], data['tileHeight']
    DIFF_STEP = int(data["levelDifficultyStep"])
    SCALE_PER_STEP = int(data["levelScalePerStep"])
    TILE_SIZE = round(WINDOW_H / HEIGHT_TILES)
    FPS = int(data['fps'])
except Exception as err:
    raise Exception("An unexpected error occurred while reading data.json:\n%s" % err)
finally:
    del data

pygame.init()
pygame.font.init()
pygame.display.set_caption('Pac Man')
icon = pygame.image.load(os.path.abspath('./img/pacman/pacman_0.png'))
pygame.display.set_icon(icon)
display: pygame.Surface = pygame.display.set_mode((WINDOW_W, WINDOW_H))
lrg_font = pygame.font.Font(os.path.abspath('./font/BarcadeBrawlRegular.ttf'), 20)
sml_font = pygame.font.Font(os.path.abspath('./font/BarcadeBrawlRegular.ttf'), 11)
clock = pygame.time.Clock()

del icon


def menu():
    """ Display Menu """

    running = True
    origin = 50, 50
    logo = pygame.image.load(os.path.abspath('./img/logo/logo.png')).convert_alpha()
    start_game_btn = Label(origin[0], origin[1] + (logo.get_height() + 50), (255, 255, 255), "Start Game", 20, lrg_font)
    settings_btn = Label(origin[0], origin[1] + (logo.get_height() + 100), (255, 255, 255), "Settings", 20, lrg_font)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if start_game_btn.rect.collidepoint(*event.pos):
                    return 'start_game'
                if settings_btn.rect.collidepoint(*event.pos):
                    return 'settings'
            if event.type == pygame.QUIT:
                running = False

        display.fill((0, 0, 0))

        # render logo
        display.blit(logo, origin)
        # render start button
        pygame.draw.rect(display, (0, 0, 0), start_game_btn.rect)
        display.blit(start_game_btn.text, start_game_btn.rect)
        # render settings button
        pygame.draw.rect(display, (0, 0, 0), settings_btn.rect)
        display.blit(settings_btn.text, settings_btn.pos)

        pygame.display.update()

    return 0


def settings():
    """ Display settings page """

    running = True
    back_btn = Label(0, 0, (255, 255, 255), '<', 10, sml_font)
    # TODO: no options in settings yet
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if back_btn.rect.collidepoint(*event.pos):
                    return 'menu'
            if event.type == pygame.QUIT:
                running = False

        display.fill((0, 0, 0))
        back_btn.render(display)

        pygame.display.update()

    return 0


def start_game():
    """ Display and Start Game """

    running = True
    level = 0
    back_btn = Label(0, 0, (255, 255, 255), '<', 10, sml_font)
    tile_map = TileMap(TILE_SIZE)
    pacman = PacMan(1, 1, 5, 50, 0)
    ghost_inky = Ghost(0, 0, 1, 50, 'inky')
    ghost_blinky = Ghost(0, 0, 1, 50, 'blinky')
    ghost_pinky = Ghost(0, 0, 1, 50, 'pinky')
    ghost_clyde = Ghost(0, 0, 1, 50, 'clyde')

    def update_per_second():
        while running:
            time.sleep(.1)
            pacman.move()
            pacman.resume_animation()
            ghost_blinky.move()
            ghost_blinky.resume_animation()

    th1 = Thread(target=update_per_second)
    th1.start()

    # TODO: game is unfinished
    while running:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if back_btn.rect.collidepoint(*event.pos):
                    return 'menu'
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    pacman.rotate(Direction('s'))
                elif event.key == pygame.K_DOWN:
                    pacman.rotate(Direction('n'))
                elif event.key == pygame.K_RIGHT:
                    pacman.rotate(Direction('e'))
                elif event.key == pygame.K_LEFT:
                    pacman.rotate(Direction('w'))
            elif event.type == pygame.QUIT:
                running = False

        display.fill((0, 0, 0))
        back_btn.render(display)
        display.blit(pacman.get_frame(), (pacman.gx, pacman.gy))
        display.blit(ghost_blinky.get_frame(), (50, 50))
        display.blit(ghost_clyde.get_frame(), (100, 50))
        display.blit(ghost_inky.get_frame(), (150, 50))
        display.blit(ghost_pinky.get_frame(), (200, 50))

        pygame.display.update()

    running = False
    return 0


managers = {
    'menu': menu,
    'start_game': start_game,
    'settings': settings
}
current_manager = 'menu'

while True:
    next_manager = managers[current_manager]()
    current_manager = next_manager
    if next_manager == 0:
        break

pygame.quit()




