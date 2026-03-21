import numpy as np
from numpy.f2py.auxfuncs import throw_error

class Grid:

    def __init__(self, grid_width, grid_height, num_row_pixels, num_column_pixels):

        if grid_width >= num_row_pixels and grid_width % num_row_pixels == 0:
            self.grid_width = grid_width
            self.num_row_pixels = num_row_pixels
        else:
            throw_error("grid width must be divisible by pixel width")

        if grid_height >= num_column_pixels and grid_height % num_column_pixels == 0:
            self.grid_height = grid_height
            self.num_column_pixels = num_column_pixels
        else:
            throw_error("grid height must be divisible by pixel height")

        self.grid = np.zeros(grid_height, grid_width)

    def get_num_row_pixels(self):
        return self.num_row_pixels

    def get_num_column_pixels(self):
        return self.num_column_pixels

    def get_grid_width(self):
        return self.grid_width

    def get_grid_height(self):
        return self.grid_height

    def get_pixel_width(self):
        return self.grid_width

    def get_pixel(self, num_pixel_in_row, num_pixel_in_column):
        return np.average(self.grid[num_pixel_in_row:num_pixel_in_row + num_pixel_in_column])

