from files import global_stuff
from files.heroes import *
from files.enemies import *
from files.environment_classes import Wall, Floor
from files.items import Plaster

# pygame stuff below
print(WIDTH, HEIGHT)
pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF, 16)
clock = pygame.time.Clock()
font = pygame.font.Font(None, 25)
PLAY_ANIMATION = pygame.USEREVENT + 1
UPDATE_ALL_STUFF = pygame.USEREVENT + 2

pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP, PLAY_ANIMATION])
pygame.time.set_timer(UPDATE_ALL_STUFF, 20)
pygame.time.set_timer(PLAY_ANIMATION, 100)


class Game:
    def __init__(self):
        self.level_just_finished = False
        self.player = SpearMan(250, 250)
        self.left_walls = []
        self.right_walls = []
        self.current_level_mobs = []
        self.generate_lvl()
        Plaster(350, 350)
        self.run()

    def generate_lvl(self):

        Wall(0, 0, "Environment/TopWall.png")
        Wall(0, 0, "Environment/LeftWall0.png")
        self.right_walls.append(Wall(1408, 0, "Environment/RightWall0.png"))
        Wall(0, 960, "Environment/BottomWall.png")
        Floor(0, 0, "Environment/floor0.png")
        for i in range(1, 5):
            Wall(1472 * i, 0, "Environment/TopWall.png")
            self.left_walls.append((Wall(1472 * i, 0, "Environment/LeftWall1.png"),
                                    Wall(1472 * i, 576, "Environment/LeftWall2.png")))
            self.right_walls.append(Wall(1472 * i + 1408, 0, "Environment/RightWall0.png"))
            Wall(1472 * i, 960, "Environment/BottomWall.png")
            Floor(1472 * i, 0, "Environment/floor.png")

    def open_next_level(self):
        self.level_just_finished = True
        self.right_walls[0].die()
        del self.right_walls[0]
        Wall(1472 * (global_stuff.current_level - 1) + 1408, 0, "Environment/RightWall1.png")
        Wall(1472 * (global_stuff.current_level - 1) + 1408, 576, "Environment/RightWall2.png")
        global_stuff.current_level += 1

    def start_wave(self):
        self.level_just_finished = False
        for i in range(global_stuff.current_level + 5):
            self.current_level_mobs.append(MiniGolem(random.randrange(1472 * (global_stuff.current_level - 1) + 300,
                                                                      1472 * (global_stuff.current_level - 1) + 1100),
                                                     random.randrange(100, 850), self.player))
        self.left_walls[0][0].die()
        self.left_walls[0][1].die()
        del self.left_walls[0]
        Wall(1472 * (global_stuff.current_level - 1), 0, "Environment/LeftWall0.png")

    def run(self):
        playing = True
        paused = False
        self.level_just_finished = False

        background_color = (34, 32, 53)
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

                    elif event.key == pygame.K_ESCAPE:
                        paused = False if paused else True

                    elif event.key == pygame.K_LSHIFT:
                        self.player.running = True

                    elif event.key == pygame.K_i:
                        self.open_next_level()

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LSHIFT:
                        self.player.running = False
            if paused:
                screen.blit(font.render(f" GAME PAUSED", True, pygame.Color("white")), (WIDTH // 2, HEIGHT // 2))
            else:
                if self.level_just_finished:
                    if self.player.global_x > 1472 * (global_stuff.current_level - 1) + 64:
                        self.start_wave()
                else:
                    if all(map(lambda x: not x.alive(), self.current_level_mobs)):
                        self.open_next_level()

                self.player.key_input()
                if self.player.gun:
                    self.player.look_at_mouse()
                all_sprites.update()
                particle_group.update()

                for i in delete_later:
                    if i.hitbox:
                        i.hitbox.kill()
                    i.kill()

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

                screen.blit(font.render(f" HP: {self.player.hp}", True, pygame.Color("white")), (50, 20))
                screen.blit(font.render(f" Current lvl: {global_stuff.current_level}", True, pygame.Color("white")),
                            (50, 40))
                screen.blit(font.render(f"FPS: {clock.get_fps()}", True, pygame.Color("white")), (50, 60))
                screen.blit(font.render(f" ARMOR: {self.player.armor}", True, pygame.Color("white")), (50, 80))

            pygame.display.flip()
            clock.tick(100)


Game()
