from files.global_variables import *
from files.basic_classes import Hitbox


class Player(pygame.sprite.Sprite):
    def __init__(self, x=0, y=0):
        super().__init__(all_sprites)
        self.image = pygame.Surface((50, 50))
        self.image.fill(pygame.Color("green"))
        self.rect = self.image.get_rect()
        self.x, self.y = x, y  # because pygame cant operate with float numbers
        self.hitbox = Hitbox(0, 30, 50, 20)
        self.hitbox.set_pos(self.rect.x, self.rect.y)

        self.speed = 10

    @staticmethod
    def get_velocity():
        keystates = pygame.key.get_pressed()
        velocity = pygame.Vector2()
        if keystates[pygame.K_a]:
            velocity.x = -1
        if keystates[pygame.K_d]:
            velocity.x = 1

        if keystates[pygame.K_w]:
            velocity.y = -1
        if keystates[pygame.K_s]:
            velocity.y = 1
        if not velocity.is_normalized() and velocity.length() != 0:
            return velocity.normalize()
        return velocity

    def update(self):
        velocity = self.get_velocity()

        self.hitbox.set_pos(self.x + velocity.x * self.speed * DELTA_TIME,
                            self.y + velocity.y * self.speed * DELTA_TIME)

        # colliding

        x_colliding, y_colliding = self.hitbox.is_colliding()
        if not x_colliding:
            self.x += velocity.x * self.speed * DELTA_TIME
            self.rect.x = int(self.x)
        if not y_colliding:
            self.y += velocity.y * self.speed * DELTA_TIME
            self.rect.y = int(self.y)

        self.hitbox.set_pos(self.x, self.y)

        all_sprites.change_layer(self, self.rect.bottom)
