import cv2
import constants
import pyautogui
import numpy as np
import easyocr

textDetectorEAST= cv2.dnn_TextDetectionModel_EAST(constants.MODEL_PATH)
textDetectorEAST.setConfidenceThreshold(constants.CONF_THRESH)
textDetectorEAST.setNMSThreshold(constants.NMS_THRESH)
textDetectorEAST.setInputParams(constants.SCALE, constants.INPUT_SIZE, constants.MEAN, constants.SWAP_RB)

reader = easyocr.Reader(['en'], gpu=True)

def find_text():
    image = pyautogui.screenshot(region=(constants.WINDOW_LEFT, constants.WINDOW_TOP, constants.WINDOW_WIDTH, constants.WINDOW_HEIGHT))
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    image_copy = cv2.resize(image, (constants.INPUT_SIZE))
    
    boxes, confidences = textDetectorEAST.detect(image_copy)

    print(constants.DEBUG)
    if constants.DEBUG:
        print(f"Detected {len(boxes)} text boxes")

    scale_x = constants.WINDOW_WIDTH / constants.INPUT_SIZE[0]
    scale_y = constants.WINDOW_HEIGHT / constants.INPUT_SIZE[1]

    for box in boxes:
        scaled_box = np.array([[int(pt[0] * scale_x), int(pt[1] * scale_y)] for pt in box], dtype=np.int32)
        if constants.DEBUG:
            print(f"Box Coordinates: {scaled_box}")
            cv2.polylines(image, [scaled_box], True, (0, 255, 0), 2)

        x, y, w, h = cv2.boundingRect(scaled_box)
        roi = image[y:y+h, x:x+w]

        if roi.size == 0:
            if constants.DEBUG:
                print(f"Skipped empty ROI at ({x}, {y}, {w}, {h})")
            continue

        result = reader.readtext(roi)
        for detection in result:
            if constants.DEBUG:
                print("Detected text:", detection[1])

    if constants.DEBUG:
        cv2.imshow("Text Detection", image)
        cv2.waitKey(0)
