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
    height, width, channels = image.shape
    max_pixel_per_channel = np.max(image, axis=(0,1))
    min_pixel_per_channel = np.min(image, axis=(0,1))
    new_image = np.zeros((width, height, channels))
    for k in range(channels):
        # Avoid dividing by zero
        if max_pixel_per_channel[k] == min_pixel_per_channel[k]:
            new_image[::k] = max_pixel_per_channel[::k]

        for i in range(height):
            for j in range(width):
                new_image[i,j, k] = WHITE_CONSTANT * (image[i, j, k] - min_pixel_per_channel[k]) / (max_pixel_per_channel[k] - min_pixel_per_channel[k])

    return new_image

def second_normalize(image):
    height, width = image.shape

    new_image = np.zeros((width, height))
    images = []
    for n in range(5):
        for i in range(height):
            for j in range(width):
                for k in range(3):
                    new_image[i,j,k] = image[i,j,k] + (width - j) * (n/10)
        images.append(new_image)
    return images


def image_weights(image):
    height, width = image.shape

    max_pixel = np.max(image)
    y0, x0 = np.unravel_index(np.argmax(image), image.shape)

    y, x = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
    dist = np.sqrt((x - x0) ** 2 + (y - y0) ** 2)

    sigma = None
    if sigma is None:
        sigma = width / 4
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

    mean_brightnesses = []

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

        weights = image_weights(frame)
        # Check before averaging
        if np.sum(weights) > 0:
            mean_brightness = np.average(frame, weights=weights)
        else:
            mean_brightness = np.mean(frame)  # Fallback to a normal average

        # Handle synchronization
        next_frame_event.set() # tell presenter it can present the next frame


    cap.release()
    queue.put(np.array(mean_brightnesses))


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

    dual_image = output_queue.get().reshape((config.DUAL_GRID_SIZE, config.DUAL_GRID_SIZE, 3))

    # Ensures the main program waits for the processes to finish before exiting
    show_patterns_process.join()
    capture_frames_process.join()

    new_dual = normalize_image(dual_image)
    new_dual_image = second_normalize(new_dual)
    print("dual image:")
    print(new_dual)
    print(new_dual_image)

    print(f"total time: {time.time() - start_time} seconds")


