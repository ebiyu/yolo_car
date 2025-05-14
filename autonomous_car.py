import cv2

from ultralytics import YOLO
from car import Car

epsilon = 8
to_close_distance = 8
to_near_distance = 16
ideal_y = 128 - (to_near_distance - to_close_distance)/2 - to_close_distance

model = YOLO("yolov8n.pt") 
car = Car()

# Open camera
cap = cv2.VideoCapture(0)

# Set video resolution
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 128)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 128)

while True:
    # Read frame from camera
    ret, frame = cap.read()

    results = model(frame, imgsz=128)

    # results = model(frame)
    boxes = results[0].boxes
    x, y1 = 0, 0
    detected_person = False

    for box in boxes:
        if box.cls == 0:

            detected_person = True

            _x1, _y1, _x2, _y2 = box.xyxy[0].tolist()
            _x = (_x1 + _x2) / 2
            if abs(x-64) > abs(_x-64):
                x = _x
            if abs(y1-ideal_y) > abs(_y1-ideal_y):
                y1 = _y1

    if detected_person:
        if x < (64 - epsilon):
            car.turn_left(70)
        elif x > (64 + epsilon):
            car.turn_right(70) 
        else:
            car.stop()


        #if y1 > (128 - to_close_distance):
        #    car.move_backward(70)

        #if y1 < (128 - to_near_distance):
        #   car.move_forward(70)

    # If frame is not read correctly, break
    if not ret: 
        print("Failed to read frame.")
        break

cap.release()
cv2.destroyAllWindows()
