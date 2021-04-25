
import numpy as np
import math
import random
import pygame

from scipy.ndimage.filters import gaussian_filter
from config import *
def rotate(image, direction):
    angle = -direction * 45 - 90
    new = pygame.transform.rotate(image, angle)
    return new

class ant:
    def __init__(self, x, y, anthill):
        self.__x = x
        self.__y = y
        self.__backpack = False
        self.__fs = P_STRENGTH
        self.__direction = random.randint(0,7) #pointer to ['N','NE','E','SE', 'S', 'SW', 'W', 'NW']
        self.__anthill = anthill

    def weaken_signal(self):
        self.__fs *= (1-P_WEAK)

    def leave_trace(self):
        if self.__backpack:
            if self.__anthill.map[self.__x, self.__y, 2] + self.__fs < MAX_P:
                self.__anthill.map[self.__x, self.__y, 2] += self.__fs
        else:
            try:
                if self.__anthill.map[self.__x, self.__y, 1] + self.__fs < MAX_P:
                    self.__anthill.map[self.__x, self.__y, 1] += self.__fs
            except :
                print (self.__x)
                print (self.__y)
                raise
        self.weaken_signal()

    def check_colisions(self, x, y):
        #walls colisions
        if self.__x + x < 0 or self.__x + x > self.__anthill.size - 2:
            return False
        if self.__y + y < 0 or self.__y + y > self.__anthill.size - 2:
            return False
        return True

    def find_target(self):

        right = self.cyclometric_direction(self.__direction, 1)

        left = self.cyclometric_direction(self.__direction, -1)


        moves = [DIRECTIONS[self.__direction], DIRECTIONS[left], DIRECTIONS[right]]
        random.shuffle(moves)
        valid = []

        for i, move in enumerate(moves):
            x, y = move
            if self.__anthill.in_nest(self.__x +x, self.__y + y):
                return C_DIRECTIONS[(x, y)]
            if self.check_colisions(x,  y):
                valid.append((x + self.__x, y + self.__y))


        max_ = [0, 0, 0] #x, y, temp max
        if not self.__backpack:

            for x, y in valid:
                if self.__anthill.map[x, y, 0]:

                    return C_DIRECTIONS[(x-self.__x, y-self.__y)]

                if self.__anthill.map[x, y, 2] > max_[2] and self.__anthill.map[x, y, 2] > ANT_SENSE:
                    max_ = [x, y, self.__anthill.map[x, y, 2]]
        else:
            for x, y in valid:
                if self.__anthill.map[x, y, 1] > max_[2]:
                    max_ = [x, y, self.__anthill.map[x, y, 1]]
        if max_[2]:

            return C_DIRECTIONS[(max_[0]-self.__x, max_[1]-self.__y)]

    def grab_food(self, ):

        if not self.__backpack:
            if self.__anthill.map[self.__x, self.__y, 0]:
                self.__backpack = True
                self.__anthill.map[self.__x, self.__y, 0] -=1
                self.change_direction(-4)
                self.__fs = P_STRENGTH

    def leave_food(self):
        if self.__anthill.in_nest(self.__x, self.__y) and self.__backpack:

                self.__backpack = False
                self.change_direction(-4)
                self.__fs = P_STRENGTH
                self.__anthill.food_update(1)

    def change_direction(self, value = 0):

        temp = random.choice([-1,0,1]) #direction change left/straigth/right
        if value:
            temp = value
        self.__direction = self.cyclometric_direction(self.__direction, temp)

    def move_forward(self):

        x, y = DIRECTIONS[self.__direction]
        if not self.check_colisions(x, y):
            self.change_direction(4)
            x, y = DIRECTIONS[self.__direction]
        if not self.check_colisions(x, y):
            self.change_direction(random.choice([1, -1]))
            x, y = DIRECTIONS[self.__direction]
        self.__x += x
        self.__y += y

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
        window.blit(sprite, pygame.Rect(self.__y * MUL + random.randint(-MUL//2, MUL//2), self.__x * MUL+ random.randint(-MUL//2, MUL//2), MUL, MUL))

    @property
    def direction(self):
        return self.__direction

    @property
    def cords(self):
        return (self.__x, self.__y)

    @staticmethod
    def cyclometric_direction(direction, rotation):

        return (direction + rotation) % 8


class anthill:
    def __init__(self, size,):
        #food, backtrack, foodpath, ants
        self.__map = np.full((size+1, size+1, 3), 0.0)
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
        print(self.__food)

    def set_food(self, x, y, width, height, quantity):

        self.__map[x:x+width, y:y+height, 0] = quantity

    def draw_nest(self, window):
        x = self.__nest[0] * MUL
        y = self.__nest[1] * MUL
        pygame.draw.circle(window, NEST_COLOR, (x, y), self.__nest_radius * MUL)

    def draw(self, window):
        for x in range(SIZE):
            for y in range(SIZE):
                color = BLACK
                if self.__map[x,y,0]:
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


