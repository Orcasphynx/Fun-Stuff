import pygame

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
Game_Sec = 0
Game_Limit = 300

all_sprites_list = pygame.sprite.Group()
e_proj_sprites_list = pygame.sprite.Group()
p_proj_sprites_list = pygame.sprite.Group()
enemy_sprites_list = pygame.sprite.Group()