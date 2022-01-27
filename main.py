import pygame
from files.global_stuff import WIDTH, HEIGHT


def pointInRect(point, rect):
    x1, y1, w, h = rect
    x2, y2 = x1 + w, y1 + h
    x, y = point
    if (x1 < x and x < x2):
        if (y1 < y and y < y2):
            return True
    return False


class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, img, sec_img=None):
        super(Button, self).__init__(sprites)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        if sec_img:
            self.sec_img = pygame.image.load(sec_img)
        else:
            self.sec_img = None

    def change_image(self):
        if self.sec_img:
            self.image, self.sec_img = self.sec_img, self.image


pygame.init()
sprites = pygame.sprite.Group()
start_pressed = False
exit_pressed = False
start_button = Button(WIDTH // 2, HEIGHT // 2, 'files/img/start.png', 'files/img/start_pressed.png')
exit_button = Button(WIDTH // 2, HEIGHT // 2 + 150, 'files/img/exit.png', 'files/img/exit_pressed.png')
statistic_button = Button(WIDTH // 2 - 200, HEIGHT // 2, 'files/img/statis.png')
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN | pygame.DOUBLEBUF, 16)
playing = True
while playing:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if pointInRect(event.pos, start_button.rect):
                start_button.change_image()
                start_pressed = True
            elif pointInRect(event.pos, exit_button.rect):
                exit_button.change_image()
                exit_pressed = True
            elif pointInRect(event.pos, statistic_button.rect):
                pass
        elif event.type == pygame.MOUSEBUTTONUP:
            if pointInRect(event.pos, start_button.rect) and start_pressed:
                from files.Game import run
                run()
            if pointInRect(event.pos, exit_button.rect) and exit_pressed:
                exit()
            if start_pressed:
                start_pressed = False
                start_button.change_image()
            if exit_pressed:
                exit_pressed = False
                exit_button.change_image()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_u:
                playing = False
    screen.fill((0, 0, 0))
    sprites.draw(screen)
    pygame.display.flip()
