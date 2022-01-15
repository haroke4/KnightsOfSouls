import pygame

from files.global_stuff import *
from files.heroes import *


class BaseEnemy(BaseGameObject):
    def __init__(self, x, y, image, hp, armor, run_speed, attack_cooldown, damage, gm=None):
        self.gm = gm
        self.is_active = False
        self.max_hp = self.hp = hp
        self.max_armor = self.armor = armor
        self.initial_run_speed = self.run_speed = run_speed
        self.attack_cooldown = attack_cooldown
        self.damage = damage
        self.velocity = pygame.Vector2(0, 0)
        super().__init__(x, y, image, [6, 35, 36, 15], ENEMY_TEAM)

    def take_damage(self, damage):
        if damage > 0:
            self.armor -= damage
            if self.armor < 0:
                self.hp -= abs(self.armor)
                if self.hp <= 0:
                    self.die()
                self.armor = 0


class GoblinEnemy(BaseEnemy):
    def __init__(self, gm, x=0, y=0):
        self.is_attack = False
        self.gm = gm
        self.player_pos = self.gm.get_player_position()
        self.target_pos = None
        data = units_characteristics.goblin
        self.vector = pygame.Vector2()
        super().__init__(x, y, data["img"], data["hp"], data["armor"], data["run_speed"],
                         data["attack_cooldown"], data["damage"])

    def attack(self):
        self.target_pos = self.gm.get_player_position()
        self.vector = pygame.Vector2(self.target_pos[0] - self.global_x, self.target_pos[1] - self.global_y).normalize()
        self.is_attack = True
        print(self.target_pos)

    def update(self):
        all_sprites.change_layer(self, self.hitbox.rect.bottom)
        self.player_pos = self.gm.get_player_position()
        if math.sqrt((self.global_x - self.player_pos[0]) ** 2 +
                     (self.global_y - self.player_pos[1]) ** 2) < 400 and not self.is_attack:
            self.attack()
        if self.is_attack:
            self.global_x += self.vector.x * self.run_speed
            self.global_y += self.vector.y * self.run_speed
            for i in self.hitbox.get_colliding_objects():
                if pygame.sprite.collide_mask(self.hitbox, i):
                    if hasattr(i.parent, "hp"):
                        dmg = self.damage
                        i.parent.take_damage(dmg)
                if self.global_x == self.target_pos[0] and self.global_y == self.target_pos[1]:
                        self.is_attack = False
                        Timer(self.attack_cooldown, self.attack)
        else:
            if self.is_active:
                self.attack()
        self.hitbox.set_pos(self.global_x, self.global_y)
        super().update()

