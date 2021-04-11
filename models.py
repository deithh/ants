from random import randint
import numpy as np
import math
import random

################## config #####################
#map
SIZE = 100
ANTS = 60
MAX_P = 30
#ants
SPAWNPOINT = (SIZE//2, SIZE//2)
P_STRENGTH = 4
RADIUS = 10
#const
BLACK = (0, 0, 0)
ANT_COLOR = (56, 38, 38)
FOOD_COLOR = (255,0,0)
DIRECTIONS = ['N','NE','E','SE', 'S', 'SW', 'W', 'NW']
DIRECTIONS_DICT = {'N' : (0,1),'NE':(1,1),'E': (1,0),'SE':(1,-1), 'S':(0,-1), 'SW':(-1,-1), 'W':(-1,0), 'NW':(-1,1)}

################## config #####################

class ant:
    def __init__(self, x, y):
        global RADIUS
        self.__home = (x, y)
        self.__x = x
        self.__y = y
        self.__backpack = False
        self.__radius = RADIUS
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
        global SIZE
        if not self.__backpack:
            max_ = [0 ,0 ,0]
            for i in range(max(self.__x - self.__radius, 0),min(self.__x + self.__radius, SIZE - 1)):
                for j in range(max(self.__y - self.__radius, 0),min(self.__y + self.__radius, SIZE - 1)):
                    if map[i,j,0]:
                        return i,j
                    elif map[i,j,2] > max_[0]:
                        max_ = [map[i,j,2],i,j]
            if max_[0]:
                return max_[1], max_[2]
        else:
            l = []
            for i in range(max(self.__x - self.__radius, 0),min(self.__x + self.__radius, SIZE - 1)):
                for j in range(max(self.__y - self.__radius, 0),min(self.__y + self.__radius, SIZE - 1)):
                    if map[i,j,1] > 0:
                        if (i, j) == self.__home:
                            return i,j
                        l.append((i,j))
            if len(l)>0:
                return random.choice(l)

    def minimal_path(self, x, y):
        min_ = [float('inf'),0,0]
        for x_ in range(-1,2,1):
            for y_ in range(-1,2,1):
                if math.sqrt((self.__x+x_-x)**2+(self.__y+y_-y)**2) < min_[0]:
                    min_ = [math.sqrt((self.__x+x_-x)**2+(self.__y+y_-y)**2), x_, y_]
        return min_[1], min_[2]

    def grab_food(self, map):
        if not self.__backpack:
            if map[self.__x, self.__y, 0]:
                self.__backpack = True
                map[self.__x, self.__y, 0] -=1

    def leave_food(self):
        if (self.__x, self.__y) == self.__home and self.__backpack:
                self.__backpack = False

    def change_direction(self):
        global DIRECTIONS
        temp = random.randint(-1,1) #direction change left/straigth/right
        if self.__direction + temp > 7:
            self.__direction = 0
        elif self.__direction + temp < 0:
            self.__direction = 7
        else:
            self.__direction += temp


    def move_forward(self, map):
        global DIRECTIONS_DICT, DIRECTIONS
        x, y = DIRECTIONS_DICT[DIRECTIONS[self.__direction]]
        while not self.check_colisions(x, y, map):
            self.change_direction()
            x, y = DIRECTIONS_DICT[DIRECTIONS[self.__direction]]
        self.__x += x
        self.__y += y

    def move(self, map):
        if self.find_target(map):
            x, y = self.minimal_path(*self.find_target(map))
            self.__x += x
            self.__y += y
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
        #trace evaporating
        for x in range(self.size):
            for y in range(self.size):
                if self.map[x, y,1]>1:
                    self.map[x, y,1] -= .3
                else:
                    self.map[x, y,1] = 0
                if self.map[x, y,2]>1:
                    self.map[x, y,2] -= .3
                else:
                    self.map[x, y,2] = 0
                #remove ants
                self.map[x, y, 3] = 0
        #place ants on new cords
        for i in ants:
            x, y = i.cords
            self.map[x, y, 3] += 1
    def set_food(self, x, y, width, height, quantity):
        for i in range(x,x+width):
            for j in range(y, y+width):
                self.map[i, j, 0] = quantity
