import cv2
import os
from latest_camera_capture import LatestFrameCapture

from ultralytics import YOLO
from car import Car
import time

WIDTH = 640
HEIGHT = 480
epsilon = WIDTH / 7
to_near_distance = HEIGHT / 2
to_far_distance = HEIGHT / 3
ideal_y = (to_near_distance + to_far_distance)/2
print(f"ideal_y = {ideal_y}")

model = YOLO("yolov5nu.pt")
car = Car()

# Open camera
cap = LatestFrameCapture(src=0, width=WIDTH, height=HEIGHT)

status = "STOP"

try:
    while True:
        # Read frame from camera
        ret, frame = cap.read()

        # print(f"Frame captured at: {time.time()}")

        results = model(frame, imgsz=128, verbose=False)

        boxes = results[0].boxes
        x, y1 = 0, -100000000000000
        detected_person = 0

        for box in boxes:
            if box.cls == 0:

                detected_person += 1

                _x1, _y1, _x2, _y2 = box.xyxy[0].tolist()
                _x = (_x1 + _x2) / 2

                if abs(x-WIDTH/2) > abs(_x-WIDTH/2) and abs(y1-ideal_y) > abs(_y1-ideal_y):
                    x = _x
                    y1 = _y1

        if detected_person > 0:
            print(f"t = {time.time():.3f}, persons = {detected_person}, x = {x:.3f}, y1 = {y1:.3f}")
        else:
            print(f"t = {time.time():.3f}, persons = {detected_person}")

        # save frame
        # os.makedirs("pictures", exist_ok=True)
        # results[0].save(f"pictures/frame_{time.time()}.jpg")

        if detected_person > 0:
            center_x = WIDTH/2
            
            # turn left or right
            if x < (center_x - epsilon):
                car.turn_left(70)
                status = "TURN_LEFT"
                continue                
            elif x > (center_x + epsilon):
                car.turn_right(70)
                status = "TURN_RIGHT"
                continue

            # go forward or backward
            if y1 < (ideal_y - (to_near_distance - to_far_distance)/2):
                car.move_backward(100)
                status = "BACKWARD"
                continue
            elif y1 > (ideal_y + (to_near_distance - to_far_distance)/2):
                car.move_forward(100)
                status = "FORWARD"
                continue
        
        car.stop()
except KeyboardInterrupt:
    print("Keyboard interrupt")
finally:
    car.stop()
    cap.stop()
