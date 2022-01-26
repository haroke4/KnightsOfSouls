import math
import random

import pygame
from threading import Timer
from files.particles import SquareParticle
from files.global_stuff import BaseGameObject, all_sprites, ENEMY_TEAM, HITBOX_FULL_RECT, WIDTH, HEIGHT
from files import units_characteristics


class BaseEnemy(BaseGameObject):
    def __init__(self, x, y, image, hp, armor, protection, speed, attack_cooldown, damage,
                 attack_range, player, hitbox=None):
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
        self.dead = False
        self.invulnerability = False

        self.distance = 0  # текущяя дистанция между игроком и мобом
        self.attack_range = attack_range
        if not hitbox:
            hitbox = [6, 35, 36, 15]
        super().__init__(x, y, image, hitbox, ENEMY_TEAM)

    def take_damage(self, damage, from_candle=False, count_of_particles=10):
        if not self.invulnerability:
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
        self.vector = pygame.Vector2(self.player.hitbox.rect.x + self.player.hitbox.rect.w // 2 - \
                                     self.hitbox.rect.x - self.hitbox.rect.w // 2,
                                     self.player.hitbox.rect.y + self.player.hitbox.rect.h // 2 - \
                                     self.hitbox.rect.y - self.hitbox.rect.h // 2)
        self.player_side = "left" if self.vector.x < 0 else "right"
        self.distance = self.vector.length()
        self.vector.normalize_ip()

    def die(self):
        super().die()
        self.dead = True

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
                         data["attack_cooldown"], data["damage"], data["attack_distance"], pl, hitbox=[30, 60, 40, 40])
        self.gun = Rock(x, y, self.team, data["damage"], self)
        self.new_rock_timer = None
        self.blood_color = pygame.Color(44, 48, 47)
        self.rock_dx, self.rock_dy = 30, 5

        self.add_animation('walk-left', 'Mini-golem/walk-left')
        self.add_animation('walk-right', 'Mini-golem/walk-right')
        self.add_animation('attack-left', 'Mini-golem/attack-left')
        self.add_animation('attack-right', 'Mini-golem/attack-right')

    def attack(self):
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
        super().__init__(x, y, units_characteristics.mini_golem['gun_img'], HITBOX_FULL_RECT, team, False)
        self.orig_image = self.image

    def shot(self):
        x = self.parent.player.hitbox.rect.x
        y = self.parent.player.hitbox.rect.y
        self.vector = pygame.Vector2(x - self.hitbox.rect.x,
                                     y - self.hitbox.rect.y).normalize()
        self.hitbox.mask = pygame.mask.from_surface(self.image)
        self.shooted = True

    def update_angle(self):
        x, y = self.parent.player.global_x, self.parent.player.global_y
        self.angle = pygame.Vector2(x - self.parent.hitbox.rect.x - self.dx, y - self.parent.hitbox.rect.y - self.dy) \
            .normalize().angle_to(pygame.Vector2(1, 0))
        if self.angle < 0:
            self.angle += 360

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
                                                        i.parent.avg_color)
                    self.die()
        else:
            self.update_angle()
            self.set_pos(self.parent.hitbox.rect.x + 50 * math.cos(self.angle / 180 * math.pi) + self.dx,
                         self.parent.hitbox.rect.y - 40 * math.sin(self.angle / 180 * math.pi) + self.dy)

        self.hitbox.set_pos(self.global_x, self.global_y)
        super().update()


class Dog(BaseEnemy):
    def __init__(self, x, y, pl):
        data = units_characteristics.dog
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["speed"],
                         data["attack_cooldown"], data["damage"], data["attack_distance"], pl,
                         hitbox=[5, 40, 83, 32])

        self.add_animation('walk-left', 'Dog/walk-left')
        self.add_animation('walk-right', 'Dog/walk-right')

    def attack(self):
        self.player.take_damage(self.damage)
        self.attack_cooldown_func()

    def update(self):
        self.look_at_player()
        if self.can_attack:
            if self.distance <= self.attack_range and self.can_attack:
                self.attack()
            else:
                self.move_to_player()
                self.play_animation(f'walk-{self.player_side}')
        all_sprites.change_layer(self, self.global_y + self.rect.h)
        super().update()


class Tree(BaseEnemy):
    def __init__(self, x, y, pl):
        data = units_characteristics.tree

        self.needles = []
        self.attack_timer = None

        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["speed"],
                         data["attack_cooldown"], data["damage"], data["attack_distance"], pl,
                         hitbox=[11, 65, 73, 35])
        self.blood_color = pygame.Color("Dark green")
        self.change_vect()
        self.attack_cooldown_func()
        self.add_animation('Walk', 'Tree/Walk')
        self.add_animation('StandUp', 'Tree/StandUp')
        self.add_animation('Spin', 'Tree/Spin')
        self.add_animation('Jump', 'Tree/Jump')
        self.play_animation('StandUp', True)
        self.play_animation('Walk', play_now=False)

    def change_vect(self):
        self.vect = pygame.Vector2(random.randrange(-3, 4, 2), random.randrange(-3, 4, 2)).normalize() * self.speed
        timer = Timer(1, self.change_vect)
        timer.daemon = True
        timer.start()

    def create_needles(self):
        x = self.global_x + self.hitbox.dx + self.hitbox.rect.w // 2
        y = self.global_y + self.hitbox.dy + self.hitbox.rect.h // 2
        for i in range(-1, 2):
            for g in range(-1, 2):
                if i == g == 0:
                    continue
                self.needles.append(Needle(x, y, pygame.Vector2(i, g).normalize()))
        self.play_animation('StandUp', once=True, play_now=True)
        self.play_animation('Walk', play_now=False)

    def update(self):
        if self.get_current_animation() == 'Walk':
            self.look_at_player()
            self.move(self.vect.x * self.speed, self.vect.y * self.speed)
            if self.can_attack:
                self.play_animation('Jump', once=True, play_now=True)
                self.play_animation('Spin', once=True, play_now=False)
                self.attack_timer = Timer(1, self.create_needles)
                self.attack_timer.start()
                self.attack_cooldown_func()
            all_sprites.change_layer(self, self.global_y + self.rect.h)
        super().update()

    def die(self):
        if self.attack_timer:
            self.attack_timer.cancel()
        super().die()


class Needle(BaseGameObject):  # игла
    def __init__(self, x, y, vect):
        self.vect = vect
        self.can_attack = True
        self.damage = units_characteristics.tree["damage"]
        self.speed = 10
        super().__init__(x, y, "Needle.png", HITBOX_FULL_RECT, ENEMY_TEAM, False)
        self.image = pygame.transform.rotate(self.image, 360 - pygame.Vector2(1, 0).angle_to(self.vect))

    def update(self):
        self.global_x += self.vect.x * self.speed
        self.global_y += self.vect.y * self.speed
        for i in self.hitbox.get_colliding_objects():
            try:
                i.parent.take_damage(self.damage)
                self.can_attack = False
            except AttributeError:
                pass
            self.die()
        self.hitbox.set_pos(self.global_x, self.global_y)
        super().update()


class IceSoul(BaseEnemy):
    def __init__(self, x, y, pl):
        data = units_characteristics.ice_soul
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["speed"],
                         data["attack_cooldown"], data["damage"], data["attack_distance"], pl, hitbox=[30, 60, 40, 40])
        self.gun = Ice(x, y, self.team, data["damage"], self)
        self.new_ice_timer = None
        self.blood_color = pygame.Color(84, 94, 176)
        self.rock_dx, self.rock_dy = 30, 5

        self.add_animation('walk-left', 'Ice spirit/walk-left')
        self.add_animation('walk-right', 'Ice spirit/walk-right')
        self.add_animation('attack-left', 'Ice spirit/attack-left')
        self.add_animation('attack-right', 'Ice spirit/attack-right')

    def attack(self):
        if self.gun:
            self.gun.shot()
            self.gun = None
            self.new_ice_timer = Timer(self.attack_cooldown, self.new_ice)
            self.new_ice_timer.start()

    def new_ice(self):
        if self.alive():
            self.gun = Ice(self.global_x, self.global_y, self.team, self.damage, self)
            self.can_attack = True
            self.gun.update()

    def die(self):
        if self.new_ice_timer:
            self.new_ice_timer.cancel()
        if self.gun:
            self.gun.die()
        super(IceSoul, self).die()

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


class Ice(BaseGameObject):
    def __init__(self, x, y, team, damage, parent: BaseEnemy = False):
        self.damage = damage
        self.parent = parent
        self.angle = 0
        self.speed = 10
        self.shooted = False
        self.vector = pygame.Vector2(0, 0)
        self.dx = 25
        self.dy = -15
        super().__init__(x, y, units_characteristics.ice_soul['gun_img'], HITBOX_FULL_RECT, team, False)
        self.orig_image = self.image

    def shot(self):
        x = self.parent.player.hitbox.rect.x
        y = self.parent.player.hitbox.rect.y
        self.vector = pygame.Vector2(x - self.hitbox.rect.x,
                                     y - self.hitbox.rect.y).normalize()
        self.hitbox.mask = pygame.mask.from_surface(self.image)
        self.shooted = True

    def update_angle(self):
        x, y = self.parent.player.global_x, self.parent.player.global_y
        self.angle = pygame.Vector2(x - self.parent.hitbox.rect.x - self.dx, y - self.parent.hitbox.rect.y - self.dy) \
            .normalize().angle_to(pygame.Vector2(1, 0))
        if self.angle < 0:
            self.angle += 360

    def update(self):
        all_sprites.change_layer(self, self.hitbox.rect.bottom)
        if self.shooted:
            self.global_x += self.vector.x * self.speed
            self.global_y += self.vector.y * self.speed
            for i in self.hitbox.get_colliding_objects():
                if pygame.sprite.collide_mask(self.hitbox, i):
                    if hasattr(i.parent, "hp"):
                        i.parent.take_damage(self.damage)
                        i.parent.get_slowing_down_effect(2, 0.75)
                    else:
                        SquareParticle.create_particles(self.global_x, self.global_y,
                                                        i.parent.avg_color)
                    self.die()
        else:
            self.update_angle()
            self.set_pos(self.parent.hitbox.rect.x + 50 * math.cos(self.angle / 180 * math.pi) + self.dx,
                         self.parent.hitbox.rect.y - 40 * math.sin(self.angle / 180 * math.pi) + self.dy)

        self.hitbox.set_pos(self.global_x, self.global_y)
        super().update()


class FireSoul(BaseEnemy):
    def __init__(self, x, y, pl):
        data = units_characteristics.fire_soul
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["speed"],
                         data["attack_cooldown"], data["damage"], data["attack_distance"], pl, hitbox=[30, 60, 40, 40])
        self.blood_color = pygame.Color(201, 52, 62)

        self.add_animation('walk-left', 'Fire spirit/walk-left')
        self.add_animation('walk-right', 'Fire spirit/walk-right')
        self.add_animation('attack-left', 'Fire spirit/attack-left')
        self.add_animation('attack-right', 'Fire spirit/attack-right')

    def attack(self):
        pos = [self.player.global_x, self.player.global_y]
        Timer(0.1, self.fire_attack, pos).start()
        self.attack_cooldown_func()

    def fire_attack(self, x, y):
        self.fire = Fire(x, y, self.team, self.damage, self)

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



# BOSSES

class DragonBoss(BaseEnemy):
    # NEED TO BE TESTED
    def __init__(self, x, y, pl):
        self.positions = [[6615, 165], [7745, 165], [6615, 815], [7745, 815]]
        data = units_characteristics.dragonboss
        self.fly_speed = data["fly_speed"]
        self.fly_to = None
        self.flying = False
        self.meele_range = data["m_range"]
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["speed"],
                         data["attack_cooldown"], data["damage"], data["attack_distance"], pl)
        self.attack_cooldown_func()

    def attack(self):
        pos = [self.player.global_x, self.player.global_y]
        Timer(0.1, self.fire_attack, pos).start()
        self.attack_cooldown_func()

    def fly(self):
        self.fly_to = random.choice(self.positions)
        while pygame.Vector2.distance_to(pygame.Vector2(self.global_x, self.global_y),
                                         pygame.Vector2(self.fly_to[0], self.fly_to[1])) <= 500:
            self.fly_to = random.choice(self.positions)
        self.vect = pygame.Vector2(self.fly_to[0] - self.global_x,
                                   self.fly_to[1] - self.global_y).normalize() * self.fly_speed
        if self.fly_to:
            self.flying = True
            Timer(1, self.stop_fly).start()

    def stop_fly(self):
        self.flying = False
        self.can_attack = True

    def fire_attack(self, x, y):
        self.fire = Fire(x, y, self.team, self.damage, self)

    def m_attack(self):
        self.player.take_damage(self.damage)
        self.attack_cooldown_func()
        self.fly()

    def update(self):
        self.look_at_player()
        if self.flying:
            self.move(self.vect.x, self.vect.y)
            self.can_attack = False
        else:
            if self.distance <= self.attack_range:
                if self.distance <= self.meele_range:
                    self.move_to_player()
                    if self.can_attack:
                        self.m_attack()
                        self.can_attack = False
                else:
                    self.move_to_player()
                    if self.can_attack:
                        self.attack()
                        self.can_attack = False
            else:
                self.move_to_player()
        all_sprites.change_layer(self, self.global_y + self.rect.h)
        super().update()


class Fire(BaseGameObject):
    def __init__(self, x, y, team, damage, parent: BaseEnemy = False):
        self.damage = damage
        self.parent = parent
        self.team = team
        self.can_attack = False
        super().__init__(x, y, 'drago_attack.png', HITBOX_FULL_RECT, team, False)
        self.orig_image = self.image
        self.pre_attack_img = pygame.image.load('files/img/drago_pre_attack.png')
        self.image = self.pre_attack_img
        Timer(0.5, self.change_img).start()
        Timer(0.5, self.change_pre_attack).start()
        Timer(5, self.die).start()

    def change_img(self):
        self.image = self.orig_image

    def change_pre_attack(self):
        self.can_attack = True

    def cooldown(self):
        self.can_attack = True

    def attack(self, i):
        i.parent.take_damage(self.damage)
        self.can_attack = False
        Timer(2, self.cooldown)

    def update(self):
        if self.can_attack:
            for i in self.hitbox.get_colliding_objects():
                if pygame.sprite.collide_mask(self.hitbox, i):
                    if hasattr(i.parent, "hp"):
                        self.attack(i)
        all_sprites.change_layer(self, self.global_y)
        super().update()


class NecroBoss(BaseEnemy):
    def __init__(self, x, y, pl):
        data = units_characteristics.necroboss
        self.enemyes = [MiniGolem, Snake, Tree, Dog]
        self.minions = []
        self.can_ult = False
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["speed"],
                         data["attack_cooldown"], data["damage"], data["attack_distance"], pl, hitbox=[30, 60, 40, 40])
        self.new_rock_timer = None

        self.add_animation('walk-left', 'Necromancer/walk-left')
        self.add_animation('walk-right', 'Necromancer/walk-right')
        Timer(2, self.allow_ult).start()

    def attack(self):
        NecroAttack(self.global_x + self.rect.w // 2, self.global_y + self.rect.h // 2, self.player)
        self.attack_cooldown_func()

    def ult(self):
        for i in self.minions:
            if not i.alive():
                self.minions.remove(i)
        if len(self.minions) < 3:
            count = 3 - len(self.minions)
            for i in random.sample(self.enemyes, count):
                self.minions.append(i(self.global_x, self.global_y, self.player))
            print(self.minions)
            self.can_ult = False
            Timer(5, self.allow_ult).start()

    def allow_ult(self):
        self.can_ult = True

    def update(self):
        self.look_at_player()
        anim = None
        if self.can_ult is True:
            self.ult()
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
        # NEED add animation to necromant
        self.play_animation(f'walk-{self.player_side}')

        all_sprites.change_layer(self, self.global_y + self.rect.h)
        super().update()

    def die(self):
        for i in self.minions:
            i.die()
        super().die()


class NecroAttack(BaseGameObject):
    def __init__(self, x, y, pl):
        pl_x = pl.hitbox.rect.x
        pl_y = pl.hitbox.rect.y

        self.speed = 10
        self.damage = units_characteristics.necroboss["damage"]
        super().__init__(x, y, 'NecromantAttack.png', HITBOX_FULL_RECT, ENEMY_TEAM, False)
        self.vector = pygame.Vector2(pl_x - self.hitbox.rect.x,
                                     pl_y - self.hitbox.rect.y).normalize()

    def update(self):
        self.global_x += self.vector.x * self.speed
        self.global_y += self.vector.y * self.speed
        for i in self.hitbox.get_colliding_objects():
            if pygame.sprite.collide_mask(self.hitbox, i):
                if hasattr(i.parent, "hp"):
                    i.parent.take_damage(self.damage)
                else:
                    SquareParticle.create_particles(self.global_x, self.global_y,
                                                    i.parent.avg_color)
                self.die()
        self.hitbox.set_pos(self.global_x, self.global_y)
        super(NecroAttack, self).update()


class Hunter(BaseEnemy):
    def __init__(self, x, y, pl):
        data = units_characteristics.hunter
        self.can_ult = False
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["speed"],
                         data["attack_cooldown"], data["damage"], data["attack_distance"], pl, hitbox=[30, 60, 40, 40])

        # self.add_animation('walk-left', 'hunter/walk-left')
        # self.add_animation('walk-right', 'hunter/walk-right')
        Timer(2, self.allow_ult).start()

    def attack(self):
        HunterAttack(self.global_x + self.rect.w // 2, self.global_y + self.rect.h // 2, self.player)
        self.attack_cooldown_func()
        self.speed = self.initial_speed

    def ult(self):
        self.enemyes = [
                Dog(self.global_x - 100, self.global_y - 200, self.player),
                Dog(self.global_x - 100, self.global_y + 200, self.player),
                Dog(self.global_x - 100, self.global_y, self.player),
            ]
        self.can_ult = False

    def allow_ult(self):
        self.can_ult = True

    def update(self):
        self.look_at_player()
        anim = None
        if self.can_ult:
            self.ult()
        if self.distance <= self.attack_range:
            if self.distance <= 500:
                anim = 'walk'
                self.move_away_from_player()
            if self.can_attack:
                self.can_attack = False
                anim = 'attack'
                self.speed += 100
                self.move_away_from_player()
                self.speed = 0
                Timer(1, self.attack).start()
        else:
            anim = 'walk'
            self.move_to_player()
        # NEED add animation to Hunter
        # self.play_animation(f'walk-{self.player_side}')

        all_sprites.change_layer(self, self.global_y + self.rect.h)
        super().update()


class HunterAttack(BaseGameObject):
    def __init__(self, x, y, pl):
        pl_x = pl.hitbox.rect.x
        pl_y = pl.hitbox.rect.y

        self.speed = 15
        self.damage = units_characteristics.hunter["damage"]
        super().__init__(x, y, 'RockBall.png', HITBOX_FULL_RECT, ENEMY_TEAM, False)
        self.vector = pygame.Vector2(pl_x - self.hitbox.rect.x,
                                     pl_y - self.hitbox.rect.y).normalize()

    def update(self):
        self.global_x += self.vector.x * self.speed
        self.global_y += self.vector.y * self.speed
        for i in self.hitbox.get_colliding_objects():
            if pygame.sprite.collide_mask(self.hitbox, i):
                if hasattr(i.parent, "hp"):
                    i.parent.take_damage(self.damage)
                    i.parent.get_slowing_down_effect(2, 0)
                else:
                    SquareParticle.create_particles(self.global_x, self.global_y,
                                                    i.parent.avg_color)
                self.die()
        self.hitbox.set_pos(self.global_x, self.global_y)
        super(HunterAttack, self).update()


class Golem(BaseEnemy):
    def __init__(self, x, y, pl):
        data = units_characteristics.hunter
        self.ult_count = 1
        self.enemyes = []
        self.need_check = False
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["protection"], data["speed"],
                         data["attack_cooldown"], data["damage"], data["attack_distance"], pl, hitbox=[30, 60, 40, 40])

        # self.add_animation('walk-left', 'hunter/walk-left')
        # self.add_animation('walk-right', 'hunter/walk-right')

    def ult(self):
        self.invulnerability = True
        self.need_check = True
        self.ult_count -= 1
        Timer(2, self.spawn_mini_golem).start()
        Timer(7, self.spawn_mini_golem).start()
        Timer(12, self.spawn_mini_golem).start()

    def spawn_mini_golem(self):
        mg = MiniGolem(self.global_x, self.global_y, self.player)
        self.enemyes.append(mg)

    def stop_ult(self):
        self.invulnerability = False
        self.need_check = False

    def allow_ult(self):
        self.can_ult = True

    def start_check(self):
        self.need_check = True

    def check_enemyes(self):
        i = 0
        while i < len(self.enemyes):
            if self.enemyes[i].dead:
                self.enemyes.remove(self.enemyes[i])
                i -= 1
            i += 1
        if len(self.enemyes) == 0:
            self.stop_ult()
        self.need_check = False

    def m_attack(self):
        self.player.take_damage(self.damage)
        self.attack_cooldown_func()

    def attack(self):
        GolemAttack(self.global_x + self.rect.w // 2, self.global_y + self.rect.h // 2, self.player)
        self.attack_cooldown_func()

    def update(self):
        if self.ult_count == 1 and self.hp <= self.max_hp // 2:
            self.ult()
        if self.invulnerability:
            anim = 'ult'
            if self.need_check:
                Timer(3, self.check_enemyes).start()
                Timer(4, self.start_check).start()
                self.need_check = False
        else:
            self.look_at_player()
            anim = None
            if self.distance <= self.attack_range:
                anim = 'walk'
                self.move_to_player()
                if self.distance <= 50:
                    if self.can_attack:
                        anim = 'attack'
                        self.m_attack()
                elif self.can_attack:
                    anim = 'attack'
                    Timer(0.5, self.attack).start()
                    self.can_attack = False
            else:
                anim = 'walk'
                self.move_to_player()
            # NEED add animation to Golem
            # self.play_animation(f'walk-{self.player_side}')

        all_sprites.change_layer(self, self.global_y + self.rect.h)
        super().update()


class GolemAttack(BaseGameObject):
    def __init__(self, x, y, pl):
        pl_x = pl.hitbox.rect.x
        pl_y = pl.hitbox.rect.y

        self.speed = 10
        self.damage = units_characteristics.hunter["damage"]
        super().__init__(x, y, 'RockBall.png', HITBOX_FULL_RECT, ENEMY_TEAM, False)
        self.vector = pygame.Vector2(pl_x - self.hitbox.rect.x,
                                     pl_y - self.hitbox.rect.y).normalize()

    def update(self):
        self.global_x += self.vector.x * self.speed
        self.global_y += self.vector.y * self.speed
        for i in self.hitbox.get_colliding_objects():
            if pygame.sprite.collide_mask(self.hitbox, i):
                if hasattr(i.parent, "hp"):
                    i.parent.take_damage(self.damage)
                else:
                    SquareParticle.create_particles(self.global_x, self.global_y,
                                                    i.parent.avg_color)
                self.die()
        self.hitbox.set_pos(self.global_x, self.global_y)
        super(GolemAttack, self).update()
