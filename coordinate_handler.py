from win32 import win32gui 
import constants

def get_win_cords():
    hwnd = win32gui.FindWindow(None, constants.GAME_NAME)
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    client_left_top = win32gui.ClientToScreen(hwnd, (left, top))
    client_right_bottom = win32gui.ClientToScreen(hwnd, (right, bottom))
    width = client_right_bottom[0] - client_left_top[0]
    height = client_right_bottom[1] - client_left_top[1]

    if constants.DEBUG:
        print(f"Client Area Coordinates: Left={client_left_top[0]}, Top={client_left_top[1]}, Right={client_right_bottom[0]}, Bottom={client_right_bottom[1]}")
        print(f"Client Area Dimensions: Width={width}, Height={height}")

    constants.WINDOW_LEFT = client_left_top[0]
    constants.WINDOW_TOP = client_left_top[1]
    constants.WINDOW_RIGHT = client_right_bottom[0]
    constants.WINDOW_BOTTOM = client_right_bottom[1]
    constants.WINDOW_WIDTH = width
    constants.WINDOW_HEIGHT = height
