from .field import Point, Field
from typing import Optional


class Agent:
    def __init__(self, field: Field) -> None:
        self._point: Optional[Point] = None
        self.on_field: bool = False
        self.next_activity: Optional[str] = None
        self.field = field

    @property
    def point(self) -> Point:
        return self._point

    @point.setter
    def point(self, value: Point) -> None:
        if (0 <= value.x < self.field.height) and (0 <= value.y < self.field.width):
            self._point = value
        else:
            raise ValueError("Point({0}) is outside of Field({1})".format(*value, *self.field.size))
