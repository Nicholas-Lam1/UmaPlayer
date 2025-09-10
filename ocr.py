from configuration import config
from coordinate import pos
import cv2
import pyautogui
import numpy as np
import easyocr
import time
import playsound

textDetectorEAST= cv2.dnn_TextDetectionModel_EAST(config.MODEL_PATH)
textDetectorEAST.setConfidenceThreshold(config.CONF_THRESH)
textDetectorEAST.setNMSThreshold(config.NMS_THRESH)
textDetectorEAST.setInputParams(config.SCALE, config.INPUT_SIZE, config.MEAN, config.SWAP_RB)

reader = easyocr.Reader(['en'], gpu=False)

def find_text(text = None):
    start_time = time.time()
    while time.time() - start_time < 10:
        if config.DEBUG:
            print("Taking screenshot...")

        image = pyautogui.screenshot(region=(pos.WINDOW_LEFT, pos.WINDOW_TOP, pos.WINDOW_WIDTH, pos.WINDOW_HEIGHT))
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        image_copy = cv2.resize(image, (config.INPUT_SIZE))
        boxes, confidences = textDetectorEAST.detect(image_copy)

        if config.DEBUG:
            print(f"Detected {len(boxes)} text boxes")

        scale_x = pos.WINDOW_WIDTH / pos.INPUT_SIZE[0]
        scale_y = pos.WINDOW_HEIGHT / pos.INPUT_SIZE[1]

        for box in boxes:
            scaled_box = np.array([[int(pt[0] * scale_x), int(pt[1] * scale_y)] for pt in box], dtype=np.int32)
            if config.DEBUG:
                print(f"Box Coordinates: {scaled_box}")
                cv2.polylines(image, [scaled_box], True, (0, 255, 0), 2)

            x, y, w, h = cv2.boundingRect(scaled_box)
            roi = image[y:y+h, x:x+w]

            if roi.size == 0:
                if config.DEBUG:
                    print(f"Skipped empty ROI at ({x}, {y}, {w}, {h})")
                continue

            result = reader.readtext(roi)
            for detection in result:
                if config.DEBUG:
                    print("Detected text:", detection[1])
                if text is None or any(word.lower() in text for word in detection[1].lower()):
                    points = detection[0]
                    x_val = [pt[0] for pt in points]
                    y_val = [pt[1] for pt in points]
                    center_x = int(sum(x_val) / 4) + pos.WINDOW_LEFT
                    center_y = int(sum(y_val) / 4) + pos.WINDOW_TOP
                    pyautogui.click(center_x, center_y)
                    print(f"Clicked on text: {detection[1]} at ({center_x}, {center_y})")
                    return True

    if config.DEBUG:
        print("No matching text found")
        cv2.imshow("Text Detection", image)
        cv2.waitKey(0)
    
    return False

def find_text_at_position(position, text=None):
    start_time = time.time()
    while time.time() - start_time < 10:
        if config.DEBUG:
            print("Taking screenshot...")

        image = pyautogui.screenshot(region=position)
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        result = reader.readtext(image)

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
        cv2.imshow("Text Detection", image)
        cv2.waitKey(0)
    
    return None

def click(position, text=None):
    pyautogui.click(position[0], position[1])
    if text is not None:
        print(f"Clicked on text: {text} at ({position[0]}, {position[1]})")
    else:
        print(f"Clicked at ({position[0]}, {position[1]})")

def find_pos_tool(positions):
    image = pyautogui.screenshot(region=(pos.WINDOW_LEFT, pos.WINDOW_TOP, pos.WINDOW_WIDTH, pos.WINDOW_HEIGHT))
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    for position in positions:
        pt1 = (position[0], position[1])
        pt2 = (position[0] + position[2], position[1] + position[3])
        cv2.rectangle(image, pt1, pt2, (0, 255, 0), 2)
    
    cv2.imshow("Position Tool", image)
    playsound.playsound('./wav_files/notification.wav')

    cv2.waitKey(0)
    cv2.destroyAllWindows()

def reference_pos_tool():
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
    cv2.imshow("Reference Tool", image)
    playsound.playsound('./wav_files/notification.wav')

    cv2.waitKey(0)
    cv2.destroyAllWindows()