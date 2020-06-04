from .field import Point
from typing import Optional, Tuple


class Agent:
    def __init__(self, field_size: Tuple[int, int]) -> None:
        self._point: Optional[Point] = None
        self.on_field: bool = False
        self.next_activity: Optional[str] = None
        self.field_size = field_size

    @property
    def point(self) -> Point:
        return self._point

    @point.setter
    def point(self, value: Point) -> None:
        if (0 <= value.x < self.field_size[0]) and (0 <= value.y < self.field_size[1]):
            self._point = value
        else:
            raise ValueError("Point({0}) is outside of Field({1})".format(*value, *self.field_size))
