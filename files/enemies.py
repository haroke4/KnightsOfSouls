import random
import math
from threading import Timer
from files.particles import SquareParticle
from files.global_stuff import *
from files.heroes import BaseHero
from files import units_characteristics


class BaseEnemy(BaseGameObject):
    def __init__(self, x, y, image, hp, armor, protection, speed, attack_cooldown, damage,
                 attack_range, player: BaseHero, anim_folder=None):
        # anim_folder для анимаций. Пока что не  трогай. Пусть остается
        self.max_hp = self.hp = hp
        self.max_armor = self.armor = armor
        self.protection = protection
        self.initial_speed = self.speed = speed
        self.attack_cooldown = attack_cooldown
        self.damage = damage
        self.vector = pygame.Vector2(0, 0)
        self.player = player
        self.slowing_down_effect_timer = None

        self.distance = 0  # текущяя дистанция между игроком и мобом
        self.attack_range = attack_range
        super().__init__(x, y, image, [6, 35, 36, 15], ENEMY_TEAM)

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
                                                pygame.Color("red"), count_of_particles)

    def look_at_player(self):
        """Меняет вектор self.vector и измеряет растояние """
        self.vector = pygame.Vector2(self.player.global_x - self.global_x, self.player.global_y - self.global_y)
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


class TestEnemy(BaseEnemy):
    def __init__(self, x, y, pl):
        data = units_characteristics.mini_golem
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["speed"],
                         data["attack_cooldown"], data["damage"], data["attack_distance"], pl)

    def update(self):
        self.look_at_player()
        if self.distance <= self.attack_range:
            self.attack()
        else:
            self.move_to_player()
        all_sprites.change_layer(self, self.global_y + self.rect.h)
        super().update()
