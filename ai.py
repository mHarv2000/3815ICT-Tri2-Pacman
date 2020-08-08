import pygame
from consts import *


class PacMan(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos):
        super(PacMan, self).__init__()
        self.images = [
            pygame.image.load('./src/img/pacman/pacman_0.png'),
            pygame.image.load('./src/img/pacman/pacman_1.png'),
            pygame.image.load('./src/img/pacman/pacman_2.png'),
            pygame.image.load('./src/img/pacman/pacman_3.png'),
            pygame.image.load('./src/img/pacman/pacman_2.png'),
            pygame.image.load('./src/img/pacman/pacman_1.png'),
        ]

        self._current_direction = Direction.SOUTH
        self._speed = 3
        self._index = 0
        self.image = pygame.transform.scale(self.images[self._index], (TILE_SIZE, TILE_SIZE))
        self.rect = pygame.Rect(x_pos, y_pos, TILE_SIZE, TILE_SIZE)

    @property
    def direction(self):
        return self._current_direction

    @direction.setter
    def direction(self, value: Direction):
        self._current_direction = value if isinstance(value, Direction) else None

    def animate(self, *args):
        self.__animate_eat()
        self.__animate_move()

    def __animate_eat(self):
        self._index += 1
        if self._index >= len(self.images):
            self._index = 0
        self.image = pygame.transform.scale(self.images[self._index], (TILE_SIZE, TILE_SIZE))

    def __animate_move(self):
        if self._current_direction == Direction.NORTH:
            self.rect.move_ip(0, -self._speed)
        elif self._current_direction == Direction.SOUTH:
            self.rect.move_ip(0, self._speed)
        elif self._current_direction == Direction.EAST:
            self.rect.move_ip(self._speed, 0)
        elif self._current_direction == Direction.WEST:
            self.rect.move_ip(-self._speed, 0)


class Ghost(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, name: str):
        super(Ghost, self).__init__()
        self.images = [
            pygame.image.load(f'./src/img/ghost/{name}/ghost_down_0.png'),
            pygame.image.load(f'./src/img/ghost/{name}/ghost_down_1.png'),
            pygame.image.load(f'./src/img/ghost/{name}/ghost_left_0.png'),
            pygame.image.load(f'./src/img/ghost/{name}/ghost_left_1.png'),
            pygame.image.load(f'./src/img/ghost/{name}/ghost_right_0.png'),
            pygame.image.load(f'./src/img/ghost/{name}/ghost_right_1.png'),
            pygame.image.load(f'./src/img/ghost/{name}/ghost_up_0.png'),
            pygame.image.load(f'./src/img/ghost/{name}/ghost_up_1.png'),
        ]

        self._current_direction = Direction.NORTH
        self._speed = 10
        self._index = 0
        self.image = self.images[self._index]
        self.rect = pygame.Rect(x_pos, y_pos, TILE_SIZE, TILE_SIZE)

    def animate_move(self):
        if self._current_direction == Direction.SOUTH and self.image == self.images[0]:
            self.image = self.images[1]
            self.rect.move_ip(0, self._speed)
        elif self._current_direction == Direction.SOUTH and self.image == self.images[1]:
            self.image = self.images[0]
            self.rect.move_ip(0, self._speed)
        elif self._current_direction == Direction.WEST and self.image == self.images[2]:
            self.image = self.images[3]
            self.rect.move_ip(-self._speed, 0)
        elif self._current_direction == Direction.WEST and self.image == self.images[3]:
            self.image = self.images[2]
            self.rect.move_ip(-self._speed, 0)
        elif self._current_direction == Direction.EAST and self.image == self.images[4]:
            self.image = self.images[5]
            self.rect.move_ip(self._speed, 0)
        elif self._current_direction == Direction.EAST and self.image == self.images[5]:
            self.image = self.images[4]
            self.rect.move_ip(self._speed, 0)
        elif self._current_direction == Direction.NORTH and self.image == self.images[6]:
            self.image = self.images[7]
            self.rect.move_ip(0, -self._speed)
        elif self._current_direction == Direction.NORTH and self.image == self.images[7]:
            self.image = self.images[6]
            self.rect.move_ip(0, -self._speed)