"""
Глобальные переменные
"""

import pygame

FPS = 144
all_sprites = pygame.sprite.LayeredUpdates()
hitbox_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

clock = pygame.time.Clock()