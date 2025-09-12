from coordinate import pos
import pyautogui
import cv2
import numpy as np
from time import sleep

class Race_Handler():
    def __init__(self):
        self.rp_count = 0

    def auto_race(self):
        self.count_filled_bars()
        if self.rp_count > 0:

    def count_filled_bars(self):
        image = pyautogui.screenshot(region=pos.get_window_from_game("RP_BAR"))
        image = np.array(image)

        # Blue color range (tune if needed)
        lower_blue = np.array([30, 50, 100])   # hue ~90–130 is blue
        upper_blue = np.array([150, 255, 255])

        # Create mask for blue
        mask = cv2.inRange(image, lower_blue, upper_blue)

        # Find contours
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Keep only reasonably sized blobs (filter out noise)
        bar_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 30]

        # Sort by x-position so they’re in order left → right
        bar_contours = sorted(bar_contours, key=lambda c: cv2.boundingRect(c)[0])

        self.rp_count = len(bar_contours)
        print(f"RP Count: {self.rp_count}/5")

    def test_rp_count(self):
        # Example usage
        count, mask = self.count_filled_bars()
        print("Detected blue bars:", count)

        cv2.imshow("Blue Mask", mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
race_handler = Race_Handler()