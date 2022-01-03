from files.global_stuff import *
from files.heroes import Player
from files.environment_classes import Wall

print(WIDTH, HEIGHT)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()

for _ in range(20):
    if _ == 3:
        continue
    Wall(50 * _, 100)
font = pygame.font.Font(None, 25)

player = Player()
playing = True
while playing:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            a = Wall(*event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                playing = False

    pygame.display.set_caption(str(clock.get_fps()))
    all_sprites.update()

    CAMERA.update(player)

    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)

    screen.blit(font.render(f"{round(CAMERA.dx, 3)}, {round(CAMERA.dy, 3)}", True, pygame.Color("white")), (50, 20))
    screen.blit(font.render(f"{int(player.global_x)}, {int(player.global_y)}", True, pygame.Color("white")), (50, 50))
    screen.blit(font.render(f"{int(CAMERA.all_x_offset)}, {int(CAMERA.all_y_offset)}", True, pygame.Color("white")), (50, 80))

    pygame.display.flip()
