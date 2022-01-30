import pygame
from files.global_stuff import WIDTH, HEIGHT
from files.ui import Button
from files.Game import run
from files.heroes import SpearMan, MagicMan, SwordMan


def start_game():
    statistic_texts.clear()
    run(current_hero)


def show_statistics():
    if not statistic_texts:
        import sqlite3
        con = sqlite3.connect("files/db.sqlite")
        data = [(0, "Mob:", "Kills:")] + con.execute("""SELECT *  from Info""").fetchall()
        con.close()
        y = HEIGHT // 2 + 50
        x = WIDTH // 2 * 0.46
        for i in data:
            statistic_texts.append((font.render(i[1], True, (255, 255, 255)), x, y))
            statistic_texts.append((font.render(str(i[2]), True, (255, 255, 255)), x + 130, y))
            y += 30
    else:
        statistic_texts.clear()


def change_character():
    global current_hero, hero_img
    if current_hero == SpearMan:
        current_hero = MagicMan
        hero_img = pygame.transform.scale(pygame.image.load('files/img/MagicMan/down/1.png'), (50 * 3, 60 * 3))
    elif current_hero == MagicMan:
        current_hero = SwordMan
        hero_img = pygame.transform.scale(pygame.image.load('files/img/SwordMan/down/1.png'), (50 * 3, 60 * 3))
    else:
        current_hero = SpearMan
        hero_img = pygame.transform.scale(pygame.image.load('files/img/SpearMan/down/1.png'), (50 * 3, 60 * 3))
    hero_button.change_image(hero_img, hero_img)
    current_hero_characteristic.clear()
    for i in range(len(current_hero.characteristic)):
        current_hero_characteristic.append((font.render(current_hero.characteristic[i], True, pygame.Color("BLACK")),
                                            (WIDTH // 2) * 1.05, (HEIGHT // 2) * 1.4 + dy + 25 * i))


def print_hi():
    print('hi')


pygame.init()
font = pygame.font.Font(None, 30)
background = pygame.image.load("files/img/main_menu.png")
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF, 16)

dy = 100
sprites = pygame.sprite.Group()
current_hero = SpearMan
hero_img = pygame.transform.scale(pygame.image.load('files/img/SpearMan/down/1.png'), (50 * 3, 60 * 3))
statistic_texts = []  # (rendered_text, x, y)

hero_text = (font.render("YOUR HERO: ", True, pygame.Color("BLACK")), (WIDTH // 2) * 1.07, (HEIGHT // 2) * 0.93 + dy)
current_hero_characteristic = []
for i in range(len(current_hero.characteristic)):
    current_hero_characteristic.append((font.render(current_hero.characteristic[i], True, pygame.Color("BLACK")),
                                        (WIDTH // 2) * 1.05, (HEIGHT // 2) * 1.4 + dy + 25 * i))
hero_button = Button((WIDTH // 2) * 1.14, (HEIGHT // 2) * 1.18 + dy, sprites, hero_img, hero_img, change_character)
start_button = Button(WIDTH // 2 * 0.85, HEIGHT // 2 + dy, sprites, 'start.png', 'start_pressed.png', start_game)
statistic_button = Button(WIDTH // 2 * 0.85, (HEIGHT // 2) * 1.2 + dy, sprites, 'statis.png', 'statis_pressed.png',
                          show_statistics)
exit_button = Button(WIDTH // 2 * 0.85, HEIGHT // 2 * 1.4 + dy, sprites, 'exit.png', 'exit_pressed.png',
                     lambda x=0: quit())

pygame.display.set_caption("Knights of souls! V1.0")
playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                playing = False

    sprites.update()
    screen.blit(background, (0, 0))
    sprites.draw(screen)
    screen.blit(hero_text[0], hero_text[1:])
    for i in statistic_texts:
        screen.blit(i[0], i[1:])
    for i in current_hero_characteristic:
        screen.blit(i[0], i[1:])
    pygame.display.flip()
