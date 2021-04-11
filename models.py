from random import randint
import numpy as np
import math
import random
class ant:
    def __init__(self, x, y, mapsize):
        self.__home = (x, y)
        self.__x = x
        self.__y = y
        self.__backpack = False
        self.__fs = 4
        self.__radius = 20
        self.mapsize = mapsize
        self.__max_p = 30

    def leave_trace(self, map):
        if self.__backpack:
            if map[self.__x, self.__y, 2] > self.__max_p:
                pass
            else:
                map[self.__x, self.__y, 2] += self.__fs
        else:
            if map[self.__x, self.__y, 1] > self.__max_p:
                pass
            else:
                map[self.__x, self.__y, 1] += self.__fs

    def check_colisions(self, x, y, map):

        if self.__x + x < 0 or self.__x + x > self.mapsize - 1:
            return False
        if self.__y + y < 0 or self.__y + y > self.mapsize - 1:
            return False
        return True

    def find_target(self, map):
        if not self.__backpack:
            max_ = [0 ,0 ,0]
            for i in range(max(self.__x - self.__radius, 0),min(self.__x + self.__radius, self.mapsize - 1)):
                for j in range(max(self.__y - self.__radius, 0),min(self.__y + self.__radius, self.mapsize - 1)):
                    if map[i,j,0]:
                        return i,j
                    elif map[i,j,2] > max_[0]:
                        max_ = [map[i,j,2],i,j]
            if max_[0]:
                return max_[1], max_[2]
        else:
            l = []
            for i in range(max(self.__x - self.__radius, 0),min(self.__x + self.__radius, self.mapsize - 1)):
                for j in range(max(self.__y - self.__radius, 0),min(self.__y + self.__radius, self.mapsize - 1)):
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

    def move(self, map):
        if self.find_target(map):
            x, y = self.minimal_path(*self.find_target(map))
        else:
            x, y = randint(-1,1), randint(-1,1)
            while not self.check_colisions(x, y, map):
                x, y = randint(-1,1), randint(-1,1)

        self.leave_trace(map)

        #move
        self.__x += x
        self.__y += y
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
