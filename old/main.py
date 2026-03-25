import multiprocessing
import os
import time

def run_script1():
    os.system('python show_patterns.py')


def run_script2():
    os.system('python build_dual_image.py')


if __name__ == '__main__':
    p1 = multiprocessing.Process(target=run_script1)
    p2 = multiprocessing.Process(target=run_script2)

    p1.start()
    p2.start()

    p1.join()
    p2.join()
