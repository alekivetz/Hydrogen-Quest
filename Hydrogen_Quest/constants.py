# Game window dimensions
TILE_WIDTH = 40
TILE_HEIGHT = 40
NUM_ROWS = 20
NUM_COLS = 24
SCREEN_WIDTH = NUM_COLS * TILE_WIDTH
SCREEN_HEIGHT = NUM_ROWS * TILE_HEIGHT
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Colors
GREY = (184, 184, 184)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_BLUE = (4, 92, 109)
LIGHT_BLUE = (166, 216, 232)

# Navigation
STOP = 0
UP = 1
DOWN = -1
LEFT = 2
RIGHT = -2

# Text
FUEL = 10
SCORE = 11
SCORE_TXT = 12
PAUSED_TXT = 13

REFUEL_TXT = 14
NO_FUEL_TXT = 15
COLLECT_TXT = 16
SEND_TXT = 17
CONSTRUCTION_TXT = 18

# Entities
MY_VEHICLE = 0
TRUCK = 1
CONV_TRUCK = 2
CAR = 3
CONV_CAR = 4
TAXI = 5
CONV_TAXI = 6
BUS = 7
CONV_BUS = 8
TRAIN = 9
CONV_TRAIN = 10

# Mazes
MAZE_DICT = {
    1: 'maze1.txt',
    2: 'maze2.txt',
    3: 'maze3.txt',
    4: 'maze4.txt',
    5: 'maze5.txt'
}

# Items
POWER_UP = 0
HYDRO = 0
SUPER_HYDRO = 1
ADD_VEHICLE = 3
ADD_STATION = 4
SEND_TRUCK = 5
PYLON = 6

# List of power up types
POWER_UP_TYPES = [HYDRO] + [SUPER_HYDRO] + [ADD_VEHICLE] * 4 + [ADD_STATION] * 4
# Nested list to store types of other vehicles, based on level
VEHICLE_TYPES = [
    [TRUCK],
    [TRUCK, TRUCK, BUS],
    [TRUCK, TRUCK, BUS, TAXI],
    [TRUCK, TRUCK, TAXI, CAR],
    [TRUCK, TRUCK, CAR, TRAIN]
]
