import pygame

from consts import Colour, Coord

WIDTH, HEIGHT = 500, 500

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
done = False

font = pygame.font.Font("./font/BarcadeBrawlRegular.ttf", 20)
text = font.render("Hello, World", True, (0, 128, 0))


class Button:

	def __init__(self, pos: Coord, size: list, text: str, colour: Colour):
		border = pygame.Rect(pos, size)
		font = pygame.font.Font("./font/BarcadeBrawlRegular.ttf", 20)
		font_disp = font.render(text, True, colour)

		self.__border = border
		self.__text = font_disp

	def get_border(self):
		return self.__border

	def get_text(self):
		return self.__text


btn = Button((50, 50), (100, 30), "Settings", (255, 0, 0))

while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
		if event.type == pygame.MOUSEBUTTONUP:
			print('up')
			if btn.get_border().collidepoint(event.pos):

				print('hit')
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				done = True

	screen.blit(btn.get_text(), (WIDTH // 2, HEIGHT // 2))
	pygame.draw.rect(screen, )

	pygame.display.flip()
	clock.tick(1)
