import math
from typing import Tuple

def breakdown_vector(vector: float, angle: float) -> Tuple[float, float]:
    angle_radians = math.radians(angle)
    vector = abs(vector)

    vector_x = round(vector * math.cos(angle), 4)
    vector_y = round(vector * math.sin(angle), 4)
    return (vector_x, vector_y)

print(breakdown_vector(4, 60))
exit()


for angle in range(0, 91, 5):
    print(angle, breakdown_vector(10, angle))

def elastic_collision(pos1, vel1, mass1, pos2, vel2, mass2):
    """Perfectly elastic collision between 2 balls.

    Args:
        pos1: Center of the first ball.
        vel1: Velocity of the first ball.
        mass1: Mass of the first ball.
        pos2: Center of the second ball.
        vel2: Velocity of the second ball.
        mass2: Mass of the second ball.

    Return:
        Two velocities after the collision.

    """
    # switch to coordinate system of ball 1
    pos_diff = np.subtract(pos2, pos1)
    vel_diff = np.subtract(vel2, vel1)

    pos_dot_vel = pos_diff.dot(vel_diff)
    assert pos_dot_vel < 0  # colliding balls do not move apart

    dist_sqrd = pos_diff.dot(pos_diff)

    bla = 2 * (pos_dot_vel * pos_diff) / ((mass1 + mass2) * dist_sqrd)
    vel1 += mass2 * bla
    vel2 -= mass1 * bla

    return vel1, vel2

