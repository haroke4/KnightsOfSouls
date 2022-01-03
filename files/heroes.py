from files.global_stuff import *


class Player(BaseGameObject):
    def __init__(self, x=0, y=0):
        super().__init__(x, y, "abobus.png", [4, 35, 32, 15])
        self.speed = 2

    @staticmethod
    def get_velocity():
        keystates = pygame.key.get_pressed()
        velocity = pygame.Vector2(0, 0)
        if keystates[pygame.K_a]:
            velocity.x += -1
        if keystates[pygame.K_d]:
            velocity.x += 1

        if keystates[pygame.K_w]:
            velocity.y += -1
        if keystates[pygame.K_s]:
            velocity.y += 1
        if not velocity.is_normalized() and velocity.length() != 0:
            return velocity.normalize()
        return velocity

    def update(self):
        velocity = self.get_velocity()
        move_x, move_y = velocity.x * self.speed, velocity.y * self.speed
        self.global_x += move_x
        self.hitbox.set_pos(self.global_x, self.global_y)
        if self.hitbox.colliding_objects():
            self.global_x -= move_x

        self.global_y += move_y
        self.hitbox.set_pos(self.global_x, self.global_y)
        if self.hitbox.colliding_objects():
            self.global_y -= move_y

        super().update()
        all_sprites.change_layer(self, self.global_y)
