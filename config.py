import numpy as np

GRID_SIZE = 512
# Each value in the grid is log2(grid_height * grid_width) bits long,
# And each bit determines the value of the pixel in a single pattern,
# So this is the number of patterns we need
NUM_PATTERNS = int(np.log2(GRID_SIZE * GRID_SIZE))
FRAME_TIME_SEC = 3 # how long a frame is shown / captured
FRAME_TIME_MILLISEC = 1000 * FRAME_TIME_SEC