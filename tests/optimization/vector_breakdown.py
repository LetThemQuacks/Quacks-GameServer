import math
from functools import cache
import time
import numpy as np
import cv2

class time_it:
    def __enter__(self):
        self.start = time.time()

    def __exit__(self, *args):
        print(f'Took {round(time.time() - self.start, 4)} seconds')

@cache
def _breakdown_vector(vector: float, angle: int):
    """
        Help function for breakdown_duck_vector
    """
    angle = math.radians(angle)
    vector = abs(vector)

    vector_x = round(vector * math.cos(angle), 4)
    vector_y = round(vector * math.sin(angle), 4)
    return (vector_x, vector_y)

original_img = np.zeros((500, 500, 3), np.uint8)
img = original_img.copy()

angle = 45
vector = 100

center = 255

while True:

    key = cv2.waitKey(25) & 0xFF

    if key == ord('q'):
        break
    elif key == 81:
        angle -= 5
    elif key == 83:
        angle += 5
    elif key == 84:
        vector -= 5
    elif key == 82:
        vector += 5
    elif key == ord(' '):
        print('--------------------------------')
        print(f'Vector: {vector} Angle: {angle}')
        print(f'X: {x} Y: {y}')


    x, y = _breakdown_vector(vector, angle - 90)
    ox, oy = x, y
    x, y = int(x), int(y)
    x += 255
    y += 255

    img = original_img.copy()

    img = cv2.circle(img, (center, center), vector, (80, 80, 80), 2)
    #img = cv2.circle(img, (x, center), vector, (255, 80, 80), 2)
    #img = cv2.circle(img, (center, y), vector, (80, 80, 255), 2)

    img = cv2.line(img, (center, center), (x, y), (255, 255, 255), 2)
    img = cv2.line(img, (center, center), (x, center), (255, 0, 0), 2)
    img = cv2.line(img, (center, center), (center, y), (0, 0, 255), 2)

    img = cv2.putText(img, f'{ox}', (x + (-25 if (x-255) > 0 else 0), center - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (255, 0, 0))
    img = cv2.putText(img, f'{oy}', (center + 5, y), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 0, 255))


    cv2.imshow('Frame', img)

cv2.destroyAllWindows()
