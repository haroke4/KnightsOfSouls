import pygame.image

from files.global_stuff import *
from files.heroes import BaseHero
from threading import Timer
from random import randint, choice


def get_random_item():
    # 77% - обычный предмет
    # 23% - редкий предмет
    if randint(0, 11) <= 7:
        return choice(ordinary_items)
    else:
        return choice(rare_items)


def get_random_epic_item():
    return choice(epic_items)


class BaseItem(BaseGameObject):
    def __init__(self, x, y, img):  # drop - предмет выпадает или нет
        super(BaseItem, self).__init__(x, y, "items/" + img, HITBOX_FULL_RECT, team=None, can_slide=False)
        self.hitbox.mask = pygame.mask.from_surface(self.image)

    def give_effect(self, obj):  # чтобы ошибка не возникала
        pass

    def update(self):
        for colliding_item in self.hitbox.get_colliding_objects():
            if isinstance(colliding_item.parent, BaseHero):
                self.give_effect(colliding_item.parent)
        super().update()


class Plaster(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "Plaster.png")

    def give_effect(self, obj):
        obj.max_hp += 7
        obj.hp += 7
        self.die()


class SteelPlaster(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "SteelPlaster.png")

    def give_effect(self, obj):
        obj.max_armor += 5
        obj.armor += 5
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
        obj.run_speed += 1
        obj.initial_run_speed += 1
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
        obj.apple_bag_count += 0.5
        self.die()


class ElectricRing(BaseItem):
    def __init__(self, x, y):
        self.can_attack = False
        self.parent = None
        self.dx = self.dy = 0
        self.damage = 1
        super().__init__(x, y, "PlasmLamp.png")

    def give_effect(self, obj):
        if not obj.has_electric_ring:
            obj.has_electric_ring = self
            self.parent = obj
            self.image = pygame.image.load("files/img/Electrofield.png")
            self.rect = self.image.get_rect()
            self.hitbox.rect = self.image.get_rect()
            self.hitbox.mask = pygame.mask.from_surface(self.image)
            self.dx = (self.rect.w - obj.rect.w) / 2
            self.dy = (self.rect.h - obj.rect.h) / 2 - 10
            self.enable_attack()
        else:
            obj.has_electric_ring.damage += 1

    def enable_attack(self):
        self.can_attack = True

    def update(self):
        if self.parent:
            all_sprites.change_layer(self, self.global_y)
            self.set_pos(self.parent.global_x - self.dx, self.parent.global_y - self.dy)
            self.hitbox.set_pos(self.global_x, self.global_y)
            if self.can_attack:
                collided = self.hitbox.get_colliding_objects()
                if collided:
                    Timer(1, self.enable_attack).start()
                    self.can_attack = False
                for i in collided:
                    if hasattr(i.parent, "hp"):  # Need live sushestvo
                        if pygame.sprite.collide_mask(self.hitbox, i):
                            i.parent.take_damage(self.damage)
        else:
            super().update()
        self.rect.x, self.rect.y = [int(i) for i in from_global_to_local_pos(self.global_x, self.global_y)]


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
        obj.candle_damage += 1
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
        super().__init__(x, y, "CursedBlood.png")

    def give_effect(self, obj):
        obj.vampirism += 0.1
        obj.max_hp -= 3
        obj.take_damage(3, from_vampirism=True)
        self.die()


class Cross(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "Cross.png")

    def give_effect(self, obj):
        obj.has_cross = True
        self.die()


class WeldingHelmet(BaseItem):
    def __init__(self, x, y):
        super().__init__(x, y, "WeldingHelmet.png")

    def give_effect(self, obj):
        obj.walk_speed -= 0.5
        obj.run_speed -= 0.5
        obj.protection += 2
        obj.armor += 10
        obj.max_armor += 10
        obj.has_welding_helmet = True
        change_draw_area(500, 220, 1400, 820)
        self.die()


class TwinMirror(BaseItem):
    def __init__(self, x, y):
        self.owner = None
        self.status = None
        self.status_changed = False
        self.timer = None
        super().__init__(x, y, "TwinMirror.png")

    def give_effect(self, obj):
        if not obj.has_mirror:
            obj.has_mirror = self
            self.image = pygame.image.load('files/img/empty.png')
            self.owner = obj
            self.status = 1  # 1 - дамаг анулируется | 2 - дамаг удва

    def change_status(self, val):
        self.status = val
        self.status_changed = False

    def update(self):
        if self.status:
            if self.status == 1 and not self.status_changed:
                self.owner.change_damage_multiplier(0)
                self.status_changed = True
                self.timer = Timer(5, self.change_status, [2])
                self.timer.daemon = True
                self.timer.start()

            elif self.status == 2 and not self.status_changed:
                self.owner.change_damage_multiplier(2)
                self.status_changed = True
                self.timer = Timer(10, self.change_status, [1])
                self.timer.daemon = True
                self.timer.start()
        else:
            super(TwinMirror, self).update()


ordinary_items = [Plaster, SteelPlaster, Steroids, EnergyDrink, PocketWatch, AppleBag, ElectricRing]
rare_items = [LHead, Candle, WeightingStone, CursedBlood]
epic_items = [Cross, WeldingHelmet, TwinMirror]
