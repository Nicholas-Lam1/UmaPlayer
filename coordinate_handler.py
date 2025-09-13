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

    pos.WINDOW_LEFT = int(client_left_top[0])
    pos.WINDOW_TOP = int(client_left_top[1])
    pos.WINDOW_RIGHT = int(client_right_bottom[0])
    pos.WINDOW_BOTTOM = int(client_right_bottom[1])
    pos.WINDOW_WIDTH = int(width)
    pos.WINDOW_HEIGHT = int(height)

def find_game_area():
    """ Function to find the game area within the window """
    # Find and set window coordinates
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

    if config.DEBUG:
        cv2.imshow("Gray", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    edges = []
    for i in range(10, gray.shape[0], int((gray.shape[0] - 20) / 8)):       # If the pin button is hit, can move the starting point down below it
        prev_pixel = None
        for j in range(0, len(gray[i])):
            if prev_pixel == None:
                prev_pixel = gray[i][j]
                continue
            if config.GAME_EDGE_THRESH <= (delta := int(prev_pixel) - int(gray[i][j])):       
                edges.append((j, i, delta))
                if config.DEBUG:
                    cv2.circle(gray, (j, i), 5, (0, 0, 255), -1)  
                break
            prev_pixel = gray[i][j]
        if config.DEBUG:
            cv2.line(gray, (0, i), (len(gray[i]), i), (0, 255, 0), 1)  

    if config.DEBUG:
        cv2.imshow("Checked Lines", gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()   

    if edges:
        sum_x = sum(x for x, y, d in edges)
        avg_x = int(sum_x / len(edges))

        for x, y, d in edges:
            if abs(x - avg_x) > 5:
                print("Detected line is not vertical.")
                return False
            
        if config.DEBUG:
            print(f"Line: ({edges[0][0]}, {edges[0][1]}) to ({edges[-1][0]}, {edges[-1][1]})")
            cv2.line(gray, (edges[0][0], edges[0][1]), (edges[-1][0], edges[-1][1]), (0, 255, 0), 2)
            print(f"Detected line")            
        
        pos.GAME_LEFT_OFFSET = avg_x
        pos.GAME_TOP_OFFSET = 0
        pos.GAME_LEFT = int(pos.WINDOW_LEFT + avg_x)
        pos.GAME_RIGHT = int(pos.WINDOW_RIGHT - avg_x)
        pos.GAME_TOP = int(pos.WINDOW_TOP)
        pos.GAME_BOTTOM = int(pos.WINDOW_BOTTOM)
        pos.GAME_WIDTH = int((pos.WINDOW_WIDTH - int(avg_x * 2)) // 2)
        pos.GAME_HEIGHT = int(pos.WINDOW_HEIGHT)

    else:
        print("Edge of game area not found.")
        return False

    if config.DEBUG:
        cv2.imshow("Found Edge", gray)
        cv2.waitKey(0)
        cv2.destroyAllWindows()  

    return True