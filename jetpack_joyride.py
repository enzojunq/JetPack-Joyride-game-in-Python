#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 16:43:11 2018

@author: Hugo Laurencon
"""

import tkinter
import pygame
from pygame.locals import *
import random
from math import floor
import unittest


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
    

def make_pavements(screen, constants, image_edge_pavement, image_main_pavement):
    for i in range(int(constants.width_window/constants.width_pavement)):
        screen.blit(image_edge_pavement, (constants.width_pavement*i, 0))
    for i in range(int(constants.width_window/constants.width_pavement)):
        for j in range(1, int((constants.height_window - constants.height_pavement)/constants.height_pavement)):
            screen.blit(image_main_pavement, (constants.width_pavement*i, constants.height_pavement*j))
    for i in range(int(constants.width_window/constants.width_pavement)):
        screen.blit(image_edge_pavement, (constants.width_pavement*i, constants.height_window - constants.height_pavement))
    return(None)
    
    
class Constants:
    def __init__(self):
        self.width_pavement = 100
        self.height_pavement = 50
        
        self.security_band = 100
        
        root = tkinter.Tk()
        self.width_window = root.winfo_screenwidth() - self.security_band - (root.winfo_screenwidth()-self.security_band)%self.width_pavement #748
        self.height_window = root.winfo_screenheight() - self.security_band - (root.winfo_screenheight()-self.security_band)%self.height_pavement #565
        
        self.edge = 50
        
        self.counter_x = floor(self.width_window/2)
        self.counter_y = 70
        
        self.v = 0.3
        
        self.nb_min_beam = 10
        self.nb_max_beam = 25
        self.speed_beam = self.v
        self.speed_max_beam = 2*self.v
        self.gap_btw_beams = 374
        
        self.nb_min_rocket = 2
        self.nb_max_rocket = 4
        self.speed_rocket = 2*self.v
        self.speed_max_rocket = 4*self.v
        self.distance_warning_rocket = 750
        
        self.laser_x = 50
        self.laser_height = 50
        self.speed_laser = self.v
        self.distance_effective_laser = 750
        self.distance_warning_laser = 750
        self.gap_laser = 3
        
        self.nb_min_wall = 5
        self.nb_max_wall = 20
        self.gap_wall = 200
        self.speed_y_max_wall = self.v/2
        self.speed_wall = self.v
        self.speed_max_wall = 2*self.v
        self.gap_btw_walls = self.height_window/2
        
        self.character_x = 65
        self.speed_walker = 20
        self.gravity = self.v
        self.speed_player = self.v


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
        
    def display(self, screen, font, constants):
        screen.blit(font.render(str(self.value),
                                     -1,
                                     (255, 255, 255)),
                                     (constants.counter_x,
                                      constants.counter_y))
        
        
class Beam:
    def __init__(self, x, y, index):
        self.image = [pygame.image.load("assets/beam0.bmp").convert_alpha(),
                      pygame.image.load("assets/beam2.bmp").convert_alpha(),
                      pygame.image.load("assets/beam3.bmp").convert_alpha(),
                      pygame.image.load("assets/beam4.bmp").convert_alpha()]
        for image in self.image:
            image.set_colorkey((0, 0, 0))
            pygame.Surface.convert_alpha(image)
        self.index = index
        self.mask = pygame.mask.from_surface(self.image[self.index])
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,
                                self.y,
                                self.image[index].get_width(),
                                self.image[index].get_height())
        self.increase_score = True
        
    def update(self, Counter, _player, constants, time):
        self.x -= constants.speed_beam*time
        self.rect[0] = self.x
        if ((self.x + self.image[self.index].get_width() < constants.character_x) and (self.increase_score)):
            Counter.update()
            self.increase_score = False
            
    def display(self, screen, _constants):
        screen.blit(self.image[self.index], (self.x, self.y))
            
    
class Rocket:
    def __init__(self, x, y):
        self.image = [pygame.image.load("assets/rocket_warning.bmp").convert_alpha(),
                      pygame.image.load("assets/rocket.bmp").convert_alpha()]
        for image in self.image:
            image.set_colorkey((0, 0, 0))
            pygame.Surface.convert_alpha(image)
        self.mask = pygame.mask.from_surface(self.image[1])
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,
                                self.y,
                                self.image[1].get_width(),
                                self.image[1].get_height())
        
    def update(self, _counter, player, constants, time):
        self.x -= constants.speed_rocket*time
        self.rect[0] = self.x
        if (self.x > constants.width_window):
            self.y = player.y
            self.rect[1] = self.y
            
    def display(self, screen, constants):
        screen.blit(self.image[1], (self.x, self.y))
        if ((self.x > constants.width_window) and (self.x <= constants.width_window + constants.distance_warning_rocket)):
            screen.blit(self.image[0],
                        (constants.width_window - self.image[0].get_width(), self.y))
            
            
class Wall:
    def __init__(self, x, y, direction, speed_y, constants):
        self.image = [pygame.image.load("assets/bottom.bmp").convert_alpha(),
                      pygame.image.load("assets/top.bmp").convert_alpha()]
        for image in self.image:
            image.set_colorkey((0, 0, 0))
            pygame.Surface.convert_alpha(image)
        self.mask = [pygame.mask.from_surface(self.image[0]),
                     pygame.mask.from_surface(self.image[1])]
        self.x = x
        self.y = y
        self.upRect = pygame.Rect(self.x,
                                  constants.height_window/2 + constants.gap_wall/2 + self.y,
                                  self.image[1].get_width(),
                                  self.image[1].get_height())
        self.downRect = pygame.Rect(self.x,
                                    constants.height_window/2 - constants.gap_wall/2 + self.y -self.image[0].get_height(),
                                    self.image[0].get_width(),
                                    self.image[0].get_height())
        self.rect = [self.upRect, self.downRect]
        self.direction = direction
        self.speed_y = speed_y
        self.increase_score = True
        
    def update(self, Counter, _player, constants, time):
        self.x -= constants.speed_wall*time
        self.upRect[0] = self.x
        self.downRect[0] = self.x
        if ((self.x < constants.character_x) and (self.increase_score)) :
            Counter.update()
            self.increase_score = False
        if ((self.y + self.direction*self.speed_y*time <= constants.height_window/2 - constants.gap_wall/2 - 2*constants.edge) and
            (self.y + self.direction*self.speed_y*time >= -(constants.height_window/2 - constants.gap_wall/2 - 2*constants.edge))):
            self.y = self.y + self.direction*self.speed_y*time
        else:
            self.direction = -self.direction
        self.upRect[1] = constants.height_window/2 + constants.gap_wall/2 + self.y
        self.downRect[1] = constants.height_window/2 - constants.gap_wall/2 + self.y -self.image[0].get_height()
        self.rect = [self.upRect, self.downRect]
        
    def display(self, screen, _constants):
        screen.blit(self.image[1], (self.x, self.upRect[1]))
        screen.blit(self.image[0], (self.x, self.downRect[1]))
            
            
class Laser:
    def __init__(self, x, y):
        self.image = [pygame.image.load("assets/laser_off.bmp").convert_alpha(),
                      pygame.image.load("assets/laser_on.bmp").convert_alpha()]
        for image in self.image:
            image.set_colorkey((0, 0, 0))
            pygame.Surface.convert_alpha(image)
        self.mask = pygame.mask.from_surface(self.image[1])
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,
                                self.y,
                                self.image[1].get_width(),
                                self.image[1].get_height())
        
    def update(self, _counter, _player, constants, time):
        self.x -= constants.speed_laser*time
        if (self.x <= constants.distance_effective_laser):
            self.rect[0] = constants.laser_x
            
    def display(self, screen, constants):
        if (self.x <= constants.distance_effective_laser):
            screen.blit(self.image[1], (constants.laser_x, self.y))
        else:
            screen.blit(self.image[0], (constants.laser_x, self.y))
        
        
class Mode_beam:
    def __init__(self, constants):
        self.beams = []
        for i in range(random.randint(constants.nb_min_beam, constants.nb_max_beam)):
            new_beam = Beam(constants.width_window + i*constants.gap_btw_beams,
                            0,
                            random.randint(0, 3))
            new_beam.y = random.randint(constants.edge, constants.height_window - new_beam.image[new_beam.index].get_height() - constants.edge)
            new_beam.rect[1] = new_beam.y
            self.beams.append(new_beam)
        max_x_beam = self.beams[-1].x
        self.rockets = []
        max_x_rocket = 0
        for i in range(random.randint(constants.nb_min_rocket, constants.nb_max_rocket)):
            new_rocket = Rocket(random.randint(floor(constants.speed_rocket/constants.speed_beam)*(constants.width_window + constants.distance_warning_rocket), floor(constants.speed_rocket/constants.speed_beam)*max_x_beam), 0)
            if (new_rocket.x >= max_x_rocket):
                max_x_rocket = new_rocket.x
                self.rockets.append(new_rocket)
            else:
                self.rockets = [new_rocket] + self.rockets
        self.obstacles = self.beams + self.rockets
        self.end = False
        self.next_mode = Mode_wall
        self.next_constants = constants
        if (self.next_constants.speed_beam < self.next_constants.speed_max_beam):
            self.next_constants.speed_beam += self.next_constants.speed_max_beam/10
        if (self.next_constants.speed_rocket < self.next_constants.speed_max_rocket):
            self.next_constants.speed_rocket += self.next_constants.speed_max_rocket/10
        
    def update(self):
        if ((self.beams[-1].x <= -self.beams[-1].image[self.beams[-1].index].get_width()) and
             (self.rockets[-1].x <= -self.rockets[-1].image[1].get_width())):
            self.end = True
            
            
class Mode_wall:
    def __init__(self, constants):
        self.walls = []
        for i in range(random.randint(constants.nb_min_wall, constants.nb_max_wall)):
            self.walls.append(Wall(constants.width_window + i*constants.gap_btw_walls,
                                   random.randint(-floor(constants.height_window/2 - constants.gap_wall/2 - 2*constants.edge), floor(constants.height_window/2 - constants.gap_wall/2 - 2*constants.edge)),
                                   random.choice([-1, 1]),
                                   random.uniform(0, constants.speed_y_max_wall),
                                   constants))
        self.obstacles = self.walls
        self.end = False
        self.next_mode = Mode_laser
        self.next_constants = constants
        if (self.next_constants.speed_wall < self.next_constants.speed_max_wall):
            self.next_constants.speed_wall += self.next_constants.speed_max_wall/10
    
    def update(self):
        if (self.walls[-1].x <= -self.walls[-1].image[0].get_width()):
            self.end = True
            
            
class Mode_laser:
    def __init__(self, constants):
        self.lasers = []
        nb_possible_lasers = floor((constants.height_window - 2*constants.edge)/constants.laser_height)
        gap = random.randint(0, floor((constants.height_window - 2*constants.edge)/constants.laser_height) - constants.gap_laser)
        for i in range(nb_possible_lasers):
            if (i < gap) or (i >= gap + constants.gap_laser):
                self.lasers.append(Laser(constants.distance_warning_laser + constants.distance_effective_laser, constants.edge+i*constants.laser_height))
        self.obstacles = self.lasers
        self.end = False
        self.next_mode = Mode_beam
        self.next_constants = constants
        
    def update(self):
        if (self.lasers[-1].x <= 0):
            self.end = True

        
class Character:
    def __init__(self, x, y):
        self.image = [pygame.image.load("assets/beggining.bmp").convert_alpha(),
                      pygame.image.load("assets/flying.bmp").convert_alpha(),
                      pygame.image.load("assets/dead.bmp").convert_alpha(),
                      pygame.image.load("assets/walk1.bmp").convert_alpha(),
                      pygame.image.load("assets/walk2.bmp").convert_alpha()]
        for image in self.image:
            image.set_colorkey((0, 0, 0))
            pygame.Surface.convert_alpha(image)
        self.mask = pygame.mask.from_surface(self.image[3])
        self.rect = pygame.Rect(x,
                                y,
                                self.image[0].get_width(),
                                self.image[0].get_height())
        self.y = y
        self.up = 0
        self.sprite = 0
        self.state = 0
        self.dead = False

    def update(self, constants, time):
        if ((self.up) and (self.y - constants.speed_player*self.up*time >= constants.edge)):
            self.y -= constants.speed_player*self.up*time
            self.up = 0
        elif (self.up):
            self.y = constants.edge
            self.up = 0
        elif (self.y + constants.gravity*time <= constants.height_window - self.image[0].get_height() - constants.edge):
            self.y += constants.gravity*time
        self.rect[1] = self.y
        
    def display(self, screen, constants, time):
        if self.dead:
            self.sprite = 2
        elif self.up:
            self.sprite = 1
        elif (self.y + constants.gravity*time >= constants.height_window - self.image[0].get_height() - constants.edge):
            if (self.sprite == 4 and self.state == 0):
                self.sprite = 3
                self.state += 1
            elif (self.state == 0):
                self.sprite = 4
                self.state += 1
            elif (self.state == constants.speed_walker):
                self.state = 0
            else:
                self.state += 1
        else:
            self.sprite = 0
        screen.blit(self.image[self.sprite], (constants.character_x, self.y))

        
class Main_menu:
    def __init__(self):
        self.edge_pavement = pygame.image.load("assets/edge_pavement.bmp").convert_alpha()
        self.main_pavement = pygame.image.load("assets/main_pavement.bmp").convert_alpha()
        pygame.font.init()
        self.font = pygame.font.Font('font.ttf',70)
        self.change_window = False
        
    def update(self, screen, clock, constants):
        clock.tick(60)
        self.display(screen, constants)
        keys = check_input()
        if keys[K_SPACE]:
            self.change_window = True
        
    def display(self, screen, constants):
        screen.fill((255, 255, 255))
        make_pavements(screen, constants, self.edge_pavement, self.main_pavement)
        screen.blit(self.font.render(str("TDLOG"),
                                     -1,
                                     (255, 255, 255)),
                                     (constants.width_window/15, constants.height_window/4))
        screen.blit(self.font.render(str("Touch space to"),
                                     -1,
                                     (255, 255, 255)),
                                     (constants.width_window/15, constants.height_window/2))
        screen.blit(self.font.render(str("continue"),
                                     -1,
                                     (255, 255, 255)),
                                     (constants.width_window/15, constants.height_window*3/4))
        pygame.display.update()
            
            
class GameOver:
    def __init__(self, counter):
        self.edge_pavement = pygame.image.load("assets/edge_pavement.bmp").convert_alpha()
        self.main_pavement = pygame.image.load("assets/main_pavement.bmp").convert_alpha()
        pygame.font.init()
        self.font = pygame.font.Font('font.ttf',70)
        self.change_window = False
        self.counter = counter
        self.best_score = Best_score()
        
    def update(self, screen, clock, constants):
        if (self.counter.value > self.best_score.value):
            self.best_score.update(self.counter.value)
        clock.tick(60)
        self.display(screen, constants)
        keys = check_input()
        if keys[K_UP]:
            self.change_window = True
        
    def display(self, screen, constants):
        screen.fill((255, 255, 255))
        make_pavements(screen, constants, self.edge_pavement, self.main_pavement)
        screen.blit(self.font.render(str("Game Over"),
                                     -1,
                                     (255, 255, 255)),
                                     (constants.width_window/8, constants.height_window/4))
        screen.blit(self.font.render("Score: " + str(self.counter.value),
                                     -1,
                                     (255, 255, 255)),
                                     (constants.width_window/8, constants.height_window/2))
        screen.blit(self.font.render("Best score: " + str(self.best_score.value),
                                     -1,
                                     (255, 255, 255)),
                                     (constants.width_window/8, 3*constants.height_window/4))
        pygame.display.update()
        

class Game(object):
    def __init__(self):
        self.edge_pavement = pygame.image.load("assets/edge_pavement.bmp").convert_alpha()
        self.main_pavement = pygame.image.load("assets/main_pavement.bmp").convert_alpha()
        pygame.font.init()
        self.font = pygame.font.Font('font.ttf',70)
        self.change_window = False     
        self.constants = Constants()      
        self.player = Character(self.constants.character_x, self.constants.height_window/2)
        self.mode = Mode_beam(self.constants) 
        self.counter = Counter()
        
    def check_collisions(self, time, test=False):
        if not test:
            for obstacle in self.mode.obstacles:
                if (isinstance(obstacle.mask, list)):
                    for i in range(len(obstacle.mask)):
                        if (obstacle.mask[i].overlap(self.player.mask, (self.player.rect[0] - obstacle.rect[i][0], self.player.rect[1] - obstacle.rect[i][1]))):
                            self.player.dead = True
                else :
                    if (obstacle.mask.overlap(self.player.mask, (self.player.rect[0] - obstacle.rect[0], self.player.rect[1] - obstacle.rect[1]))):
                        self.player.dead = True
            if (self.player.dead and (self.player.y + self.constants.gravity*time >= self.constants.height_window - self.player.image[0].get_height() - self.constants.edge)):
                self.change_window = True
           
    def display(self, screen, time):
        screen.fill((255, 255, 255))
        make_pavements(screen, self.constants, self.edge_pavement, self.main_pavement) 
        for obstacle in self.mode.obstacles:
            obstacle.display(screen, self.constants)
        self.player.display(screen, self.constants, time)
        self.counter.display(screen, self.font, self.constants)
        pygame.display.update()
        
    def update(self, screen, time_loop, test=False):
        keys = check_input()
        if keys[K_UP] and not self.player.dead:
            self.player.up = 1
        pygame.time.delay(1)
        self.display(screen, time_loop)
        if self.mode.end:
            self.constants = self.mode.next_constants
            self.mode = self.mode.next_mode(self.constants) 
        else:
            for obstacle in self.mode.obstacles:
                obstacle.update(self.counter, self.player, self.constants, time_loop)
            self.mode.update()
        self.player.update(self.constants, time_loop)
        self.check_collisions(time_loop, test)
        
        
def main():
    const = Constants()
    screen = pygame.display.set_mode((const.width_window, const.height_window))
    clock = pygame.time.Clock()
    done = False
    time_loop = 0
    while not done:
        main_menu = Main_menu()
        while not main_menu.change_window and not done:
            main_menu.update(screen, clock, const)
            done = done_with_game()
        game = Game()
        while not game.change_window and not done:
            time_before_loop = pygame.time.get_ticks()
            game.update(screen, time_loop)
            time_after_loop = pygame.time.get_ticks()
            time_loop = time_after_loop - time_before_loop
            print(time_loop)
            done = done_with_game()
        gameover = GameOver(game.counter)
        while not gameover.change_window and not done:
            gameover.update(screen, clock, const)
            done = done_with_game()
            
            
class TestMethods(unittest.TestCase):
    
    def test_check_collision(self):
        pygame.init()
        const = Constants()
        pygame.display.set_mode((const.width_window, const.height_window))
        player = Character(0, 0)
        beam_1 = Beam(0, 0, 0)
        self.assertTrue(beam_1.mask.overlap(player.mask, (player.rect[0] - beam_1.rect[0], player.rect[1] - beam_1.rect[1])))
        beam_2 = Beam(player.image[player.sprite].get_width(), player.image[player.sprite].get_height(), 0)
        self.assertFalse(beam_2.mask.overlap(player.mask, (player.rect[0] - beam_2.rect[0], player.rect[1] - beam_2.rect[1])))
        pygame.quit()
        
    def test_game(self):
        pygame.init()
        const = Constants()
        init_const = Constants()
        screen = pygame.display.set_mode((const.width_window, const.height_window))
        game = Game()
        game.mode = Mode_beam(const)
        nb_beams = len(game.mode.beams)
        while not game.mode.end:
            game.update(screen, 1000, test=True)
        self.assertEqual(game.counter.value, nb_beams)
        game.update(screen, 0.001, test=True)
        self.assertEqual(game.constants.speed_beam, init_const.speed_beam + init_const.speed_max_beam/10)
        self.assertEqual(game.constants.speed_rocket, init_const.speed_rocket + init_const.speed_max_rocket/10)
        self.assertTrue(isinstance(game.mode, Mode_wall))
        nb_walls = len(game.mode.walls)
        while not game.mode.end:
            game.update(screen, 1000, test=True)
        self.assertEqual(game.counter.value, nb_beams+nb_walls)
        game.update(screen, 0.001, test=True)
        self.assertEqual(game.constants.speed_wall, init_const.speed_wall + init_const.speed_max_wall/10)
        self.assertTrue(isinstance(game.mode, Mode_laser))
        while not game.mode.end:
            game.update(screen, 1000, test=True)
        self.assertEqual(game.counter.value, nb_beams+nb_walls)
        game.update(screen, 0.001, test=True)
        self.assertTrue(isinstance(game.mode, Mode_beam))
        pygame.quit()
        
                
if __name__ == "__main__":
    pygame.init()
    main()
    pygame.quit()
            

#if __name__ == '__main__':
#    unittest.main()
