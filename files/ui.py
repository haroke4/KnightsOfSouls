import math

import pygame
from files.global_stuff import WIDTH, HEIGHT


# TODO: Сделать отображение чего то чего взял

class Button(pygame.sprite.Sprite):
    def __init__(self, x, y, sprite_group, img, sec_img, func, *args, **kwargs):
        super(Button, self).__init__(sprite_group)
        if type(img) == str:
            self.image = pygame.image.load('files/img/buttons/' + img)
            self.sec_img = pygame.image.load('files/img/buttons/' + sec_img)
        else:
            self.image = img
            self.sec_img = sec_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.just_pressed = False
        self.is_pressed = False
        self.func = func
        self.func_args = args
        self.func_kwargs = kwargs

    def press(self):
        self.image, self.sec_img = self.sec_img, self.image
        self.is_pressed = True

    def unpress(self):
        if self.is_pressed:
            self.image, self.sec_img = self.sec_img, self.image
            self.is_pressed = False

    def change_image(self, img1, img2):
        if type(img1) == str:
            self.image = pygame.image.load('files/img/buttons/' + img1)
            self.sec_img = pygame.image.load('files/img/buttons/' + img2)
        else:
            self.image = img1
            self.sec_img = img2

    def update(self):
        x1, y1, w, h = self.rect
        x2, y2 = x1 + w, y1 + h
        x, y = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        if x1 < x < x2 and y1 < y < y2:
            if mouse_pressed and not self.is_pressed:
                self.press()
            if not mouse_pressed and self.is_pressed:
                self.unpress()
                self.func(*self.func_args, **self.func_kwargs)

        if not mouse_pressed and self.is_pressed:
            self.unpress()


class Bar(pygame.sprite.Sprite):
    def __init__(self, x, y, color, target, val_attr, max_val_attr, screen, group, text=None, len_=400, h=50,
                 c=False):  # c - Center
        super().__init__(group)
        self.x, self.y = x, y
        self.length = len_
        self.height = h
        self.rect = pygame.Rect(self.x, self.y, self.length, self.height)
        if c:
            self.rect.centerx = x
            self.rect.centery = y
        self.color = color
        self.speed = 3
        self.text = text
        self.font = pygame.font.SysFont("Arial", 25)

        self.target = target
        self.current_value = self.length
        self.value_attr = val_attr
        self.max_value_attr = max_val_attr
        self.screen = screen

    def update(self):
        if not self.target.alive():
            self.kill()
        ratio = self.length / getattr(self.target, self.max_value_attr)
        target_value = getattr(self.target, self.value_attr) * ratio
        if target_value - 3 < self.current_value < target_value + 3:
            pass
        elif target_value > self.current_value:
            self.current_value += self.speed
        elif target_value < self.current_value:
            self.current_value -= self.speed

        if self.text:
            t = self.font.render(self.text, True, pygame.Color("white"))
            x = self.rect.centerx - t.get_rect().w // 2
            y = self.rect.y - t.get_rect().height - 5
            self.screen.blit(t, (x, y))

        pygame.draw.rect(self.screen, (255, 255, 255), self.rect)
        pygame.draw.rect(self.screen, self.color,
                         [self.rect.x + 5, self.rect.y + 5, self.current_value - 10, self.height - 10])
        t = self.font.render(
            f'{round(getattr(self.target, self.value_attr), 1)} / {getattr(self.target, self.max_value_attr)}',
            True, pygame.Color("black"))
        self.screen.blit(t, (self.rect.centerx - t.get_rect().w // 2, self.rect.centery - t.get_rect().h // 2))


class TextBanner(pygame.sprite.Sprite):
    def __init__(self, text, screen, group):
        self.text = text
        self.screen = screen
        super().__init__(group)
        self.font = pygame.font.SysFont("Arial", 25)
        cur = 0
        cnt = 1
        self.lines = {}
        for i in text.split(' '):
            cur += len(i)
            if cur > 50:
                cnt += 1
                self.cur = 0
            if cnt in self.lines.keys():
                self.lines[cnt].append(i)
            else:
                self.lines[cnt] = [i]
        self.texts = []
        for i in self.lines.values():
            self.texts.append(' '.join(i))

    def update(self):
        pygame.draw.rect(self.screen, pygame.Color("black"),
                         [500, HEIGHT - len(self.texts) * 50 - 50, 26 * 50, 50 * len(self.texts)])
        y = 50 * (len(self.lines) + 1)
        for i in self.texts:
            self.screen.blit(self.font.render(i, True, pygame.Color('white')), (500, HEIGHT - y))
            y -= 50
