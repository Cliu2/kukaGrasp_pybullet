import serial
import time

class Gripper():
    def __init__(self):
        self.ser = serial.Serial("/dev/arduino-75734323939351C011C0", 
            baudrate=115200, timeout=0.1)
        # init the speed and disable it
        time.sleep(2) # somehow you need 2s delay
        self.status = False
        time.sleep(0.01)
        self.speed = 100

    @property
    def status(self):
        return self._status

    @property
    def speed(self):
        return self._speed
    
    @status.setter
    def status(self, status):
        self._status = status
        self.ser.write("e{}\n".format(int(self._status)).encode())
        time.sleep(0.002)

    @speed.setter
    def speed(self, speed):
        self._speed = speed
        self.ser.write("m{}\n".format(self._speed).encode())
        time.sleep(0.002) # usb serial delay

    def toggle(self):
        self.status = not self.status

if __name__ == "__main__":
    g = Gripper()