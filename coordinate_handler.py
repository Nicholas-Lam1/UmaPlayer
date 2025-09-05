from win32 import win32gui 
import constants

def get_win_cords():
    hwnd = win32gui.FindWindow(None, constants.GAME_NAME)
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    width = right - left
    height = bottom - top

    if constants.DEBUG:
        print(f"Window Coordinates: Left={left}, Top={top}, Right={right}, Bottom={bottom}")
        print(f"Window Dimensions: Width={width}, Height={height}")

    constants.WINDOW_LEFT = left
    constants.WINDOW_TOP = top
    constants.WINDOW_RIGHT = right
    constants.WINDOW_BOTTOM = bottom
    constants.WINDOW_WIDTH = width
    constants.WINDOW_HEIGHT = height
