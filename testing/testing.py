import glob
import pygame
from src.scripts.misc import Direction


class PacMan:

    def __init__(self, gx, gy, size):
        try:
            url = glob.glob('../img/pacman/*.png')
            self.__animation_seq = [pygame.transform.scale(pygame.image.load(img), (size, size)) for img in url]
        except FileNotFoundError as err:
            raise FileExistsError("file path to directory: '%s' does not exist" % err)
        self.__gx = gx
        self.__gy = gy

        self.__frame_index = 0
        self.__animation_playback = 1
        self.frame = self.__animation_seq[0]

        self.__current_direction = Direction('e')
        self.__speed = 10

    @property
    def x(self):
        return self.__gx

    @property
    def y(self):
        return self.__gy

    def get(self):
        return self.frame

    def update_frame(self):
        if self.__frame_index == len(self.__animation_seq) - 1:
            self.__animation_playback = -1
        elif self.__frame_index == 0:
            self.__animation_playback = 1
        self.__frame_index += self.__animation_playback
        self.frame = self.__animation_seq[self.__frame_index]

    def update(self):
        if self.__current_direction == 0:
            self.__gy += self.__speed
        elif self.__current_direction == 1:
            self.__gx += self.__speed
        elif self.__current_direction == 2:
            self.__gy -= self.__speed
        elif self.__current_direction == 3:
            self.__gx -= self.__speed

    def rotate(self, new_direction):
        old_angle = int(self.__current_direction) * 90
        new_angle = int(new_direction) * 90
        self.__current_direction = new_direction
        for i, frame in enumerate(self.__animation_seq):
            self.__animation_seq[i] = pygame.transform.rotate(self.__animation_seq[i], -old_angle)
            self.__animation_seq[i] = pygame.transform.rotate(self.__animation_seq[i], new_angle)

