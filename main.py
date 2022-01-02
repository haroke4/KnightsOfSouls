import pygame

from files.global_variables import *
from files.player import Player
from files.environment_classes import Wall
from files.basic_classes import Camera

pygame.init()
pygame.mixer.init()  # music activation
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
font = pygame.font.Font(None, 25)

for _ in range(20):
    if _ == 3:
        continue
    Wall(50 * _, 100)

player = Player()
camera = Camera()
playing = True
while playing:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            Wall(*event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                playing = False

    pygame.display.set_caption(str(clock.get_fps()))
    all_sprites.update()

    camera.update(player)
    for obj in all_sprites:
        camera.apply(obj)

    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)
    screen.blit(font.render(f"{camera.dx}, {camera.dy}", True, pygame.Color("white")), (50, 20))
    screen.blit(font.render(f"{int(player.global_x)}, {int(player.global_y)}", True, pygame.Color("white")), (50, 80))

    pygame.display.flip()
