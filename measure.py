import cv2
import os
from latest_camera_capture import LatestFrameCapture

from ultralytics import YOLO
from car import Car
import time

WIDTH = 640
HEIGHT = 480
epsilon = 100
to_near_distance = 500
to_far_distance = 300
ideal_y = (to_near_distance + to_far_distance)/2
print(f"ideal_y = {ideal_y}")

model = YOLO("yolov8n.pt")
car = Car()

# Open camera
cap = LatestFrameCapture(src=0, width=WIDTH, height=HEIGHT)

# cap = cv2.VideoCapture(0)
# if not cap.isOpened():
#     raise RuntimeError("Failed to open camera.")

# cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
# cap.set(cv2.CAP_PROP_BUFFERSIZE, 2)
# cap.set(cv2.CAP_PROP_FPS, 60)
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

# print("Frame rate: ", cap.get(cv2.CAP_PROP_FPS))

status = "STOP"

try:
    for i in range(50):
    # while True:
        # Read frame from camera
        ret, frame = cap.read()
        print(f"t = {time.time():.3f}, ", end="")

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

                # print(f"Detected: {_x}, {_y1}")

                if abs(x-WIDTH/2) > abs(_x-WIDTH/2) and abs(y1-ideal_y) > abs(_y1-ideal_y):
                    x = _x
                    y1 = _y1

        print(f"x, y1 = {x:.3f}, {y1:.3f}, detected_person = {detected_person}")

        if i == 10:
            car.turn_left(70)
            print("STARTED!!!")

    print("Keyboard interrupt")
finally:
    car.stop()
    cap.stop()
