import random
import math
from threading import Timer

import pygame

from files.particles import SquareParticle
from files.global_stuff import *
from files.heroes import BaseHero
from files import units_characteristics


class BaseEnemy(BaseGameObject):
    def __init__(self, x, y, image, hp, armor, protection, speed, attack_cooldown, damage,
                 attack_range, player: BaseHero, hitbox=None):
        self.max_hp = self.hp = hp
        self.max_armor = self.armor = armor
        self.protection = protection
        self.initial_speed = self.speed = speed
        self.attack_cooldown = attack_cooldown
        self.can_attack = True
        self.damage = damage
        self.vector = pygame.Vector2(0, 0)
        self.player = player
        self.slowing_down_effect_timer = None
        self.player_side = "left"
        self.blood_color = pygame.Color("red")

        self.distance = 0  # текущяя дистанция между игроком и мобом
        self.attack_range = attack_range
        if not hitbox:
            hitbox = [6, 35, 36, 15]
        super().__init__(x, y, image, hitbox, ENEMY_TEAM)

    def take_damage(self, damage, from_candle=False, count_of_particles=10):
        damage = damage - self.protection
        print(f'{self.__class__.__name__} : {damage}')  # ДЛЯ ДЕБАГГИНГА
        if damage > 0:
            self.armor -= damage
            if self.armor < 0:
                self.hp -= abs(self.armor)
                if self.hp <= 0:
                    self.die()
                self.armor = 0

        if self.alive():
            if from_candle:
                SquareParticle.create_particles(self.global_x + self.rect.w // 2, self.global_y + self.rect.h // 2,
                                                pygame.Color("orange"), count_of_particles)
            else:
                SquareParticle.create_particles(self.global_x + self.rect.w // 2, self.global_y + self.rect.h // 2,
                                                self.blood_color, count_of_particles)

    def look_at_player(self):
        """Меняет вектор self.vector и измеряет растояние """
        self.vector = pygame.Vector2(self.player.hitbox.rect.x - self.hitbox.rect.x,
                                     self.player.hitbox.rect.y - self.hitbox.rect.y)
        self.player_side = "left" if self.vector.x < 0 else "right"
        self.distance = self.vector.length()
        self.vector.normalize_ip()

    def attack(self):
        pass

    def move(self, movement_x, movement_y):
        # двигаем игрока и его хитбокс по по ИКСУ к Игроку
        self.global_x += movement_x
        self.hitbox.set_pos(self.global_x, self.global_y)

        # Если во что то уперлись двигаем моба назад
        if self.hitbox.get_colliding_objects(include_not_slidable_obj=False):
            self.global_x -= movement_x
            self.hitbox.set_pos(self.global_x, self.global_y)

        # двигаем игрока и его хитбокс по по ИГРИКУ к Игроку
        self.global_y += movement_y
        self.hitbox.set_pos(self.global_x, self.global_y)

        # Если во что то уперлись двигаем моба назад
        if self.hitbox.get_colliding_objects(include_not_slidable_obj=False):
            self.global_y -= movement_y
            self.hitbox.set_pos(self.global_x, self.global_y)

    def move_to_player(self):
        """Идти к игроку.  Двигает моба по вектору К игроку"""
        self.move(self.vector.x * self.speed, self.vector.y * self.speed)

    def move_away_from_player(self):
        """Убегать от игрока. Анологичен move_to_player , только двигается по противоположному вектору"""
        self.move(-self.vector.x * self.speed, -self.vector.y * self.speed)

    def get_slowing_down_effect(self, time, value):  # 0.00 < value <= 1
        self.speed = self.initial_speed * value
        if self.slowing_down_effect_timer:
            self.slowing_down_effect_timer.cancel()
        self.slowing_down_effect_timer = Timer(time, self.remove_slowing_down_effect)
        self.slowing_down_effect_timer.start()

    def remove_slowing_down_effect(self):
        self.speed = self.initial_speed

    def can_attack_func(self):
        self.can_attack = True

    def attack_cooldown_func(self):
        self.can_attack = False
        Timer(self.attack_cooldown, self.can_attack_func).start()


class TestEnemy(BaseEnemy):
    def __init__(self, x, y, pl):
        data = units_characteristics.mini_golem
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["speed"],
                         data["attack_cooldown"], data["damage"], data["attack_distance"], pl)

    def attack(self):
        self.player.take_damage(0)
        self.attack_cooldown_func()

    def update(self):
        self.look_at_player()
        if self.distance <= self.attack_range:
            if self.can_attack:
                self.attack()
        else:
            self.move_to_player()
        all_sprites.change_layer(self, self.global_y + self.rect.h)
        super().update()


class Snake(BaseEnemy):
    def __init__(self, x, y, pl):
        data = units_characteristics.snake
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["speed"],
                         data["attack_cooldown"], data["damage"], data["attack_distance"], pl)

    def attack(self):
        self.player.take_damage(self.damage, from_poison=True)
        self.die()

    def update(self):
        self.look_at_player()
        if self.distance <= self.attack_range:
            if self.can_attack:
                self.attack()
        else:
            self.move_to_player()
        all_sprites.change_layer(self, self.global_y + self.rect.h)
        super().update()


class MiniGolem(BaseEnemy):
    def __init__(self, x, y, pl):
        data = units_characteristics.mini_golem
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["speed"],
                         data["attack_cooldown"], data["damage"], data["attack_distance"], pl, hitbox=[30, 80, 40, 20])
        self.gun = Rock(x, y, self.team, data["damage"], self)
        self.new_rock_timer = None
        self.blood_color = pygame.Color(44, 48, 47)
        self.rock_dx, self.rock_dy = 30, 5

        self.add_animation('walk-left', 'Mini-golem/walk-left')
        self.add_animation('walk-right', 'Mini-golem/walk-right')
        self.add_animation('attack-left', 'Mini-golem/attack-left')
        self.add_animation('attack-right', 'Mini-golem/attack-right')

    def attack(self):
        pass
        if self.gun:
            self.gun.shot()
            self.gun = None
            self.new_rock_timer = Timer(self.attack_cooldown, self.new_rock)
            self.new_rock_timer.start()

    def new_rock(self):
        if self.alive():
            self.gun = Rock(self.global_x, self.global_y, self.team, self.damage, self)
            self.can_attack = True
            self.gun.update()

    def die(self):
        if self.new_rock_timer:
            self.new_rock_timer.cancel()
        if self.gun:
            self.gun.die()
        super(MiniGolem, self).die()

    def update(self):
        self.look_at_player()
        anim = None
        if self.distance <= self.attack_range:
            if self.distance <= 200:
                anim = 'walk'
                self.move_away_from_player()
            if self.can_attack:
                self.can_attack = False
                anim = 'attack'
                Timer(0.7, self.attack).start()
        else:
            anim = 'walk'
            self.move_to_player()

        if anim == 'attack':
            self.play_animation(f'attack-{self.player_side}', once=True)
        elif anim == 'walk':
            self.play_animation(f'walk-{self.player_side}')

        all_sprites.change_layer(self, self.global_y + self.rect.h)
        super().update()


class Rock(BaseGameObject):
    def __init__(self, x, y, team, damage, parent: BaseEnemy = False):
        self.damage = damage
        self.parent = parent
        self.angle = 0
        self.speed = 10
        self.shooted = False
        self.vector = pygame.Vector2(0, 0)
        self.dx = 25
        self.dy = -15
        super().__init__(x, y, units_characteristics.mini_golem['gun_img'], HITBOX_ARROW, team, False)
        self.orig_image = self.image

    def shot(self):
        self.vector = pygame.Vector2(1, 0).rotate(-self.angle).normalize()
        self.hitbox.mask = pygame.mask.from_surface(self.image)
        self.shooted = True

    def look_at_player(self):
        x, y = self.parent.player.global_x, self.parent.player.global_y
        self.angle = pygame.Vector2(x - self.parent.hitbox.rect.x - self.dx,
                                    y - self.parent.hitbox.rect.y - self.dy) \
                                    .normalize().angle_to(pygame.Vector2(1, 0))
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
                        i.parent.take_damage(self.damage)
                    else:
                        SquareParticle.create_particles(self.global_x, self.global_y,
                                                        pygame.transform.average_color(i.parent.image))
                    self.die()
        else:
            self.look_at_player()
            self.set_pos(self.parent.hitbox.rect.x + 50 * math.cos(self.angle / 180 * math.pi) + self.dx,
                         self.parent.hitbox.rect.y - 40 * math.sin(self.angle / 180 * math.pi) + self.dy)

        self.hitbox.set_pos(self.global_x, self.global_y)
        super().update()