import numpy as np
import matplotlib.pyplot as plt
import cv2 as cv
import PIL

def get_binary_digit(length, i):
    mask = np.zeros(length)
    mask[i] = 1
    return mask

grid_width = 4
grid_height = 4

grid = np.arange(grid_width * grid_height, dtype = int).reshape(grid_width, grid_height)
convert_to_binary = np.vectorize(lambda x: format(x, 'b'))
binary_grid = convert_to_binary(grid)

print(binary_grid)

# Each value in the grid is log2(grid_height * grid_width) bits long,
# And each bit determines the value of the pixel in a single pattern,
# So this is the number of patterns we need
num_patterns = np.log2(grid_height * grid_width)
patterns = []
for i in range(num_patterns):
    pattern = np.vectorize(get_binary_digit)












