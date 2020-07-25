from typing import NewType, List, Type


# X and Y Axis Coordinate [x, y]
Coord = NewType('Coord', [int, int])
# more precise coordinate [x.00..., y.00...]
Point = NewType('Point', [float, float])
