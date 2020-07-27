import pygame

from consts import TILE_SIZE, Direction


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
        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x_pos, y_pos, TILE_SIZE, TILE_SIZE)

    def animate_eat(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]


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

        self.direction = Direction.NORTH

        self.index = 0
        self.image = self.images[self.index]
        self.rect = pygame.Rect(x_pos, y_pos, TILE_SIZE, TILE_SIZE)

    def animate_move(self):
        if self.direction == Direction.SOUTH and self.image == self.images[0]:
            self.image = self.images[1]
        elif self.direction == Direction.SOUTH and self.image == self.images[1]:
            self.image = self.images[0]
        elif self.direction == Direction.WEST and self.image == self.images[2]:
            self.image = self.images[3]
        elif self.direction == Direction.WEST and self.image == self.images[3]:
            self.image = self.images[2]
        elif self.direction == Direction.EAST and self.image == self.images[4]:
            self.image = self.images[5]
        elif self.direction == Direction.EAST and self.image == self.images[5]:
            self.image = self.images[4]
        elif self.direction == Direction.NORTH and self.image == self.images[6]:
            self.image = self.images[7]
        elif self.direction == Direction.NORTH and self.image == self.images[7]:
            self.image = self.images[6]
