import numpy as np

GRID_SIZE = 256 # Grid that is scaled to the size of the object when lighted
DUAL_GRID_SIZE = 32
BLOCK_SIZE = int(GRID_SIZE / DUAL_GRID_SIZE) # Our "effective" pixel that we light each time
NUM_FRAMES = DUAL_GRID_SIZE ** 2 # We take a photo of the wall for each block we light to get the dual image

FPS = 5 # frames per second
FRAME_TIME_SEC = 1/ FPS
FRAME_TIME_MILLISECOND = int(1000 * FRAME_TIME_SEC)
DELAY = 0.1


WHITE_CONSTANT = 255
BLACK_CONSTANT = 0
GREY_CONSTANT = 122