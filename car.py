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
        self.ser.write(b'{"N":3,"D1":3,"D2":' + str(speed).encode() + b'}\r\n')

    def move_backward(self, speed):
        self.ser.write(b'{"N":3,"D1":4,"D2":' + str(speed).encode() + b'}\r\n')

    def turn_left(self, speed):
        self.ser.write(b'{"N":3,"D1":1,"D2":' + str(speed).encode() + b'}\r\n')

    def turn_right(self, speed):
        self.ser.write(b'{"N":3,"D1":2,"D2":' + str(speed).encode() + b'}\r\n')

    def stop(self):
        self.ser.write(b'{"N":1,"D1":0,"D2":0,"D3":0}\r\n')

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
