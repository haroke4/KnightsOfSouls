"""
Глобальные нужные вещи (камера, константы, переменные)
"""
import pygame
import ctypes


def from_local_to_global_pos(x, y):
    return x - CAMERA.all_x_offset, y - CAMERA.all_y_offset


def from_global_to_local_pos(global_x, global_y):
    return global_x + CAMERA.all_x_offset, global_y + CAMERA.all_y_offset


class Hitbox(pygame.sprite.Sprite):
    def __init__(self, dx, dy, width, height):
        super().__init__(hitbox_group, all_sprites)  # add second argument "all_sprites" to show image of hitbox
        self.rect = pygame.Rect(0, 0, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill(pygame.Color("red"))
        self.dx, self.dy = dx, dy

    def set_pos(self, x, y):
        self.rect.x, self.rect.y = int(x + self.dx), int(y + self.dy)

    def colliding_objects(self):
        temp = pygame.sprite.spritecollide(self, hitbox_group, False)
        temp.remove(self)
        return temp


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.all_x_offset = self.all_y_offset = 0
# 1920 1080
# 1680
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)
        if self.dx < -1 or self.dx > 1:
            self.dx = self.dx * 0.01 if not -0.4 < self.dx * 0.01 < 0.4 else 0.4 * self.dx / abs(self.dx)
        if self.dy < -1 or self.dy > 1:
            self.dy = self.dy * 0.01 if not -0.4 < self.dy * 0.01 < 0.4 else 0.4 * self.dy / abs(self.dy)

        self.all_x_offset += self.dx
        self.all_y_offset += self.dy


class BaseGameObject(pygame.sprite.Sprite):
    def __init__(self, x, y, img, hitbox=None):  # hitbox = [dx, dy, width, height]
        super().__init__(all_sprites)
        self.image = pygame.image.load(f"files/img/{img}")
        self.rect = self.image.get_rect()
        self.global_x, self.global_y = from_local_to_global_pos(x, y)
        if hitbox:
            self.hitbox = Hitbox(*hitbox)
            self.hitbox.set_pos(self.global_x, self.global_y)
        else:
            self.hitbox = None
        all_sprites.change_layer(self, self.global_y)

    def update(self):
        self.rect.x, self.rect.y = [int(i) for i in from_global_to_local_pos(self.global_x, self.global_y)]


ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))

FPS = 144
WIDTH = true_res[0]
HEIGHT = true_res[1]

all_sprites = pygame.sprite.LayeredUpdates()
hitbox_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

CAMERA = Camera()
