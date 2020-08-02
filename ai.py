import json

import pygame

from consts import *
import numpy as np

from tile import Tile


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

        self._current_direction = Direction.NORTH

        self._index = 0
        self.image = pygame.transform.scale(self.images[self._index], (TILE_SIZE, TILE_SIZE))
        self.rect = pygame.Rect(x_pos, y_pos, TILE_SIZE, TILE_SIZE)

    def animate_eat(self):
        self._index += 1
        if self._index >= len(self.images):
            self._index = 0
        self.image = pygame.transform.scale(self.images[self._index], (TILE_SIZE, TILE_SIZE))

    def move(self):
        if self._current_direction == Direction.NORTH:
            self.rect.move_ip(0, -self._speed)
        elif self._current_direction == Direction.SOUTH:
            self.rect.move_ip(0, self._speed)
        elif self._current_direction == Direction.EAST:
            self.rect.move_ip(self._speed, 0)
        elif self._current_direction == Direction.WEST:
            self.rect.move_ip(-self._speed, 0)

    def change_direction(self, direction, speed):
        if direction == Direction.NORTH:
            self.rect.move_ip(0, -speed)
        elif direction == Direction.SOUTH:
            self.rect.move_ip(0, speed)
        elif direction == Direction.EAST:
            self.rect.move_ip(speed, 0)
        elif direction == Direction.WEST:
            self.rect.move_ip(-speed, 0)


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

        self._index = 0
        self.image = self.images[self._index]
        self.rect = pygame.Rect(x_pos, y_pos, TILE_SIZE, TILE_SIZE)

    def animate_move(self):
        if self._current_direction == Direction.SOUTH and self.image == self.images[0]:
            self.image = self.images[1]
        elif self._current_direction == Direction.SOUTH and self.image == self.images[1]:
            self.image = self.images[0]
        elif self._current_direction == Direction.WEST and self.image == self.images[2]:
            self.image = self.images[3]
        elif self._current_direction == Direction.WEST and self.image == self.images[3]:
            self.image = self.images[2]
        elif self._current_direction == Direction.EAST and self.image == self.images[4]:
            self.image = self.images[5]
        elif self._current_direction == Direction.EAST and self.image == self.images[5]:
            self.image = self.images[4]
        elif self._current_direction == Direction.NORTH and self.image == self.images[6]:
            self.image = self.images[7]
        elif self._current_direction == Direction.NORTH and self.image == self.images[7]:
            self.image = self.images[6]

data = None
with open('src/data/data.json', 'r') as file:
    data = json.load(file)

mep = np.array([[Tile(x, y, x * TILE_SIZE, y * TILE_SIZE) for y in range(WINDOW_TILE_WIDTH)] for x in range(WINDOW_TILE_HEIGHT)])
for y, column in enumerate(data['staticLevel']):
    for x, value in enumerate(column):
        print(x, y)
        if value == ' ':
            mep[y, x].tileId = TileID.BLANK
        elif value == '!':
            mep[y, x].tileType = TileType.DBL_WALL
            mep[y, x].tileId = TileID.DBL_WALL_V
        elif value == '=':
            mep[y, x].tileType = TileType.DBL_WALL
            mep[y, x].tileId=TileID.DBL_WALL_H
        elif value == 'o':
            mep[y, x].tileType = TileType.DBL_CORNER
        elif value == '|':
            mep[y, x].tileType = TileType.WALL
            mep[y, x].tileId=TileID.WALL_V
        elif value == '-':
            mep[y, x].tileType = TileType.WALL
            mep[y, x].tileId = TileID.WALL_H
        elif value == '+':
            mep[y, x].tileType = TileType.CORNER
        elif value == '.':
            mep[y, x].tileId = TileID.FRUIT
        elif value == '*':
            mep[y, x].tileId = TileID.ENERGIZER
        elif value == 'c':
            mep[y, x].tileId = TileID.CHERRY
        elif value == 'd':
            mep[y, x].tileType = TileType.DOOR

mep = np.array([*mep], dtype=object)
print(mep[-1])