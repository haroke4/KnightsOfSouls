"""
Глобальные переменные
"""

import pygame

FPS = 144
DELTA_TIME = 1 / FPS

all_sprites = pygame.sprite.LayeredUpdates()

hitbox_group = pygame.sprite.Group()

enemy_group = pygame.sprite.Group()
