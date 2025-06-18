import time
import os
import serial

class Car:
    def __init__(self):
        os.system('stty -F /dev/ttyUSB0 min 100 time 2 -icanon -echo -opost -hupcl')
        time.sleep(0.1)
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        print(self.ser.name)
        self.ser.flushInput()
        self.ser.flushOutput()
    
    def move(self, vertical_speed, horizontal_speed):
        self.set_speed(l=vertical_speed + horizontal_speed, r=vertical_speed - horizontal_speed)

    def move_forward(self, speed):
        self.set_speed(l=speed, r=speed)

    def move_backward(self, speed):
        self.set_speed(l=-speed, r=-speed)

    def turn_left(self, speed):
        self.set_speed(l=-speed, r=speed)

    def turn_right(self, speed):
        self.set_speed(l=speed, r=-speed)

    def stop(self):
        self.set_speed(l=0, r=0)

    def set_speed(self, l, r):
        """
        l, r: -255 - 255
        """
        self.ser.write(b'M' + str(r).encode() + b' ' + str(l).encode() + b'\n')

    def set_LED(self, r, g, b):
        """
        r, g, b: 0 - 255
        """
        self.ser.write(b'L' + str(r).encode() + b' ' + str(g).encode() + b' ' + str(b).encode() + b'\n')


    def close(self):
        self.ser.close()

if __name__ == "__main__":
    car = Car()
    
    car.set_LED(255, 0, 0)
    car.move_forward(70)
    time.sleep(0.6)
    car.set_LED(0, 255, 0)
    car.move_backward(70)
    time.sleep(0.6)
    car.set_LED(0, 0, 255)
    car.turn_left(70)
    time.sleep(0.6)
    car.set_LED(255, 255, 255)
    car.turn_right(70)
    time.sleep(0.6)
    car.set_LED(0, 0, 0)
    car.stop()
    car.close()
