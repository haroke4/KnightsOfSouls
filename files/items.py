from files.global_stuff import *
from files.heroes import BaseHero


class BaseItem(BaseGameObject):
    def __init__(self, x, y, img):  # drop - предмет выпадает или нет
        super(BaseItem, self).__init__(x, y, img, HITBOX_FULL_RECT, team=None, can_slide=False)
        self.hitbox.mask = pygame.mask.from_surface(self.image)

    def give_effect(self, obj):  # чтобы ошибка не возникала
        pass

    def update(self):
        for colliding_item in self.hitbox.get_colliding_objects():
            if isinstance(colliding_item.parent, BaseHero):
                if pygame.sprite.collide_mask(self.hitbox, colliding_item):
                    self.give_effect(colliding_item.parent)
        super().update()


class Plaster(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "Plaster.png")

    def give_effect(self, obj):
        obj.max_hp += 7
        self.die()




