from files.global_stuff import *
from files.heroes import Archer
from files.environment_classes import MovingWall, Wall

print(WIDTH, HEIGHT)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 25)

player = Archer()
MovingWall(50, 50)
Wall(100, 100)
playing = True
while playing:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            a = MovingWall(*event.pos)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                playing = False
            elif event.key == pygame.K_LSHIFT:
                player.running = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                player.running = False

    pygame.display.set_caption(str(clock.get_fps()))
    all_sprites.update()

    CAMERA.update(player)

    screen.fill(pygame.Color("black"))
    all_sprites.draw(screen)

    screen.blit(font.render(f" HP: {player.heath}", True, pygame.Color("white")), (50, 20))
    screen.blit(font.render(f"Armor: {player.armor}, {int(player.global_y)}", True, pygame.Color("white")), (50, 50))
    screen.blit(font.render(f"{player.walk_speed} | {player.run_speed}", True, pygame.Color("white")), (50, 80))

    pygame.display.flip()
