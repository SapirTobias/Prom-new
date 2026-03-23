import numpy as np
import time


import config
start_time = time.time()



import film_results

frames = film_results.frames_array
print(frames.shape)
print(f"{(time.time() - start_time):.4f} seconds to finish filming frames")

