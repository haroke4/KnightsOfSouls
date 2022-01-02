"""
Базовые игровые классы такие как хитбокс, партиклы, эффекты и тд.
"""
from files.global_variables import *


class Hitbox(pygame.sprite.Sprite):
    def __init__(self, dx, dy, width, height):
        super().__init__(hitbox_group)  # add second argument "all_sprites" to show image of hitbox
        self.rect = pygame.Rect(0, 0, width, height)
        self.dx, self.dy = dx, dy

    def set_pos(self, x, y):
        self.rect.x, self.rect.y = int(x + self.dx), int(y + self.dy)

    def colliding_objects(self):
        temp = pygame.sprite.spritecollide(self, hitbox_group, False)
        temp.remove(self)
        return temp


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        if hasattr(obj, "x"):
            obj.x += self.dx
            obj.y += self.dy
        else:
            obj.rect.x += self.dx
            obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.x + target.rect.w // 2 - WIDTH // 2.5)
        self.dy = -(target.y + target.rect.h // 2 - HEIGHT // 2.5)
