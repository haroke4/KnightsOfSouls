from files.global_stuff import *
from files.heroes import Spearman
from files.environment_classes import MovingWall, Wall

print(WIDTH, HEIGHT)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 25)

player = Spearman(250, 250)

# box
for i in range(20):
    Wall(50 * i, 50)
for i in range(20):
    if i == 3:
        continue
    Wall(50 * i, 500)
for i in range(23):
    Wall(50, 50 + 20 * i)
for i in range(23):
    Wall(950, 50 + 20 * i)
playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.attack(*event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                playing = False
            elif event.key == pygame.K_LSHIFT:
                player.running = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                player.running = False

    all_sprites.update()

    CAMERA.update(player)

    screen.fill(pygame.Color("grey"))
    all_sprites.draw(screen)

    screen.blit(font.render(f" HP: {player.heath}", True, pygame.Color("white")), (50, 20))
    screen.blit(font.render(f"FPS: {clock.get_fps()}", True, pygame.Color("white")), (50, 40))
    screen.blit(font.render(f"{player.spear.angle}", True, pygame.Color("white")), (50, 60))
    screen.blit(font.render(f"{player.spear.global_x, player.spear.global_y}", True, pygame.Color("white")), (50, 80))
    screen.blit(font.render(f"{player.global_x, player.global_y}", True, pygame.Color("white")), (50, 100))

    pygame.display.flip()
    clock.tick(FPS)
