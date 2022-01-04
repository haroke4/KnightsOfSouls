import pygame.mouse

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


class Archer(BaseHero):
    def __init__(self, x=0, y=0):
        data = get_hero_characteristic("archer")
        super().__init__(x, y, "abobus.png", *data[:-1])
        self.bow = Bow(x, y, self.team, data[-1])

    def attack(self, x, y):
        self.bow.shot(x, y)

    def update(self):
        self.bow.set_pos(self.global_x + 30, self.global_y + 1)
        all_sprites.change_layer(self.bow, self.bow.global_y + self.bow.rect.h)
        self.bow.look_at_mouse()
        super().update()


class Bow(BaseGameObject):
    def __init__(self, x, y, team, damage):
        super().__init__(x, y, "Bow.png", hitbox=None, team=team)
        self.orig_image = self.image
        self.damage = damage
        self.last_arrow = None
        self.angle = 0

    def shot(self, x, y):
        x, y = from_local_to_global_pos(x, y)
        v = pygame.Vector2(1, 0).rotate(-self.angle)

        self.last_arrow = Arrow(self.global_x + self.rect.w // 2, self.global_y + self.rect.h // 2,
                                self.team, self.damage, v.normalize() * 10, self.angle)

    def look_at_mouse(self):
        x, y = from_local_to_global_pos(*pygame.mouse.get_pos())
        self.angle = pygame.Vector2(x - self.global_x - self.rect.w // 2,
                                    y - self.global_y - self.rect.h // 2).normalize().angle_to(pygame.Vector2(1, 0))
        self.image = pygame.transform.rotate(self.orig_image, self.angle)
        rot_rect = self.image.get_rect(center=self.rect.center)

        self.global_x -= self.rect.x - rot_rect.x
        self.global_y -= self.rect.y - rot_rect.y


class Arrow(BaseGameObject):
    def __init__(self, x, y, team, damage, vector, angle):
        super().__init__(x, y, "arrow.png", ARROW, team)
        self.image = pygame.transform.rotate(self.image, angle)
        self.hitbox.mask = pygame.mask.from_surface(self.image)
        rot_rect = self.image.get_rect(center=self.rect.center)
        self.global_x -= self.rect.x - rot_rect.x
        self.global_y -= self.rect.y - rot_rect.y

        self.damage = damage
        self.vector = vector
        self.angle = angle

    def update(self):
        self.global_x += self.vector.x
        self.global_y += self.vector.y

        if self in all_sprites:
            all_sprites.change_layer(self, self.hitbox.rect.bottom)
            self.hitbox.set_pos(self.global_x, self.global_y)
            super().update()

            colliding_obj = self.hitbox.get_colliding_objects(include_team_members=False)
            for i in colliding_obj:
                if pygame.sprite.collide_mask(self.hitbox, i):
                    self.kill()
                    self.hitbox.kill()


class TestHero(BaseHero):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, "abobus.png", 1, 1, 1, 1, 2, 1)
