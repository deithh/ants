
from models import *
import pygame
import keyboard as kb
import time


#simulation
RUN = True
CLOCK = pygame.time.Clock()

def _window():
    global SIZE, BLACK
    window = pygame.display.set_mode((SIZE*10, SIZE*10))
    pygame.display.set_caption("ants")
    window.fill(BLACK)
    return window

def draw(window, map):
    global SIZE, ANT_COLOR
    for x in range(SIZE):
        for y in range(SIZE):
            color = (0,0,0)
            if map[x, y, 3]:
                color = ANT_COLOR
            elif map[x,y,0]:
                color = FOOD_COLOR
            elif map[x,y,1] or map[x,y,2]:
                color = (0, min(map[x,y,1], 30),min(map[x, y,2],130))


            pygame.draw.rect(window, color, [x*10+1,y*10+1,8,8],0)

def new (x):
    global  SPAWNPOINT
    x = ant(*SPAWNPOINT)
    return x
def main():
    global RUN, ANTS, CLOCK
    map = anthill(SIZE)
    map.set_food(10,10,5,5,10)

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
        CLOCK.tick(30)







main()