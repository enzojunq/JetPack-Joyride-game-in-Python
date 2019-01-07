#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:43:11 2018

@author: Hugo Laurencon
"""

import pygame
from pygame.locals import *
import random
from math import floor

import os
os.chdir("/Users/clemence/Documents/GitHub/TDLOG")



width_window = 748
height_window = 565


def check_input():
    keys = pygame.key.get_pressed()
    return(keys)
    

def done_with_game():
    done = False
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            done = True
    return(done)


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
        
    def print_counter(self, screen, font):
        screen.blit(font.render(str(self.value),
                                     -1,
                                     (255, 255, 255)),
                                     (width_window/2, height_window/8))
        
        
class Beam:
    def __init__(self, x, y, index, step):
        self.image = [pygame.image.load("assets/beam0.bmp").convert(),
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
        self.step = step
        
    def update(self, Counter):
        self.x -= self.step
        self.rect[0] = self.x
        if ((self.x + self.image[self.index].get_width() < floor(width_window/11)) and (self.x + self.image[self.index].get_width() >= floor(width_window/11) - self.step)) :
            Counter.update()
            
    def print_beam(self, screen):
        screen.blit(self.image[self.index], (self.x, self.y))
            
    
class Rocket:
    def __init__(self, x, y, step):
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
        self.step = step
        
    def update(self, player):
        self.x -= self.step
        self.rect[0] = self.x
        if (self.x > width_window):
            self.y = player.y
            self.rect[1] = self.y
            
    def print_rocket(self, screen):
        screen.blit(self.image[1], (self.x, self.y))
        if ((self.x > width_window) and (self.x <= 2*width_window)):
            screen.blit(self.image[0],
                        (width_window - self.image[0].get_width(), self.y))
            
            
class Wall:
    def __init__(self, x, gap, y, direction, speed, step):
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
        self.rect = [self.upRect, self.downRect]
        self.direction = direction
        self.speed = speed
        self.step = step
        
    def update(self, Counter):
        self.x -= self.step
        self.upRect[0] = self.x
        self.downRect[0] = self.x
        if ((self.x < floor(width_window/11)) and (self.x >= floor(width_window/11) - self.step)) :
            Counter.update()
        if ((self.y + self.direction*self.speed <= floor(height_window/6)) and
            (self.y + self.direction*self.speed >= -floor(height_window/6))):
            self.y = self.y + self.direction*self.speed
        else:
            self.direction = -self.direction
        self.upRect[1] = height_window/3 + self.gap - self.y
        self.downRect[1] = -height_window/3 - self.gap - self.y
        self.rect = [self.upRect, self.downRect]
        
    def print_wall(self, screen):
        screen.blit(self.image[1], (self.x, height_window/3 + self.gap - self.y))
        screen.blit(self.image[0], (self.x, -height_window/3 - self.gap - self.y))
            
            
class Laser:
    def __init__(self, x, y, step):
        self.image = [pygame.image.load("assets/laser_off.bmp").convert(),
                      pygame.image.load("assets/laser_on.bmp").convert()]
        for i in range(len(self.image)):
            self.image[i].set_colorkey((0, 0, 0))
            pygame.Surface.convert_alpha(self.image[i])
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,
                                self.y,
                                self.image[1].get_width(),
                                self.image[1].get_height())
        self.step = step
        
    def update(self):
        self.x -= self.step
        if (self.x <= width_window):
            self.rect[0] = width_window/15
            
    def print_laser(self, screen):
        if (self.x <= width_window):
            screen.blit(self.image[1], (width_window/15, self.y))
        else:
            screen.blit(self.image[0], (width_window/15, self.y))
        
        
class Mode_beam:
    def __init__(self, nb_beams, step_beam, gap_btw_beams, nb_rockets, step_rocket):
        self.beams = []
        for i in range(nb_beams):
            self.beams.append(Beam(width_window + i*gap_btw_beams,
                                  0,
                                  random.randint(0, 3),
                                  step_beam))
            self.beams[-1].y = random.randint(80, height_window - self.beams[-1].image[self.beams[-1].index].get_height() - 80) #80 is the lenght between the floor and the bottom of the image
            self.beams[-1].rect[1] = self.beams[-1].y
        max_x = self.beams[-1].x
        self.rockets = []
        for i in range(nb_rockets):
            self.rockets.append(Rocket(random.randint(floor(step_rocket/step_beam)*2*width_window, floor(step_rocket/step_beam)*max_x), 0, step_rocket))
        self.obstacles = self.beams + self.rockets
        self.id = 1
        self.end = False
        
    def update(self, counter, player):
        for i in range(len(self.beams)):
            self.beams[i].update(counter)
        for i in range(len(self.rockets)):
            self.rockets[i].update(player)
        if (self.beams[-1].x <= -self.beams[-1].image[self.beams[-1].index].get_width()):
            self.end = True
            
    def print_mode(self, screen):
        for i in range(len(self.beams)):
            self.beams[i].print_beam(screen)
        for i in range(len(self.rockets)):
            self.rockets[i].print_rocket(screen)
            
            
class Mode_wall:
    def __init__(self, nb_walls, gap_wall, speed_max_wall, step_wall, gap_btw_walls):
        self.walls = []
        for i in range(nb_walls):
            self.walls.append(Wall(width_window + i*gap_btw_walls,
                                   gap_wall,
                                   random.randint(-floor(height_window/6), floor(height_window/6)),
                                   random.choice([-1, 1]),
                                   random.randint(0, speed_max_wall),
                                   step_wall))
        self.obstacles = self.walls
        self.id = 2
        self.end = False
    
    def update(self, counter, player):
        for i in range(len(self.walls)):
            self.walls[i].update(counter)
        if (self.walls[-1].x <= -self.walls[-1].image[0].get_width()):
            self.end = True
            
    def print_mode(self, screen):
        for i in range(len(self.obstacles)):
            self.walls[i].print_wall(screen)  
            
            
class Mode_laser:
    def __init__(self, step_laser):
        self.lasers = []
        gap = random.randint(0, 5)
        for i in range(8):
            if ((i != gap) and (i != gap+1) and (i != gap+2)):
                self.lasers.append(Laser(2*width_window, 80+i*50, step_laser)) # 50 = character.image[3].get_width()
        self.obstacles = self.lasers
        self.id = 3
        self.end = False
        
    def update(self, counter, player):
        for i in range(len(self.lasers)):
            self.lasers[i].update()
        if (self.lasers[-1].x <= 0):
            self.end = True
            
    def print_mode(self, screen):
        for i in range(len(self.obstacles)):
            self.lasers[i].print_laser(screen)

        
class Character:
    def __init__(self, x, y, speed, gravity, step):
        self.image = [pygame.image.load("assets/beggining.bmp").convert(),
                      pygame.image.load("assets/flying.bmp").convert(),
                      pygame.image.load("assets/dead.bmp").convert(),
                      pygame.image.load("assets/walk1.bmp").convert(),
                      pygame.image.load("assets/walk2.bmp").convert()]
        for i in range(len(self.image)):
            self.image[i].set_colorkey((255, 255, 255)) #modif au lieu de 0 0 0
            pygame.Surface.convert_alpha(self.image[i])
        self.rect = pygame.Rect(x,
                                y,
                                self.image[0].get_width(),
                                self.image[0].get_height())
        self.y = y
        self.step = step
        self.speed = speed
        self.gravity = gravity
        self.up = 0
        self.sprite = 0
        self.state = 0
        self.dead = False

    def update(self):
        if ((self.up) and (self.y - self.step*self.up >= 80)): #80 is the lenght between the floor and the bottom of the image
            self.y -= self.step*self.up
            self.up = 0
        elif (self.up):
            self.y = 80
            self.up = 0
        elif (self.y + self.gravity <= height_window - self.image[0].get_height() - 80): #80 is the lenght between the floor and the bottom of the image
            self.y += self.gravity
        self.rect[1] = self.y
        
    def print_character(self, screen):
        if self.dead:
            self.sprite = 2
        elif self.up:
            self.sprite = 1
        elif (self.y + self.gravity >= height_window - self.image[0].get_height() - 80): #80 is the lenght between the floor and the bottom of the image
            if (self.sprite == 4 and self.state == 0):
                self.sprite = 3
                self.state += 1
            elif (self.state == 0):
                self.sprite = 4
                self.state += 1
            elif (self.state == self.speed):
                self.state = 0
            else:
                self.state += 1
        else:
            self.sprite = 0
        screen.blit(self.image[self.sprite], (width_window/11, self.y))

        
class Main_menu:
    def __init__(self):
        self.background = pygame.image.load("assets/bg.bmp").convert()
        pygame.font.init()
        self.font = pygame.font.Font('font.ttf',70)
        self.change_window = False
        
    def update(self, screen, clock):
        clock.tick(60)
        self.print_main_menu(screen)
        keys = check_input()
        if keys[K_SPACE]:
            self.change_window = True
        
    def print_main_menu(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.background, (0, 0))
        screen.blit(self.font.render(str("TDLOG"),
                                     -1,
                                     (255, 255, 255)),
                                     (width_window/15, height_window/4))
        screen.blit(self.font.render(str("Touch space to"),
                                     -1,
                                     (255, 255, 255)),
                                     (width_window/15, height_window/2))
        screen.blit(self.font.render(str("continue"),
                                     -1,
                                     (255, 255, 255)),
                                     (width_window/15, height_window*3/4))
        pygame.display.update()
            
            
class GameOver:
    def __init__(self, counter):
        self.background = pygame.image.load("assets/bg.bmp").convert()
        pygame.font.init()
        self.font = pygame.font.Font('font.ttf',70)
        self.change_window = False
        self.counter = counter
        self.best_score = Best_score()
        
    def update(self, screen, clock):
        if (self.counter.value > self.best_score.value):
            self.best_score.update(self.counter.value)
        clock.tick(60)
        self.print_gameover(screen)
        keys = check_input()
        if keys[K_UP]:
            self.change_window = True
        
    def print_gameover(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.background, (0, 0))
        screen.blit(self.font.render(str("Game Over"),
                                     -1,
                                     (255, 255, 255)),
                                     (width_window/8, height_window/4))
        screen.blit(self.font.render("Score: " + str(self.counter.value),
                                     -1,
                                     (255, 255, 255)),
                                     (width_window/8, height_window/2))
        screen.blit(self.font.render("Best score: " + str(self.best_score.value),
                                     -1,
                                     (255, 255, 255)),
                                     (width_window/8, 3*height_window/4))
        pygame.display.update()
        

class Game(object):
    def __init__(self):
        self.background = pygame.image.load("assets/bg.bmp").convert()
        pygame.font.init()
        self.font = pygame.font.Font('font.ttf',70)
        self.change_window = False
        
        self.step_beam = 5
        self.step_max_beam = 10
        self.gap_btw_beams = width_window/2
        
        self.step_rocket = 10
        self.step_max_rocket = 20
        
        self.step_laser = 5
        
        self.gap_wall = 200
        self.speed_max_wall = 2
        self.step_wall = 5
        self.step_max_wall = 10
        self.gap_btw_walls = width_window/4
        
        self.speed_walker = 5
        self.gravity = 5
        self.step_player = 5
        self.player = Character(width_window/11, height_window/2,
                                self.speed_walker, self.gravity,
                                self.step_player)

        self.mode = Mode_beam(random.randint(10, 25), self.step_beam,
                              self.gap_btw_beams, random.randint(2,4),
                              self.step_rocket) 
        self.counter = Counter()
        
    def check_collisions(self):
        for i in range(len(self.mode.obstacles)):
            if (isinstance(self.mode.obstacles[i].rect, list)):
                for j in range(len(self.mode.obstacles[i].rect)):
                    if (self.mode.obstacles[i].rect[j].colliderect(self.player.rect)):
                        self.player.dead = True
            else :
                if (self.mode.obstacles[i].rect.colliderect(self.player.rect)):
                    self.player.dead = True
        if (self.player.dead and (self.player.y + self.player.gravity >= height_window - self.player.image[0].get_height() - 80)): #80 is the lenght between the floor and the bottom of the image
            self.change_window = True
           
    def print_game(self, screen):
        screen.fill((255, 255, 255))
        screen.blit(self.background, (0, 0))
        self.mode.print_mode(screen)
        self.player.print_character(screen)
        self.counter.print_counter(screen, self.font)
        pygame.display.update()
        
    def update(self, screen, clock, time_loop):
        keys = check_input()
        if keys[K_UP] and not self.player.dead:
            self.player.up = 1
        pygame.time.delay(30 - time_loop)
        #clock.tick(60)
        #print(clock.get_time())
        #print(pygame.time.get_ticks())
        print(clock.get_fps())
        print(time_loop)
        self.print_game(screen)
        if self.mode.end:
            if (self.mode.id == 1):
                self.mode = Mode_wall(random.randint(5, 20), self.gap_wall,
                                      self.speed_max_wall, self.step_wall,
                                      self.gap_btw_walls)
                if (self.step_beam < self.step_max_beam):
                    self.step_beam += 1
                if (self.step_rocket < self.step_max_rocket):
                    self.step_rocket += 1
            elif (self.mode.id == 2):
                self.mode = Mode_laser(self.step_laser)
                if (self.step_wall < self.step_max_wall):
                    self.step_wall += 1
            else:
                self.mode = Mode_beam(random.randint(10, 25), self.step_beam,
                                      self.gap_btw_beams, random.randint(2,4),
                                      self.step_rocket) 
        else:
            self.mode.update(self.counter, self.player)
        self.player.update()
        self.check_collisions()
        
        
def main():
    screen = pygame.display.set_mode((width_window, height_window))
    clock = pygame.time.Clock()
    done = False
    previous_time_loop = 0
    time_loop = 0
    while not done:
        main_menu = Main_menu()
        while not main_menu.change_window and not done:
            main_menu.update(screen, clock)
            done = done_with_game()
        game = Game()
        while not game.change_window and not done:
            time_before_loop = pygame.time.get_ticks()
            game.update(screen, clock, time_loop)
            time_after_loop = pygame.time.get_ticks()
            time_loop = time_after_loop - time_before_loop - (30 - previous_time_loop)
            previous_time_loop = time_loop
            done = done_with_game()
        gameover = GameOver(game.counter)
        while not gameover.change_window and not done:
            gameover.update(screen, clock)
            done = done_with_game()
        
                
if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
