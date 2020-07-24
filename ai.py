import pygame


class PacMan(pygame.sprite.Sprite):

    def __init__(self, x_pos, y_pos, size):
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
        self.rect = pygame.Rect(x_pos, y_pos, size, size)

    def animate_eat(self):
        self.index += 1
        if self.index >= len(self.images):
            self.index = 0
        self.image = self.images[self.index]
