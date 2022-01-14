import random

import pygame.mouse
import math
from files import units_characteristics
from files.global_stuff import *
from threading import Timer


class BaseHero(BaseGameObject):
    def __init__(self, x, y, image, hp, armor, protection, walk_speed, run_speed, attack_cooldown, damage, anim_folder):
        self.dead = False
        self.max_hp = self.hp = hp
        self.max_armor = self.armor = armor
        self.protection = protection
        self.initial_walk_speed = self.walk_speed = walk_speed
        self.initial_run_speed = self.run_speed = run_speed
        self.attack_cooldown = attack_cooldown
        self.damage = damage
        self.running = False
        self.gun = None
        self.velocity = pygame.Vector2(0, 0)
        super().__init__(x, y, image, [6, 35, 36, 15], PLAYER_TEAM)
        self.damage_multiplier = 1
        self.has_candle = False  # для предмета "свеча"
        self.has_cross = False  # for item Cross
        self.vampirism = 0  # FLOAT
        self.has_welding_helmet = False

        # настройка анимаций
        self.add_animation('up', anim_folder + '/up')
        self.add_animation('left', anim_folder + '/left')
        self.add_animation('right', anim_folder + '/right')
        self.add_animation('down', anim_folder + '/down')

    def key_input(self):
        keystates = pygame.key.get_pressed()
        self.velocity.x = self.velocity.y = 0
        if keystates[pygame.K_a]:
            self.velocity.x += -1
        if keystates[pygame.K_d]:
            self.velocity.x += 1
        if keystates[pygame.K_w]:
            self.velocity.y += -1
        if keystates[pygame.K_s]:
            self.velocity.y += 1
        if not self.velocity.is_normalized() and self.velocity.length() != 0:
            self.velocity.normalize_ip()

        if pygame.mouse.get_pressed()[0]:
            self.running = False
            self.attack(*pygame.mouse.get_pos())

        if self.velocity.length() == 0:
            self.stop_animation()
            return

        if self.velocity.y > 0 and self.velocity.x == 0:
            self.play_animation("down")
        elif self.velocity.y < 0 and self.velocity.x == 0:
            self.play_animation("up")

        if self.velocity.x > 0:
            self.play_animation("right")
        elif self.velocity.x < 0:
            self.play_animation("left")

    def attack(self, x, y):  # Чтобы ошибка не возникала
        pass

    def update(self):
        self.key_input()
        if self.running:
            move_x, move_y = self.velocity.x * self.run_speed, self.velocity.y * self.run_speed
        else:
            move_x, move_y = self.velocity.x * self.walk_speed, self.velocity.y * self.walk_speed

        self.global_x += move_x
        self.hitbox.set_pos(self.global_x, self.global_y)
        if self.hitbox.get_colliding_objects(include_not_slidable_obj=False):
            self.global_x -= move_x
            self.hitbox.set_pos(self.global_x, self.global_y)

        self.global_y += move_y
        self.hitbox.set_pos(self.global_x, self.global_y)
        if self.hitbox.get_colliding_objects(include_not_slidable_obj=False):
            self.global_y -= move_y
            self.hitbox.set_pos(self.global_x, self.global_y)

        all_sprites.change_layer(self, self.global_y + self.rect.h)
        super().update()

    def take_damage(self, damage, from_candle=False):
        """from_candle НЕНАДО ставить TRUE. Это только для предмета свеча"""
        damage = damage * self.damage_multiplier - self.protection
        print(damage, from_candle)
        if damage > 0:
            self.armor -= damage
            if self.armor < 0:
                self.hp -= abs(self.armor)

                if self.hp <= 0:
                    if self.has_cross:  # если есть крест не убиваем
                        self.hp = self.max_hp
                        self.armor = self.max_armor
                        self.damage_multiplier = 0  # дается бессмертие на 3 секунды
                        self.has_cross = False
                        Timer(3, self.change_damage_multiplier, [1]).start()  # убираем бессмертие

                    else:
                        self.die()
                self.armor = 0
        if self.has_candle and not from_candle:
            # индикатор огня
            Timer(1, self.take_damage, [1, True]).start()
            Timer(2, self.take_damage, [1, True]).start()

    def heal(self, value):
        self.hp += value
        if self.hp > self.max_hp:
            self.hp = self.max_hp

    def increase_damage(self, value):  # увеличить урон
        self.damage += value
        if self.gun:
            self.gun.damage += value

    def change_damage_multiplier(self, val):
        self.damage_multiplier = val

    def get_slowing_down_effect(self, time, value):  # 0.00 < value <= 1
        self.run_speed = self.initial_run_speed * value
        self.walk_speed = self.initial_walk_speed

    def remove_slowing_down_effect(self):
        self.run_speed = self.initial_run_speed
        self.walk_speed = self.initial_walk_speed


class SpearMan(BaseHero):
    def __init__(self, x=0, y=0):
        data = units_characteristics.spearman
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["walk_speed"],
                         data["run_speed"], data["attack_cooldown"], data["damage"], 'SpearMan')
        self.gun = Spear(x, y, self.team, data["damage"], self)
        self.spear_dx, self.spear_dy = 30, 5

    def attack(self, x, y):
        if self.gun:
            self.gun.shot()
            self.gun = None
            Timer(self.attack_cooldown, self.new_spear).start()

    def new_spear(self):
        self.gun = Spear(self.global_x, self.global_y, self.team, self.damage, self)
        self.gun.update()


class Spear(BaseGameObject):
    def __init__(self, x, y, team, damage, parent: SpearMan):
        self.damage = damage
        self.parent = parent
        self.angle = 0
        self.speed = 10
        self.shooted = False
        self.vector = pygame.Vector2(0, 0)

        super().__init__(x, y, units_characteristics.spearman['gun_img'], hitbox=HITBOX_ARROW, team=team)
        self.orig_image = self.image

    def shot(self):
        self.vector = pygame.Vector2(1, 0).rotate(-self.angle).normalize()
        self.hitbox.mask = pygame.mask.from_surface(self.image)
        self.shooted = True

    def look_at_mouse(self):
        x, y = from_local_to_global_pos(*pygame.mouse.get_pos())
        self.angle = pygame.Vector2(x - self.parent.global_x - self.rect.w // 2, y - self.parent.global_y
                                    - self.rect.h // 2).normalize().angle_to(pygame.Vector2(1, 0))
        if self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotate(self.orig_image, self.angle)

    def update(self):
        all_sprites.change_layer(self, self.hitbox.rect.bottom)
        if self.shooted:
            self.global_x += self.vector.x * self.speed
            self.global_y += self.vector.y * self.speed
            for i in self.hitbox.get_colliding_objects():
                if pygame.sprite.collide_mask(self.hitbox, i):
                    if hasattr(i.parent, "hp"):
                        dmg = self.damage * 3 if random.randrange(1, 11) == 9 else self.damage
                        i.parent.take_damage(dmg)
                        self.parent.heal(dmg * self.parent.vampirism)
                        if self.parent.has_candle:
                            Timer(1, i.parent.take_damage, [1, True]).start()
                            Timer(2, i.parent.take_damage, [1, True]).start()
                            Timer(3, i.parent.take_damage, [1, True]).start()
                            Timer(4, i.parent.take_damage, [1, True]).start()
                            Timer(5, i.parent.take_damage, [1, True]).start()
                    self.die()
        else:
            self.look_at_mouse()
            self.set_pos(self.parent.global_x + 40 * math.cos(self.angle / 180 * math.pi) + 3,
                         self.parent.global_y - 40 * math.sin(self.angle / 180 * math.pi) + 15)

        self.hitbox.set_pos(self.global_x, self.global_y)
        super().update()


class MagicMan(BaseHero):
    def __init__(self, x=0, y=0):
        data = units_characteristics.magicman
        self.can_shot = True
        self.attack_range = data["attack_range"]
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["walk_speed"],
                         data["run_speed"], data["attack_cooldown"], data["damage"], 'MagicMan')
        super().update()

    def attack(self, x, y):
        if self.can_shot:
            x, y = from_local_to_global_pos(x, y)
            vector = pygame.Vector2(x - self.global_x, y - self.global_y)
            if vector.length() >= self.attack_range:
                vector = vector.normalize() * self.attack_range + (self.global_x, self.global_y)
                x, y = vector.x, vector.y
            fire = MagicManFire(x, y, self.damage, self.team, self)
            self.can_shot = False
            Timer(self.attack_cooldown, self.enable_shot).start()
            Timer(self.attack_cooldown, fire.die).start()

    def enable_shot(self):
        self.can_shot = True


class MagicManFire(BaseGameObject):
    def __init__(self, x, y, damage, team, parent):
        self.damage = damage
        self.parent = parent
        self.damage_taken = []
        super().__init__(x - 50, y - 20, units_characteristics.magicman["gun_img"], HITBOX_FULL_RECT, team, False)
        all_sprites.change_layer(self, 0)

    def update(self):
        for i in self.hitbox.get_colliding_objects():
            if i in self.damage_taken:
                continue
            if hasattr(i.parent, "hp"):
                i.parent.take_damage(self.damage)
                self.parent.heal(self.damage * self.parent.vampirism)
                # i.parent.get_slowing_down_effect(time, percent)
                if self.parent.has_candle:
                    Timer(1, i.parent.take_damage, [1, True]).start()
                    Timer(2, i.parent.take_damage, [1, True]).start()
                    Timer(3, i.parent.take_damage, [1, True]).start()
                    Timer(4, i.parent.take_damage, [1, True]).start()
                    Timer(5, i.parent.take_damage, [1, True]).start()
            self.damage_taken.append(i)
        super().update()


class SwordMan(BaseHero):
    def __init__(self, x=0, y=0):
        data = units_characteristics.swordman
        self.can_attack = True
        self.dash_length = 30
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["walk_speed"],
                         data["run_speed"], data["attack_cooldown"], data["damage"], 'SwordMan')
        self.gun = Sword(x, y, self.damage, self.team, self)

    def enable_attack(self):
        self.can_attack = True

    def attack(self, x, y):
        if self.can_attack:
            self.gun.attack()
            self.can_attack = False
            Timer(self.attack_cooldown, self.enable_attack).start()


class Sword(BaseGameObject):
    def __init__(self, x, y, damage, team, parent):
        self.damage = damage
        self.parent = parent
        self.damage_taken = []
        self.attacking = False
        self.angle = 0
        self.vector = pygame.Vector2(0, 0)
        super().__init__(x - 50, y - 20, units_characteristics.swordman["gun_img"], HITBOX_ARROW, team)
        self.orig_image = self.image
        all_sprites.change_layer(self, 0)

    def look_at_mouse(self):
        x, y = from_local_to_global_pos(*pygame.mouse.get_pos())
        self.angle = pygame.Vector2(x - self.parent.global_x - self.rect.w // 2, y - self.parent.global_y
                                    - self.rect.h // 2).normalize().angle_to(pygame.Vector2(1, 0))
        if self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotate(self.orig_image, self.angle)

    def attack(self):
        self.vector = pygame.Vector2(1, 0).rotate(-self.angle).normalize()
        self.attacking = True
        Timer(0.05, self.attacking_false).start()

    def attacking_false(self):
        self.attacking = False
        self.damage_taken.clear()
        self.vector = pygame.Vector2(0, 0)

    def update(self):
        all_sprites.change_layer(self, self.hitbox.rect.bottom)
        if self.attacking:
            self.global_x += self.vector.x * 10
            self.global_y += self.vector.y * 10
            for i in self.hitbox.get_colliding_objects():
                if i not in self.damage_taken:
                    if pygame.sprite.collide_mask(self.hitbox, i):
                        if hasattr(i.parent, "hp"):
                            i.parent.take_damage(self.damage)
                            self.parent.heal(self.damage * self.parent.vampirism)
                            if self.parent.has_candle:
                                Timer(1, i.parent.take_damage, [1, True]).start()
                                Timer(2, i.parent.take_damage, [1, True]).start()
                                Timer(3, i.parent.take_damage, [1, True]).start()
                                Timer(4, i.parent.take_damage, [1, True]).start()
                                Timer(5, i.parent.take_damage, [1, True]).start()
                        self.damage_taken.append(i)

        else:
            self.look_at_mouse()
            self.set_pos(self.parent.global_x + 40 * math.cos(self.angle / 180 * math.pi) + 3,
                         self.parent.global_y - 40 * math.sin(self.angle / 180 * math.pi) + 20)
        self.hitbox.set_pos(self.global_x, self.global_y)
        super().update()


class Meshok(BaseHero):
    def __init__(self, x, y):
        data = units_characteristics.spearman
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["walk_speed"],
                         data["run_speed"], data["attack_cooldown"], data["damage"], 'SpearMan')
        self.team = None
        self.hitbox.team = None

    def key_input(self):
        pass
