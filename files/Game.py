import time
import sys
import random
import sqlite3
from threading import Thread

import pygame.font

from files.ui import Bar, Button
from files.enemies import *
from files.environment_classes import Wall, Floor
from files.items import *
from files.global_stuff import *
from files.units_characteristics import increase_mob_characteristics, make_default_mob_characteristics

# pygame stuff below
print(WIDTH, HEIGHT)
pygame.init()
pygame.mixer.init()
game_instance = None
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF, 16)
clock = pygame.time.Clock()
font = pygame.font.Font("files/font1.ttf", 36)
font_splash_boot = pygame.font.SysFont('rockwell', 100)
PLAY_ANIMATION = pygame.USEREVENT + 1

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, PLAY_ANIMATION])
pygame.time.set_timer(PLAY_ANIMATION, 100)
pygame.display.set_caption("Knights of souls! V1.0")


class Game:
    player_start_pos = [(128, 448), (128, 576), (320, 576), (320, 448)]

    def __init__(self, chosen_hero):

        self.left_walls = []
        self.right_walls = []
        self.other_environment = []
        self.current_level_mobs = []
        self.items_on_maps = []
        self.bar_group = pygame.sprite.Group()
        self.banners_group = pygame.sprite.Group()
        self.buttons_group = pygame.sprite.Group()

        self.running = False
        self.level_just_finished = False
        self.playing = True
        self.quitting = False
        self.paused = False
        self.current_level = 0
        self.last_level = False
        self.floor = 1
        self.dx = 576

        self.on_player_die_timer = False
        self.render_text = ""
        self.transitioning = []
        self.transition_counter = 255

        self.generate_levels()
        self.player = chosen_hero(*random.choice(self.player_start_pos))
        # ui stuff
        self.hp_bar = Bar(50, HEIGHT - 170, pygame.Color('red'), self.player, "hp", "max_hp", screen, self.bar_group)
        self.armor_bar = Bar(50, HEIGHT - 110, pygame.Color('grey'), self.player, "armor", "max_armor", screen,
                             self.bar_group)
        self.exit_button = False

    def quit_this_window(self):
        change_draw_area(0, 0, WIDTH, HEIGHT)
        particle_group.empty()
        hitbox_group.empty()
        all_sprites.empty()
        con = sqlite3.connect("files/db.sqlite")
        cur = con.cursor()
        for i in temp_stats:
            update_statistics(i, cur)
        con.commit()
        con.close()
        make_default_mob_characteristics()
        for i in temp_stats:
            temp_stats[i] = 0
        self.running = False

    def exit_button_pressed(self):
        self.quitting = True
        self.exit_button.kill()
        self.render_text = ["Cleaning battlefield..."]
        self.transitioning = [self.fade_in, self.render_center_text]
        self.playing = False
        Timer(3, self.quit_this_window).start()

    def fade_in(self):
        surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        surface.fill(pygame.Color(0, 0, 0, int(self.transition_counter)))
        screen.blit(surface, (0, 0))
        self.transition_counter += 2
        if self.transition_counter >= 255:
            self.transitioning = []

    def fade_out(self):
        surface = pygame.Surface((WIDTH, HEIGHT)).convert_alpha()
        surface.fill(pygame.Color(0, 0, 0, int(self.transition_counter)))
        screen.blit(surface, (0, 0))

        self.transition_counter -= 1.5
        if self.transition_counter <= 0:
            self.transitioning = []

    def render_center_text(self):
        y = -60
        for str_text in self.render_text:
            text = font_splash_boot.render(str_text, True, (255, 255, 255))
            text.set_alpha(self.transition_counter)
            dx, dy = text.get_width() // 2, text.get_height() // 2
            screen.blit(text, (WIDTH // 2 - dx, HEIGHT // 2 - dy + y))
            y += 120

    def on_player_die(self):
        self.quitting = True
        a = sum([g for i, g in temp_stats.items()])
        self.render_text = ["YOU DIED", f'Enemies killed: {a}']
        self.transitioning = [self.fade_in, self.render_center_text]
        self.playing = False
        Timer(5, self.quit_this_window).start()

    def generate_levels(self):
        # creating START room!
        self.other_environment.append(Wall(0, 256, "Environment/MiniRoom/TopWall.png"))
        self.other_environment.append(Wall(0, 704, "Environment/MiniRoom/BottomWall.png"))
        self.other_environment.append(Wall(0, 256, "Environment/MiniRoom/LeftWall0.png"))
        self.other_environment.append(Wall(self.dx - 64, 256, "Environment/MiniRoom/RightWall1.png"))
        self.other_environment.append(Wall(self.dx - 64, 576, "Environment/MiniRoom/RightWall2.png"))
        Floor(0, 256, "Environment/MiniRoom/Floor.png")

        for i in range(0, 5):
            self.other_environment.append(Wall(1472 * i + self.dx, 0, "Environment/TopWall.png"))
            self.left_walls.append((Wall(1472 * i + self.dx, 0, "Environment/LeftWall1.png"),
                                    Wall(1472 * i + self.dx, 576, "Environment/LeftWall2.png")))
            self.right_walls.append(Wall(1472 * i + 1408 + self.dx, 0, "Environment/RightWall0.png"))
            self.other_environment.append(Wall(1472 * i + self.dx, 960, "Environment/BottomWall.png"))
            self.other_environment.append(Floor(1472 * i + self.dx, 0, "Environment/floor.png"))

        self.other_environment.append(Wall(self.dx + 1472 * 5, 256, "Environment/MiniRoom/TopWall.png"))
        self.other_environment.append(Wall(self.dx + 1472 * 5, 704, "Environment/MiniRoom/BottomWall.png"))
        self.other_environment.append(Wall(self.dx + 1472 * 5, 256, "Environment/MiniRoom/LeftWall1.png"))
        self.other_environment.append(Wall(self.dx + 1472 * 5, 576, "Environment/MiniRoom/LeftWall2.png"))
        self.other_environment.append(Wall(self.dx * 2 - 64 + 1472 * 5, 256, "Environment/MiniRoom/RightWall0.png"))
        self.other_environment.append(Floor(self.dx + 1472 * 5, 256, "Environment/MiniRoom/Floor.png"))

        self.transitioning = [self.fade_out, self.render_center_text]
        self.render_text = [f"FLOOR {self.floor}", "Welcome to the dungeons"]

    def next_floor(self):
        self.level_just_finished = False
        self.playing = False
        self.transition_counter = 0
        self.transitioning = [self.fade_in]
        for i in self.items_on_maps:
            if not (isinstance(i, TwinMirror) or isinstance(i, ElectricRing)):
                i.die()
        for i in self.right_walls + self.left_walls + self.other_environment:
            try:
                i.die()
            except Exception:
                pass

        self.items_on_maps.clear()
        self.right_walls.clear()
        self.left_walls.clear()
        self.other_environment.clear()

        self.generate_levels()
        self.player.set_pos(*self.player_start_pos[0])

        self.level_just_finished = True
        self.last_level = False
        self.current_level = 0
        self.floor += 1
        increase_mob_characteristics(self.floor)
        self.render_text = [f"FLOOR {self.floor}", "Mobs became more dangerous"]

        while self.transitioning:
            time.sleep(0.25)

        self.transition_counter = 255
        self.transitioning = [self.fade_out, self.render_center_text]
        self.playing = True
        con = sqlite3.connect("files/db.sqlite")
        cur = con.cursor()
        for i in temp_stats:
            update_statistics(i, cur)
        con.commit()
        con.close()

    def level_finished(self):
        print("LEVEL FINISHED")

        self.level_just_finished = True
        self.right_walls[0].die()
        del self.right_walls[0]
        self.other_environment.append(
            Wall(1472 * (self.current_level - 1) + 1408 + self.dx, 576, "Environment/RightWall2.png"))
        self.other_environment.append(
            Wall(1472 * (self.current_level - 1) + 1408 + self.dx, 0, "Environment/RightWall1.png"))
        if self.player.apple_bag_count:
            self.player.max_hp += self.player.apple_bag_count
            self.player.heal(self.player.apple_bag_count)

        if self.current_level == 5:
            self.last_level = True
            self.items_on_maps.append(get_random_epic_item()(1472 * (self.current_level - 0.5) + self.dx, 512))
        else:
            self.items_on_maps.append(get_random_item()(1472 * (self.current_level - 0.5) + self.dx, 512))

    def start_wave(self):

        print("START WAVE")
        self.level_just_finished = False
        self.left_walls[0][0].die()
        self.left_walls[0][1].die()
        del self.left_walls[0]
        self.left_walls.append(Wall(1472 * (self.current_level - 1) + self.dx, 0, "Environment/LeftWall0.png"))
        for i in range(self.current_level + self.floor):
            temp = random.choice([MiniGolem, Snake, Tree, Dog, IceSoul, FireSoul])
            self.current_level_mobs.append(
                temp(random.randrange(1472 * (self.current_level - 1) + TILE_WIDTH + self.dx,
                                      1472 * (self.current_level - 1) + 1000 + self.dx),
                     random.randrange(TILE_HEIGHT * 2, 1024 - TILE_HEIGHT * 3),
                     [self.player])
            )

    def start_boss_fighting(self):
        print("START BOSS FIGHT")

        # closing door
        self.level_just_finished = False
        self.left_walls[0][0].die()
        self.left_walls[0][1].die()
        del self.left_walls[0]
        self.left_walls.append(Wall(1472 * (self.current_level - 1) + self.dx, 0, "Environment/LeftWall0.png"))

        temp = random.choice([DragonBoss, Golem, NecroBoss, Hunter])(1472 * (self.current_level - 0.5)
                                                                     + self.dx, 512, [self.player])
        self.current_level_mobs.append(temp)
        Bar(WIDTH // 2, 120, pygame.Color("red"), self.current_level_mobs[0], "hp",
            "max_hp", screen, self.bar_group, text=f"{temp.name} HP", c=True, len_=WIDTH * 0.8)

    def run(self):
        self.level_just_finished = True
        self.running = True
        background_color = (34, 32, 53)
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                elif event.type == PLAY_ANIMATION:
                    for _obj in play_animation_group:
                        _obj.change_image()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.quitting is True:
                            continue
                        self.paused = False if self.paused else True
                        if self.paused:
                            self.exit_button = Button(WIDTH // 2, HEIGHT // 2, self.buttons_group, "main_menu.png",
                                                      "main_menu_pressed.png", self.exit_button_pressed)
                        else:
                            self.exit_button.kill()

                    elif event.key == pygame.K_LSHIFT:
                        self.player.running = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT:
                        self.player.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.player.attack(*event.pos)

            if self.paused:
                t = font.render(f" GAME PAUSED", True, pygame.Color("BLACK"))
                screen.blit(t, (WIDTH // 2 - t.get_rect().w // 2, HEIGHT // 2 - 100 - t.get_rect().h // 2))

            elif self.playing:
                if self.player.hp <= 0 and not self.on_player_die_timer:
                    Timer(1, self.on_player_die).start()
                    self.on_player_die_timer = True

                # checking game status
                if self.level_just_finished:
                    if self.player.global_x > 1472 * self.current_level + 64 + self.dx:
                        self.current_level += 1
                        if self.current_level == 5:
                            self.start_boss_fighting()
                        elif self.current_level != 6:
                            self.start_wave()
                        else:
                            Thread(target=self.next_floor, daemon=True).start()
                elif 0 < self.current_level and len(self.current_level_mobs) == 0 and not self.last_level:
                    self.level_finished()

                self.player.key_input()
                if self.player.gun:
                    self.player.look_at_mouse()

                all_sprites.update()
                particle_group.update()

                CAMERA.update(self.player)

                screen.fill(background_color)
                all_sprites.draw(screen)
                particle_group.draw(screen)
                if self.player.has_welding_helmet:  # это все для ПРЕДМЕТА сварочный шлем
                    pygame.draw.rect(screen, pygame.Color("black"), [0, 0, draw_area['l'], HEIGHT])
                    pygame.draw.rect(screen, pygame.Color("black"), [draw_area['r'], 0, WIDTH - draw_area['r'], HEIGHT])
                    pygame.draw.rect(screen, pygame.Color("black"), [draw_area['l'], 0, draw_area['r'] - draw_area['l'],
                                                                     draw_area['t']])
                    pygame.draw.rect(screen, pygame.Color("black"),
                                     [draw_area['l'], draw_area['b'], draw_area['r'] - draw_area['l'],
                                      draw_area['b'] - draw_area['t']])
                # screen.blit(font.render(f" HP: {self.player.hp}", True, pygame.Color("white")), (50, 20))
                # screen.blit(font.render(f" Current lvl: {self.current_level}", True, pygame.Color("white")),
                #             (50, 40))
                # screen.blit(font.render(f"FPS: {clock.get_fps()}", True, pygame.Color("white")), (50, 60))
                # screen.blit(
                #     font.render(f" ARMOR: {self.player.armor} DMG: {self.player.damage}", True, pygame.Color("white")),
                #     (50, 80))
                # screen.blit(font.render(f" prt: {self.player.protection}", True, pygame.Color("white")),
                #             (50, 100))

                self.bar_group.update()
                items_text.update()

            # updating buttons
            self.buttons_group.update()
            self.buttons_group.draw(screen)

            for i in self.transitioning:
                i()

            for i in delete_later:
                if i in self.current_level_mobs:
                    self.current_level_mobs.remove(i)
                if i.hitbox:
                    i.hitbox.kill()
                i.kill()

            delete_later.clear()
            pygame.display.flip()
            clock.tick(FPS)


def run(chosen_hero):
    global game_instance
    game_instance = Game(chosen_hero)
    game_instance.run()
