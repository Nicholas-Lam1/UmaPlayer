from coordinate import pos
import cv2
import pyautogui
import numpy as np
import playsound

def find_start_tool():
    """ Tool to display game area with rectangles at specified positions for reference """
    image = pyautogui.screenshot(region=(pos.WINDOW_LEFT, pos.WINDOW_RIGHT, pos.WINDOW_WIDTH, pos.WINDOW_HEIGHT))
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    position = pos.rel_to_abs(pos.START_WINDOW["START_BUTTON"])

    if len(position) == 4:
        pt1 = (position[0], position[1])
        pt2 = (position[0] + position[2], position[1] + position[3])
        cv2.rectangle(image, pt1, pt2, (0, 255, 0), 2)
    else:
        raise ValueError(f"Unsupported position format: {position}")
    
    cv2.imshow("Start Tool", image)
    playsound.playsound('./wav_files/notification.wav')

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def find_pos_tool():
    """ Tool to display game area with rectangles at specified positions for reference """
    image = pyautogui.screenshot(region=(pos.GAME_LEFT, pos.GAME_TOP, pos.GAME_WIDTH, pos.GAME_HEIGHT))
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    positions = []

    for name, rel in pos.RELATIVE_WINDOWS.items():
        abs_pos = pos.rel_to_abs(rel)
        positions.append(abs_pos)

    for name, rel in pos.RELATIVE_POINTS.items():
        abs_pos = pos.rel_to_abs(rel)
        positions.append(abs_pos)

    for position in positions:
        if len(position) == 4:
            pt1 = (position[0], position[1])
            pt2 = (position[0] + position[2], position[1] + position[3])
            cv2.rectangle(image, pt1, pt2, (0, 255, 0), 2)
        elif len(position) == 2:
            center = (position[0], position[1])
            cv2.circle(image, center, 10, (255, 0, 0), -1)
        else:
            raise ValueError(f"Unsupported position format: {position}")
    
    cv2.imwrite("position_tool.png", image)
    cv2.imshow("Position Tool", image)
    playsound.playsound('./wav_files/notification.wav')

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def reference_pos_tool():
    """ Tool to display game area with eighths grid overlay for reference """
    image = pyautogui.screenshot(region=(pos.GAME_LEFT, pos.GAME_TOP, pos.GAME_WIDTH, pos.GAME_HEIGHT))
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # Draw vertical lines at eighths intervals
    for i in range(1, 8):
        x = int(pos.GAME_WIDTH * i / 8)
        cv2.line(image, (x, 0), (x, pos.GAME_HEIGHT), (0, 0, 255), 1)  

    # Draw horizontal lines at eighths intervals
    for i in range(1, 8):
        y = int(pos.GAME_HEIGHT * i / 8)
        cv2.line(image, (0, y), (pos.GAME_WIDTH, y), (0, 0, 255), 1) 

    cv2.imwrite("reference_tool.png", image)
    cv2.imshow("Reference Tool", image)
    playsound.playsound('./wav_files/notification.wav')

    cv2.waitKey(0)
    cv2.destroyAllWindows()