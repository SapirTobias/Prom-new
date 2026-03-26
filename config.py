import numpy as np

GRID_SIZE = 512 # Grid that is scaled to the size of the object when lighted
DUAL_GRID_SIZE = 64
BLOCK_SIZE = int(GRID_SIZE / DUAL_GRID_SIZE) # Our "effective" pixel that we light each time
NUM_FRAMES = DUAL_GRID_SIZE ** 2 # We take a photo of the wall for each block we light to get the dual image
i_RATIO = 2
j_RATIO = 2

NORM_CONST = 1
WEIGHT_POWER = 2

WHITE_CONSTANT = 255
BLACK_CONSTANT = 0
GREY_CONSTANT = 122

