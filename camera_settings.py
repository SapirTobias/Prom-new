import numpy as np
import cv2
import time
import config
FRAME_TIME = config.FRAME_TIME_SEC
GRID_SIZE = config.GRID_SIZE
FRAME_COUNT = config.NUM_FRAMES

frames = []
cap = cv2.VideoCapture(0) #defines the camera to use

last_cap_time = 0
frame_cnt = 0
while True:

     ret, frame = cap.read() #read the image
     frame = cv2.resize(frame, (GRID_SIZE, GRID_SIZE))

     current_time = time.time()
     if int(current_time - last_cap_time) > FRAME_TIME:   #if FRAME_TIME seconds passed, update the last time and add the frame to frames
         last_cap_time = current_time
         gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
         frames.append(gray)
         print(f"Captured frame #{len(frames)}")
         frame_cnt += 1

     cv2.imshow('frame',frame)

     if cv2.waitKey(1) & 0xFF == ord('q'):
         break


     if frame_cnt == FRAME_COUNT:
        break

# print all of the frames
for i, frame in enumerate(frames):
    cv2.imshow("Frames Playback", frame)

    print(f"Showing frame {i + 1}")

    if cv2.waitKey(2000) & 0xFF == 27:
         break


cap.release()
cv2.destroyAllWindows()





