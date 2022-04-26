from ast import alias
from math import trunc
from os import truncate
import pygame
import random
from pygame import display
from pygame import surface
from pygame.constants import KEYDOWN
from pygame.time import Clock
from pygame.sprite import spritecollide
from datetime import datetime
import time

from pygame.locals import (
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    K_SPACE,
    KEYDOWN,
    QUIT,
)

pygame.init()
pygame.font.init()

# -- Constants -- #

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800

FRAMERATE = 60

FONT_SIZE = 30

PLAYERSPEED = 5
PROJECTILESPEED = 8

NUMALIENSX = 11
NUMALIENSY = 5

COOLDOWN_TIME = 0.5

# -- Other Definitions -- #

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
mainfont = pygame.font.SysFont('Consolas', FONT_SIZE)

playerscore = 0

# -- Class Definitions -- #

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((60, 20))
        self.surf.fill((0, 255, 0))
        self.rect = self.surf.get_rect(center = (30, 700))
        self.speed = PLAYERSPEED
    
    def update(self, pressed_keys):
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:   
            self.rect.right = SCREEN_WIDTH

player = Player()

class Projectile(pygame.sprite.Sprite):
    def __init__(self):
        super(Projectile, self).__init__()
        self.color = (0, 255, 0)
        self.surf = pygame.Surface((15, 15))
        self.surf.fill(self.color)
        self.rect = self.surf.get_rect(center = (player.rect.center))
        self.speed = PROJECTILESPEED
        self.isAlien = False

    def update(self):
        self.rect.move_ip(0, -self.speed)
        if self.rect.centery < 0:
            self.kill()

all_projectles = pygame.sprite.Group()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super(Alien, self).__init__()
        self.surf = pygame.Surface((30, 30))
        self.surf.fill((255, 0, 0))
        self.rect = self.surf.get_rect(center = (30, 200))
    

    def update(self):
        global playerscore
        hit_right = False

        if pygame.sprite.spritecollide(self, all_projectles, True):
            self.kill()
            playerscore += 1




ATTACK = pygame.USEREVENT + 1
pygame.time.set_timer(ATTACK, random.randint(500, 5000))

MOVEALIEN = pygame.USEREVENT + 2
pygame.time.set_timer(MOVEALIEN, 2000)

all_sprites = pygame.sprite.Group()
all_aliens = pygame.sprite.Group()
alien_projectiles = pygame.sprite.Group()
all_sprites.add(player)

for i in range(NUMALIENSX):
    new_alien = Alien()
    new_alien.rect.center = (new_alien.rect.centerx + (((SCREEN_WIDTH/NUMALIENSX) - 0.54) * i), new_alien.rect.centery)
    all_aliens.add(new_alien)
    all_sprites.add(new_alien)
    for j in range(NUMALIENSY):
        new_alien = Alien()
        new_alien.rect.center = (new_alien.rect.centerx + (((SCREEN_WIDTH/NUMALIENSX) - 0.54) * i), new_alien.rect.centery + ((((SCREEN_HEIGHT/3)/NUMALIENSY) - 0.54) * j))
        all_aliens.add(new_alien)
        all_sprites.add(new_alien)

# -- Main Game Loop -- #

running = True
hit_right = False
hit_left = True

sidehits = 0

# Set the initial time for the cooldown
lastprojectilelaunch = time.time()

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:
                running = False

            if event.key == K_SPACE:
                # Check if the cooldown time has passed
                if time.time() - lastprojectilelaunch > COOLDOWN_TIME:
                    new_projectile = Projectile()
                    all_projectles.add(new_projectile)
                    all_sprites.add(new_projectile)
                    # Set the current time for the cooldown
                    lastprojectilelaunch = time.time()

        elif event.type == QUIT:
            running = False

        elif event.type == ATTACK:
            alien = all_aliens.sprites()[random.randint(1, len(all_aliens.sprites()))-1]
            alien_proj = Projectile()
            alien_proj.color = (255, 0, 0)
            alien_proj.rect.center = alien.rect.center
            alien_proj.speed = -PROJECTILESPEED
            alien_proj.isAlien = True
            alien_projectiles.add(alien_proj)
            all_sprites.add(alien_proj)

        elif event.type == MOVEALIEN:
            for alien in all_aliens:
                if alien.rect.right >= SCREEN_WIDTH:
                    
                    for alien in all_aliens:
                        alien.rect.move_ip(0,2)

                    alien.rect.right = SCREEN_WIDTH

                    hit_left = False
                    hit_right = True

                if alien.rect.left <= 0:

                    for alien in all_aliens:
                        alien.rect.move_ip(0,2)

                    alien.rect.left = 0

                    hit_right = False
                    hit_left = True
            
            if hit_right:
                for alien in all_aliens:
                    alien.rect.move_ip(-5, 0)

            if hit_left:
                for alien in all_aliens:
                    alien.rect.move_ip(5, 0)
    
    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    all_aliens.update()
    alien_projectiles.update()
    all_projectles.update()

    screen.fill((0,0,0))

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    if pygame.sprite.spritecollideany(player, alien_projectiles):
        running = False

    if len(all_aliens.sprites()) == 0:
        running = False

    textsurf = mainfont.render("SCORE: " + str(playerscore) ,False, (255,255,255))
    screen.blit(textsurf, (0,0))

    textsurf2 = mainfont.render("ARROW KEYS: MOVE    SPACE: SHOOT",False, (255,255,255))
    screen.blit(textsurf2, (10,SCREEN_HEIGHT-50))

    pygame.display.flip()

    clock.tick(FRAMERATE)
 
