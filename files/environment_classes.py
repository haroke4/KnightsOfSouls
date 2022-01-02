"""
Классы окружающей среды
"""
from files.global_variables import *
from files.basic_classes import Hitbox


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, img=None): # У каждой команаты будет свой wall
        super().__init__(all_sprites)
        self.image = pygame.image.load("files/img/wall.png")
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.hitbox = Hitbox(0, 30, 50, 20)
        self.hitbox.set_pos(self.rect.x, self.rect.y)

    def update(self):
        all_sprites.change_layer(self, self.rect.bottom)
