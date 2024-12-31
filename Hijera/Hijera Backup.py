# Importing and initializing the pygame module
import pygame
import random
pygame.init()

# Settings
WIDTH = 600
HEIGHT = 480
SCALE = 4
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
FPS = 60
SPEED = 5
SHIELDCOLOR = (185, 0, 185)

clock = pygame.time.Clock()

SCREEN = pygame.display.set_mode([WIDTH, HEIGHT])

pygame.display.set_caption("Hijera: Beginnings")

all_sprites_list = pygame.sprite.Group()
e_proj_sprites_list = pygame.sprite.Group()
p_proj_sprites_list = pygame.sprite.Group()
enemy_sprites_list = pygame.sprite.Group()

hudfont = pygame.font.SysFont("impact.tff", 36)

# Background class
class background(pygame.sprite.Sprite):
    def __init__(self, scale, spawnx, spawny):
        pygame.sprite.Sprite.__init__(self, all_sprites_list)

        self.image = pygame.transform.scale(pygame.image.load("background.png"), (150 * scale, 120 * scale))

        self.rect = self.image.get_rect()
        self.rect.x = spawnx
        self.rect.y = spawny
        self.makesure = 0

    def move(self, direction):
        if direction == 1:
            if self.rect.x >= WIDTH:
                self.rect.x = -self.rect.width
        if direction == -1:
            if self.rect.x + self.rect.width <= 0:
                self.rect.x = WIDTH
        self.rect.x += direction * SPEED

bg1 = background(SCALE, 0, 0)
bg2 = background(SCALE, WIDTH, 0)

lightbeams = []

class Lightbeam(pygame.sprite.Sprite):
    def __init__(self, scale, spawnx, spawny, direction):
        pygame.sprite.Sprite.__init__(self, p_proj_sprites_list)

        self.image = pygame.transform.scale(pygame.image.load("Lightbeam.png"), (3*scale, 2*scale))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()

        self.spawnx = spawnx

        self.spawny = spawny

        self.rect.x = spawnx
        self.rect.y = spawny

        self.direction = direction

        self.damage = 1

    def move(self, speed):

        self.rect.x += speed*self.direction

    def check(self):
        if self.rect.left > WIDTH or self.rect.right < 0:
            self.reset()

    def reset(self):
        self.rect.x = self.spawnx
        self.rect.y = self.spawny
        lightbeams.pop(lightbeams.index(self))
        p_proj_sprites_list.remove(self)


# Character Class
# If direction = -1 and whichleg = 1, the character's image will be "Solonright.png"
# If direction = -1 and whichleg = -1, the character's image will be "Solon.png"
# If direction = 1 and whichleg = -1, the character's image will be "Solonleft.png"
# If direction = 1 and whichleg = 1, the character's image will be "Solonflip.png"
class Solon(pygame.sprite.Sprite):
    def __init__(self, scale):
        pygame.sprite.Sprite.__init__(self, all_sprites_list)
        self.image = pygame.transform.scale(pygame.image.load("Solon.png"), (10*scale, 13*scale))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()
        self.rect.x = WIDTH / 2 - self.rect.width/2
        self.rect.y = HEIGHT - scale*63
        self.whichleg = 1
        self.legtime = 0
        self.picture = ""
        self.cooldown = 0
        self.normal = WIDTH/2
        self.sword = False
        self.jumptime = 0
        self.jumpable = False
        self.jump_height = 90
        self.down = 5
        self.lives = 10
    def move(self, scale, direction):
        if not self.legtime:
            if direction == -1:
                if self.whichleg == 1:
                    self.picture = "Solonright.png"
                else:
                    self.picture = "Solon.png"
            else:
                if self.whichleg == -1:
                    self.picture = "Solonleft.png"
                else:
                    self.picture = "Solonflip.png"

            self.image = pygame.transform.scale(pygame.image.load(self.picture), (10 * scale, 13 * scale))
            self.image.set_colorkey(BLACK)
            self.legtime = 20
            self.whichleg *= -1
        if self.legtime:
            self.legtime -= 1
        if self.cooldown:
            self.cooldown -= 1
        self.sword = False
    def jump(self):
        if self.jumpable:
            self.rect.y -= self.jump_height
            self.jumptime = self.jump_height
            self.jumpable = False
    def attack(self, scale, direction):
        if not self.cooldown:
            if direction == -1:
                if self.whichleg == 1:
                    self.picture = "Solonstrikeright.png"
                else:
                    self.picture = "Solonstrike.png"
            else:
                if self.whichleg == -1:
                    self.picture = "Solonstrikeleft.png"
                else:
                    self.picture = "Solonstrikeflip.png"

            self.image = pygame.transform.scale(pygame.image.load(self.picture), (14 * scale, 13 * scale))
            self.image.set_colorkey(BLACK)
            self.cooldown = 20
            self.whichleg *= -1
            self.sword = True
            lightbeams.append(Lightbeam(SCALE, self.rect.centerx, self.rect.centery, -direction))
    def check(self, scale):
        if self.picture == "Solonstrikeleft.png" or self.picture == "Solonstrikeflip.png":
            self.rect.x = self.normal - 4*scale
        else:
            self.rect.x = self.normal
        if self.jumptime:
            if self.jumptime <= self.down:
                self.rect.y += self.jump_height/self.down
            self.jumptime -= 1
        elif self.rect.y == HEIGHT - scale*63:
            self.jumpable = True

Solon_first = Solon(SCALE)

class Shield(pygame.sprite.Sprite):
    def __init__(self, scale):
        pygame.sprite.Sprite.__init__(self, all_sprites_list)

        self.image = pygame.transform.scale(pygame.image.load("Shield.png"), (14*scale, 2*scale))
        self.image.set_colorkey(SHIELDCOLOR)

        self.rect = self.image.get_rect()

        self.rect.x = Solon_first.rect.x
        self.rect.y = Solon_first.rect.y + Solon_first.rect.height
        self.durable = True
        self.repairtime = 100

    def check(self, use):
        if self.durable:
            if use:
                self.image.set_colorkey(WHITE)
            else:
                self.image.set_colorkey(SHIELDCOLOR)
            self.rect.x = Solon_first.rect.x
            self.rect.y = Solon_first.rect.y + Solon_first.rect.height
        if not self.durable and use:
            print("The Shield is currently disabled")
        if self.repairtime:
            self.repairtime -= 1
        if not self.repairtime and not self.durable:
            print("The Shield is repaired")
            self.repairtime = 100
            self.durable = True

Shield1 = Shield(SCALE)


# Fort class
# Because the player is "walking" on this sprite and the players normally stays in the middle of the screen, the fort class will have a move function do give the user an impression that the character is moving
# Forts will check to see if they may need more forts to cover the entire screen
# Forts will check to see if they are off screen
class Fort(pygame.sprite.Sprite):
    def __init__(self, scale, spawnx, spawny):
        pygame.sprite.Sprite.__init__(self, all_sprites_list)

        self.image = pygame.transform.scale(pygame.image.load("Fort.png"), (78*scale, 50*scale))
        self.image.set_colorkey(WHITE)

        self.rect = self.image.get_rect()

        self.rect.x = spawnx
        self.rect.y = spawny
        self.onscreen = True
        self.maynf = False
        self.maynb = False

    def move(self, direction):
        self.rect.x += direction * SPEED

    def check(self):
        if self.rect.x + self.rect.width < 0 or self.rect.x > WIDTH:
            self.onscreen = False
        if self.rect.x < WIDTH:
            self.maynf = True
        if self.rect.x > 0:
            self.maynb = True

class Skull(pygame.sprite.Sprite):
    def __init__(self, scale, spawnx, spawny):
        pygame.sprite.Sprite.__init__(self, all_sprites_list)
        self.image = pygame.transform.scale(pygame.image.load("Skull.png"), (10 * scale, 10 * scale))
        self.image.set_colorkey(BLACK)

        self.rect = self.image.get_rect()

        self.rect.x = spawnx
        self.rect.y = spawny
        self.paired = 0

    def move(self, direction):
        self.rect.x += direction * SPEED

    def tell(self):
        return self.paired

eproj = []

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




class Shadow(Enemy):
    def __init__(self):
        Enemy.__init__(self, SCALE, "Shadow.png", 16, 12, random.choice([0, 640]), HEIGHT - 62*SCALE, 10, "Shadowdie.png", 16, 12)
        self.fire_range_begin = random.randint(200, 300)
        self.cooldown = 0
    def attack(self, speed):
        if not abs(Solon_first.rect.centerx - self.rect.centerx) < self.fire_range_begin:
            if Solon_first.rect.x > self.rect.x:
                self.rect.x += speed
            else:
                self.rect.x -= speed

        elif not self.cooldown:
            if Solon_first.rect.x > self.rect.x:
                eproj.append(Fireball(SCALE, self.rect.centerx, self.rect.y, 1))
            else:
                eproj.append(Fireball(SCALE, self.rect.centerx, self.rect.y, -1))
            self.cooldown = 50

        if self.cooldown:
            self.cooldown -= 1

enemies = []


# Make objects
newfort = Fort(SCALE, 0, HEIGHT - 50*SCALE)
forts = [newfort]
skulls = [Skull(SCALE, newfort.rect.centerx - 5*SCALE, HEIGHT - newfort.rect.height * 4/5)]
enemies.append(Shadow())



# Loop that keeps the game running
running = True
while running:
    Solon_first.check(SCALE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                Solon_first.attack(SCALE, -1)
            if event.key == pygame.K_LEFT:
                Solon_first.attack(SCALE, 1)
            if event.key == pygame.K_SPACE:
                Solon_first.jump()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_f]:
        Solon_first.move(SCALE, -1)
        for fort in forts:
            fort.move(-1)
        for s in skulls:
            s.move(-1)
        bg1.move(-1)
        bg2.move(-1)

    if keys[pygame.K_a]:
        Solon_first.move(SCALE, 1)
        for fort in forts:
            fort.move(1)
        for s in skulls:
            s.move(1)
        bg1.move(1)
        bg2.move(1)

    if keys[pygame.K_DOWN]:
        Shield1.check(True)
    else:
        Shield1.check(False)

    for fort in forts:
        fort.check()
        if not fort.onscreen:
            for s in skulls:
                if s.tell() == fort:
                    all_sprites_list.remove(s)
                    skulls.pop(skulls.index(s))
            all_sprites_list.remove(fort)
            forts.pop(forts.index(fort))

    makesure = True

    while makesure:
        needb = True
        needf = True
        minfort = 0
        maxfort = 0
        xlist = []
        for fort in forts:
            if not fort.maynb:
                needb = False
            if not fort.maynf:
                needf = False

        for fort in forts:
            xlist.append(fort.rect.x)

        if needb:
            forts.append(Fort(SCALE, min(xlist) - 78 * SCALE, HEIGHT - 50 * SCALE))
            newfort = forts[len(forts) - 1]
            skulls.append(Skull(SCALE, newfort.rect.centerx - 5*SCALE, HEIGHT - newfort.rect.height * 4/5))

        if needf:
            forts.append(Fort(SCALE, max(xlist) + 78 * SCALE, HEIGHT - 50 * SCALE))
            newfort = forts[len(forts) - 1]
            skulls.append(Skull(SCALE, newfort.rect.centerx - 5 * SCALE, HEIGHT - newfort.rect.height * 4 / 5))

        if not needf and not needb:
            break

        for s in enemies:
            s.attack(SPEED * 3/2)
        for f in eproj:
            f.move(SPEED)
            f.check()
        for l in lightbeams:
            l.move(SPEED)
            l.check()

    damaged = pygame.sprite.spritecollide(Solon_first, e_proj_sprites_list, True)
    for d in damaged:
        eproj.pop(eproj.index(d))
        Solon_first.lives -= 1
        if Solon_first.lives > 0:
            print("You have lost a life! Current lives: " + str(Solon_first.lives))
        else:
            print("You are dead!")

    block = pygame.sprite.spritecollide(Shield1, e_proj_sprites_list, True)
    if Shield1.durable:
        for b in block:
            eproj.pop(eproj.index(b))
            Shield1.durable = False
            print("The Shield is broken!")

    hit = pygame.sprite.groupcollide(enemy_sprites_list, p_proj_sprites_list, False, True)
    for h in hit.keys():
        h.lives -= hit[h][0].damage

    for e in enemies:
        e.check()

    SCREEN.fill(BLACK)
    all_sprites_list.draw(SCREEN)
    e_proj_sprites_list.draw(SCREEN)
    p_proj_sprites_list.draw(SCREEN)
    enemy_sprites_list.draw(SCREEN)

    pygame.display.flip()

    clock.tick(FPS)



