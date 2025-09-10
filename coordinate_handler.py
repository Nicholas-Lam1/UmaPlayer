from configuration import config
from coordinate import pos
from win32 import win32gui 
import pyautogui
import cv2
import numpy as np

def get_win_cords():
    """ Function to get the window coordinates, ignoring title bar and borders """
    hwnd = win32gui.FindWindow(None, config.GAME_NAME)
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    client_left_top = win32gui.ClientToScreen(hwnd, (left, top))
    client_right_bottom = win32gui.ClientToScreen(hwnd, (right, bottom))
    width = client_right_bottom[0] - client_left_top[0]
    height = client_right_bottom[1] - client_left_top[1]

    if config.DEBUG:
        print(f"Client Area Coordinates: Left={client_left_top[0]}, Top={client_left_top[1]}, Right={client_right_bottom[0]}, Bottom={client_right_bottom[1]}")
        print(f"Client Area Dimensions: Width={width}, Height={height}")

    pos.WINDOW_LEFT = client_left_top[0]
    pos.WINDOW_TOP = client_left_top[1]
    pos.WINDOW_RIGHT = client_right_bottom[0]
    pos.WINDOW_BOTTOM = client_right_bottom[1]
    pos.WINDOW_WIDTH = width
    pos.WINDOW_HEIGHT = height

def find_game_area():
    """ Function to find the game area within the window """
    # Find and set window coordinates
    get_win_cords()
    if config.DEBUG:
        print("Initial Window:", pos.WINDOW_LEFT, pos.WINDOW_TOP,
            pos.WINDOW_RIGHT, pos.WINDOW_BOTTOM,
            pos.WINDOW_WIDTH, pos.WINDOW_HEIGHT)

    # Image left edge of window to find game area
    image = pyautogui.screenshot(region=(
        pos.WINDOW_LEFT,
        pos.WINDOW_TOP,
        pos.WINDOW_WIDTH // 8,
        pos.WINDOW_HEIGHT
    ))

    # Find left edge of game area by detecting vertical line
    image = np.array(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 25, 50)

    if config.DEBUG:
        cv2.imshow("Gray", gray)
        cv2.imshow("Blur", image)
        cv2.imshow("Edges", edges)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    lines = cv2.HoughLinesP(
        edges,
        rho=1,
        theta=np.pi/180,
        threshold=100,
        minLineLength=pos.WINDOW_HEIGHT * 0.99,
        maxLineGap=pos.WINDOW_HEIGHT
    )

    # If a single vertical line is found, set game area coordinates
    if lines is not None and len(lines) == 1:
        x1, y1, x2, y2 = lines[0][0]
        if config.DEBUG:
            print(f"Line: ({x1}, {y1}) to ({x2}, {y2})")
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            print(f"Detected {len(lines)} lines")

        # Ensure the line is vertical, otherwise, line may not be correct (Maybe swap this to a repeat until found?)
        if abs(x1 - x2) > 5:
            raise Exception("Detected line is not vertical.")

        pos.GAME_LEFT = pos.WINDOW_LEFT + int(x1)
        pos.GAME_RIGHT = pos.WINDOW_RIGHT - int(x1)
        pos.GAME_TOP = pos.WINDOW_TOP
        pos.GAME_BOTTOM = pos.WINDOW_BOTTOM
        pos.GAME_WIDTH = int((pos.WINDOW_WIDTH - int(x1 * 2)) // 2)
        pos.GAME_HEIGHT = pos.WINDOW_HEIGHT

    # If no or multiple lines found, raise exception
    else:
        raise Exception("Edge of game area not found.")
        
    if config.DEBUG:
        cv2.imshow("Detected Lines", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

