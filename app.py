import pygame
import pygame.display
import pygame.event
import pygame.key
import pygame.sprite
import pygame.font

import sys
import random

from pygame.locals import *

pygame.init()
pygame.font.init()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, sprite, color):
        super().__init__()

        self.image = pygame.Surface((15, 50)).convert()
        self.image.fill(color)

        self.rect = pygame.Rect(
            (sprite.rect.x + sprite.image.get_width()/2) - self.image.get_width()/2,
            sprite.rect.y - self.image.get_height()/2,
            self.image.get_width(),
            self.image.get_height()
        )

        self.speed = 5
    
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()

        if pygame.sprite.spritecollide(self, enemy_group, True):
            self.kill()



class Player(pygame.sprite.Sprite):
    def __init__(self, pos=(), size=()):
        super().__init__()
        
        self.pos = pos
        self.size = size

        self.image = pygame.Surface(size).convert()
        self.image.fill((210, 210, 210))

        self.rect = pygame.Rect(
            self.pos[0] - self.image.get_width()/2,
            self.pos[1] - self.image.get_height()/2,
            self.size[0],
            self.size[1]
        )

        self.speed = 8
    
    def update(self):
        keys_pressed = pygame.key.get_pressed()
    
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

        if keys_pressed[K_d] and self.rect.x < width - self.image.get_width():
            self.rect.x += self.speed

        if keys_pressed[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed

        if keys_pressed[K_s] and self.rect.y < height - self.image.get_height():
            self.rect.y += self.speed

        # Collision
        pygame.sprite.spritecollide(self, enemy_group, True)
    
    def shoot(self):

        self.bullet = Bullet(self, (150, 150, 150))
        bullet_group.add(self.bullet)



class Enemy(pygame.sprite.Sprite):
    def __init__(self, size=(75, 75), color=None):
        super().__init__()

        self.image = pygame.Surface(size)
        self.image.fill(color)

        self.rect = pygame.Rect(
            random.randrange(0, width - self.image.get_width()),
            random.randrange(-200, 0),
            self.image.get_width(),
            self.image.get_height()
        )

        self.speed = 3
    
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > height:
            self.kill()



width, height = 1800, 900

clock = pygame.time.Clock()
FPS = 60

title = "Shooter"

display = pygame.display.set_mode((width, height))
pygame.display.set_caption(title)


# Groups
player_group = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()


class Game():
    def __init__(self):
        self.run = 1

        self.player = Player((width/2, height/2), (100, 100))
        player_group.add(self.player)

        self.enemy_colors = [(80, 80, 80), (200, 200, 200), (250, 250, 250)]

        self.score = 1
        self.level = 0

        self.font = pygame.font.SysFont("ComicSans", 75)


    def draw(self):
        display.fill((50, 50, 50))

        bullet_group.draw(display)
        bullet_group.update()

        player_group.draw(display)
        player_group.update()

        enemy_group.draw(display)
        enemy_group.update()

        display.blit(self.score_render, (10, 20))
        display.blit(self.level_render, (width - (self.level_render.get_width() + 10), 20))

        pygame.display.update()


    def start(self):
        while self.run:
            
            self.score += 1/FPS
            self.display_score = int(self.score)

            self.score_render = self.font.render(f"Score : {self.display_score}", True, (255,255,255))
            self.level_render = self.font.render(f"Level : {self.level}", True, (255,255,255))

            clock.tick(FPS)

            self.draw()

            for event in pygame.event.get():
                
                if event.type == QUIT:
                    self.run = 0
                    pygame.quit()
                    sys.exit()
                
                if event.type == KEYDOWN:
                    
                    if event.key == K_SPACE:
                        self.player.shoot()
            
            if len(enemy_group) == 0:
                for i in range(5):
                    enemy = Enemy(color=(120, 120, 120))
                    enemy_group.add(enemy)

                self.level += 1

            
                    
        pygame.quit()
            

if __name__ == "__main__":
    Game().start()
