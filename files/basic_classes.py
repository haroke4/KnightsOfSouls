"""
Базовые игровые классы такие как хитбокс, партиклы, эффекты и тд.
"""
from files.global_variables import *


class Hitbox(pygame.sprite.Sprite):
    def __init__(self, dx, dy, width, height):
        super().__init__(hitbox_group)  # add second argument "all_sprites" to show image of hitbox
        self.rect = pygame.Rect(0, 0, width, height)

        # self.image = pygame.Surface((width, height))
        # self.image.fill(pygame.Color("red"), self.rect)
        # self.image.fill(pygame.Color("light blue"), self.rect.inflate(-5, -5))

        self.dx, self.dy = dx, dy

    def set_pos(self, x, y):
        self.rect.x, self.rect.y = int(x + self.dx), int(y + self.dy)

    def update(self):
        all_sprites.change_layer(self, self.rect.bottom)

    def is_colliding(self):
        temp = pygame.sprite.spritecollide(self, hitbox_group, False)
        temp.remove(self)
        y = x = False
        for i in temp:
            _y = min(abs(self.rect.top - i.rect.bottom),
                     abs(self.rect.bottom - i.rect.top))
            _x = min(abs(self.rect.right - i.rect.left),
                     abs(self.rect.left - i.rect.right))
            y = _x > _y if not y else y  # if y == True we doesnt change value
            x = _y > _x if not x else x
        return x, y
