import glob
from src.scripts.consts import *


class Character(pygame.sprite.Sprite):
    """
    Generic Character for AI or PLayer control

    AI or player controlled sprite with path finding, animation and transform control. Used with an external pygame
    display to render and update the character each frame
    """

    def __init__(self, x: int, y: int, speed: float, frames_path: str):
        """
        :param lx: local x coordinate
        :type lx: int
        :param ly: local y coordinate
        :type lx: int
        :param gx: grid x coordinate
        :type gx: int
        :param gy: grid y coordinate
        :type gx: int
        :param speed: the number of tiles pacman travels every second
        :type speed: float
        :param frames_path: path to directory containing the png images used for character animation, animation is
                            generated based on the order of the images. path must end with /*.png as only png images
                            are supported
        :type frames_path: str
        """

        super(Character, self).__init__()
        try:
            self.images = glob.glob(frames_path)
            self.images = [pygame.image.load(path) for path in self.images]
        except FileNotFoundError as err:
            raise FileExistsError("file path to directory: '%s' does not exist" % err)
        self._x = x
        self._y = y
        self._current_direction = Direction.SOUTH
        self._speed = (speed * TILE_SIZE) // FPS
        if self._speed == 0:
            self._speed = 1
        self._index = 0
        self.image = pygame.transform.scale(self.images[self._index], (TILE_SIZE, TILE_SIZE))
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    @property
    def direction(self) -> Direction:
        """ get current direction """
        return self._current_direction

    @direction.setter
    def direction(self, value: Direction):
        """ set current direction to another direction """
        if not isinstance(value, Direction):
            raise ValueError("direction must be a Direction Enum value; NORTH, SOUTH, EAST or WEST")
        self._current_direction = value

    def animate(self):
        """
        Run Animation Functions

        animations setup should be used in separate unctions and then called from here
        """
        ...


class PacMan(Character):
    """The PacMan Character Controller

    The PacMan class controls the animation, direction, events and state of the character
    controlled through pygame key-events externally.

    -   sprite animation relies on a group of image icons to animate each frame.
    -   pacman movement is updated constantly and may only change direction when an arrow key event is triggered
    """

    def __init__(self, x: int, y: int, speed: float, frames_path: str):
        super(PacMan, self).__init__(x, y, speed, frames_path)

    def __rotate(self) -> pygame.Rect:
        """
        rotate pacman to face direction
        """
        # TODO: make __rotate function
        pass

    @Character.direction.setter
    def direction(self, value: Direction):
        """ set current direction to another direction """
        if not isinstance(value, Direction):
            raise ValueError("direction must be a Direction Enum value; NORTH, SOUTH, EAST or WEST")
        self.rect = self.__rotate(value)
        self._current_direction = value

    def animate(self) -> None:
        self.__animate_eat()
        self.__move()

    def __animate_eat(self) -> None:
        """ animate pacman eating """
        self._index += 1
        if self._index >= len(self.images):
            self._index = 0
        self.image = pygame.transform.scale(self.images[self._index], (TILE_SIZE, TILE_SIZE))

    def __move(self) -> None:
        """ move and rotate pacman in the current direction """
        self._gx = self.rect.x
        self._gy = self.rect.y
        if self._current_direction == Direction.NORTH:
            self.rect.move_ip(0, -self._speed)
        elif self._current_direction == Direction.SOUTH:
            self.rect.move_ip(0, self._speed)
        elif self._current_direction == Direction.EAST:
            self.rect.move_ip(self._speed, 0)
        elif self._current_direction == Direction.WEST:
            self.rect.move_ip(-self._speed, 0)


class Ghost(Character):
    """The Ghost Character Controller

    The Ghost class controls the animation, direction, events and state of the character
    controlled through game events.

    -   sprite animation relies on a group of image icons to animate each frame depending on the direction.
    -   ghost movement is updated constantly and may only change when the the route to the pacman's position changes
        or because of game events
    """

    def __init__(self, x: int, y: int, speed: float, frames_path: str):
        super(Ghost, self).__init__(x, y, speed, frames_path)
        if not os.path.exists(frames_path):
            raise FileExistsError("file path: %s to pacman icons does nto exist" % frames_path)
        self.images = glob.glob(frames_path)
        self.__current_direction = Direction.NORTH
        self.__speed = 10
        self.__index = 0
        self.image = self.images[self.__index]
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)

    def animate(self):
        self.__move()

    def __move(self) -> None:
        """ move the ghost in the current direction """
        if self.__current_direction == Direction.SOUTH and self.image == self.images[0]:
            self.image = self.images[1]
            self.rect.move_ip(0, self.__speed)
        elif self.__current_direction == Direction.SOUTH and self.image == self.images[1]:
            self.image = self.images[0]
            self.rect.move_ip(0, self.__speed)
        elif self.__current_direction == Direction.WEST and self.image == self.images[2]:
            self.image = self.images[3]
            self.rect.move_ip(-self.__speed, 0)
        elif self.__current_direction == Direction.WEST and self.image == self.images[3]:
            self.image = self.images[2]
            self.rect.move_ip(-self.__speed, 0)
        elif self.__current_direction == Direction.EAST and self.image == self.images[4]:
            self.image = self.images[5]
            self.rect.move_ip(self.__speed, 0)
        elif self.__current_direction == Direction.EAST and self.image == self.images[5]:
            self.image = self.images[4]
            self.rect.move_ip(self.__speed, 0)
        elif self.__current_direction == Direction.NORTH and self.image == self.images[6]:
            self.image = self.images[7]
            self.rect.move_ip(0, -self.__speed)
        elif self.__current_direction == Direction.NORTH and self.image == self.images[7]:
            self.image = self.images[6]
            self.rect.move_ip(0, -self.__speed)