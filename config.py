import numpy as np

GRID_SIZE = 256
DUAL_GRID_SIZE = 32
BLOCK_SIZE = int(GRID_SIZE / DUAL_GRID_SIZE)

# Each value in the grid is log2(grid_height * grid_width) bits long,
# And each bit determines the value of the pixel in a single pattern,
# So this is the number of patterns we need
NUM_PATTERNS = int(np.log2(GRID_SIZE * GRID_SIZE))
FPS = 20 # 20 frames per second
FRAME_TIME_SEC = 1/ FPS
FRAME_TIME_MILLISEC = int(1000 * FRAME_TIME_SEC)