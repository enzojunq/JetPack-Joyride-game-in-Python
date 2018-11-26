#!/usr/bin/env python

import pygame
from pygame.locals import *
import sys
import random

#test de clémence 
import os
os.chdir("/Users/clemence/Documents/GitHub/TDLOG")



screen = pygame.display.set_mode((480*2-80, 708))
background = pygame.image.load("assets/background.bmp").convert()
characterSprites = [pygame.image.load("assets/1.bmp").convert(),
                         pygame.image.load("assets/2.bmp").convert(),
                         pygame.image.load("assets/dead.bmp")]
walls = [pygame.image.load("assets/bottom.bmp").convert(),
              pygame.image.load("assets/top.bmp").convert()]
for i in range(len(characterSprites)):
    characterSprites[i].set_colorkey((0, 0, 0))
    pygame.Surface.convert_alpha(characterSprites[i])
for i in range(len(walls)):
    walls[i].set_colorkey((0, 0, 0))
    pygame.Surface.convert_alpha(walls[i])
            
            

class Counter:
    def __init__(self):
        self.value = 0
    
    def update(self):
        self.value += 1
        
    def reset(self):
        self.value = 0
    
    
class Wall:
    def __init__(self):
        self.x = 880
        self.gap = 170 #135
        self.y = random.randint(-110, 110)
        self.upRect = pygame.Rect(self.x,
                                  360 + self.gap - self.y + 10,
                                  walls[1].get_width() - 10,
                                  walls[1].get_height())
        self.downRect = pygame.Rect(self.x,
                                    0 - self.gap - self.y - 10,
                                    walls[0].get_width() - 10,
                                    walls[0].get_height())
        self.direction = random.choice([-1,1])
        self.speed = random.randint(0,2)
        
    def update(self, Counter):
        self.x -= 5
        self.upRect[0] = self.x
        self.downRect[0] = self.x
        if self.x < -80  :
            self.reset()
            Counter.update()
        if ((self.y + self.direction*self.speed <= 110) and
            (self.y + self.direction*self.speed >= -110)):
            self.y = self.y + self.direction*self.speed
        else:
            self.direction = -self.direction
        self.upRect[1] = 360 + self.gap - self.y + 10
        self.downRect[1] = 0 - self.gap - self.y - 10
            
    def reset(self):
        self.x = 880
        self.gap = 170
        self.y = random.randint(-110, 110) 
        self.upRect = pygame.Rect(self.x,
                                  360 + self.gap - self.y + 10,
                                  walls[1].get_width() - 10,
                                  walls[1].get_height())
        self.downRect = pygame.Rect(self.x,
                                    0 - self.gap - self.y - 10,
                                    walls[0].get_width() - 10,
                                    walls[0].get_height())
        self.direction = random.choice([-1,1])
        self.speed = random.randint(0,5)
        
        
class Character:
    def __init__(self):
        self.rect = pygame.Rect(65, 354, 50, 50)
        self.y = 354
        self.up = 0
        self.down = 0
        self.sprite = 0

    def update(self):
        if self.up:
            self.y -= 5*self.up
            self.up = 0
        if self.down:
            self.y += 5*self.down
            self.down = 0
        self.rect[1] = self.y
            
    def reset(self):
        self.rect = pygame.Rect(65, 354, 50, 50)
        self.y = 354
        self.up = 0
        self.down = 0
        self.dead = False
        self.sprite = 0
            
            
class Game(object):
    def __init__(self,nWalls): #
        self.mainScreen = True
        self.startGame = False
        self.gameOver = False
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.Font('iomanoid.ttf',70)
        self.player = Character()
        self.spaceBtwnWall = 480 # 
        
        #
        self.nWalls = nWalls
        self.walls = [] #
        
        currentWall = Wall()
        currentWall.x = 400
        currentWall.downRect[0] = 400
        self.walls.append(currentWall)
        
        for i in range (nWalls-1):
            self.walls.append(Wall())  
        #
             
        #self.wall1 = Wall()
        #self.wall1.x = 400
        #self.wall1.upRect[0] = 400
        #self.wall1.downRect[0] = 400
        #self.wall2 = Wall()
        
        self.counter = Counter()
        
    def reset(self):
        self.mainScreen = True
        self.startGame = False
        self.gameOver = False
        self.player.reset()
        self.walls[0].reset()#
        self.walls[0].x = 400#
        self.walls[0].upRect[0] = 400#
        self.walls[0].downRect[0] = 400#
        for i in range(self.nWalls-1):#
            self.walls[i] = Wall()#
            
        self.counter.reset()
        
    def check_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[K_UP] and not self.gameOver:
            self.player.up = 1
        if keys[K_DOWN] and not self.gameOver:
            self.player.down = 1
        
    def check_collisions(self):
        if (self.wall1.upRect.colliderect(self.player.rect) or
            self.wall1.downRect.colliderect(self.player.rect) or
            self.wall2.upRect.colliderect(self.player.rect) or
            self.wall2.downRect.colliderect(self.player.rect)):
            self.gameOver = True
            self.startGame = False
            
    def create_main_menu(self):
        self.clock.tick(60)
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        screen.blit(self.font.render(str("Press any key to continue"),
                                     -1,
                                     (255, 255, 255)),
                                     (40, 300))
        pygame.display.update()
            
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                    self.mainScreen = False
                    self.startGame = True
            
    def create_game_over(self):
        self.clock.tick(60)
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        screen.blit(self.font.render(str("Game Over"),
                                     -1,
                                     (255, 255, 255)),
                                     (250, 75))
        screen.blit(self.font.render("Score: " + str(self.counter.value),
                                     -1,
                                     (255, 255, 255)),
                                     (300, 225))
        screen.blit(self.font.render("Best score: " + str(self.counter.value),
                                     -1,
                                     (255, 255, 255)),
                                     (225, 375))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                self.reset()
        
    def print_game(self):
        screen.fill((255, 255, 255))
        screen.blit(background, (0, 0))
        screen.blit(walls[1],
                    (self.wall1.x, 360 + self.wall1.gap - self.wall1.y))
        screen.blit(walls[0],
                    (self.wall1.x, 0 - self.wall1.gap - self.wall1.y))
        screen.blit(walls[1],
                    (self.wall2.x, 360 + self.wall2.gap - self.wall2.y))
        screen.blit(walls[0],
                    (self.wall2.x, 0 - self.wall2.gap - self.wall2.y))
        screen.blit(self.font.render(str(self.counter.value),
                                     -1,
                                     (255, 255, 255)),
                                     (440, 50))
        if self.gameOver:
            self.player.sprite = 2
        elif self.player.up:
            self.player.sprite = 1
        screen.blit(characterSprites[self.player.sprite], (70, self.player.y))
        if not self.gameOver:
            self.player.sprite = 0
     
    def main(self):
        while True:
            if self.mainScreen:
                self.create_main_menu()
            elif self.startGame:
                self.clock.tick(60)
                self.check_input()
                self.print_game()
                self.wall1.update(self.counter)
                self.wall2.update(self.counter)
                self.player.update()
                self.check_collisions()
                pygame.display.update()
            elif self.gameOver:
                self.create_game_over()
                

if __name__ == "__main__":
    Game(2).main()
