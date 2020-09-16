import glob
import pygame
from src.scripts.misc import Direction


class PacMan:
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
    :type speed: float
    """

    def __init__(self, lx: int, ly: int, size: int, speed: int):
        try:
            url = glob.glob('../img/pacman/*.png')
            self.__animation_seq = [pygame.transform.scale(pygame.image.load(img), (size, size)) for img in url]
        except FileNotFoundError as err:
            raise FileExistsError("file path to directory: '%s' does not exist" % err)

        self.__lx = lx
        self.__ly = ly
        self.__gx = lx * size
        self.__gy = ly * size

        self.__frame_index = 0
        self.__animation_playback = 1
        self.__frame = self.__animation_seq[0]

        self.__current_direction = Direction('e')
        self.__speed = speed

    @property
    def lx(self):
        """ get the local x-coordinate relative to the grid """
        return self.__lx

    @property
    def ly(self):
        """ get the local y-coordinate relative to the grid """
        return self.__ly

    @property
    def gx(self):
        """ get the global x-coordinate """
        return self.__gx

    @property
    def gy(self):
        """ get the global y-coordinate """
        return self.__gy

    def get(self):
        """ get current frame of animation """
        return self.__frame

    def update_frame(self):
        """ update frame in animation """
        if self.__frame_index == len(self.__animation_seq) - 1:
            self.__animation_playback = -1
        elif self.__frame_index == 0:
            self.__animation_playback = 1
        self.__frame_index += self.__animation_playback
        self.__frame = self.__animation_seq[self.__frame_index]

    def update(self):
        """ move in the current direction """
        if self.__current_direction == 0:
            self.__gy += self.__speed
        elif self.__current_direction == 1:
            self.__gx += self.__speed
        elif self.__current_direction == 2:
            self.__gy -= self.__speed
        elif self.__current_direction == 3:
            self.__gx -= self.__speed

    def rotate(self, new_direction):
        """ rotate to face the current direction """
        old_angle = int(self.__current_direction) * 90
        new_angle = int(new_direction) * 90
        self.__current_direction = new_direction
        for i, frame in enumerate(self.__animation_seq):
            self.__animation_seq[i] = pygame.transform.rotate(self.__animation_seq[i], -old_angle)
            self.__animation_seq[i] = pygame.transform.rotate(self.__animation_seq[i], new_angle)


class Ghost(Character):
    """
    The Ghost Character Controller

    The Ghost class controls the animation, direction, events and state of the character
    controlled through game events.
    -   sprite animation relies on a group of image icons to animate each frame depending on the direction.
    -   ghost movement is updated constantly and may only change when the the route to the pacman's position changes
        or because of game events

    :param x: local x coordinate
    :type x: int
    :param y: local y coordinate
    :type x: int
    :param speed: how many tiles are travelled per second
    :type speed: float
    :param frames_path: path to directory containing the png images used for character animation, animation is
                        generated based on the order of the images. path must end with /*.png as only png images
                        are supported
    :type frames_path: str

    """

    def __init__(self, x: int, y: int, speed: float, frames_path: str):
        super(Ghost, self).__init__(x, y, speed, frames_path)

    def animate(self):
        self.__move()

    def __move(self) -> None:
        """ move the ghost in the current direction """
        if self._current_direction == 's' and self.image == self.images[0]:
            self.image = self.images[1]
            self.rect.move_ip(0, self._speed)
        elif self._current_direction == 's' and self.image == self.images[1]:
            self.image = self.images[0]
            self.rect.move_ip(0, self._speed)
        elif self._current_direction == 'w' and self.image == self.images[2]:
            self.image = self.images[3]
            self.rect.move_ip(-self._speed, 0)
        elif self._current_direction == 'w' and self.image == self.images[3]:
            self.image = self.images[2]
            self.rect.move_ip(-self._speed, 0)
        elif self._current_direction == 'e' and self.image == self.images[4]:
            self.image = self.images[5]
            self.rect.move_ip(self._speed, 0)
        elif self._current_direction == 'e' and self.image == self.images[5]:
            self.image = self.images[4]
            self.rect.move_ip(self._speed, 0)
        elif self._current_direction == 'n' and self.image == self.images[6]:
            self.image = self.images[7]
            self.rect.move_ip(0, -self._speed)
        elif self._current_direction == 'n' and self.image == self.images[7]:
            self.image = self.images[6]
            self.rect.move_ip(0, -self._speed)
