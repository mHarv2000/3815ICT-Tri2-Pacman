from typing import Tuple
import pygame


class Label:
	"""
	Label/Button UI Element

	A pygame label displaying text which can be used for events.
	"""

	def __init__(self, x, y, colour, text_str, padding, font):
		"""
		:param x: x-Axis coordinate
		:type x: int
		:param y: y-Axis coordinate
		:type y: int
		:param text_str: the text string
		:type text_str: str
		:param colour: colour of the text
		:type colour: Colour
		:param font: type of font
		:type font: pygame.font.Font
		:param padding: the space between the edges of the label and the text
		:type padding: int
		"""

		self.__x = x
		self.__y = y
		self.__text_str = text_str
		self.__colour = colour
		self.__font = font
		self.__padding = padding
		self.__text = font.render(text_str, True, colour)
		self.__rect = pygame.Rect(x, y, self.__text.get_width() + padding, self.__text.get_height() + padding)
		self.__text_pos = (self.__rect.centerx - (self.__text.get_width() // 2),
		                   self.__rect.centery - (self.__text.get_height() // 2))

	@property
	def rect(self) -> pygame.Rect:
		""" get label box """
		return self.__rect

	@property
	def text_str(self) -> str:
		""" get text string """
		return self.__text_str

	@text_str.setter
	def text_str(self, text: str) -> None:
		""" set text string """
		if not isinstance(text, str):
			raise TypeError("text must be string")
		self.__text_str = text
		self.__text = self.__font.render(self.__text_str, True, self.__colour)
		self.__rect = pygame.Rect(self.__x, self.__y, self.__text.get_width() + self.__padding,
		                          self.__text.get_height() + self.__padding)
		self.__text_pos = (self.__rect.centerx - (self.__text.get_width() // 2),
		                   self.__rect.centery - (self.__text.get_height() // 2))

	@property
	def text(self) -> pygame.Surface:
		""" get text object """
		return self.__text

	@property
	def pos(self) -> Tuple[int, int]:
		""" get x and y position """
		return self.__text_pos

	def render(self, display) -> None:
		"""
		display the elements to the screen
		:param display: the current pygame display
		:type display: pygame.Surface
		"""
		pygame.draw.rect(display, (0, 0, 0), self.__rect)
		display.blit(self.__text, self.__text_pos)


class Spinner:
	"""
	Spinner Input UI Element

	A UI Integer input with arrows to increase/decrease the value by a given step amount
	"""

	def __init__(self, x, y, value, font, minimum=0, maximum=1, step=1):
		"""
		:param x: x coordinte
		:type x: int
		:param y: y coordinte
		:type y: int
		:param value: integer value of the text
		:type value: int
		:param font: font object
		:type value: pygame.font.Font
		:param minimum: the minimum value the value can go to
		:type minimum: int
		:param maximum: the maximum value the value can go to
		:type maximum: int
		:param step: the amount to increase the value by
		:type step: int
		"""
		self.__x = x
		self.__y = y
		self.__value = value
		self.__font = font
		self.__minimum = minimum
		self.__maximum == maximum
		self.__step = step
		self.__text = font.render(str(value), True, (255, 255, 255))
		self.__rect = pygame.Rect(self.__x, self.__y, self.__text.get_width() + 5,
		                          self.__text.get_height() + 5)
		self.__text_pos = (self.__rect.centerx - (self.__text.get_width() // 2),
		                   self.__rect.centery - (self.__text.get_height() // 2))

	def add_step(self, is_positive=True) -> None:
		"""
		increase/decrease value by step
		:param is_positive: should the value be increased (False means decrease)
		:type is_positive: bool
		"""
		self.__value += self.__step

	@property
	def rect(self) -> pygame.Rect:
		""" get rectangle """
		return self.__rect

	@property
	def value(self) -> None:
		""" get value """
		return self.__value

	@value.setter
	def value(self, new_value: int) -> None:
		""" set value and update spinner elements """
		self.__value = new_value if self.__minimum <= new_value <= self.__maximum else self.__value
		self.__recreate()

	@property
	def pos(self):
		return self.__x, self.__y

	def set_step(self, value: int) -> None:
		""" set step amount """
		if not isinstance(value, int) and value <= self.__maximum:
			raise ValueError("step size exceeds the maximum amount")
		self.__step = value

	def set_font(self, new_font: pygame.font.Font) -> None:
		""" set font """
		if not isinstance(new_font, pygame.font.Font):
			raise ValueError("new font must be a pygame Font object")
		self.__font = new_font
		self.__recreate()

	def __recreate(self) -> None:
		""" recreate spinner object by reinitialising it's elements """
		self.__text = self.__font.render(str(self.__value), True, (255, 255, 255))
		self.__rect = pygame.Rect(self.__x, self.__y, self.__text.get_width() + 5,
		                          self.__text.get_height() + 5)
		self.__text_pos = (self.__rect.centerx - (self.__text.get_width() // 2),
		                   self.__rect.centery - (self.__text.get_height() // 2))

	def render(self, display) -> None:
		"""
		display the elements to the screen
		:param display: the current pygame display
		:type display: pygame.Surface
		:return:
		"""
		# TODO: make render function
