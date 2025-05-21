import cv2
import os
from latest_camera_capture import LatestFrameCapture

from ultralytics import YOLO
from car import Car
import time

WIDTH = 1920
HEIGHT = 1080
epsilon = 100
to_near_distance = 500
to_far_distance = 300
ideal_y = (to_near_distance + to_far_distance)/2
print(f"ideal_y = {ideal_y}")

model = YOLO("yolov8n.pt")
car = Car()

# Open camera
cap = LatestFrameCapture(src=0, width=WIDTH, height=HEIGHT)

try:
    while True:
        # Read frame from camera
        ret, frame = cap.read()

        results = model(frame, imgsz=128, verbose=False)

        # results = model(frame)
        boxes = results[0].boxes
        x, y1 = 0, -100000000000000
        detected_person = False

        for box in boxes:
            if box.cls == 0:

                detected_person = True

                _x1, _y1, _x2, _y2 = box.xyxy[0].tolist()
                _x = (_x1 + _x2) / 2

                print(f"Detected: {_x}, {_y1}")

                if abs(x-WIDTH/2) > abs(_x-WIDTH/2) and abs(y1-ideal_y) > abs(_y1-ideal_y):
                    x = _x
                    y1 = _y1

        print(f"x, y1 = {x}, {y1}, detected_person = {detected_person}", end="")

        if detected_person:
            if x < (WIDTH/2 - epsilon):
                car.turn_left(70)
                time.sleep(0.1)
                print(f" left", end="")
                car.stop()
                
            elif x > (WIDTH/2 + epsilon):
                car.turn_right(70)
                time.sleep(0.1)
                print(f" right", end="")
                car.stop()

            if y1 < (ideal_y - (to_near_distance - to_far_distance)/2):
                car.move_backward(70)
                time.sleep(0.5)
                car.stop()
                print(f" backward", end="")

            if y1 > (ideal_y + (to_near_distance - to_far_distance)/2):
                car.move_forward(70)
                time.sleep(0.5)
                car.stop()
                print(f" forward", end="")
            
        
        # save frame
        os.makedirs("pictures", exist_ok=True)
        results[0].save(f"pictures/frame_{time.time()}.jpg")

        print(f"")

        # If frame is not read correctly, break
        # if not ret
        #     print("Failed to read frame.")
        #     break
except KeyboardInterrupt:
    print("Keyboard interrupt")
finally:
    car.stop()
    cap.stop()
