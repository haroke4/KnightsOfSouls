"""
Классы окружающей среды
"""
from files.global_stuff import *


class Wall(BaseGameObject):
    def __init__(self, x, y, img=None):  # У каждой команаты будет свой wall
        super().__init__(x, y, "wall.png", [0, 30, 50, 20])
