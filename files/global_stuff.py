"""
Глобальные нужные вещи (камера, константы, переменные)
"""
import pygame
import ctypes
import sqlite3


def from_local_to_global_pos(x, y):
    return x - CAMERA.all_x_offset, y - CAMERA.all_y_offset


def from_global_to_local_pos(global_x, global_y):
    return global_x + CAMERA.all_x_offset, global_y + CAMERA.all_y_offset


def get_hero_characteristic(name):
    con = sqlite3.connect("files/database.sqlite")
    data = con.execute(f"""SELECT * FROM characteristics WHERE name == "{name}" """).fetchone()
    return data[1:-1]


class Hitbox(pygame.sprite.Sprite):
    def __init__(self, dx, dy, width, height, parent):
        super().__init__(hitbox_group, all_sprites)  # add second argument "all_sprites" to show image of hitbox
        self.rect = pygame.Rect(0, 0, width, height)
        self.image = pygame.Surface((width, height))
        self.image.fill(pygame.Color("red"))
        self.dx, self.dy = dx, dy
        self.parent: BaseGameObject = parent

    def set_pos(self, x, y):
        self.rect.x, self.rect.y = int(x + self.dx), int(y + self.dy)

    def get_colliding_objects(self, include_team_members=False):
        temp = pygame.sprite.spritecollide(self, hitbox_group, False)
        temp.remove(self)
        if include_team_members:
            return temp
        return list(filter(lambda x: x.parent.team != self.parent.team or x.parent.team is None, temp))


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.all_x_offset = self.all_y_offset = 0

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
    def __init__(self, x, y, img, hitbox=None, team=None, ):  # hitbox = [dx, dy, width, height]
        super().__init__(all_sprites)
        self.image = pygame.image.load(f"files/img/{img}")
        self.rect = self.image.get_rect()
        self.global_x, self.global_y = x, y
        self.team = team

        if hitbox == FROM_MASK:
            self.hitbox = Hitbox(0, 16, self.rect.w, self.rect.h, self)
            self.hitbox.mask = pygame.mask.from_surface(self.image)
            self.hitbox.set_pos(self.global_x, self.global_y)

        elif hitbox:
            self.hitbox = Hitbox(*hitbox, self)
            self.hitbox.set_pos(self.global_x, self.global_y)
        else:
            self.hitbox = None
        all_sprites.change_layer(self, self.global_y + self.rect.h)

    def set_pos(self, glob_x, glob_y):
        self.global_x, self.global_y = glob_x, glob_y

    def update(self):
        self.rect.x, self.rect.y = [int(i) for i in from_global_to_local_pos(self.global_x, self.global_y)]


ctypes.windll.user32.SetProcessDPIAware()
true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))

FROM_MASK = 2
PLAYER_TEAM = 20
FPS = 144
WIDTH = true_res[0]
HEIGHT = true_res[1]

all_sprites = pygame.sprite.LayeredUpdates()
hitbox_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

CAMERA = Camera()
