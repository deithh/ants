from random import randint
import numpy as np
import math
import random

################## config #####################
#map
SIZE = 150
ANTS = 500
MAX_P = 255
P_EVAPOR = .05
#ants
SPAWNPOINT = (SIZE//2, SIZE//2)
P_STRENGTH = 6

################## config #####################

DIRECTIONS = {0: (0,1), 1: (1,1), 2: (1,0), 3: (1,-1), 4: (0,-1), 5: (-1,-1), 6: (-1,0), 7: (-1,1)}

class ant:
    def __init__(self, x, y):
        global RADIUS
        self.__home = (x, y)
        self.__x = x
        self.__y = y
        self.__backpack = False

        self.__direction = random.randint(0,7) #pointer to ['N','NE','E','SE', 'S', 'SW', 'W', 'NW']

    def leave_trace(self, map):
        global MAX_P
        if self.__backpack:
            if map[self.__x, self.__y, 2] > MAX_P:
                pass
            else:
                map[self.__x, self.__y, 2] += P_STRENGTH
        else:
            if map[self.__x, self.__y, 1] > MAX_P:
                pass
            else:
                map[self.__x, self.__y, 1] += P_STRENGTH

    def check_colisions(self, x, y, map):
        global SIZE

        if self.__x + x < 0 or self.__x + x > SIZE - 1:
            return False
        if self.__y + y < 0 or self.__y + y > SIZE - 1:
            return False
        return True

    def find_target(self, map):
        global SIZE, DIRECTIONS
        moves = [DIRECTIONS[self.__direction]] #<<<<<<<<<
        valid = []
        for i, move in enumerate(moves):
            x, y = move
            if self.check_colisions(x + self.__x, y + self.__y, map):
                valid.append((x + self.__x, y + self.__y))


        max_ = [0, 0, 0] #x, y, temp max
        if not self.__backpack:

            for x, y in valid:
                if map[x, y, 0]:

                    return x, y

                if map[x, y, 2] > max_[2]:
                    max_ = [x, y, map[x, y, 2]]
        else:
            for x, y in valid:
                if map[x, y, 1] > max_[2]:
                    max_ = [x, y, map[x, y, 1]]
        if max_[2]:

            return max_[0], max_[1]



    def grab_food(self, map):
        if not self.__backpack:
            if map[self.__x, self.__y, 0]:
                self.__backpack = True
                map[self.__x, self.__y, 0] -=1
                self.change_direction(4)


    def leave_food(self):
        if (self.__x, self.__y) == self.__home and self.__backpack:
                self.__backpack = False
                self.change_direction(4)

    def change_direction(self, value = 0):

        temp = random.randint(-1,1) #direction change left/straigth/right
        if value:
            temp = value

        if self.__direction + temp > 7:
            self.__direction = 0
        elif self.__direction + temp < 0:
            self.__direction = 7
        else:
            self.__direction += temp



    def move_forward(self, map):
        global  DIRECTIONS
        x, y = DIRECTIONS[self.__direction]
        while not self.check_colisions(x, y, map):
            self.change_direction()
            x, y = DIRECTIONS[self.__direction]
        self.__x += x
        self.__y += y

    def move(self, map):
        if self.find_target(map):
            x, y = self.find_target(map)
            self.__x = x
            self.__y = y

        else:
            self.move_forward(map)

        self.change_direction()
        self.leave_trace(map)
        self.grab_food(map)
        self.leave_food()

    @property
    def cords(self):
        return (self.__x, self.__y)


class anthill:
    def __init__(self, size):
        #food, backtrack, foodpath, ants
        self.map = np.full((size, size, 4), 0.0)
        self.size = size


    def update(self, ants):
        global P_EVAPOR

        #trace evaporating
        self.map[:, :, 1:3] *= (1-P_EVAPOR)
        #remove ants
        self.map[:, :, 3] = 0

        #place ants on new cords
        for i in ants:
            x, y = i.cords
            self.map[x, y, 3] += 1

    def set_food(self, x, y, width, height, quantity):

        self.map[x:x+width, y:y+height, 0] = quantity
