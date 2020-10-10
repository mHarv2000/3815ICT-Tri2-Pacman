import glob
import threading
import time

import pygame
from src.scripts.misc import Direction


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
            url = glob.glob('../img/pacman/*.png')
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
            url = glob.glob(f'../img/ghost/{ghost_name}/*.png')
            vuln_url = glob.glob('../img/ghost/vulnerable/*.png')
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
        timer = threading.Thread(target=__timer, args=(sec,))
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