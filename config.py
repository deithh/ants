#map
SIZE = 100
MUL = 10
ANTS = 200
MAX_P = 255
P_EVAPOR = .008
P_TRAVEL = 0.65


#ants
SPAWNPOINT = (SIZE//2, SIZE//2)
P_STRENGTH = 10
P_WEAK = .075
ANT_SENSE = 1
#colors
BLACK = (0, 0, 0)
ANT_COLOR = (56, 38, 38)
FOOD_COLOR = (255,0,0)
NEST_COLOR = (255, 255, 255)

DIRECTIONS = {0: (0,1), 1: (1,1), 2: (1,0), 3: (1,-1), 4: (0,-1), 5: (-1,-1), 6: (-1,0), 7: (-1,1)}
C_DIRECTIONS ={(0,1): 0, (1,1): 1, (1,0): 2, (1,-1): 3, (0,-1): 4, (-1,-1): 5, (-1,0): 6, (-1,1): 7}
FPS = 30