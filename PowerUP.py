#202411
from campy.graphics.gobjects import GRect
import random

POWERUP_SIZE = 25
POWERUP_SPEED = 3


class PowerUp(GRect):
    def __init__(self, x, y):
        super().__init__(POWERUP_SIZE, POWERUP_SIZE, x=x, y=y)
        self.filled = True
        color = random.choice(["gold", "blue", "red", "Purple "])  # Correct usage of random.choice
        self.fill_color = color
        self.color = color

    def move(self, dx=0, dy=POWERUP_SPEED):
        self.y += dy


