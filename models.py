import numpy as np
import math
import random
import pygame

from scipy.ndimage.filters import gaussian_filter
from config import *


############# functions ###############

def rotate(image, direction):
    angle = math.degrees(direction)
    new = pygame.transform.rotate(image, angle)
    return new

#######################################

class ant:
    def __init__(self, anthill, x = 0, y = 0):
        self.__x = x
        self.__y = y
        self.__backpack = False
        self.__fs = PHEROMONE_STRENGTH
        self.__direction = random.uniform(0, 2 * math.pi)
        self.__anthill = anthill

    def check_colisions(self, x, y):
        #walls colisions
        if self.__x + x < 0 or self.__x + x > self.__anthill.size:
            return False
        if self.__y + y < 0 or self.__y + y > self.__anthill.size:
            return False
        if self.__anthill.map[math.floor(self.__x + x),math.floor(self.__y + y), 3]:
            return False
        return True

    def weaken_signal(self):
        self.__fs *= (1-P_WEAK)

    def grab_food(self):
        if not self.__backpack:
            if self.__anthill.map[self.cord_x, self.cord_y, 0]:
                self.__backpack = True
                self.__anthill.map[self.cord_x, self.cord_y, 0] -=1
                self.change_direction(math.pi)
                self.__fs = PHEROMONE_STRENGTH

    def leave_food(self):
        if self.__anthill.in_nest(self.__x, self.__y) and self.__backpack:
                self.__backpack = False
                self.change_direction(math.pi)
                self.__fs = PHEROMONE_STRENGTH
                self.__anthill.food_update(1)

    def change_direction(self, angle = 0):
        if not angle:
            angle = random.uniform(-FOV, FOV)
        self.__direction = self.cyclometric_angle(self.__direction, angle)

    def calc_move(self):

        y = math.sin(self.__direction)
        x = math.cos(self.__direction)

        return (x,y)

    def move_forward(self):

        x, y = self.calc_move()

        if not self.check_colisions(x, y):
            self.change_direction(math.pi)
            x, y = self.calc_move()
        while not self.check_colisions(x, y):
            self.change_direction(random.uniform(0,2*math.pi))
            x, y = self.calc_move()

        self.__x += x
        self.__y += y

    def leave_trace(self):
        if self.__backpack:
            if self.__anthill.map[self.cord_x, self.cord_y, 2] + self.__fs < MAX_P:
                self.__anthill.map[self.cord_x, self.cord_y, 2] += self.__fs
        else:
            if self.__anthill.map[self.cord_x, self.cord_y, 1] + self.__fs < MAX_P:
                self.__anthill.map[self.cord_x, self.cord_y, 1] += self.__fs
        self.weaken_signal()

    def find_target(self):

        angles = [
                    self.cyclometric_angle(self.__direction, -(1/8)* 2 * math.pi),
                    self.cyclometric_angle(self.__direction,  (1/8)* 2 * math.pi),
                    self.__direction
                   ]
        random.shuffle(angles)

        valid = []
        for angle in angles:
            x, y = math.cos(angle), math.sin(angle)
            if self.check_colisions(x, y):
                valid.append(angle)

        max_ = 0
        max_a = None
        for angle in valid:
            x, y = math.floor(math.cos(angle) + self.__x), math.floor(math.sin(angle) + self.__y)
            if self.__anthill.map[x, y, 0] and not self.__backpack:
                return angle
            if self.__anthill.in_nest(x, y) and self.__backpack:
                return angle
            if self.__anthill.map[x, y, 2 - self.__backpack] > max_:
                max_ = self.__anthill.map[x, y, 2 - self.__backpack]
                max_a = angle

        if max_ > ANT_SENSE:
            return max_a


    def move(self):

        if self.find_target():
            self.__direction = self.find_target()
            self.move_forward()

        else:
            self.move_forward()
            self.change_direction()

        self.leave_trace()
        self.grab_food()
        self.leave_food()

    def draw(self, window, texture):
        sprite = rotate(texture, self.__direction)
        window.blit(sprite, pygame.Rect(self.__y * MUL, self.__x * MUL, MUL, MUL))

    @property
    def direction(self):
        return self.__direction

    @property
    def cord_x(self):
        return math.floor(self.__x)

    @property
    def cord_y(self):
        return math.floor(self.__y)

    @staticmethod
    def cyclometric_angle(direction, angle):
        return (direction + angle) % (2 * math.pi)

class anthill:
    def __init__(self, size):
        #food, backtrack, foodpath, ants
        self.__map = np.full((size+1, size+1, 4), 0.0)
        self.__size = size
        self.__frame = 0
        self.__nest = (size//2, size//2)
        self.__nest_radius = 5
        self.__food = 0

    def update(self, ants):

        #trace evaporating
        self.__map[:, :, 1:3] *= (1-P_EVAPOR)
        if self.__frame % 5 == 0:
            self.__map[:,:, 1] = gaussian_filter(self.__map[:,:, 1], P_TRAVEL)
            self.__map[:,:, 2] = gaussian_filter(self.__map[:,:, 2], P_TRAVEL)



        self.__frame+=1

    def set_food(self, x, y, width, height, quantity):

        self.__map[x:x+width, y:y+height, 0] = quantity

    def set_rocks(self, x, y, width, height):

        self.__map[x:x+width, y:y+height, 3] = 1

    def draw_nest(self, window):
        x = self.__nest[0] * MUL
        y = self.__nest[1] * MUL
        pygame.draw.circle(window, NEST_COLOR, (x, y), self.__nest_radius * MUL)

    def draw(self, window):
        for x in range(SIZE):
            for y in range(SIZE):
                color = BLACK
                if self.__map[x, y, 3]:
                    color = (30, 30, 30)
                elif self.__map[x,y,0]:
                    color = FOOD_COLOR
                elif self.__map[x,y,1] or self.__map[x,y,2]:
                    color = (0, min(self.__map[x,y,1],255),min(self.__map[x, y,2],255))
                pygame.draw.rect(window, color, [y * MUL,x * MUL, MUL, MUL],0)
        self.draw_nest(window)

    @property
    def map(self):
        return self.__map

    @property
    def size(self):
        return self.__size

    def food_update(self, value = 1):
        self.__food +=1

    def in_nest(self, ax, ay): #ant x, y cords
        nx, ny = self.__nest #nest x, y cords
        if math.sqrt((nx - ax)**2 + (ny - ay)**2) < self.__nest_radius:
            return True

        return False