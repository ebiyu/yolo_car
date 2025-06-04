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
        l, r: -100 - 100
        """
        l = int(l * 256 / 100)
        r = int(r * 256 / 100)
        self.ser.write(str(r).encode() + b' ' + str(l).encode() + b'\n')

    def close(self):
        self.ser.close()

if __name__ == "__main__":
    car = Car()
    
    car.move_forward(70)
    time.sleep(0.6)
    car.move_backward(70)
    time.sleep(0.6)
    car.turn_left(70)
    time.sleep(0.6)
    car.turn_right(70)
    time.sleep(0.6)
    car.stop()
    car.close()
