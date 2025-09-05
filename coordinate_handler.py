from win32 import win32gui 
from constants import *

def get_win_cords(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    if DEBUG:
        print(f"Window Coordinates: Left={left}, Top={top}, Right={right}, Bottom={bottom}")
        print(f"Window Dimensions: Width={width}, Height={height}")

    return left, top, width, height
