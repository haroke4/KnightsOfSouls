from files.global_variables import *
from files.player import Player
from files.environment_classes import Wall

pygame.init()
pygame.mixer.init()  # music activation
screen = pygame.display.set_mode((500, 500))
clock = pygame.time.Clock()

Wall()
Wall(100, 50)
Player()
playing = True
while playing:
    for __event in pygame.event.get():
        if __event.type == pygame.QUIT:
            playing = False
        if __event.type == pygame.MOUSEBUTTONDOWN:
            Wall(*__event.pos)
    all_sprites.update()

    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)

    pygame.display.flip()
