from dataclasses import dataclass
from typing import Tuple


@dataclass
class Duck:
    """
        :Attributes:
            - `position`: The Duck 2D position in the map
            - `velocity`: Duck's Velocity Vector
            - `velocity_bd`: Duck's Velocity Vector broken down in x and y
            - `angle`: Duck's angle ( used to calculate velocity_bd )
            - `max_velocity`: The duck's max velocity
    """

    position: Tuple[float, float] = (0.0, 0.0)
    velocity: float = 0.0
    velocity_bd: Tuple[float, float] = (0.0, 0.0)
    angle: int = 0

    max_velocity: float = 10
    radius: float = 5 # TODO: Check this value in-game
