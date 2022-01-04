import pygame.mouse
import math

from files.global_stuff import *


class BaseHero(BaseGameObject):
    def __init__(self, x, y, image, health, armor, protection, walk_speed, run_speed, attack_cooldown):
        super().__init__(x, y, image, [6, 35, 36, 15], PLAYER_TEAM)
        self.heath = health
        self.armor = armor
        self.protection = protection
        self.walk_speed = walk_speed
        self.run_speed = run_speed
        self.attack_cooldown = attack_cooldown
        self.running = False
        self.velocity = pygame.Vector2(0, 0)

    def update_velocity(self):
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

    def update(self):
        self.update_velocity()
        if self.running:
            move_x, move_y = self.velocity.x * self.run_speed, self.velocity.y * self.run_speed
        else:
            move_x, move_y = self.velocity.x * self.walk_speed, self.velocity.y * self.walk_speed

        self.global_x += move_x
        self.hitbox.set_pos(self.global_x, self.global_y)
        if self.hitbox.get_colliding_objects():
            self.global_x -= move_x
            self.hitbox.set_pos(self.global_x, self.global_y)

        self.global_y += move_y
        self.hitbox.set_pos(self.global_x, self.global_y)
        if self.hitbox.get_colliding_objects():
            self.global_y -= move_y
            self.hitbox.set_pos(self.global_x, self.global_y)

        all_sprites.change_layer(self, self.global_y + self.rect.h)
        super().update()


class Spearman(BaseHero):
    def __init__(self, x=0, y=0):
        data = get_hero_characteristic("archer")
        super().__init__(x, y, "abobus.png", *data[:-1])
        self.spear = Spear(x, y, self.team, data[-1], self)
        self.spear_dx, self.spear_dy = 30, 5
        self.damage = data[-1]

    def attack(self, x, y):
        self.spear.shot()
        self.spear = Spear(250, 250, self.team, self.damage, self)
        self.spear.update()


class Spear(BaseGameObject):
    def __init__(self, x, y, team, damage, parent):
        super().__init__(x, y, "arrow.png", hitbox=ARROW, team=team)
        self.orig_image = self.image
        self.damage = damage
        self.parent = parent

        self.angle = 0
        self.speed = 6
        self.shooted = False
        self.vector = pygame.Vector2(0, 0)

    def shot(self):
        self.vector = pygame.Vector2(1, 0).rotate(-self.angle).normalize()
        self.hitbox.mask = pygame.mask.from_surface(self.image)
        self.shooted = True

    def look_at_mouse(self):
        x, y = from_local_to_global_pos(*pygame.mouse.get_pos())
        self.angle = pygame.Vector2(x - self.parent.global_x - self.rect.w // 2,
                                    y - self.parent.global_y - self.rect.h // 2).normalize().angle_to(pygame.Vector2(1, 0))
        if self.angle < 0:
            self.angle += 360
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        self.rect = self.image.get_rect(center=(self.rect.x + 100 * math.cos(self.angle/180*math.pi) - 5,
                                                self.rect.y - 100 * math.sin(self.angle/180*math.pi)))

    def update(self):
        if self.shooted:
            self.global_x += self.vector.x * self.speed
            self.global_y += self.vector.y * self.speed
            for i in self.hitbox.get_colliding_objects(include_team_members=False):
                if pygame.sprite.collide_mask(self.hitbox, i):
                    self.kill()
                    self.hitbox.kill()
        else:
            self.look_at_mouse()
            self.set_pos(self.parent.global_x + 50 * math.cos(self.angle/180*math.pi),
                         self.parent.global_y - 50 * math.sin(self.angle/180*math.pi))
            all_sprites.change_layer(self, self.global_y + self.rect.h)
        self.hitbox.set_pos(self.global_x, self.global_y)
        super().update()


class TestHero(BaseHero):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, "abobus.png", 1, 1, 1, 1, 2, 1)
