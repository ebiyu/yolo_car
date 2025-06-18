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

class PIDController:
    def __init__(self, kp, ki, kd, setpoint):
        self.kp = kp  # 比例ゲイン
        self.ki = ki  # 積分ゲイン
        self.kd = kd  # 微分ゲイン
        self.setpoint = setpoint  # target value

        self.previous_error = 0
        self.integral = 0
        self.last_time = time.time()

    def update(self, current_value):
        """
        PID制御の計算を行い、制御量を出力する
        """
        current_time = time.time()
        dt = current_time - self.last_time

        error = self.setpoint - current_value  # 偏差

        # P
        proportional = self.kp * error

        # I
        self.integral += error * dt
        integral_term = self.ki * self.integral

        # D
        derivative = (error - self.previous_error) / dt
        derivative_term = self.kd * derivative

        # PID制御量
        output = proportional + integral_term + derivative_term

        # 状態更新
        self.previous_error = error
        self.last_time = current_time

        return output

# Open camera
cap = LatestFrameCapture(src=0, width=WIDTH, height=HEIGHT)

status = "STOP"

pid_horizontal = PIDController(kp=0.01, ki=0, kd=0, setpoint=WIDTH / 2)
pid_vertical = PIDController(kp=0.01, ki=0, kd=0, setpoint=HEIGHT * 5 / 12)

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
            car.set_LED(0, 255, 0)
            print(f"t = {time.time():.3f}, persons = {detected_person}, x = {x:.3f}, y1 = {y1:.3f}")
        else:
            car.set_LED(255, 0, 0)
            print(f"t = {time.time():.3f}, persons = {detected_person}")

        # save frame
        # os.makedirs("pictures", exist_ok=True)
        # results[0].save(f"pictures/frame_{time.time()}.jpg")

        if detected_person > 0:
            center_x = WIDTH/2

            horizontal_output = pid_horizontal.update(x)
            vertical_output = pid_vertical.update(y1)

            # # decide direction
            # x_direction = 0 # 0: center, 1: left, -1: right
            # if x < (center_x - epsilon):
            #     x_direction = 1
            # elif x > (center_x + epsilon):
            #     x_direction = -1
            
            # y_direction = 0 # 0: center, 1: forward, -1: back
            # if y1 < (ideal_y - (to_near_distance - to_far_distance)/2):
            #     y_direction = -1
            # elif y1 > (ideal_y + (to_near_distance - to_far_distance)/2):
            #     y_direction = 1

            # car.set_speed(
            #     l=140 * y_direction - 70 * x_direction,
            #     r=140 * y_direction + 70 * x_direction,
            # )
            car.move(
                vertical_speed=vertical_output,
                horizontal_speed=horizontal_output,
            )

        else:
            car.stop()

except KeyboardInterrupt:
    print("Keyboard interrupt")
finally:
    car.set_LED(0, 0, 0)
    car.stop()
    cap.stop()
