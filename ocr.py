import cv2
import constants as const
import pyautogui
import numpy as np
import easyocr
import time
import playsound

textDetectorEAST= cv2.dnn_TextDetectionModel_EAST(const.MODEL_PATH)
textDetectorEAST.setConfidenceThreshold(const.CONF_THRESH)
textDetectorEAST.setNMSThreshold(const.NMS_THRESH)
textDetectorEAST.setInputParams(const.SCALE, const.INPUT_SIZE, const.MEAN, const.SWAP_RB)

reader = easyocr.Reader(['en'], gpu=False)

def find_text(text = None):
    start_time = time.time()
    while time.time() - start_time < 10:
        if const.DEBUG:
            print("Taking screenshot...")

        image = pyautogui.screenshot(region=(const.WINDOW_LEFT, const.WINDOW_TOP, const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        image_copy = cv2.resize(image, (const.INPUT_SIZE))
        boxes, confidences = textDetectorEAST.detect(image_copy)

        if const.DEBUG:
            print(f"Detected {len(boxes)} text boxes")

        scale_x = const.WINDOW_WIDTH / const.INPUT_SIZE[0]
        scale_y = const.WINDOW_HEIGHT / const.INPUT_SIZE[1]

        for box in boxes:
            scaled_box = np.array([[int(pt[0] * scale_x), int(pt[1] * scale_y)] for pt in box], dtype=np.int32)
            if const.DEBUG:
                print(f"Box Coordinates: {scaled_box}")
                cv2.polylines(image, [scaled_box], True, (0, 255, 0), 2)

            x, y, w, h = cv2.boundingRect(scaled_box)
            roi = image[y:y+h, x:x+w]

            if roi.size == 0:
                if const.DEBUG:
                    print(f"Skipped empty ROI at ({x}, {y}, {w}, {h})")
                continue

            result = reader.readtext(roi)
            for detection in result:
                if const.DEBUG:
                    print("Detected text:", detection[1])
                if text is None or any(word.lower() in text for word in detection[1].lower()):
                    points = detection[0]
                    x_val = [pt[0] for pt in points]
                    y_val = [pt[1] for pt in points]
                    center_x = int(sum(x_val) / 4) + const.WINDOW_LEFT
                    center_y = int(sum(y_val) / 4) + const.WINDOW_TOP
                    pyautogui.click(center_x, center_y)
                    print(f"Clicked on text: {detection[1]} at ({center_x}, {center_y})")
                    return True

    if const.DEBUG:
        print("No matching text found")
        cv2.imshow("Text Detection", image)
        cv2.waitKey(0)
    
    return False

def find_text_at_position(position, text=None):
    start_time = time.time()
    while time.time() - start_time < 10:
        if const.DEBUG:
            print("Taking screenshot...")

        image = pyautogui.screenshot(region=position)
        image = np.array(image)
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        result = reader.readtext(image)

        for detection in result:
            if const.DEBUG:
                print("Detected text:", detection[1])
            if text is None or text.lower() in detection[1].lower():
                points = detection[0]
                x_val = [pt[0] for pt in points]
                y_val = [pt[1] for pt in points]
                center_x = int(sum(x_val) / 4) + position[0]
                center_y = int(sum(y_val) / 4) + position[1]
                return [center_x, center_y]

    if const.DEBUG:
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
    image = pyautogui.screenshot(region=(const.WINDOW_LEFT, const.WINDOW_TOP, const.WINDOW_WIDTH, const.WINDOW_HEIGHT))
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    for position in positions:
        pt1 = (position[0], position[1])
        pt2 = (position[0] + position[2], position[1] + position[3])
        cv2.rectangle(image, pt1, pt2, (0, 255, 0), 2)
    
    cv2.imshow("Position Tool", image)
    playsound.playsound('./wav_files/notification.wav')

    cv2.waitKey(0)