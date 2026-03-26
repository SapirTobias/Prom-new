import numpy as np
import cv2
import pyautogui
from multiprocessing import Process, Event, Queue
import time
import config
import create_patterns

WHITE_CONSTANT = config.WHITE_CONSTANT
WEIGHT_POWER = config.WEIGHT_POWER
NORM_CONST = config.NORM_CONST
start_time = time.time()


def normalize_image(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    v = hsv[:, :, 2].astype(np.float32)
    v_min, v_max = v.min(), v.max()

    if v_max == v_min:
        return image.copy()
    v = WHITE_CONSTANT * (v - v_min) / (v_max - v_min)
    hsv[:, :, 2] = v.astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

def second_normalize(image):
    height, width, channels = image.shape

    new_image = np.zeros((height, width, channels))
    images = []
    for n in range(5):
        new_image = np.zeros((height, width, channels))
        for i in range(height):
            for j in range(width):
                for k in range(3):
                    new_image[i,j,k] = int(image[i,j,k] + (width - j) * (n/8.00))
        images.append(new_image)
    return images


def image_weights(frame, sigma=None):
    # Ensure frame is float to prevent overflow during arithmetic
    frame_float = frame.astype(float)

    # Step 1: Calculate brightness
    # (Coefficients suggest the input is in BGR format, standard for OpenCV)
    brightness = 0.114 * frame_float[:, :, 0] + 0.587 * frame_float[:, :, 1] + 0.299 * frame_float[:, :, 2]

    # Step 2: Find the brightest pixel coordinates (row, col)
    y0, x0 = np.unravel_index(np.argmax(brightness), brightness.shape)

    # Step 3: Create distance map
    height, width = brightness.shape
    # indexing='ij' ensures 'y' maps to rows (height) and 'x' maps to cols (width)
    y, x = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
    dist = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)

    # Step 4: Calculate Gaussian weights
    if sigma is None:
        sigma = width / 4.0

    weights = np.exp(-dist ** 2 / (2 * sigma ** 2))

    return weights

def present_patterns(frame_ready_event, next_frame_event, stop_event, patterns):

    screen_width, screen_height = pyautogui.size()
    pattern_height, pattern_width = np.shape(patterns[0]) # All patterns have the same shape

    # Set background to full black screen
    canvas = np.zeros((screen_height, screen_width), np.uint8)
    cv2.namedWindow("Full Screen Patterns", cv2.WINDOW_NORMAL)
    cv2.setWindowProperty("Full Screen Patterns", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    # Show patterns
    for i, pattern in enumerate(patterns):

        print(f"showing pattern: {i} whose max pixel is {np.max(pattern)}")
        # Show pattern
        canvas[screen_height - pattern_height:, screen_width - pattern_width:] = pattern
        cv2.imshow("Full Screen Patterns", canvas)
        key = cv2.waitKey(1)
        time.sleep(0.02)  # small fixed delay for screen refresh

        # Stop all if clicked q
        if key == ord('q'):
            frame_ready_event.set() # So the film frames stops waiting
            stop_event.set() # So the film frames will end
            break

        # Handle synchronization
        frame_ready_event.set() # tell filmer that the frame is ready to be captured
        next_frame_event.wait() # wait for the filmer to approve moving on to present next frame
        next_frame_event.clear() #  so at the next iteration it waits for the signal again

    cv2.destroyAllWindows()


def film_frames(frame_ready_event, next_frame_event, stop_event, frame_height, frame_width, num_frames, queue, camera=0):

    # Get camera
    cap = cv2.VideoCapture(camera)
    if not cap.isOpened():
        raise Exception("Could not open camera")

    for i in range(5):
        ret, wall = cap.read()

    # Change filmed frame to the desired size, and convert to greyscale and weight by brightness level
    wall = cv2.resize(wall, (frame_height, frame_width))  # shape = (frame_height, frame_width, 3)

    # camera films in rgb and we cv2 uses as bgr
    wall = cv2.cvtColor(wall, cv2.COLOR_RGB2BGR)

    # After filming wall, Handle synchronization - return to presenting the next patterns
    next_frame_event.set()

    mean_brightness_list = []
    # Film frames
    for i in range(num_frames):

        # Handle synchronization
        if stop_event.is_set():
            break
        frame_ready_event.wait() # wait until presenter shows the frame
        frame_ready_event.clear() # so at the next iteration it waits for the signal again

        print("Filmed frame #{}".format(i))

        # Film frame
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        # Change filmed frame to the desired size, and convert to greyscale and weight by brightness level
        frame = cv2.resize(frame, (frame_height, frame_width))
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        frame = cv2.subtract(frame, wall)

        weights = image_weights(frame)
        # Check before averaging
        if np.sum(weights) > 0:
            # Result is an array of 3 values: [blue_mean, green_mean, red_mean]
            frame_mean = np.average(frame, weights=weights, axis=(0,1))
        else:
            frame_mean = np.mean(frame, axis=(0, 1))

        mean_brightness_list.append(frame_mean)

        # Handle synchronization
        next_frame_event.set()

    cap.release()
    queue.put(np.array(mean_brightness_list))

if __name__ == '__main__':
    frame_ready = Event()
    next_frame = Event()
    stop = Event()
    output_queue = Queue()

    show_patterns_process = Process(target=present_patterns,
                                    args=(frame_ready, next_frame, stop, create_patterns.patterns))
    capture_frames_process = Process(target=film_frames,
                                     args=(frame_ready, next_frame, stop, config.DUAL_GRID_SIZE,
                                           config.DUAL_GRID_SIZE, config.NUM_FRAMES, output_queue,1))

    # Starts the processes without blocking the continuation of the main code
    show_patterns_process.start()
    capture_frames_process.start()

    dual_image = output_queue.get().reshape((config.DUAL_GRID_SIZE, config.DUAL_GRID_SIZE, 3)).astype(np.uint8)

    # Ensures the main program waits for the processes to finish before exiting
    show_patterns_process.join()
    capture_frames_process.join()

    #new_dual = normalize_greyscale_image(cv2.cvtColor(dual_image, cv2.COLOR_BGR2GRAY))
    new_dual = normalize_image(dual_image)
    new_dual_image = second_normalize(new_dual)

    print("dual image:")
    print(new_dual)
    #print(new_dual_image)

    print(f"total time: {time.time() - start_time} seconds")


