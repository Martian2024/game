from pygame.sprite import Sprite
from pygame import Surface, SRCALPHA, Rect
import pygame
import random
from math import sqrt

class SimpleHouse(Sprite):
    def __init__(self, pos, rect, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = Surface(rect)
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.rect(self.image, '#39FF14', (0, 0, rect[0], rect[1]), width=5)
        self.rect = Rect(pos[0] - rect[0] // 2, pos[1] - rect[1] // 2, rect[0], rect[1]) 


class Tree(Sprite):
    def __init__(self, pos, size, group):
        pygame.sprite.Sprite.__init__(self, group) 
        self.image = pygame.transform.scale(pygame.image.load(f'images\\tree{random.randint(1, 2)}.png'), (size, size))
        self.rect = self.image.get_rect()
        self.rect.center = pos

class RifleMan(Sprite):
    def __init__(self, pos, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.images = [Surface((20, 20)), Surface((20, 20))]
        self.images[0].set_colorkey((0, 0, 0))
        self.images[1].set_colorkey((0, 0, 0))
        pygame.draw.circle(self.images[0], '#39FF14', (10, 10), 10, width=2)
        pygame.draw.circle(self.images[1], '#39FF14', (10, 10), 10)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.order = 'STOP'
        self.auto_attack = True
        self.motionvector = (0, 0)

        self.selected = False

        self.speed = 1.5
        self.position = pos
        self.destination = (0, 0)

        self.vision = 250

        self.hp = 2
        self.max_hp = 2
        self.target = None
        self.cooldown_counter = 0
        self.counter_max = 60

    def update(self):
        if self.selected:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

        if self.order == 'MOTION':
            x = self.destination[0] - self.position[0]
            y = self.destination[1] - self.position[1]
            length = sqrt(x ** 2 + y ** 2)
            self.motionvector = (x * (self.speed / length), 
                                               y * (self.speed / length))

            self.position = (self.position[0] + self.motionvector[0], self.position[1] + self.motionvector[1])
            self.rect.center = self.position

            if 0 < abs(self.position[0] - self.destination[0]) < 1 and 0 < abs(self.position[1] - self.destination[1]) < 1:
                self.order = 'STOP'
        if self.hp <= 0:
            self.kill()
        if self.target:
            if not self.target.alive():
                self.target = None

class Shield(Sprite):
    def __init__(self, pos, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.images = [pygame.transform.scale(pygame.image.load('images\\shield\\shield1.png'), (20, 20)), pygame.transform.scale(pygame.image.load('images\\shield\\shield2.png'), (20, 20))]
        self.images[0].set_colorkey((0, 0, 0))
        self.images[1].set_colorkey((0, 0, 0))
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.order = 'STOP'
        self.auto_attack = False
        self.motionvector = (0, 0)

        self.selected = False

        self.speed = 1
        self.position = pos
        self.destination = (0, 0)

        self.vision = 250

        self.hp = 1
        self.max_hp = 20
        self.hp_regen = 1
        self.target = None
        self.cooldown_counter = 0
        self.counter_max = 60

    def update(self):
        self.hp = min(self.hp + self.hp_regen, self.max_hp)
        if self.selected:
            self.image = self.images[1]
        else:
            self.image = self.images[0]

        if self.order == 'MOTION':
            x = self.destination[0] - self.position[0]
            y = self.destination[1] - self.position[1]
            length = sqrt(x ** 2 + y ** 2)
            self.motionvector = (x * (self.speed / length), 
                                               y * (self.speed / length))

            self.position = (self.position[0] + self.motionvector[0], self.position[1] + self.motionvector[1])
            self.rect.center = self.position

            if 0 < abs(self.position[0] - self.destination[0]) < 1 and 0 < abs(self.position[1] - self.destination[1]) < 1:
                self.order = 'STOP'
        if self.hp <= 0:
            self.kill()


class BaseEnemy(Sprite):
    def __init__(self, pos, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = Surface((20, 20))
        self.image.set_colorkey((0, 0, 0))
        pygame.draw.circle(self.image, '#FF0000', (5, 5), 5)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.order = 'STOP'
        self.motionvector = (0, 0)

        self.speed = 1.5
        self.position = pos
        self.destination = (0, 0)

        self.vision = 250
        self.target = None
        self.cooldown_counter = 0
        self.counter_max = 30
        self.hp = 3

    def update(self):
        if self.target:
            x = self.target.rect.center[0] - self.position[0]
            y = self.target.rect.center[1] - self.position[1]
            length = sqrt(x ** 2 + y ** 2)
            self.motionvector = (x * (self.speed / length), 
                                               y * (self.speed / length))

            self.position = (self.position[0] + self.motionvector[0], self.position[1] + self.motionvector[1])
            self.rect.center = self.position

            if 0 < abs(self.position[0] - self.target.rect.center[0]) < 1 and 0 < abs(self.position[1] - self.target.rect.center[1]) < 1:
                self.order = 'STOP'
                if self.cooldown_counter == 0:
                    self.target.hp -= 1
                    self.cooldown_counter += 1
                else:
                    self.cooldown_counter += 1
                    if self.cooldown_counter == self.counter_max:
                        self.cooldown_counter = 0

        if self.hp <= 0:
            self.kill()
        if self.target:
            if not self.target.alive():
                self.target = None

class Boss(Sprite):
    def __init__(self, pos, group):
        pygame.sprite.Sprite.__init__(self, group)
        self.image = pygame.transform.scale(pygame.image.load(f'images\\boss.png'), (50, 50))
        self.image.set_colorkey((0, 0, 0))
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.speed = 1.5
        self.position = pos
        self.destination = (0, 0)

        self.vision = 250
        self.target = None
        self.cooldown_counter = 0
        self.counter_max = 240
        self.hp = 20

    def update(self):
        if self.cooldown_counter == 0:
            self.cooldown_counter += 1
        else:
            self.cooldown_counter += 1
            if self.cooldown_counter == self.counter_max:
                self.cooldown_counter = 0

        if self.hp <= 0:
            self.kill()
        if self.target:
            if not self.target.alive():
                self.target = None
                

class MouseSprite(Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect((0, 0, 1, 1))
        self.previous_pos = (0, 0)






