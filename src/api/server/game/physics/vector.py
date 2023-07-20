import math
from .duck import Duck
from typing import Float
from core import logging

try:
    from functools import cache
except ImportError:
    from functools import lru_cache as cache
    logging.warning('Failed to import "cache" from functools, using "lru_cache" instead.')


def breakdown_duck_velocity(duck: Duck) -> None:
    """
        Breakdown the duck's velocity vector in X and Y
    """
    angle_radians = math.radians(duck.angle)
    duck.vector_bd = _breakdown_vector(abs(duck.velocity), angle_radians)

@cache()
def _breakdown_vector(vector: float, angle: int) -> Tuple[float, float]:
    """
        Help function for breakdown_duck_vector
    """
    vector_x = round(vector * math.cos(angle), 4)
    vector_y = round(vector * math.sin(angle), 4)
    return (vector_x, vector_y)

