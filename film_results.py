import cv2
import time
import numpy as np
import config

def capture_frames(frame_height, frame_width, num_frames, fps, camera=0):
    cap = cv2.VideoCapture(camera)

    if not cap.isOpened():
        raise Exception("Could not open camera")

    delay = 1.0 / fps
    frames = []
    for i in range(num_frames):
        start_time = time.time()

        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        frame = cv2.resize(frame, (frame_height, frame_width))
        frames.append(frame.copy())  # store frame as numpy array (color BGR)

        # wait to maintain FPS
        elapsed = time.time() - start_time
        time_to_wait = max(0, delay - elapsed)
        time.sleep(time_to_wait)

    cap.release()
    return np.array(frames)  # shape: (num_frames, height, width, 3)

frames_array = capture_frames(frame_height=config.DUAL_GRID_SIZE,
                              frame_width=config.DUAL_GRID_SIZE, num_frames=config.NUM_FRAMES, fps=config.FPS)