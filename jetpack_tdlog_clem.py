#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:43:11 2018

@authors: Hugo Laurencon, Louis Ravillon, Clemence Barillot
"""
import os
os.chdir("/Users/clemence/Documents/GitHub/TDLOG")


import pygame
from pygame.locals import *
import sys
import random
from math import floor


width_window = 748
height_window = 565


class Best_score:
    def __init__(self):
        file = open("best_score.txt", "r")
        self.value = int(file.read())
        file.close()
        
    def update(self, new_best_score):
        self.value = new_best_score
        file = open("best_score.txt", "w")
        file.write(str(new_best_score))
        file.close()
        

class Counter:
    def __init__(self):
        self.value = 0
    
    def update(self):
        self.value += 1
        
    def reset(self):
        self.value = 0
        
        
class Beam:
    def __init__(self, x, y, index):
        self.image = [pygame.image.load("assets/beam0.bmp").convert(),
                      pygame.image.load("assets/beam1.bmp").convert(),
                      pygame.image.load("assets/beam2.bmp").convert(),
                      pygame.image.load("assets/beam3.bmp").convert(),
                      pygame.image.load("assets/beam4.bmp").convert()]
        for i in range(len(self.image)):
            self.image[i].set_colorkey((0, 0, 0))
            pygame.Surface.convert_alpha(self.image[i])
        self.index = index
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,
                                self.y,
                                self.image[index].get_width(),
                                self.image[index].get_height())
        
    def update(self, step, Counter):
        self.x -= step
        self.rect[0] = self.x
        if ((self.x + self.image[self.index].get_width() < floor(width_window/11)) and (self.x + self.image[self.index].get_width() >= floor(width_window/11) - step)) :
            Counter.update()
            
    
class Rocket:
    def __init__(self, x, y):
        self.image = [pygame.image.load("assets/rocket_warning.bmp").convert(),
                      pygame.image.load("assets/rocket.bmp").convert()]
        for i in range(len(self.image)):
            self.image[i].set_colorkey((0, 0, 0))
            pygame.Surface.convert_alpha(self.image[i])
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,
                                self.y,
                                self.image[1].get_width(),
                                self.image[1].get_height())
        
    def update(self, step, player):
        self.x -= step
        self.rect[0] = self.x
        if (self.x > width_window):
            self.y = player.y
            self.rect[1] = self.y
    
    
class Wall:
    def __init__(self, x, gap, y, direction, speed):
        self.image = [pygame.image.load("assets/bottom.bmp").convert(),
                      pygame.image.load("assets/top.bmp").convert()]
        for i in range(len(self.image)):
            self.image[i].set_colorkey((0, 0, 0))
            pygame.Surface.convert_alpha(self.image[i])
        self.x = x
        self.gap = gap
        self.y = y
        self.upRect = pygame.Rect(self.x,
                                  height_window/3 + self.gap - self.y,
                                  self.image[1].get_width(),
                                  self.image[1].get_height())
        self.downRect = pygame.Rect(self.x,
                                    -height_window/3 - self.gap - self.y,
                                    self.image[0].get_width(),
                                    self.image[0].get_height())
        self.direction = direction
        self.speed = speed
        
    def update(self, step, Counter):
        self.x -= step
        self.upRect[0] = self.x
        self.downRect[0] = self.x
        if ((self.x < floor(width_window/11)) and (self.x >= floor(width_window/11) - step)) :
            Counter.update()
        if ((self.y + self.direction*self.speed <= floor(height_window/6)) and
            (self.y + self.direction*self.speed >= -floor(height_window/6))):
            self.y = self.y + self.direction*self.speed
        else:
            self.direction = -self.direction
        self.upRect[1] = height_window/3 + self.gap - self.y
        self.downRect[1] = -height_window/3 - self.gap - self.y
        
        
class Character:
    def __init__(self, x, y, gravity):
        self.image = [pygame.image.load("assets/beggining.bmp").convert(),
                      pygame.image.load("assets/flying.bmp").convert(),
                      pygame.image.load("assets/dead.bmp").convert(),
                      pygame.image.load("assets/walk1.bmp").convert(),
                      pygame.image.load("assets/walk2.bmp").convert()]
        for i in range(len(self.image)):
            self.image[i].set_colorkey((0, 0, 0))
            pygame.Surface.convert_alpha(self.image[i])
        self.rect = pygame.Rect(x,
                                y,
                                self.image[0].get_width(),
                                self.image[0].get_height())
        self.y = y
        self.gravity = gravity
        self.up = 0
        self.sprite = 0

    def update(self, step):
        if ((self.up) and (self.y - step*self.up >= 80)):
            self.y -= step*self.up
            self.up = 0
        elif (self.y + self.gravity <= height_window - self.image[0].get_height() - 80):
            self.y += self.gravity
        self.rect[1] = self.y
            
    def reset(self, x, y, gravity):
        self.rect = pygame.Rect(x,
                                y,
                                self.image[0].get_width(),
                                self.image[0].get_height())
        self.y = y
        self.gravity = gravity
        self.up = 0
        self.sprite = 0
            
            
class Game(object):
    def __init__(self):
        self.screen = pygame.display.set_mode((width_window, height_window))
        self.background = pygame.image.load("assets/bg.bmp").convert()
        self.mainScreen = True
        self.startGame = False
        self.gameOver = False
        self.clock = pygame.time.Clock()
        pygame.font.init()
        self.font = pygame.font.Font('font.ttf',70)
        self.step_player = 5
        self.step_wall = 5  
        self.step_beam = 5
        self.step_rocket = 10
        self.gravity = 5
        self.gap_wall = 200
        self.gap_btw_walls = width_window/4
        self.gap_btw_beams = width_window/2
        self.speed_max_wall = 2
        self.player = Character(width_window/11, height_window/2, self.gravity)
        self.counter = Counter()
        self.mode = 1
        self.walls = []
        self.beams = []
        self.rockets = []
        self.best_score = Best_score()
        
    def reset(self):
        self.mainScreen = True
        self.startGame = False
        self.gameOver = False
        self.player.reset(width_window/11, height_window/2, self.gravity)
        self.counter.reset()
        self.step_wall = 5
        self.step_beam = 5
        self.step_rocket = 10
        self.mode = 1
        self.walls = []
        self.beams = []
        self.rockets = []
        
    def check_input(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()
        keys = pygame.key.get_pressed()
        if keys[K_UP] and not self.gameOver:
            self.player.up = 1
        
    def check_collisions(self):
        if (self.mode == 1):
            for i in range(len(self.beams)):
                if (self.beams[i].rect.colliderect(self.player.rect)):
                    self.gameOver = True
                    self.startGame = False
            for i in range(len(self.rockets)):
                if (self.rockets[i].rect.colliderect(self.player.rect)):
                    self.gameOver = True
                    self.startGame = False
        elif (self.mode == 2):
            for i in range(len(self.walls)):
                if (self.walls[i].upRect.colliderect(self.player.rect) or
                    self.walls[i].downRect.colliderect(self.player.rect)):
                    self.gameOver = True
                    self.startGame = False
            
    def create_main_menu(self):
        self.clock.tick(60)
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.font.render(str("TDLOG"),
                                     -1,
                                     (255, 255, 255)),
                                     (width_window/8, height_window/4))
        self.screen.blit(self.font.render(str("Press any key to"),
                                     -1,
                                     (255, 255, 255)),
                                     (width_window/8, height_window/2))
        self.screen.blit(self.font.render(str("continue"),
                                     -1,
                                     (255, 255, 255)),
                                     (width_window/8, 3*height_window/4))
        pygame.display.update()
            
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                    self.mainScreen = False
                    self.startGame = True
            
    def create_game_over(self):
        self.clock.tick(60)
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        self.screen.blit(self.font.render(str("Game Over"),
                                     -1,
                                     (255, 255, 255)),
                                     (width_window/8, height_window/4))
        self.screen.blit(self.font.render("Score: " + str(self.counter.value),
                                     -1,
                                     (255, 255, 255)),
                                     (width_window/8, height_window/2))
        self.screen.blit(self.font.render("Best score: " + str(self.best_score.value),
                                     -1,
                                     (255, 255, 255)),
                                     (width_window/8, 3*height_window/4))
        pygame.display.update()
        
        if (self.counter.value > self.best_score.value):
            self.best_score.update(self.counter.value)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN):
                self.reset()
                
    def create_game(self):
        if (self.mode == 1):
            if (len(self.beams) == 0):
                nb_beams = random.randint(10, 25)
                for i in range(nb_beams):
                    self.beams.append(Beam(width_window + i*self.gap_btw_beams,
                                           0,
                                           random.randint(0, 4)))
                    self.beams[-1].y = random.randint(80, height_window - self.beams[-1].image[self.beams[-1].index].get_height() - 80)
                    self.beams[-1].rect[1] = self.beams[-1].y
                nb_rockets = floor(nb_beams/5)
                for i in range(nb_rockets):
                    self.rockets.append(Rocket(random.randint(floor(self.step_rocket/self.step_beam)*2*width_window, floor(self.step_rocket/self.step_beam)*self.beams[-1].x), 0))
            if (self.beams[-1].x <= -self.beams[-1].image[self.beams[-1].index].get_width()):
                self.beams = []
                self.rockets = []
                self.mode = 2
                if (self.step_beam < 10):
                    self.step_beam += 1
                if (self.step_rocket < 20):
                    self.step_rocket += 1
                self.clock.tick(60)
                self.check_input()
                self.print_game()
                self.player.update(self.step_player)
                pygame.display.update()
            else:
                self.clock.tick(60)
                self.check_input()
                self.print_game()
                for i in range(len(self.beams)):
                    self.beams[i].update(self.step_beam, self.counter)
                for i in range(len(self.rockets)):
                    self.rockets[i].update(self.step_rocket, self.player)
                self.player.update(self.step_player)
                self.check_collisions()
                pygame.display.update()
            
        elif (self.mode == 2):
            if (len(self.walls) == 0):
                nb_walls = random.randint(5, 20)
                for i in range(nb_walls):
                    self.walls.append(Wall(width_window + i*self.gap_btw_walls,
                                           self.gap_wall,
                                           random.randint(-floor(height_window/6), floor(height_window/6)),
                                           random.choice([-1, 1]),
                                           random.randint(0, self.speed_max_wall)))
            if (self.walls[-1].x <= -self.walls[-1].image[0].get_width()):
                self.walls = []
                self.mode = 1
                if (self.step_wall < 10):
                    self.step_wall += 1
                self.clock.tick(60)
                self.check_input()
                self.print_game()
                self.player.update(self.step_player)
                pygame.display.update()
            else:
                self.clock.tick(60)
                self.check_input()
                self.print_game()
                for i in range(len(self.walls)):
                    self.walls[i].update(self.step_wall, self.counter)
                self.player.update(self.step_player)
                self.check_collisions()
                pygame.display.update()
                      
    def print_game(self):
        self.screen.fill((255, 255, 255))
        self.screen.blit(self.background, (0, 0))
        for i in range(len(self.beams)):
            self.screen.blit(self.beams[i].image[self.beams[i].index],
                             (self.beams[i].x, self.beams[i].y))
        for i in range(len(self.rockets)):
            self.screen.blit(self.rockets[i].image[1],
                            (self.rockets[i].x, self.rockets[i].y))
            if ((self.rockets[i].x > width_window) and (self.rockets[i].x <= 2*width_window)):
                self.screen.blit(self.rockets[i].image[0],
                            (width_window - self.rockets[i].image[0].get_width(), self.rockets[i].y))
        for i in range(len(self.walls)):
            self.screen.blit(self.walls[i].image[1],
                             (self.walls[i].x, height_window/3 + self.walls[i].gap - self.walls[i].y))
            self.screen.blit(self.walls[i].image[0],
                             (self.walls[i].x, -height_window/3 - self.walls[i].gap - self.walls[i].y))
        self.screen.blit(self.font.render(str(self.counter.value),
                                     -1,
                                     (255, 255, 255)),
                                     (width_window/2, height_window/8))
        if self.gameOver:
            self.player.sprite = 2
            self.screen.blit(self.player.image[self.player.sprite], (width_window/11, self.player.y))
        elif self.player.up:
            self.player.sprite = 1
            self.screen.blit(self.player.image[self.player.sprite], (width_window/11, self.player.y))
            self.player.sprite = 0
        elif (self.player.y + self.player.gravity >= height_window - self.player.image[0].get_height() - 80):
            if (self.player.sprite == 4):
                self.player.sprite = 3
            else:
                self.player.sprite = 4
            self.screen.blit(self.player.image[self.player.sprite], (width_window/11, self.player.y))
        else:
            self.screen.blit(self.player.image[self.player.sprite], (width_window/11, self.player.y))
     
    def main(self):
        while True:
            if self.mainScreen:
                self.create_main_menu()
            elif self.startGame:
                self.create_game()
            elif self.gameOver:
                self.create_game_over()
                

if __name__ == "__main__":
    Game().main()
