from configuration import config
from coordinate import pos
from rand_adjust import rand_move_type
import cv2
import pyautogui
import numpy as np
import easyocr
from time import monotonic
import math

class Screen_Reader():
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=False)

    def screenshot(self, position):
        image = pyautogui.screenshot(region=position)
        image = np.array(image)
        return image

    def find_text_at_position(self, position, text=None, timeout=None):
        end_time = None if timeout is None else monotonic() + timeout
        while end_time is None or monotonic() < end_time:
            if config.DEBUG:
                print("Taking screenshot...")
                print(f"Position: {position}")

            image = self.screenshot(position)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            result = self.reader.readtext(image)

            for detection in result:
                if config.DEBUG:
                    print("Detected text:", detection[1])
                if text is None or text.lower() in detection[1].lower():
                    points = detection[0]
                    x_val = [pt[0] for pt in points]
                    y_val = [pt[1] for pt in points]
                    center_x = int(sum(x_val) / 4) + position[0]
                    center_y = int(sum(y_val) / 4) + position[1]
                    return [center_x, center_y]

        if config.DEBUG:
            print("No matching text found")
            for detection in result:
                print("Detected text:", detection[1])
            cv2.imshow("Text Detection", image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
        return None

    def click(self, position, text=None):
        dist = math.hypot(pyautogui.position().x - position[0], pyautogui.position().y - position[1])
        time = dist / config.PIX_SEC_RATIO
        pyautogui.moveTo(position[0], position[1], time, rand_move_type())
        pyautogui.click()
        if text is not None:
            print(f"Clicked on text: {text} at ({position[0]}, {position[1]})")
        else:
            print(f"Clicked at ({position[0]}, {position[1]})")

    def click_and_find(self, button_key, window_key, expected_text):
        ''' Click until the expected text is found to confirm menu change '''
        while not screen_reader.find_text_at_position(position=pos.get_window_from_game(window_key), text=expected_text) is not None:
            screen_reader.click(pos.get_point_from_game(button_key), expected_text)

screen_reader = Screen_Reader()