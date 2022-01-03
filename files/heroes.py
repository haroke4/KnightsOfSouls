from files.global_stuff import *


class BaseHero(BaseGameObject):
    def __init__(self, x, y, image, health, armor, protection, walk_speed, run_speed, attack_cooldown, damage):
        super().__init__(x, y, image, [6, 35, 36, 15])
        self.heath = health
        self.armor = armor
        self.protection = protection
        self.walk_speed = walk_speed
        self.run_speed = run_speed
        self.attack_cooldown = attack_cooldown
        self.damage = damage
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
            self.velocity.normalize()

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

        super().update()
        all_sprites.change_layer(self, self.global_y)


class Archer(BaseHero):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, "abobus.png", *get_hero_characteristic("archer"))


class TestHero(BaseHero):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, "abobus.png", 1, 1, 1, 1, 2, 1, 1)
