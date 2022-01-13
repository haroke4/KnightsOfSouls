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


class SteelPlaster(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "SteelPlaster.png")

    def give_effect(self, obj):
        obj.max_armor += 5
        self.die()


class Steroids(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "Steroids.png")

    def give_effect(self, obj):
        obj.increase_damage(2)
        self.die()


class EnergyDrink(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "EnergyDrink.png")

    def give_effect(self, obj):
        obj.run_speed += 0.5
        self.die()


class PocketWatch(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "PocketWatch.png")

    def give_effect(self, obj):
        obj.attack_cooldown -= 0.2 if obj.attack_cooldown - 0.2 > 0.2 else 0
        self.die()


class AppleBag(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "AppleBag.png")
        self.parent = None

    def give_effect(self, obj):
        pass


class Garlic(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "Garlic.png")
        self.parent = None

    def give_effect(self, obj):
        self.parent = obj
        self.image = pygame.image.load("GarlicCircle.png")
        self.hitbox.rect = self.image.get_rect()
        self.hitbox.mask = pygame.mask.from_surface(self.image)


#    def update(self):
#        if self.parent:
#            self.set_pos(self.parent.global_x, self.parent.global_y)
#            for i in self.hitbox.get_colliding_objects():
#                if isinstance(i, BaseMob): #NEED BASE MOB!
#                    if pygame.sprite.collide_mask(self.hitbox, i):
#                        i.take_damage(1)
#        super().update()

class LHead(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "LHead.png")

    def give_effect(self, obj):
        obj.increase_damage(5)
        obj.protection -= 2
        self.die()


class Candle(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "Candle.png")

    def give_effect(self, obj):
        obj.fire_damage = True
        self.die()


class WeightingStone(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "WeightingStone.png")

    def give_effect(self, obj):
        obj.increase_damage(5)
        obj.attack_cooldown += 0.2
        self.die()


class CursedBlood(BaseItem):
    def __init__(self, x, y):
        """Класс сделан! А у самих героев вампиризм не реализован!!"""
        super().__init__(x, y, "CursedBlood.png")

    def give_effect(self, obj):
        obj.vampirism += 0.1
        obj.max_hp -= 3
        obj.hp -= 3
        self.die()


class Mirror(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "Mirror.png")

    def give_effect(self, obj):
        pass
        # реализовать с помощью damage multiplier!!!!
