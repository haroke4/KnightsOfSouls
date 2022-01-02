import pygame

from files.global_variables import *
from files.player import Player

pygame.init()
pygame.mixer.init()  # music activation
screen = pygame.display.set_mode((500, 500))
player = Player()

playing = True
while playing:
    for __event in pygame.event.get():
        if __event.type == pygame.QUIT:
            playing = False
    all_sprites.update()

    # drawing
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)

    pygame.display.flip()
