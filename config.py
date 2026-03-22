import numpy as np

GRID_SIZE = 16
# Each value in the grid is log2(grid_height * grid_width) bits long,
# And each bit determines the value of the pixel in a single pattern,
# So this is the number of patterns we need
NUM_PATTERNS = int(np.log2(GRID_SIZE * GRID_SIZE))
FRAME_TIME = 0.02