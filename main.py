import pygame

from files.global_stuff import *
from files.heroes import *
from files.enemies import *
from files.items import *
from files.environment_classes import MovingWall, Wall

print(WIDTH, HEIGHT)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 25)
PLAY_ANIMATION = pygame.USEREVENT + 1
pygame.time.set_timer(PLAY_ANIMATION, 100)

player = SwordMan(250, 250)
enemy = TestEnemy(450, 300, player)
TestEnemy(120, 120, player)
TestEnemy(170, 120, player)
TestEnemy(200, 120, player)

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

        elif event.type == PLAY_ANIMATION:
            for _obj in play_animation_group:
                _obj.change_image()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                playing = False

            elif event.key == pygame.K_LSHIFT:
                player.running = True

            elif event.key == pygame.K_i:
                player.take_damage(99)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LSHIFT:
                player.running = False

    all_sprites.update()
    particle_group.update()

    for i in delete_later:
        if i.hitbox:
            i.hitbox.kill()
        i.kill()

    CAMERA.update(player)

    screen.fill(pygame.Color("grey"))
    all_sprites.draw(screen)
    particle_group.draw(screen)

    if player.has_welding_helmet:  # это все для ПРЕДМЕТА сварочный шлем
        pygame.draw.rect(screen, pygame.Color("black"), [0, 0, draw_area['l'], HEIGHT])
        pygame.draw.rect(screen, pygame.Color("black"), [draw_area['r'], 0, WIDTH - draw_area['r'], HEIGHT])
        pygame.draw.rect(screen, pygame.Color("black"), [draw_area['l'], 0, draw_area['r'] - draw_area['l'],
                                                         draw_area['t']])
        pygame.draw.rect(screen, pygame.Color("black"),
                         [draw_area['l'], draw_area['b'], draw_area['r'] - draw_area['l'],
                          draw_area['b'] - draw_area['t']])

    screen.blit(font.render(f" HP: {player.hp}", True, pygame.Color("white")), (50, 20))
    screen.blit(font.render(f" ENEMY HP: {enemy.hp}", True, pygame.Color("white")), (50, 40))
    screen.blit(font.render(f"FPS: {clock.get_fps()}", True, pygame.Color("white")), (50, 60))
    pygame.display.flip()

    clock.tick(FPS)

