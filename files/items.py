from files.global_stuff import *
from files.heroes import BaseHero


class BaseItem(BaseGameObject):
    def __init__(self, x, y, img, drop: bool):  # drop - предмет выпадает или нет
        self.drop = drop  #
        super(BaseItem, self).__init__(x, y, img, HITBOX_FULL_RECT, team=None, can_slide=False)

    def give_effect(self, obj):  # чтобы ошибка не возникала
        pass

    def update(self):
        if self.drop:
            for colliding_item in self.hitbox.get_colliding_objects():
                if isinstance(colliding_item.parent, BaseHero):
                    self.give_effect(colliding_item.parent)
        super().update()


class Plaster(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "Plaster.png", True)  # True if dropable

    def give_effect(self, obj):
        print("pick2")
