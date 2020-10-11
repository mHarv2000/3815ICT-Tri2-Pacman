import unittest
from src.scripts.misc import Direction


class TestDirection(unittest.TestCase):
    def test_values(self):
        """ test orientation and digit values during assignment """
        direction1 = Direction('n')
        direction2 = Direction('e')
        direction3 = Direction('s')
        direction4 = Direction('w')

        # test character n for North
        self.assertEqual(direction1.orientation, 'n')
        # test integer 0 for North
        self.assertEqual(direction1.digit, 0)
        # test if north or south
        self.assertEqual(direction1.is_north_or_south(), True)

        # test character s for South
        self.assertEqual(direction3.orientation, 's')
        # test integer 2 for South
        self.assertEqual(direction3.digit, 2)
        # test if north or south
        self.assertEqual(direction3.is_north_or_south(), True)

        # test character e for East
        self.assertEqual(direction2.orientation, 'e')
        # test character 1 for East
        self.assertEqual(direction2.digit, 1)
        # test if north or south
        self.assertEqual(direction2.is_north_or_south(), False)

        # test character w for West
        self.assertEqual(direction4.orientation, 'w')
        # test character 3 for West
        self.assertEqual(direction4.digit, 3)
        # test if north or south
        self.assertEqual(direction4.is_north_or_south(), False)

    def test_convert(self):
        """ test converting between orientation and digit values """
        direction = Direction('n')

        # test converting s to 2
        self.assertEqual(direction.convert('s'), 2)
        # test converting 0 to n
        self.assertEqual(direction.convert(0), 'n')

        # test throwing error on incorrect type
        self.assertRaises(TypeError, direction.convert, 1.0)
        # test throwing error when digit is out of range
        self.assertRaises(ValueError, direction.convert, 4)
        # test throwing error when orientation is not found
        self.assertRaises(ValueError, direction.convert, 'q')

    def test_add(self):
        """ test addition """
        direction = Direction('n')
        direction += 1

        # test adding and assigning works
        self.assertEqual(direction.digit, 1)
        # test adding works
        self.assertEqual(int(direction + 1), 2)

        direction += 3
        # test digit resets to 0 once limit is exceeded
        self.assertEqual(direction.digit, 0)

    def test_sub(self):
        """ test subtraction """
        direction = Direction('w')
        direction -= 1

        self.assertEqual(direction.digit, 2)
        self.assertEqual(int(direction - 1), 1)

        direction -= 3
        # test digit resets to 3 once digit goes below 0
        self.assertEqual(direction.digit, 3)


if __name__ == '__main__':
    unittest.main()
