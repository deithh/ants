
from models import ant
from models import anthill

from config import *

import pygame
import keyboard as kb
import time

#simulation
RUN = True
CLOCK = pygame.time.Clock()
IMG = {}



def load_textures():
    IMG['ant'] = pygame.transform.scale(pygame.image.load('textures/'+'ant'+'.png'), (MUL,MUL))

def window_():
    window = pygame.display.set_mode((SIZE * MUL, SIZE * MUL))
    pygame.display.set_caption("ants")
    window.fill(BLACK)
    return window

def draw(window, anthill, ants):
    anthill.draw(window)
    for ant in ants:
        ant.draw(window, IMG['ant'])

def new (x, anthill):
    x = ant(*SPAWNPOINT, anthill)
    return x

def main():
    global RUN
    load_textures()
    Anthill = anthill(SIZE)
    # Anthill.set_food(0,0,1,100,100)
    # Anthill.set_food(0,0,100,1,100)
    # Anthill.set_food(99,0,1,100,100)
    # Anthill.set_food(0,99,100,1,100)
    Anthill.set_food(10,10,10,10,100)

    ants = [new(i, Anthill) for i in range(ANTS)]
    pygame.init()
    window = window_()


    while RUN:

        pygame.event.get()

        for ant in ants:
            ant.move()
        Anthill.update(ants)

        if kb.is_pressed('esc'):
            pygame.quit()
            RUN = False
        draw(window, Anthill, ants)
        pygame.display.flip()
        CLOCK.tick(FPS)





main()