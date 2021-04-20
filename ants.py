
from models import *
import pygame
import keyboard as kb
import time




#simulation
RUN = True
CLOCK = pygame.time.Clock()
#colors
BLACK = (0, 0, 0)
ANT_COLOR = (56, 38, 38)
FOOD_COLOR = (255,0,0)



def _window():
    global SIZE, BLACK
    window = pygame.display.set_mode((SIZE*10, SIZE*10))
    pygame.display.set_caption("ants")
    window.fill(BLACK)
    return window

def draw(window, map):
    global SIZE, ANT_COLOR, BLACK
    for x in range(SIZE):
        for y in range(SIZE):
            color = BLACK
            if map[x, y, 3]:
                color = ANT_COLOR
            elif map[x,y,0]:
                color = FOOD_COLOR
            elif map[x,y,1] or map[x,y,2]:
                color = (0, min(map[x,y,1],255),min(map[x, y,2],255))

            if color == ANT_COLOR:
                pygame.draw.rect(window, color, [x*10+3,y*10+3,4,4],0)
            else:
                pygame.draw.rect(window, color, [x*10,y*10,10,10],0)

def new (x):
    global  SPAWNPOINT
    x = ant(*SPAWNPOINT)
    return x
def main():
    global RUN, ANTS, CLOCK

    map = anthill(SIZE)
    map.set_food(0,0,1,100,10)
    map.set_food(0,0,100,1,10)
    map.set_food(99,0,1,100,10)
    map.set_food(0,99,100,1,10)
    #map.set_food(0,0,10,10,10)

    ants = [new(i) for i in range(ANTS)]
    pygame.init()
    window = _window()


    while RUN:

        pygame.event.get()

        for ant in ants:
            ant.move(map.map)
        map.update(ants)

        if kb.is_pressed('esc'):
            pygame.quit()
            RUN = False
        draw(window, map.map)
        pygame.display.flip()
        CLOCK.tick(300)





main()