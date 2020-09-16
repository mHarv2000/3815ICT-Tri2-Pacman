class Direction:
    """ A clock-wise lateral dynamically incremental compass used to tell the direction relative to the grid.

    Each direction Is iterable and can be iterated over infinitely to return a string based
    representation of each compass direction (orientation) or a number representing the orientation (digit);
    'n' | 0 (North), 'e' | 1 (East), 's' | 2 (South) and 'w' | 3 (West)

    """
    def __init__(self, value):
        if isinstance(value, str):
            self.__orientation = value
            self.__digit = self.convert(value)
        elif isinstance(value, int):
            self.__digit = value
            self.__orientation = self.convert(value)

    @property
    def orientation(self):
        """ get direction

        :return: string representation of direction """
        return self.__orientation

    @orientation.setter
    def orientation(self, value):
        """ set direction by string

        :param value: string character (n, s, e, w) """
        self.__orientation = value
        self.__digit = self.convert(value)

    @property
    def digit(self) -> int:
        """ get digit

        :return: digit representing the direction """
        return self.__digit

    @digit.setter
    def digit(self, value) -> None:
        """ set digit

        :param value: digit (0-3)
        """
        self.__digit = value
        self.__orientation = self.convert(value)

    @staticmethod
    def convert(value):
        """ set orientation equivalent to the digit and vice versa

        :param value: orientation or digit
        :return: return the opposite value of the one passed in through value,
                 e.g. passing in orientation will return the digit
        """
        if isinstance(value, int):
            if value == 0:
                return 'n'
            elif value == 1:
                return 'e'
            elif value == 2:
                return 's'
            elif value == 3:
                return 'w'
            else:
                raise ValueError('digit must be in the range 0-3')
        elif isinstance(value, str):
            if value == 'n':
                return 0
            elif value == 'e':
                return 1
            elif value == 's':
                return 2
            elif value == 'w':
                return 3
            else:
                raise ValueError(f'character \'{value}\' does not exist')
        else:
            raise TypeError('only accepts the characters n, s, e, w and integers 0-3')

    def is_north_or_south(self):
        """ check if direction is north or south

        :return: True/False """
        return True if self.__digit == 0 \
                       or self.__digit == 2 else False

    def __repr__(self):
        return self.__orientation.upper()

    def __str__(self):
        """ when cast to a string, return the orientation """
        return self.__orientation

    def __int__(self):
        """ when cast to an integer, return the digit """
        return self.__digit

    def __add__(self, other):
        """ allow direction objects to be incremental

        The RHS can allow for integers but also other directions to be incremented, however,
        digit is reset to 0 after exceeding 3 and resumes incrementing. e.g. 0 + 5 = 1

        :return: the sum of both digits"""
        return Direction((self.__digit + other) % 4)

    def __eq__(self, other):
        """ check if orientation or digit is equal to RHS """
        if isinstance(other, str):
            return self.__orientation == other
        elif isinstance(other, int):
            return self.__digit == other
        return False

    def __sub__(self, other):
        """ allow direction objects to be decremental

        digit is reset to 3 after subceeding 0 and resumes decrementing. e.g. 3 - 5 = 2

        :param other: integer value or Direction
        :return: the sum of subtracted digits"""
        return Direction((self.__digit - other) % 4)

    def __iadd__(self, other):
        """ adds and sets digit and orientation with the += operator

        :param other: orientation or digit
        :returns self:
        """
        self.__digit += other
        if self.__digit < 0 or self.__digit > 3:
            self.__digit %= abs(4)
        self.__orientation = self.convert(self.__digit)
        return self

    def __isub__(self, other):
        """ subtracts and sets digit and orientation with the -= operator

        :param other: orientation or digit
        :returns self:
        """
        self.__digit -= other
        if self.__digit < 0:
            self.__digit %= 4
        self.__orientation = self.convert(self.__digit)
        return self

    def __reversed__(self):
        """ subtracts 2 from the digit to get the opposite direction

        example: inverting north will be south (n -> s), (0 -> 2)
        """
        return Direction((self.__digit - 2) % 4)
