from typing import Tuple
from math import sqrt, pow
from .duck import Duck
from core import logging

try:
    from functools import cache
except ImportError:
    from functools import lru_cache as cache
    logging.warning('Failed to import "cache" from functools, using "lru_cache" instead.')



Vector = Tuple[float, float]

class Collisions:
    @staticmethod
    def are_colliding(duck1: Duck, duck2: Duck) -> bool:
        return Collisions._are_colliding(duck1.position, duck1.radius, duck2.position, duck2.radius)

    @staticmethod
    @cache()
    def _are_colliding(pos1: Vector, radius1: float, pos2: Vector, radius2: float) -> bool:
        """
            Help funciton for Collisions.are_colliding
        """
        return Collisions._points_distance(pos1, pos2) <= (radius1 + radius2)

    @staticmethod
    @cache()
    def _points_distance(pos1: Vector, pos2: Vector) -> Vector:
        """
            Help function for Collisions._are_colliding
        """
        return sqrt(pow(pos2[0] - pos1[0], 2) + pow(pos2[1] - pos1[1], 2))
