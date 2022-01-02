from files.global_variables import *
from files.player import Player
from files.environment_classes import Wall

pygame.init()
pygame.mixer.init()  # music activation
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)


for _ in range(250):
    if _ == 3:
        continue
    Wall(50 * _, 100)
Player()
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
    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)

    pygame.display.flip()
