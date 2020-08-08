import math

import pygame
from ai import PacMan
from consts import *
from level import Grid, TileMap
from state import GameManager

grid = TileMap(GenType.SQUAREGRID)
pacman = PacMan(grid[0][0].x, grid[1][1].y)
pcmg = pygame.sprite.GroupSingle(pacman)
pygame.init()

clock = pygame.time.Clock()
main_screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT),
                                      flags=pygame.FULLSCREEN if IS_FULLSCREEN else 0)


def draw():
    for row in grid:
        for tile in row:
            print(tile)
            if tile.tile_id == TileID.DBL_WALL_TL:
                pygame.draw.arc(main_screen, BLUE, tile.rect, math.pi * .5, math.pi, 1)
                pygame.draw.rect(main_screen, RED, tile.rect, 1)
            elif tile.tile_id == TileID.DBL_WALL_TR:
                pygame.draw.arc(main_screen, BLUE, tile.rect, 0, math.pi * .5, 1)
                pygame.draw.rect(main_screen, RED, tile.rect, 1)
            elif tile.tile_id == TileID.DBL_WALL_BR:
                pygame.draw.arc(main_screen, BLUE, tile.rect, math.pi * 1.5, math.pi * 2, 1)
                pygame.draw.rect(main_screen, RED, tile.rect, 1)
            elif tile.tile_id == TileID.DBL_WALL_BL:
                pygame.draw.arc(main_screen, BLUE, tile.rect, math.pi, math.pi * 1.5, 1)
                pygame.draw.rect(main_screen, RED, tile.rect, 1)
            elif tile.tile_id == TileID.DBL_WALL_H:
                pygame.draw.line(main_screen, BLUE,
                                 [tile.x, tile.y + int(TILE_SIZE / 2)],
                                 [tile.x + TILE_SIZE, tile.y + int(TILE_SIZE / 2)])
            elif tile.tile_id == TileID.DBL_WALL_V:
                pygame.draw.line(main_screen, BLUE,
                                 [tile.x + int(TILE_SIZE / 2), tile.y],
                                 [tile.x + int(TILE_SIZE / 2), tile.y + TILE_SIZE])
            elif tile.tile_id == TileID.WALL_TL:
                pygame.draw.arc(main_screen, BLUE, tile.rect, math.pi * .5, math.pi, 1)
                pygame.draw.rect(main_screen, RED, tile.rect, 1)
            elif tile.tile_id == TileID.WALL_TR:
                pygame.draw.arc(main_screen, BLUE, tile.rect, 0, math.pi * .5, 1)
                pygame.draw.rect(main_screen, RED, tile.rect, 1)
            elif tile.tile_id == TileID.WALL_BR:
                pygame.draw.arc(main_screen, BLUE, tile.rect, math.pi * 1.5, math.pi * 2, 1)
                pygame.draw.rect(main_screen, RED, tile.rect, 1)
            elif tile.tile_id == TileID.WALL_BL:
                pygame.draw.arc(main_screen, BLUE, tile.rect, math.pi, math.pi * 1.5, 1)
                pygame.draw.rect(main_screen, RED, tile.rect, 1)
            elif tile.tile_id == TileID.WALL_H:
                pygame.draw.line(main_screen, BLUE,
                                 [tile.x, tile.y + int(TILE_SIZE / 2)],
                                 [tile.x + TILE_SIZE, tile.y + int(TILE_SIZE / 2)])
            elif tile.tile_id == TileID.WALL_V:
                pygame.draw.line(main_screen, BLUE,
                                 [tile.x + int(TILE_SIZE / 2), tile.y],
                                 [tile.x + int(TILE_SIZE / 2), tile.y + TILE_SIZE])

manager = GameManager()

while True:
    manager()
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                pacman.direction = Direction.NORTH
            elif event.key == pygame.K_DOWN:
                pacman.direction = Direction.SOUTH
            elif event.key == pygame.K_RIGHT:
                pacman.direction = Direction.EAST
            elif event.key == pygame.K_LEFT:
                pacman.direction = Direction.WEST
        if event.type == pygame.QUIT:
            pygame.quit()
            quit(0)

    main_screen.fill((0, 0, 0))
    draw()
    pacman.animate()
    pcmg.draw(main_screen)
    pygame.display.flip()

