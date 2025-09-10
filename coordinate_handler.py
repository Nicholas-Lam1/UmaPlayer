from win32 import win32gui 
import pyautogui
import cv2
import numpy as np
import constants as const

def get_win_cords():
    hwnd = win32gui.FindWindow(None, const.GAME_NAME)
    left, top, right, bottom = win32gui.GetClientRect(hwnd)
    client_left_top = win32gui.ClientToScreen(hwnd, (left, top))
    client_right_bottom = win32gui.ClientToScreen(hwnd, (right, bottom))
    width = client_right_bottom[0] - client_left_top[0]
    height = client_right_bottom[1] - client_left_top[1]

    if const.DEBUG:
        print(f"Client Area Coordinates: Left={client_left_top[0]}, Top={client_left_top[1]}, Right={client_right_bottom[0]}, Bottom={client_right_bottom[1]}")
        print(f"Client Area Dimensions: Width={width}, Height={height}")

    const.WINDOW_LEFT = client_left_top[0]
    const.WINDOW_TOP = client_left_top[1]
    const.WINDOW_RIGHT = client_right_bottom[0]
    const.WINDOW_BOTTOM = client_right_bottom[1]
    const.WINDOW_WIDTH = width
    const.WINDOW_HEIGHT = height

def find_game_area():
    get_win_cords()
    if const.DEBUG:
        print("Initial Window:", const.WINDOW_LEFT, const.WINDOW_TOP,
            const.WINDOW_RIGHT, const.WINDOW_BOTTOM,
            const.WINDOW_WIDTH, const.WINDOW_HEIGHT)

    image = pyautogui.screenshot(region=(
        const.WINDOW_LEFT,
        const.WINDOW_TOP,
        const.WINDOW_WIDTH // 8,
        const.WINDOW_HEIGHT
    ))

    image = np.array(image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 25, 50)

    if const.DEBUG:
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
        minLineLength=const.WINDOW_HEIGHT * 0.99,
        maxLineGap=const.WINDOW_HEIGHT
    )

    if lines is not None and len(lines) == 1:
        print(lines[0][0])
        x1, y1, x2, y2 = lines[0][0]
        if const.DEBUG:
            print(f"Line: ({x1}, {y1}) to ({x2}, {y2})")
            cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
            print(f"Detected {len(lines)} lines")
        if abs(x1 - x2) > 5:
            raise Exception("Detected line is not vertical.")

        const.WINDOW_LEFT += int(x1)
        const.WINDOW_RIGHT -= int(x1)
        const.WINDOW_WIDTH -= int(x1 * 2)
        const.WINDOW_WIDTH = int(const.WINDOW_WIDTH / 2)

    else:
        raise Exception("Edge of game area not found.")
        
    if const.DEBUG:
        cv2.imshow("Detected Lines", image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

