from files.global_stuff import *
from threading import Timer
from random import randrange


class BaseParticle(pygame.sprite.Sprite):
    def __init__(self, x, y, img, vector):
        self.vector = vector
        self.image = pygame.image.load(f"files/img/{img}")
        self.rect = self.image.get_rect()
        self.global_x, self.global_y = x, y
        super().__init__(particle_group)
        Timer(randrange(10, 40) / 100, self.kill).start()

    def update(self):
        self.global_x += self.vector.x
        self.global_y += self.vector.y
        self.vector.y += 0.1
        self.rect.x, self.rect.y = [int(i) for i in from_global_to_local_pos(self.global_x, self.global_y)]


class SquareParticle(BaseParticle):
    def __init__(self, x, y, vector: pygame.Vector2, color):
        i = randrange(1, 3)
        super().__init__(x, y, f"Particles/Blood/{i}.png", vector)
        if color:
            self.image.fill(color)

    @staticmethod
    def create_particles(x, y, color, cnt=10):
        for _ in range(cnt):
            SquareParticle(x, y, pygame.Vector2(randrange(-11, 11) / 3, randrange(-11, 11) / 3), color)
