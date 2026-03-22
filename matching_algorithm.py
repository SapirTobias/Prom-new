import cv2
import numpy as np

import config
import camera_settings as camera_settings
import create_patterns as create_patterns
from camera_settings import GRID_SIZE

BLACK_CONSTANT = 0
WHITE_CONSTANT = 1
FRAME_COUNT = camera_settings.FRAME_COUNT


patterns = create_patterns.patterns
frames = camera_settings.frames
#This function returns the weighted average between all of the frames in the current index
def weighted_avg(index):
    pattern_i_j = [pattern[index[0]][index[1]] for pattern in patterns] #list with all of the patterns in the index place
    frames_i_j = [frame[index[0]][index[1]] for frame in frames] #list of all the frames in index position

    sum = 0
    white_cnt = 0
    for i in range(len(pattern_i_j)):
        if(pattern_i_j[i] == WHITE_CONSTANT):
            sum += frames_i_j[i]
            white_cnt += 1

    return sum/white_cnt

threshold = 123
match_mat = [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        for l in range(GRID_SIZE):
            for m in range(GRID_SIZE):
                for k, frame in enumerate(frames):
                    if (frame[l,m] < threshold and patterns[k][i][j] == 1) or (frame[l,m] >= threshold and patterns[k][i][j] == 0):
                        break
                match_mat[i][j] = (l,m)



dual_image = np.zeros((GRID_SIZE, GRID_SIZE), dtype=np.uint8)

for i in range(GRID_SIZE):
    for j in range(GRID_SIZE):
        dual_image[i][j] = weighted_avg(match_mat[i][j])

cv2.imshow("dual_image", dual_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
