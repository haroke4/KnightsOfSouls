"""
Классы окружающей среды
"""
import pygame

from files.global_stuff import *


class Wall(BaseGameObject):
    def __init__(self, x, y, img):
        super().__init__(x, y, img, HITBOX_FULL_RECT, can_slide=True)
        self.avg_color = pygame.Color(17, 23, 12)


class Floor(BaseGameObject):
    def __init__(self, x, y, img):
        super().__init__(x, y, img, None, can_slide=False)
        self.image = pygame.Surface((1472, 1024))
        self.image.fill((115, 125, 156))
        self.rect = self.image.get_rect()
        all_sprites.change_layer(self, -9999)


class MovingWall(BaseGameObject):
    def __init__(self, x, y, img=None):  # У каждой команаты будет свой wall
        super().__init__(x, y, "wall.png", [0, 30, 50, 20])
        self.goto = "right"

    def update(self):
        self.global_x += 1 if self.goto == "right" else -1

        self.hitbox.set_pos(self.global_x, self.global_y)
        for i in self.hitbox.get_colliding_objects():
            i.parent.global_x += 1 if self.goto == "right" else -1
        if self.global_x > 150:
            self.goto = "l"
        elif self.global_x < 0:
            self.goto = "right"
        super().update()
