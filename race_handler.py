from coordinate import pos
import pyautogui
import cv2
import numpy as np
import matplotlib

def count_filled_bars(image_path):
    # Load image
    image = pyautogui.screenshot(region=pos.get_window_from_game("RP_BAR"))
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Blue color range (tune if needed)
    lower_blue = np.array([90, 80, 80])   # hue ~90–130 is blue
    upper_blue = np.array([130, 255, 255])

    # Create mask for blue
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Keep only reasonably sized blobs (filter out noise)
    bar_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 30]

    # Sort by x-position so they’re in order left → right
    bar_contours = sorted(bar_contours, key=lambda c: cv2.boundingRect(c)[0])

    return len(bar_contours), mask

# Example usage
count, mask = count_filled_bars("1a853e10-d644-4da8-995a-438e22239ba0.png")
print("Detected blue bars:", count)

cv2.imshow("Blue Mask", mask)
cv2.waitKey(0)
cv2.destroyAllWindows()