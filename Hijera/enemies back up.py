import pygame
from Settings import *
import random

class Fireball(pygame.sprite.Sprite):
    def __init__(self, scale, spawnx, spawny, direction):
        pygame.sprite.Sprite.__init__(self, e_proj_sprites_list)
        self.image = pygame.transform.scale(pygame.image.load("Fireball.png"), (8*scale, 8*scale))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

        self.spawnx = spawnx
        self.spawny = spawny

        self.rect.x = spawnx
        self.rect.y = spawny

        self.direction = direction

    def move(self, speed):
        self.rect.x += speed * self.direction

    def reset(self):
        self.rect.x = self.spawnx
        self.rect.y = self.spawny

    def check(self):
        if self.rect.left > WIDTH or self.rect.right < 0:
            e_proj_sprites_list.remove(self)
            eproj.pop(eproj.index(self))

eproj = []

class Enemy(pygame.sprite.Sprite):
    def __init__(self, scale, picture, width, height, spawnx, spawny, lives, death, dwidth, dheight):
        pygame.sprite.Sprite.__init__(self, enemy_sprites_list)
        self.image = pygame.transform.scale(pygame.image.load(picture), (width*scale, height*scale))
        self.deathimage = pygame.transform.scale(pygame.image.load(death), (dwidth*scale, dheight*scale))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()

        self.rect.x = spawnx
        self.rect.y = spawny
        self.lives = lives
        self.deathtime = 30
        self.dead = False
        self.spawn[spawnx, spawny]

    def check(self):
        if self.lives <= 0:
            self.image = self.deathimage
            self.image.set_colorkey(WHITE)
            self.dead = True
        if self.dead:
            if self.deathtime:
                self.deathtime -= 1
            else:
                enemy_sprites_list.remove(self)
                enemies.pop(enemies.index(self))

    def reset(self):
        self.rect.x = self.spawn[0]
        self.rect.y = self.spawn[1]




class Shadow(Enemy):
    def __init__(self):
        Enemy.__init__(self, SCALE, "Shadow.png", 16, 12, random.choice([0, 640]), HEIGHT - 62*SCALE, 10, "Shadowdie.png", 16, 12)
        self.fire_range_begin = random.randint(200, 300)
        self.cooldown = 0
    def attack(self, speed, existence_center, existence):
        if not existence_center < self.fire_range_begin:
            if existence > self.rect.x:
                self.rect.x += speed
            else:
                self.rect.x -= speed

        elif not self.cooldown:
            if existence > self.rect.x:
                eproj.append(Fireball(SCALE, self.rect.centerx, self.rect.y, 1))
            else:
                eproj.append(Fireball(SCALE, self.rect.centerx, self.rect.y, -1))
            self.cooldown = 50

        if self.cooldown:
            self.cooldown -= 1

enemies = []
